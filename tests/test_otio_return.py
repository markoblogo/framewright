"""Safe external-editor cut intake; optional native OTIO, no model calls."""
import importlib.util
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
import wave

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'skills/video-production-router/scripts'
HAS_OTIO=importlib.util.find_spec('opentimelineio') is not None

@unittest.skipUnless(HAS_OTIO,'Optional native OpenTimelineIO unavailable')
class OtioReturnTest(unittest.TestCase):
    def setUp(self):
        import opentimelineio as o
        self.o=o;self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.exp=runpy.run_path(str(BASE/'otio_export.py'));self.spec=self.root/'spec.json';self.before=self.root/'before.otio';self.after=self.root/'after.otio';self.report=self.root/'report.json'
        media=[]
        for name,seconds,level in [('voice',2,64),('music',3,128)]:
            file=self.root/(name+'.wav')
            with wave.open(str(file),'wb') as f:f.setparams((1,2,8000,0,'NONE',''));f.writeframes(level.to_bytes(2,'little',signed=True)*8000*seconds)
            media.append({'id':name,'path':file.name,'sha256':self.exp['E']['file_hash'](file)})
        self.data={'schema':'framewright-otio-export-v1','name':'fixture','rate':30,'duration_frames':90,'media':media,'tracks':[
            {'id':'Voice','kind':'audio','items':[{'id':'lead','type':'gap','duration_frames':15},{'id':'v','type':'clip','media':'voice','in_frames':0,'duration_frames':60},{'id':'tail','type':'gap','duration_frames':15}]},
            {'id':'Music','kind':'audio','items':[{'id':'m','type':'clip','media':'music','in_frames':0,'duration_frames':90}]}]}
        self.spec.write_text(json.dumps(self.data));self.exp['export'](self.spec,self.before)
        self.timeline=o.adapters.read_from_file(str(self.before));self.timeline.metadata.clear();self.timeline.metadata['kdenlive']={'version':'fixture'}
        del self.timeline.tracks[0][-1]
        for c in self.timeline.find_clips():c.metadata.clear();c.media_reference.metadata.clear();c.name='editor-name';c.media_reference.target_url=str(self.root/c.media_reference.target_url)
        self.save_after()
    def save_after(self):self.o.adapters.write_to_file(self.timeline,str(self.after))
    def cli(self,*args,ok=True):
        r=subprocess.run([sys.executable,str(BASE/'otio_return.py'),*map(str,args)],capture_output=True,text=True,timeout=30)
        self.assertEqual(r.returncode==0,ok,r.stderr);return r
    def inspect(self,ok=True):return self.cli('inspect',self.spec,'--baseline',self.before,'--after',self.after,'--output',self.report,ok=ok)
    def test_unchanged_cut_ignores_editor_ids_and_implicit_trailing_silence(self):
        self.inspect();r=json.loads(self.report.read_text())
        self.assertFalse(r['delta']['timeline_changed']);self.assertEqual(r['delta']['duration_frames'],0)
        self.assertTrue(r['metadata']['different']);self.assertFalse(r['approval_inherited'])
        self.assertEqual(r['review_requirements'],['technical','listening','creative'])

    def trim(self):
        del self.timeline.tracks[0][0]
        self.timeline.tracks[1][0].source_range=self.o.opentime.TimeRange(self.o.opentime.RationalTime(15,30),self.o.opentime.RationalTime(75,30))
        self.save_after()

    def test_trim_reports_exact_duration_and_changed_tracks_without_mutating_files(self):
        self.trim();before=self.before.read_bytes();after=self.after.read_bytes();self.inspect()
        r=json.loads(self.report.read_text());self.assertEqual((r['before']['frames'],r['after']['frames'],r['delta']['duration_frames']),(90,75,-15))
        self.assertEqual({x['track'] for x in r['delta']['changed_ranges']},{'Voice','Music'})
        self.assertEqual((self.before.read_bytes(),self.after.read_bytes()),(before,after))

    def test_unknown_changed_remote_and_escaping_sources_rejected(self):
        ref=self.timeline.tracks[0][1].media_reference
        original=ref.target_url
        for value in ['https://example.com/voice.wav','file://remote/voice.wav']:
            ref.target_url=value;self.save_after();self.inspect(ok=False);self.assertFalse(self.report.exists())
        unknown=self.root/'unknown.wav';unknown.write_bytes(b'unknown source')
        ref.target_url=str(unknown);self.save_after();self.inspect(ok=False)
        ref.target_url=original;self.save_after()
        self.root.joinpath('voice.wav').write_bytes(b'changed');self.inspect(ok=False)
        self.assertFalse(self.report.exists())

    def test_effects_fractional_ranges_and_extra_tracks_fail_closed(self):
        clip=self.timeline.tracks[0][1]
        clip.effects.append(self.o.schema.LinearTimeWarp(time_scalar=2));self.save_after();self.inspect(ok=False)
        clip.effects.clear();clip.source_range=self.o.opentime.TimeRange(self.o.opentime.RationalTime(.5,30),self.o.opentime.RationalTime(60,30));self.save_after();self.inspect(ok=False)
        clip.source_range=self.o.opentime.TimeRange(self.o.opentime.RationalTime(0,30),self.o.opentime.RationalTime(61,30));self.save_after();self.inspect(ok=False)
        clip.source_range=self.o.opentime.TimeRange(self.o.opentime.RationalTime(0,30),self.o.opentime.RationalTime(60,30))
        self.timeline.tracks.append(self.o.schema.Track(name='Extra',kind=self.o.schema.TrackKind.Audio));self.save_after();self.inspect(ok=False)
        self.assertFalse(self.report.exists())

    def project_cli(self,*args):
        r=subprocess.run([sys.executable,str(BASE/'project.py'),*map(str,args)],capture_output=True,text=True,timeout=30)
        self.assertEqual(r.returncode,0,r.stderr);return r

    def make_project(self):
        self.project=self.root/'project.json';self.project_cli('create',self.project,'--goal','Fixture','--note','Synthetic only')
        render=self.root/'render.wav'
        with wave.open(str(render),'wb') as f:f.setparams((1,2,8000,0,'NONE',''));f.writeframes(b'\0\0'*20000)
        for name,file in [('spec',self.spec),('before',self.before),('after',self.after),('render',render)]:
            self.project_cli('asset',self.project,name,'--kind','test');self.project_cli('retain',self.project,name,file)
        self.project_cli('observe',self.project,'output:before','--kind','creative','--result','accepted','--actor','owner','--provenance','owner_report','--note','Synthetic baseline only')
        self.project_cli('task',self.project,'wait','--label','Existing wait','--waiting-for','owner','--note','Preserve this explicit wait')
        return json.loads(self.project.read_text())

    def stage(self,packet=None,ok=True,render=True):
        self.packet=packet or self.root/'packet.json'
        flags=['stage',self.project,self.report,'--id','edit-v1','--spec-subject','output:spec','--baseline-subject','output:before','--after-subject','output:after','--output',self.packet]
        if render:flags+=['--render-subject','output:render']
        return self.cli(*flags,ok=ok)

    def test_stage_preserves_baseline_and_wait_and_creates_only_pending_new_reviews(self):
        self.trim();self.inspect();old=self.make_project();self.stage();data=json.loads(self.project.read_text())
        self.assertEqual(data['artifacts']['before'],old['artifacts']['before'])
        self.assertEqual(next(x for x in data['steps'] if x['id']=='wait'),old['steps'][0])
        self.assertEqual(data['journal'][:len(old['journal'])],old['journal'])
        rows=[x for x in data['journal'][len(old['journal']):] if x['kind'] in {'technical','listening','creative'}]
        self.assertEqual({x['kind'] for x in rows},{'technical','listening','creative'})
        self.assertTrue(all(x['result']=='pending' for x in rows));self.assertTrue(all('output:before' in x['pins'] for x in rows))
        saved=self.project.read_bytes();self.stage(self.root/'duplicate.json',ok=False)
        self.assertEqual(self.project.read_bytes(),saved);self.assertFalse((self.root/'duplicate.json').exists())

    def test_stage_rechecks_tampered_report_and_wrong_render_without_mutation(self):
        self.trim();self.inspect();self.make_project();saved=self.project.read_bytes();original=self.report.read_bytes()
        report=json.loads(original);report['review_requirements']=[];self.report.write_text(json.dumps(report))
        self.stage(ok=False);self.assertEqual(self.project.read_bytes(),saved);self.assertFalse(self.packet.exists())
        self.report.write_bytes(original)
        self.project_cli('retain',self.project,'render',self.root/'music.wav','--replace');saved=self.project.read_bytes()
        self.stage(ok=False);self.assertEqual(self.project.read_bytes(),saved);self.assertFalse(self.packet.exists())

    def test_source_drift_or_missing_render_blocks_intake(self):
        self.trim();self.inspect();self.make_project();saved=self.project.read_bytes()
        self.stage(ok=False,render=False);self.assertEqual(self.project.read_bytes(),saved)
        with (self.root/'voice.wav').open('ab') as f:f.write(b'changed')
        self.stage(ok=False);self.assertEqual(self.project.read_bytes(),saved);self.assertFalse(self.packet.exists())

    def test_untrusted_editor_approval_is_not_inherited(self):
        self.timeline.metadata['framewright']={'approval':'accepted','publication_authorized':True}
        self.save_after();self.inspect();report=json.loads(self.report.read_text())
        self.assertFalse(report['approval_inherited']);self.assertFalse(report['publication_authorized'])

    def test_explicit_track_mapping_and_known_replacement_uses_hash_not_name(self):
        self.timeline.tracks[0].name='Unmapped';self.save_after();self.inspect(ok=False)
        self.timeline.tracks[0].name='Voice';folder=self.root/'copy';folder.mkdir();file=folder/'voice.wav'
        file.write_bytes((self.root/'music.wav').read_bytes())
        # A known music hash must not be mistaken for the old voice: source duration is different,
        # so it is a permitted material replacement, reported as changed rather than unchanged.
        self.timeline.tracks[0][1].media_reference.target_url=str(file);self.save_after();self.inspect()
        report=json.loads(self.report.read_text());self.assertTrue(report['delta']['timeline_changed'])
        self.assertEqual(report['after']['tracks']['Voice']['items'][0]['material'],'music')

    def test_external_and_symlink_paths_rejected_even_with_matching_content(self):
        with tempfile.TemporaryDirectory() as external:
            file=Path(external)/'voice.wav';file.write_bytes((self.root/'voice.wav').read_bytes())
            for ref in [file,self.root/'link.wav']:
                if ref!=file:ref.symlink_to(file)
                self.timeline.tracks[0][1].media_reference.target_url=str(ref);self.save_after();self.inspect(ok=False)
                self.assertFalse(self.report.exists())

    def test_replacing_receipt_media_reopens_completed_candidate_check(self):
        self.trim();self.inspect();old=self.make_project();self.stage();data=json.loads(self.project.read_text())
        subject='output:otio-return:edit-v1:render';entry=next(x for x in data['journal'] if x['subject']==subject and x['kind']=='technical')
        flags=['observe',self.project,subject,'--kind','technical','--result','pass','--actor','fixture','--provenance','operator_observation','--note','Synthetic check only']
        for dep in entry['pins']:
            if dep!=subject:flags+=['--depends-on',dep]
        self.project_cli(*flags);self.project_cli('mark',self.project,'otio-return:edit-v1:review-technical','--state','done','--evidence','Synthetic check')
        source=next(k for k in data['artifacts'] if k.startswith('otio-return:edit-v1:media:'))
        self.project_cli('retain',self.project,source,self.root/'render.wav','--replace')
        changed=json.loads(self.project.read_text());task=next(x for x in changed['steps'] if x['id']=='otio-return:edit-v1:review-technical')
        self.assertNotEqual(task['state'],'done')
        self.assertEqual(changed['journal'][:len(old['journal'])],old['journal'])

    def test_existing_task_id_collision_or_disabled_baseline_is_rejected(self):
        self.trim();self.inspect();self.make_project()
        self.project_cli('task',self.project,'otio-return:edit-v1:received','--label','Existing task')
        saved=self.project.read_bytes();self.stage(ok=False)
        self.assertEqual(self.project.read_bytes(),saved);self.assertFalse(self.packet.exists())
        self.report.unlink()
        t=self.o.adapters.read_from_file(str(self.before));t.tracks[0].enabled=False;self.o.adapters.write_to_file(t,str(self.before))
        self.inspect(ok=False);self.assertFalse(self.report.exists())


class ReturnIntervalTest(unittest.TestCase):
    def setUp(self):self.module=runpy.run_path(str(BASE/'otio_return.py'))
    def cut(self,n,items):return {'frames':n,'tracks':{'Picture':{'kind':'video','items':items}}}
    def item(self,at,start,duration,enabled=True):return {'at':at,'in':start,'duration':duration,'sha256':'a','enabled':enabled}
    def test_implicit_silence_and_identical_split_are_semantically_unchanged(self):
        before=self.cut(90,[self.item(0,0,60)])
        after=self.cut(90,[self.item(0,0,30),self.item(30,30,30)])
        self.assertEqual(self.module['intervals'](before,after),[])
    def test_offset_and_disabled_picture_are_detected(self):
        before=self.cut(60,[self.item(0,0,60)])
        for after in [self.cut(60,[self.item(0,1,60)]),self.cut(60,[self.item(0,0,60,False)])]:
            self.assertEqual(self.module['intervals'](before,after)[0]['ranges'],[{'start':0,'end':60}])

if __name__=='__main__':unittest.main()
