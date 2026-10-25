"""Accepted-source template snapshots and deterministic content stress packets."""
import copy,json
from pathlib import Path
import shutil,subprocess,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'skills/video-production-router/scripts'

@unittest.skipUnless(shutil.which('ffprobe') and shutil.which('ffmpeg'),'Existing FFmpeg required')
class TemplateTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.project=self.root/'project.json';self.film=self.root/'film.mp4'
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=blue:s=64x64:r=24:d=1',
                        '-c:v','libx264','-threads','1',str(self.film)],check=True,capture_output=True)
        self.cli('project.py','create',self.project,'--goal','Template fixture','--note','Synthetic only')
        self.cli('project.py','asset',self.project,'film','--kind','video')
        self.cli('project.py','retain',self.project,'film',self.film)
        self.design={'id':'series','renderer':'Existing selected renderer; no command execution',
                     'canvas':{'width':1920,'height':1080,'fps':24},'style':{'palette':['#000','#fff'],'font':'Owner selected'},
                     'fields':{'title':{'type':'text','required':True,'max_chars':96,'long_after':24,'example':'A short title'},
                               'score':{'type':'number','required':True,'minimum':0,'maximum':100,'example':42},
                               'hero':{'type':'media','kind':'image','required':False,'fallback':'omit'}},
                     'scenes':[{'id':'opening','duration_seconds':4,'bindings':{'headline':'title','number':'score','image':'hero'},
                                'layout':'regular','long_text_layout':'expanded','missing_media_layout':'text-only'}]}
        self.spec=self.root/'design.json';self.template=self.root/'template.json'

    def cli(self,script,*args,ok=True):
        r=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True,timeout=30)
        self.assertEqual(r.returncode==0,ok,r.stderr);return r
    def accept(self):
        self.cli('project.py','observe',self.project,'output:film','--kind','creative','--result','accepted',
                 '--actor','fixture-owner','--provenance','owner_report','--note','Synthetic test approval')
    def extract(self):
        self.spec.write_text(json.dumps(self.design))
        return self.cli('templates.py','extract',self.project,'output:film',self.spec,'--output',self.template)

    def test_only_current_accepted_media_can_seed_a_template_and_no_variant_inherits_approval(self):
        self.spec.write_text(json.dumps(self.design));before=self.project.read_bytes()
        self.cli('templates.py','extract',self.project,'output:film',self.spec,'--output',self.template,ok=False)
        self.assertEqual(before,self.project.read_bytes());self.assertFalse(self.template.exists())
        self.accept();self.extract();t=json.loads(self.template.read_text())
        self.assertEqual(t['baseline']['subject'],'output:film');self.assertTrue(t['baseline']['acceptance_receipt'])
        self.assertEqual(t['design_review'],'pending')
        values=self.root/'values.json';values.write_text(json.dumps({'title':'Fresh title','score':50}))
        out=self.root/'variant.json'
        self.cli('templates.py','instantiate',self.template,values,'--output',out)
        v=json.loads(out.read_text());self.assertEqual(v['style'],self.design['style'])
        self.assertEqual(v['scenes'][0]['content']['headline'],'Fresh title')
        self.assertEqual(v['scenes'][0]['layout']['media'],'text-only')
        self.assertFalse(v['publication_authorized']);self.assertEqual(v['creative_review'],'pending')

    def test_stress_packets_cover_short_long_and_missing_media_without_claiming_render(self):
        self.accept();self.extract();folder=self.root/'cases'
        self.cli('templates.py','check',self.template,'--output',folder)
        report=json.loads((folder/'report.json').read_text())
        self.assertEqual(set(report['cases']),{'short-text','long-text','missing-optional-media'})
        short=json.loads((folder/'short-text.json').read_text());long=json.loads((folder/'long-text.json').read_text())
        self.assertLessEqual(len(short['values']['title']),24);self.assertEqual(len(long['values']['title']),96)
        self.assertEqual(long['scenes'][0]['layout']['text'],'expanded')
        self.assertEqual(long['style'],short['style']);self.assertIsNone(long['values']['hero'])
        self.assertTrue(all(v['render']=='not_performed' and v['data_validation']=='pass' for v in report['cases'].values()))
        self.cli('templates.py','check',self.template,'--output',folder,ok=False)

    def test_bad_values_and_edited_template_do_not_create_outputs(self):
        self.accept();self.extract();values=self.root/'values.json';out=self.root/'bad.json'
        for value in [{'title':'x'*97,'score':1},{'title':'Fine','score':True}, {'title':'Fine','score':float('nan')},
                      {'title':'Fine','score':101},{'title':'Fine','score':1,'style':{'font':'Changed'}}, {'score':1}]:
            values.write_text(json.dumps(value));self.cli('templates.py','instantiate',self.template,values,'--output',out,ok=False)
            self.assertFalse(out.exists())
        t=json.loads(self.template.read_text());t['design']['canvas']['width']=999
        self.template.write_text(json.dumps(t));values.write_text(json.dumps({'title':'Fine','score':1}))
        self.cli('templates.py','instantiate',self.template,values,'--output',out,ok=False)

    def test_media_needs_its_own_current_file_and_rights_and_can_be_omitted(self):
        self.accept();self.extract();picture=self.root/'hero.png'
        subprocess.run(['ffmpeg','-v','error','-filter_threads','1','-f','lavfi','-i','color=red:s=64x64',
                        '-frames:v','1',str(picture)],check=True,capture_output=True)
        values=self.root/'values.json';payload={'title':'Fine','score':12,'hero':{'path':'hero.png','origin':'Synthetic fixture',
                    'rights_status':'unknown','rights_evidence':''}}
        values.write_text(json.dumps(payload));out=self.root/'with-image.json'
        self.cli('templates.py','instantiate',self.template,values,'--output',out)
        variant=json.loads(out.read_text());self.assertTrue(variant['values']['hero']['sha256'])
        self.assertTrue(variant['publication_blockers'])
        folder=self.root/'with-and-without-image'
        self.cli('templates.py','check',self.template,'--values',values,'--output',folder)
        self.assertIsNotNone(json.loads((folder/'short-text.json').read_text())['values']['hero'])
        self.assertIsNone(json.loads((folder/'missing-optional-media.json').read_text())['values']['hero'])
        payload['hero']['rights_status']='denied';values.write_text(json.dumps(payload))
        self.cli('templates.py','instantiate',self.template,values,'--output',self.root/'bad.json',ok=False)

    def test_pending_or_stale_baseline_cannot_seed_a_new_template(self):
        self.accept()
        self.cli('project.py','observe',self.project,'output:film','--kind','creative','--result','pending',
                 '--actor','fixture-owner','--provenance','owner_report','--note','New review needed')
        self.spec.write_text(json.dumps(self.design))
        self.cli('templates.py','extract',self.project,'output:film',self.spec,'--output',self.template,ok=False)
        self.accept();self.film.write_bytes(self.film.read_bytes()+b'changed')
        self.cli('templates.py','extract',self.project,'output:film',self.spec,'--output',self.template,ok=False)
