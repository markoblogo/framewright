import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE=Path(__file__).resolve().parents[1]/'skills/video-production-router/scripts'


class ShotTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.project=self.root/'project.json'
        self.cli('project.py','create',self.project,'--goal','Synthetic shot contracts','--note','Fake scene, never render')
        source=self.root/'fixture.blend';source.write_bytes(b'NOT A REAL BLEND FILE: dry-run fixture')
        self.cli('project.py','retain',self.project,'scene',source,'--input')
        self.spec={'id':'stage','version':'v1','scene':'input:scene','resources':[],
            'canvas':{'width':320,'height':180,'fps':12},'frames':{'start':0,'end':24},
            'engine':{'name':'CYCLES','device':'CPU','samples':4,'seed':7},
            'settings':{'camera':{'object':'Camera','location':[4,-6,3],'rotation_euler':[1,0,0.5],'lens':45},
                'actions':{'Actor':'Glide'},'lights':{'Key':{'energy':500,'color':[1,0.8,0.6],'location':[0,-2,4],'size':3}}},
            'audio':None,'bindings':[]}

    def cli(self,script,*args,ok=True):
        r=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True,timeout=30)
        self.assertEqual(r.returncode==0,ok,r.stderr);return r

    def prepare(self):
        s=self.root/'spec.json';s.write_text(json.dumps(self.spec))
        return self.cli('shots.py','prepare',self.project,s,'--output',self.root/'shot.json','--actor','fixture')

    def test_dry_run_never_launches_blender_or_creates_render_output_and_patch_is_one_field(self):
        self.prepare();before=self.project.read_bytes()
        r=self.cli('shots.py','render',self.project,'output:shot:stage:v1','--start','8','--end','16',
                   '--attempt','preview','--output',self.root/'render','--blender','/does/not/exist')
        self.assertFalse(json.loads(r.stdout)['execution_started']);self.assertFalse((self.root/'render').exists())
        self.assertEqual(before,self.project.read_bytes())
        self.cli('shots.py','patch',self.project,'output:shot:stage:v1','--parameter','settings.lights.Key.energy',
                 '--value','1000','--version','v2','--output',self.root/'shot-v2.json','--actor','fixture')
        a=json.loads((self.root/'shot.json').read_text());b=json.loads((self.root/'shot-v2.json').read_text())
        expected=json.loads(json.dumps(a['spec']));expected['version']='v2';expected['settings']['lights']['Key']['energy']=1000
        self.assertEqual(expected,b['spec']);self.assertEqual(b['parent'],'output:shot:stage:v1')
        self.assertEqual(a['spec']['settings']['lights']['Key']['energy'],500)

    def test_changed_scene_bad_range_and_arbitrary_patch_cannot_execute(self):
        self.prepare();before=self.project.read_bytes()
        self.cli('shots.py','patch',self.project,'output:shot:stage:v1','--parameter','scene',
                 '--value','"untrusted.py"','--version','bad','--output',self.root/'bad.json','--actor','fixture',ok=False)
        self.assertFalse((self.root/'bad.json').exists());self.assertEqual(before,self.project.read_bytes())
        self.cli('shots.py','render',self.project,'output:shot:stage:v1','--start','1','--end','25',
                 '--attempt','bad-range','--output',self.root/'bad-render',ok=False)
        self.assertFalse((self.root/'bad-render').exists())
        (self.root/'fixture.blend').write_bytes(b'changed')
        self.cli('shots.py','render',self.project,'output:shot:stage:v1','--attempt','changed',
                 '--output',self.root/'changed-render',ok=False)
        self.assertFalse((self.root/'changed-render').exists())

    def test_draft_passport_blocks_execution_and_new_version_does_not_rebind_existing_shot(self):
        passport={'id':'hero','version':'v1','kind':'character','name':'Unselected future hero',
            'references':[],'dimensions_m':None,'materials':[],'constraints':[],
            'character':{'proportions':'','clothing':'','palette':[],
                'rig':{'required':True,'subject':None,'note':'Not selected'},'actions':[]}}
        path=self.root/'passport-spec.json';path.write_text(json.dumps(passport))
        self.cli('passports.py','create',self.project,path,'--output',self.root/'passport.json','--actor','fixture')
        self.spec['bindings']=[{'passport':'output:passport:hero:v1','object':'Actor'}]
        self.prepare()
        r=self.cli('shots.py','render',self.project,'output:shot:stage:v1','--attempt','draft',
                   '--output',self.root/'draft-render')
        self.assertIn('incomplete',' '.join(json.loads(r.stdout)['blockers']))
        self.cli('shots.py','render',self.project,'output:shot:stage:v1','--attempt','draft',
                 '--output',self.root/'draft-render','--execute','--blender','/does/not/exist',ok=False)
        self.assertFalse((self.root/'draft-render').exists())
        passport['version']='v2';path.write_text(json.dumps(passport))
        self.cli('passports.py','create',self.project,path,'--output',self.root/'passport-v2.json',
                 '--actor','fixture','--supersedes','output:passport:hero:v1')
        bound=json.loads((self.root/'shot.json').read_text())['spec']['bindings'][0]['passport']
        self.assertEqual(bound,'output:passport:hero:v1')
        uses=json.loads(self.cli('passports.py','uses',self.project,bound,'--json').stdout)
        self.assertEqual([r['shot'] for r in uses],['output:shot:stage:v1'])

    def test_nonfinite_configuration_and_frame_clock_rejected_without_writes(self):
        for value in [float('nan'),True,-2]:
            self.spec['settings']['lights']['Key']['energy']=value
            path=self.root/'bad-spec.json';path.write_text(json.dumps(self.spec));before=self.project.read_bytes()
            self.cli('shots.py','prepare',self.project,path,'--output',self.root/'bad.json','--actor','fixture',ok=False)
            self.assertEqual(before,self.project.read_bytes());self.assertFalse((self.root/'bad.json').exists())


    def test_current_approval_and_worker_revision_are_checked_at_render_time(self):
        passport={'id':'set','version':'v1','kind':'environment','name':'Synthetic scene',
            'references':['input:scene'],'dimensions_m':[5,5,3],
            'materials':[{'id':'floor','description':'Slate fixture','subject':None}],
            'constraints':['Keep one path'],
            'environment':{'layout':'One original arch','lighting':'Two area lights',
                           'anchors':[{'id':'origin','position_m':[0,0,0],'description':'Fixture origin'}]}}
        path=self.root/'passport-spec.json';path.write_text(json.dumps(passport))
        self.cli('passports.py','create',self.project,path,'--output',self.root/'passport.json','--actor','fixture')
        subject='output:passport:set:v1'
        self.cli('project.py','observe',self.project,subject,'--kind','creative','--result','accepted',
                 '--actor','fixture-owner','--provenance','owner_report','--topic','passport-review','--note','Synthetic approval')
        self.spec['bindings']=[{'passport':subject,'object':None}];self.prepare()
        def preview():
            return json.loads(self.cli('shots.py','render',self.project,'output:shot:stage:v1',
                '--attempt','dry','--output',self.root/'unused').stdout)
        self.assertEqual(preview()['blockers'],[])
        self.cli('project.py','observe',self.project,subject,'--kind','creative','--result','pending',
                 '--actor','fixture-owner','--provenance','owner_report','--topic','passport-review','--note','Review reopened')
        self.assertIn('draft',' '.join(preview()['blockers']))
        # A separately retained record with an old worker fingerprint must not execute.
        row=json.loads((self.root/'shot.json').read_text());row['worker_sha256']='0'*64
        changed=self.root/'old-worker.json';changed.write_text(json.dumps(row))
        self.cli('project.py','retain',self.project,'shot:stage:v1',changed,'--replace')
        self.assertIn('worker changed',' '.join(preview()['blockers']))
        self.cli('shots.py','render',self.project,'output:shot:stage:v1','--attempt','old-worker',
                 '--output',self.root/'unused','--execute','--blender','/does/not/exist',ok=False)
        self.assertFalse((self.root/'unused').exists())


    def test_one_control_patch_preserves_dotted_blender_object_names(self):
        self.spec['settings']['lights']['Key.001']=self.spec['settings']['lights'].pop('Key')
        self.spec['settings']['actions']={'Actor.001':'Glide'};self.prepare()
        self.cli('shots.py','patch',self.project,'output:shot:stage:v1','--parameter','settings.lights.Key.001.energy',
                 '--value','900','--version','v2','--output',self.root/'v2.json','--actor','fixture')
        row=json.loads((self.root/'v2.json').read_text())
        self.assertEqual(row['spec']['settings']['lights']['Key.001']['energy'],900)
        self.cli('shots.py','patch',self.project,'output:shot:stage:v2','--parameter','settings.actions.Actor.001',
                 '--value','"OtherAction"','--version','v3','--output',self.root/'v3.json','--actor','fixture')
        row=json.loads((self.root/'v3.json').read_text())
        self.assertEqual(row['spec']['settings']['actions'],{'Actor.001':'OtherAction'})
        self.assertEqual(row['spec']['settings']['lights']['Key.001']['energy'],900)


    def test_fractional_source_offset_keeps_absolute_audio_sample_clock(self):
        import runpy
        audio_window=runpy.run_path(str(BASE/'shots.py'))['audio_window']
        # A half-sample offset must be rounded once, not after float frame addition.
        for offset in [0.5/48000,1.5/48000,0.1234567]:
            first,total=audio_window(offset,0,36,12)
            sub,length=audio_window(offset,12,24,12)
            tail,remaining=audio_window(offset,24,36,12)
            self.assertEqual(sub,first+48000)
            self.assertEqual(tail,sub+length)
            self.assertEqual(total,length*3)
            self.assertEqual(length,remaining)


if __name__=='__main__':unittest.main()
