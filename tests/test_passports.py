import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE=Path(__file__).resolve().parents[1]/'skills/video-production-router/scripts'


class PassportTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.project=self.root/'project.json'
        self.cli('project.py','create',self.project,'--goal','Synthetic canon test','--note','No real character approval')
        ref=self.root/'reference.txt';ref.write_text('Synthetic reference fixture')
        self.cli('project.py','retain',self.project,'reference',ref,'--input')
        self.spec={'id':'hero','version':'v1','kind':'character','name':'Fixture hero',
                   'references':['input:reference'],'dimensions_m':[0.5,0.3,0.7],
                   'materials':[{'id':'coat','description':'Dark coat','subject':None}],
                   'constraints':['No costume changes'],
                   'character':{'proportions':'Short stylised body','clothing':'Dark coat','palette':['#333333'],
                                'rig':{'required':False,'subject':None,'note':'Static fixture'},'actions':[]}}

    def cli(self,script,*args,ok=True):
        r=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True,timeout=30)
        self.assertEqual(r.returncode==0,ok,r.stderr);return r

    def create(self,spec=None,name='passport.json',extra=()):
        p=self.root/('spec-'+name);p.write_text(json.dumps(spec or self.spec))
        return self.cli('passports.py','create',self.project,p,'--output',self.root/name,'--actor','fixture',*extra)

    def state(self,subject='output:passport:hero:v1'):
        return json.loads(self.cli('passports.py','status',self.project,subject,'--json').stdout)

    def test_versions_do_not_inherit_approval_and_references_stale_old_acceptance(self):
        self.create();self.assertEqual(self.state()['state'],'draft')
        self.cli('project.py','observe',self.project,'output:passport:hero:v1','--kind','creative','--result','accepted',
                 '--actor','fixture-owner','--provenance','owner_report','--topic','passport-review','--note','Synthetic approval')
        self.assertEqual(self.state()['state'],'approved')
        new={**self.spec,'version':'v2'}
        self.create(new,'passport-v2.json',('--supersedes','output:passport:hero:v1'))
        self.assertEqual(self.state('output:passport:hero:v2')['state'],'draft')
        self.assertEqual(self.state()['state'],'approved')
        (self.root/'reference.txt').write_text('Changed reference')
        self.assertEqual(self.state()['state'],'stale')

    def test_incomplete_passport_is_a_draft_not_visual_identity_or_rights_proof(self):
        self.spec['dimensions_m']=None;self.spec['references']=[]
        self.spec['character']['rig']={'required':True,'subject':None,'note':'Pending rig'}
        self.create();s=self.state()
        self.assertEqual(s['state'],'incomplete');self.assertTrue(s['missing'])
        self.assertFalse(s['visual_identity_checked']);self.assertFalse(s['rights_cleared'])
        before=self.project.read_bytes()
        p=self.root/'other.json';p.write_text(json.dumps(self.spec))
        self.cli('passports.py','create',self.project,p,'--output',self.root/'duplicate.json','--actor','fixture',ok=False)
        self.assertEqual(before,self.project.read_bytes());self.assertFalse((self.root/'duplicate.json').exists())


    def test_environment_anchors_and_latest_pending_review(self):
        spec={k:v for k,v in self.spec.items() if k!='character'}
        spec.update(kind='environment',id='forest',name='Synthetic set',
                    environment={'layout':'One path, original fixture', 'lighting':'Cool fill',
                                 'anchors':[{'id':'gate','position_m':[0,2,0],'description':'Path endpoint'}]})
        self.create(spec)
        subject='output:passport:forest:v1'
        self.assertEqual(self.state(subject)['state'],'draft')
        for result,state in [('accepted','approved'),('pending','draft'),('rejected','rejected')]:
            self.cli('project.py','observe',self.project,subject,'--kind','creative','--result',result,
                     '--actor','fixture-owner','--provenance','owner_report','--topic','passport-review',
                     '--note','Synthetic latest review')
            self.assertEqual(self.state(subject)['state'],state)
        bad={**spec,'version':'v2'};bad['environment']={**spec['environment'],'anchors':[
            {'id':'bad','position_m':[0,float('inf'),0],'description':'Invalid'}]}
        path=self.root/'bad-environment.json';path.write_text(json.dumps(bad));before=self.project.read_bytes()
        self.cli('passports.py','create',self.project,path,'--output',self.root/'bad.json','--actor','fixture',ok=False)
        self.assertEqual(self.project.read_bytes(),before);self.assertFalse((self.root/'bad.json').exists())


if __name__=='__main__':unittest.main()
