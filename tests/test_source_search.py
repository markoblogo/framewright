"""Explicit-source lexical retrieval preserves revision and evidence boundaries."""
import json
from pathlib import Path
import runpy
import tempfile
import unittest
import wave

ROOT=Path(__file__).resolve().parents[1]
S=runpy.run_path(str(ROOT/'skills/video-production-router/scripts/source_search.py'))


class SourceSearchTest(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name)
        self.audio=self.root/'take.wav'
        with wave.open(str(self.audio),'wb') as f:f.setparams((1,2,8000,0,'NONE',''));f.writeframes(b'\0\0'*8000)
        self.sidecar=self.root/'captions.txt';self.sidecar.write_text('supplied annotation')
        self.spec=self.root/'sources.json'
        self.data={'sources':[{'id':'take','path':'take.wav','evidence_sha256':S['E']['file_hash'](self.audio),
             'transcript':[{'id':'line1','start':0,'end':0.8,'text':'Connect the agent to the platform'}],
             'observations':[],'annotation_provenance':{'method':'synthetic supplied fixture','scope':'Not real speech'}}],
             'evidence_files':[{'path':'captions.txt','sha256':S['E']['file_hash'](self.sidecar)}]}
        self.write()

    def write(self):self.spec.write_text(json.dumps(self.data))

    def asr_fixture(self):
        raw=self.root/'asr.json';raw.write_text(json.dumps({'segments':[{'start':0.1,'end':0.8,'text':' Connect agent.'}]}))
        receipt=self.root/'receipt.json'
        receipt.write_text(json.dumps({'schema':'framewright-local-whisper-receipt-v1',
             'source_sha256':S['E']['file_hash'](self.audio),'transcript_sha256':S['E']['file_hash'](raw),
             'timing_origin':'source_playback_zero','model':{'package':'fixture','version':'1','weights':[{'sha256':'fixture'}]}}))
        return raw,receipt

    def test_asr_import_preserves_raw_text_and_provenance(self):
        raw,receipt=self.asr_fixture();before=raw.read_bytes()
        spec=S['import_whisper'](self.audio,raw,receipt,'asr-take')
        self.spec.write_text(json.dumps(spec));index=S['build'](self.spec)
        row=S['search'](index,'connect agent')['results'][0]
        self.assertEqual((row['start'],row['end'],row['text']),(0.1,0.8,' Connect agent.'))
        self.assertEqual(row['annotation_provenance']['method'],'local_asr_unverified')
        self.assertEqual(before,raw.read_bytes())
        self.assertEqual(len(spec['evidence_files']),2)

    def test_asr_import_rejects_changed_raw_or_source(self):
        raw,receipt=self.asr_fixture();raw.write_text('{}')
        with self.assertRaises(ValueError):S['import_whisper'](self.audio,raw,receipt,'take')
        raw,receipt=self.asr_fixture()
        with self.audio.open('ab') as f:f.write(b'changed')
        with self.assertRaises(ValueError):S['import_whisper'](self.audio,raw,receipt,'take')

    def test_asr_import_rejects_unmapped_origin_and_missing_model(self):
        raw,receipt=self.asr_fixture();r=json.loads(receipt.read_text());r['timing_origin']='trimmed excerpt';receipt.write_text(json.dumps(r))
        with self.assertRaises(ValueError):S['import_whisper'](self.audio,raw,receipt,'take')
        r['timing_origin']='source_playback_zero';r['model']={};receipt.write_text(json.dumps(r))
        with self.assertRaises(ValueError):S['import_whisper'](self.audio,raw,receipt,'take')

    def test_asr_import_rejects_empty_or_invalid_segments(self):
        for segments in [[],[{'start':0.2,'end':0.2,'text':'word'}],[{'start':0,'end':2,'text':'word'}]]:
            raw,receipt=self.asr_fixture();raw.write_text(json.dumps({'segments':segments}))
            r=json.loads(receipt.read_text());r['transcript_sha256']=S['E']['file_hash'](raw);receipt.write_text(json.dumps(r))
            with self.assertRaises(ValueError):S['import_whisper'](self.audio,raw,receipt,'take')

    def test_retrieval_is_lexical_and_preserves_source_and_time(self):
        index=S['build'](self.spec);before=self.audio.read_bytes()
        r=S['search'](index,'CONNECT agent','transcript');row=r['results'][0]
        self.assertEqual((row['source'],row['start'],row['end']),('take',0,0.8))
        self.assertEqual(row['qualification'],'candidate_requires_review')
        self.assertEqual(S['search'](index,'multiplayer voice chat')['status'],'not_found_in_index')
        self.assertEqual(before,self.audio.read_bytes());self.assertEqual(r['automatic_model_calls'],0)

    def test_media_replacement_invalidates_index(self):
        index=S['build'](self.spec)
        with self.audio.open('ab') as f:f.write(b'changed')
        with self.assertRaises(ValueError):S['search'](index,'agent')

    def test_multiple_sources_keep_identity_even_with_same_cue_id(self):
        second=self.root/'other.wav';second.write_bytes(self.audio.read_bytes())
        row=json.loads(json.dumps(self.data['sources'][0]));row.update(id='second',path='other.wav')
        row['transcript'][0].update(start=0.2,end=0.9,text='Connect the agent in another source')
        self.data['sources'].append(row);self.write()
        hits=S['search'](S['build'](self.spec),'connect agent')['results']
        self.assertEqual([(r['source'],r['evidence_id'],r['start']) for r in hits],
                         [('take','line1',0),('second','line1',0.2)])

    def test_changed_unmatched_source_invalidates_multisource_index(self):
        second=self.root/'other.wav';second.write_bytes(self.audio.read_bytes())
        row=json.loads(json.dumps(self.data['sources'][0]));row.update(id='second',path='other.wav')
        row['transcript'][0]['text']='A separate topic';self.data['sources'].append(row);self.write()
        index=S['build'](self.spec)
        with second.open('ab') as f:f.write(b'replacement')
        with self.assertRaises(ValueError):S['search'](index,'connect agent')

    def test_annotation_and_sidecar_replacement_invalidate_index(self):
        index=S['build'](self.spec);self.sidecar.write_text('changed caption')
        with self.assertRaises(ValueError):S['search'](index,'agent')
        self.sidecar.write_text('supplied annotation');self.data['sources'][0]['transcript'][0]['text']='Updated words';self.write()
        with self.assertRaises(ValueError):S['search'](index,'agent')

    def test_index_edit_is_not_a_valid_new_source(self):
        index=S['build'](self.spec);index['sources'][0]['transcript'][0]['text']='invented'
        with self.assertRaises(ValueError):S['search'](index,'invented')

    def test_still_observation_has_no_fabricated_time_or_speech(self):
        img=self.root/'image.png';img.write_bytes(b'fixture bytes; decoder not run')
        self.data['sources'].append({'id':'still','kind':'image','path':'image.png','evidence_sha256':S['E']['file_hash'](img),
              'observations':[{'id':'frame','text':'A drawn book cover'}],
              'annotation_provenance':{'method':'synthetic fixture','scope':'Not decoded'}});self.write()
        row=S['search'](S['build'](self.spec),'book cover','observations')['results'][0]
        self.assertIsNone(row['start']);self.assertIsNone(row['end'])

    def test_unpinned_or_out_of_bounds_annotations_fail(self):
        self.data['sources'][0]['evidence_sha256']='wrong';self.write()
        with self.assertRaises(ValueError):S['build'](self.spec)
        self.data['sources'][0]['evidence_sha256']=S['E']['file_hash'](self.audio)
        self.data['sources'][0]['transcript'][0]['end']=2;self.write()
        with self.assertRaises(ValueError):S['build'](self.spec)


if __name__=='__main__':unittest.main()
