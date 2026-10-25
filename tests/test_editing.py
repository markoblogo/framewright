"""Public editing CLI: source identity, source/output time and cut-review media."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/video-production-router/scripts/editing.py'

@unittest.skipUnless(shutil.which('ffprobe'), 'Existing ffprobe required')
class EditingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'take.wav'
        with wave.open(str(self.source), 'wb') as f:
            f.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
            f.writeframes(b'\x00\x10' * 8000 * 4)
        self.spec = {'sources': [{'id': 'take', 'path': 'take.wav'}]}
        self.plan = self.root / 'plan.json'

    def cli(self, *args, ok=True):
        r = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(r.returncode == 0, ok, r.stderr)
        return r

    def save(self):
        self.plan.write_text(json.dumps(self.spec))

    def test_inventory_pins_media_but_never_invents_a_transcript_or_visual_review(self):
        self.save(); before = self.source.read_bytes()
        out = self.root / 'inventory.json'
        self.cli('inspect', self.plan, '--output', out)
        r = json.loads(out.read_text()); s = r['sources'][0]
        self.assertEqual(s['sha256'], hashlib.sha256(before).hexdigest())
        self.assertAlmostEqual(s['duration_seconds'], 4, places=2)
        self.assertEqual(s['transcript'], [])
        self.assertEqual(s['review']['content'], 'not_performed')
        self.assertEqual(s['review']['listening'], 'not_performed')
        self.assertFalse(r['publication_authorized'])
        self.assertEqual(before, self.source.read_bytes())
        self.cli('inspect', self.plan, '--output', out, ok=False)
        self.assertEqual(r, json.loads(out.read_text()))

    def make_map(self, edits=None):
        self.spec['edits'] = edits if edits is not None else [
            {'source': 'take', 'in_seconds': 0, 'out_seconds': 1, 'reason': 'Keep opening'},
            {'source': 'take', 'in_seconds': 2, 'out_seconds': 4, 'reason': 'Remove long pause'}]
        self.save(); p = self.root / 'map.json'
        self.cli('map', self.plan, '--output', p)
        return p

    def test_map_retimes_cues_and_marks_removed_and_clipped_speech_for_review(self):
        self.spec['sources'][0].update(evidence_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(), transcript=[
            {'id': 'a', 'start': 0, 'end': .8, 'text': 'Opening'},
            {'id': 'b', 'start': 1.2, 'end': 1.8, 'text': 'Removed'},
            {'id': 'c', 'start': 1.9, 'end': 2.4, 'text': 'Cut word'},
            {'id': 'd', 'start': 2.6, 'end': 3, 'text': 'Ending'}])
        m = self.make_map(); out = self.root / 'retimed.json'
        self.cli('retime', m, '--output', out)
        r = json.loads(out.read_text()); cues = r['cues']
        self.assertEqual([x['cue_id'] for x in cues], ['a', 'c', 'd'])
        self.assertAlmostEqual(cues[2]['start'], 1.6)
        self.assertAlmostEqual(cues[2]['end'], 2)
        self.assertTrue(cues[1]['needs_review'])
        self.assertEqual(r['removed_cues'][0]['cue_id'], 'b')
        self.assertFalse(r['semantic_review_performed'])
        self.cli('retime', m, '--output', self.root/'unsafe.json', '--srt', self.root/'unsafe.srt', ok=False)
        self.assertFalse((self.root/'unsafe.srt').exists())
        self.assertFalse((self.root/'unsafe.json').exists())

    def test_reordered_repeated_source_has_distinct_output_occurrences_and_safe_srt(self):
        self.spec['sources'][0].update(evidence_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(), transcript=[
            {'id': 'word', 'start': 2.2, 'end': 2.7, 'text': 'Repeat'}])
        m = self.make_map([{'source': 'take', 'in_seconds': a, 'out_seconds': b, 'reason': 'Reorder'}
                           for a,b in [(2,3),(0,1),(2,3)]])
        out = self.root/'retimed.json'; srt = self.root/'captions.srt'
        self.cli('retime', m, '--output', out, '--srt', srt)
        cues=json.loads(out.read_text())['cues']
        self.assertEqual([x['segment'] for x in cues], [1,3])
        self.assertAlmostEqual(cues[0]['start'], .2); self.assertAlmostEqual(cues[1]['start'], 2.2)
        self.assertIn('00:00:02,200 --> 00:00:02,700', srt.read_text())

    def test_out_of_range_nonfinite_speed_and_ambiguous_source_evidence_are_rejected(self):
        for change in [{'out_seconds': 5}, {'in_seconds': float('nan')}, {'speed': 2}]:
            self.spec['edits']=[dict({'source':'take','in_seconds':0,'out_seconds':1,'reason':'Test'},**change)]
            self.save(); self.cli('map', self.plan, '--output', self.root/'bad.json', ok=False)
            self.assertFalse((self.root/'bad.json').exists())
        self.spec['sources'][0]['transcript']=[{'id':'x','start':0,'end':1,'text':'Unbound'}]
        self.save(); self.cli('inspect', self.plan, '--output', self.root/'bad.json', ok=False)

    def test_changed_source_or_edited_time_map_is_rejected_before_reuse(self):
        m=self.make_map(); original=m.read_text()
        data=json.loads(original); data['segments'][0]['output_end']=99
        m.write_text(json.dumps(data))
        self.cli('retime',m,'--output',self.root/'bad.json',ok=False)
        m.write_text(original)
        self.source.write_bytes(self.source.read_bytes()+b'changed')
        self.cli('retime',m,'--output',self.root/'bad.json',ok=False)

    @unittest.skipUnless(shutil.which('ffmpeg'), 'Existing FFmpeg required')
    def test_join_pack_contains_playable_context_waveform_frames_and_pending_reviews(self):
        video=self.root/'red.mkv'; silent=self.root/'green.mkv'
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=red:s=96x64:r=24:d=2',
                        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
                        '-c:v','ffv1','-c:a','pcm_s16le',str(video)],check=True,capture_output=True)
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=green:s=64x96:r=15:d=2',
                        '-c:v','ffv1',str(silent)],check=True,capture_output=True)
        self.spec={'sources':[{'id':'red','path':'red.mkv'},{'id':'green','path':'green.mkv'}]}
        m=self.make_map([{'source':'red','in_seconds':0,'out_seconds':1.3,'reason':'Before'},
                         {'source':'green','in_seconds':.5,'out_seconds':1.5,'reason':'After'}])
        folder=self.root/'joins'
        self.cli('joins',m,'--output',folder,'--context','.37')
        r=json.loads((folder/'report.json').read_text()); j=r['joins'][0]
        self.assertEqual(j['listening'],'pending'); self.assertEqual(j['semantic_review'],'pending')
        self.assertEqual(j['synthetic_silence'], ['green'])
        self.assertAlmostEqual(j['preview_cut_seconds'],.375,places=3)
        for name in ['preview.mp4','frames.png','waveform.png','words.json']:
            self.assertTrue((folder/'join-001'/name).is_file(),name)
        self.assertEqual(j['preview_sha256'],hashlib.sha256((folder/'join-001/preview.mp4').read_bytes()).hexdigest())
        subprocess.run(['ffmpeg','-v','error','-i',str(folder/'join-001/preview.mp4'),'-f','null','-'],check=True,capture_output=True)
        import array, math
        raw=self.root/'decoded.wav'
        subprocess.run(['ffmpeg','-v','error','-i',str(folder/'join-001/preview.mp4'),'-vn',
                        '-ar','48000','-ac','1','-c:a','pcm_s16le',str(raw)],check=True,capture_output=True)
        with wave.open(str(raw)) as f:
            samples=array.array('h',f.readframes(f.getnframes()))
        def rms(a,b):
            part=samples[round(a*48000):round(b*48000)]
            return math.sqrt(sum(x*x for x in part)/len(part))/32768
        self.assertGreater(rms(.1,.3),.02);self.assertLess(rms(.65,.85),.001)
        for t,channel in [('0.2',0),('0.333333',0),('0.375',1),('0.7',1)]:
            pixel=subprocess.run(['ffmpeg','-v','error','-filter_threads','1','-ss',t,
                                  '-i',str(folder/'join-001/preview.mp4'),'-vf','crop=2:2:320:180',
                                  '-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-'],check=True,capture_output=True).stdout
            self.assertGreater(pixel[channel],pixel[1-channel]*3)
        before=(folder/'report.json').read_bytes()
        self.cli('joins',m,'--output',folder,ok=False)
        self.assertEqual(before,(folder/'report.json').read_bytes())

    @unittest.skipUnless(shutil.which('ffmpeg'), 'Existing FFmpeg required')
    def test_audio_only_join_is_wav_and_context_limit_is_checked(self):
        m=self.make_map(); out=self.root/'audio-joins'
        self.cli('joins',m,'--output',out,'--context','.25')
        r=json.loads((out/'report.json').read_text())
        self.assertEqual(r['joins'][0]['preview_file'],'join-001/preview.wav')
        self.assertFalse((out/'join-001/frames.png').exists())
        with wave.open(str(out/'join-001/preview.wav')) as f:
            self.assertAlmostEqual(f.getnframes()/f.getframerate(),.5,places=2)
        self.cli('joins',m,'--output',self.root/'bad-joins','--context','nan',ok=False)
        self.assertFalse((self.root/'bad-joins').exists())

    def test_overlay_times_follow_the_same_map_and_unselected_intervals_are_retained(self):
        m=self.make_map(); data=json.loads(m.read_text())
        self.assertEqual(data['unselected_source_intervals'],[{'source':'take','start':1,'end':2,'reason':'Not selected by this edit list'}])
        cues=self.root/'overlays.json'
        cue={'id':'label','source':'take','source_sha256':hashlib.sha256(self.source.read_bytes()).hexdigest(),
             'kind':'overlay','start':2.2,'end':2.8,'text':'A caption'}
        cues.write_text(json.dumps([cue])); out=self.root/'overlays-retimed.json'
        self.cli('retime',m,'--cues',cues,'--output',out)
        result=json.loads(out.read_text())['cues'][0]
        self.assertEqual(result['kind'],'overlay');self.assertAlmostEqual(result['start'],1.2)
        cue['source_sha256']='0'*64;cues.write_text(json.dumps([cue]))
        self.cli('retime',m,'--cues',cues,'--output',self.root/'bad.json',ok=False)

    def test_overlapping_subtitles_and_remote_sources_fail_without_outputs(self):
        self.spec['sources'][0].update(evidence_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(),transcript=[
            {'id':'one','start':0,'end':.8,'text':'One'}, {'id':'two','start':.5,'end':.9,'text':'Two'}])
        m=self.make_map(); out=self.root/'retimed.json'
        self.cli('retime',m,'--output',out,'--srt',self.root/'bad.srt',ok=False)
        self.assertFalse(out.exists())
        self.spec['sources']=[{'id':'remote','path':'https://example.test/video.mp4'}];self.save()
        self.cli('inspect',self.plan,'--output',out,ok=False)
        self.assertFalse(out.exists())
