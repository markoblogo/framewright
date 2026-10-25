import copy,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CLI=ROOT/'skills/video-production-router/scripts/branding.py'
class BrandingTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.p=Path(self.tmp.name)
  for n,b in [('logo.png',b'original logo'),('font.ttf',b'font bytes'),('OFL.txt',b'fixture licence'),('deck.pptx',b'reference deck')]: (self.p/n).write_bytes(b)
  asset=lambda n:{'path':n,'origin':'Explicit synthetic fixture','rights_status':'granted','rights_evidence':'Fixture owned by test'}
  self.spec={'id':'example-brand','palette':{'paper':'#FFFFFF','ink':'#151515','accent':'#E0E11C','muted':'#A2A2A2','negative':'#F16D20'},'typography':{'family':'Commissioner','heading_px':82,'hero_px':196,'body_px':44,'meta_px':36,'heading_weight':780},'layout':{'width':1080,'height':1920,'margin_x':100,'content_top':168,'content_bottom':1505,'logo_width':600},'motion':{'enter_seconds':.28,'chart_seconds':.8},'assets':{'logo':asset('logo.png'),'font':asset('font.ttf'),'licence':asset('OFL.txt')},'sources':[{'path':'deck.pptx','note':'Style source; not statistical data'}]}
  self.src=self.p/'spec.json';self.out=self.p/'profile.json'
 def cli(self,*args,ok=True):
  r=subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True,timeout=10)
  self.assertEqual(r.returncode==0,ok,r.stderr or r.stdout);return r
 def freeze(self):
  self.src.write_text(json.dumps(self.spec));self.cli('create',self.src,'--output',self.out)
 def test_profile_exports_same_fixed_brand_for_two_independent_productions(self):
  self.spec['assets']['logo']['path']=str(self.p/'logo.png');self.freeze();first=self.p/'film-a';second=self.p/'film-b'
  for folder in [first,second]:self.cli('export',self.out,'--output',folder)
  self.assertEqual((first/'brand.css').read_bytes(),(second/'brand.css').read_bytes())
  self.assertEqual((first/'logo.png').read_bytes(),b'original logo')
  self.assertIn('--brand-logo-width:600px',(first/'brand.css').read_text())
  info=json.loads((second/'brand.json').read_text());self.assertNotIn(str(self.p),(second/'brand.json').read_text());self.assertFalse(info['publication_authorized']);self.assertEqual(info['creative_review'],'pending')
  self.cli('export',self.out,'--output',second,ok=False)
 def test_optional_reading_hold_exports_and_rejects_out_of_bounds(self):
  self.spec['motion']['settled_hold_seconds']=2
  self.freeze()
  folder=self.p/'reading-hold';self.cli('export',self.out,'--output',folder)
  self.assertIn('--brand-settled-hold:2s',(folder/'brand.css').read_text())
  self.out.unlink()
  for value in [-.1,10.1,True,float('nan')]:
   self.spec['motion']['settled_hold_seconds']=value
   self.src.write_text(json.dumps(self.spec));self.cli('create',self.src,'--output',self.out,ok=False)
   self.assertFalse(self.out.exists())
  self.spec['motion']['settled_hold_seconds']=0;self.freeze()
 def test_changed_reference_or_logo_blocks_use_before_writing(self):
  self.freeze();(self.p/'logo.png').write_bytes(b'changed');self.cli('check',self.out,ok=False)
  folder=self.p/'blocked';self.cli('export',self.out,'--output',folder,ok=False);self.assertFalse(folder.exists())
 def test_profile_tampering_is_not_an_approved_brand_revision(self):
  self.freeze();x=json.loads(self.out.read_text());x['design']['palette']['accent']='#000000';self.out.write_text(json.dumps(x));self.cli('export',self.out,'--output',self.p/'bad',ok=False)
 def test_css_injection_and_invalid_layout_are_rejected(self):
  for field,value in [('colour','red; background:url(https://example.invalid)'),('font','A";}body{display:none'),('layout',2000),('number',float('nan'))]:
   s=copy.deepcopy(self.spec)
   if field=='colour':s['palette']['accent']=value
   elif field=='font':s['typography']['family']=value
   elif field=='layout':s['layout']['content_top']=value
   else:s['motion']['enter_seconds']=value
   self.src.write_text(json.dumps(s));self.cli('create',self.src,'--output',self.out,ok=False);self.assertFalse(self.out.exists())
 def test_unknown_rights_remain_a_blocker_and_denied_assets_are_refused(self):
  self.spec['assets']['logo'].update(rights_status='unknown',rights_evidence='');self.freeze();self.cli('export',self.out,'--output',self.p/'unresolved');m=json.loads((self.p/'unresolved/brand.json').read_text());self.assertTrue(m['publication_blockers'])
  self.out.unlink();self.spec['assets']['logo']['rights_status']='denied';self.src.write_text(json.dumps(self.spec));self.cli('create',self.src,'--output',self.out,ok=False)
if __name__=='__main__':unittest.main()
