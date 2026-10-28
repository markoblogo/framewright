import json
from pathlib import Path
import runpy
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
P=runpy.run_path(str(ROOT/'skills/video-production-router/scripts/project.py'))

class ProjectCostsTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.path=Path(self.tmp.name)/'project.json'
  # Use existing schema-v2 create entrypoint, not a separate cost database.
  import subprocess,sys
  subprocess.run([sys.executable,str(ROOT/'skills/video-production-router/scripts/project.py'),'create',str(self.path),'--goal','Synthetic costs','--note','No calls'],check=True,capture_output=True)
  self.data=P['load'](self.path)
  self.cost=runpy.run_path(str(ROOT/'skills/video-production-router/scripts/costs.py'))
 def add(self,kind,amount,op='one',unit='USD',**extra):
  e={'id':f'e{len(self.data.get("costs",{}).get("events",[]))+1}','kind':kind,'amount':amount,'unit':unit,'operation':None if kind=='limit' else op,'supplier':'fixture','category':'generation','basis':'Synthetic control; not a provider bill','provenance':'operator_observation',**extra}
  return self.cost['record'](self.data,e,P)
 def report(self):return self.cost['report'](self.data)
 def test_unknown_and_reservation_do_not_become_free_after_timeout(self):
  self.add('limit','5');self.add('reserve','3');self.add('unknown',None)
  r=self.report()['units']['USD'];self.assertEqual(r['reserved'],'3');self.assertEqual(r['remaining'],'2');self.assertEqual(r['unknown_operations'],1)
  with self.assertRaises(ValueError):self.add('reserve','2.01',op='retry')
  self.add('settle','2.40',receipt='provider/one')
  r=self.report()['units']['USD'];self.assertEqual(r['reserved'],'0');self.assertEqual(r['settled'],'2.40');self.assertEqual(r['remaining'],'2.60')
 def test_receipt_dedup_tags_and_gateway_usage_do_not_double_bill(self):
  self.add('limit','10');self.add('reserve','4');self.add('usage','2.50',tags=['model','film'])
  self.add('settle','2.50',receipt='provider/one');count=len(self.data['costs']['events'])
  duplicate=dict(self.data['costs']['events'][-1]);duplicate.pop('recorded_at');duplicate['id']='new-id'
  self.assertFalse(self.cost['record'](self.data,duplicate,P));self.assertEqual(len(self.data['costs']['events']),count)
  self.add('adjust','-0.50',receipt='provider/refund')
  self.assertEqual(self.report()['units']['USD']['remaining'],'8.00')
 def test_truthful_overspend_and_late_charge_after_release_are_visible(self):
  self.add('limit','5');self.add('reserve','4');self.add('release',None)
  self.assertEqual(self.report()['units']['USD']['remaining'],'5')
  self.add('usage',None)
  self.assertEqual(self.report()['units']['USD']['unknown_operations'],1)
  self.add('settle','6',receipt='late/one')
  self.assertTrue(self.report()['units']['USD']['over_cap'])
  with self.assertRaises(ValueError):self.add('reserve','0.01',op='new')
 def test_decimal_evidence_is_exact_and_invalid_amounts_are_rejected(self):
  self.add('limit','999999999999999999999999999999.30')
  self.add('settle','0.10',receipt='decimal/one')
  self.assertEqual(self.report()['units']['USD']['remaining'],'999999999999999999999999999999.20')
  for bad in [float('nan'),True,'NaN','1e3','-2']:
   with self.assertRaises(ValueError):self.add('reserve',bad,op='bad')
 def test_conflicting_duplicate_receipt_and_reused_attempt_are_rejected(self):
  self.add('limit','5');self.add('reserve','2')
  with self.assertRaises(ValueError):self.add('reserve','1')
  self.add('settle','1',receipt='supplier/one')
  with self.assertRaises(ValueError):self.add('settle','2',receipt='supplier/one')
  with self.assertRaises(ValueError):self.add('adjust','-2',receipt='refund/too-much')

 def test_units_unknowns_and_hash_validation(self):
  self.add('limit','10');self.add('estimate',None);self.add('usage',None)
  self.add('limit','100',unit='credits');self.add('settle','25',unit='credits',op='other',receipt='credit/one')
  r=self.report();self.assertIsNone(r['units']['USD']['remaining']);self.assertEqual(r['units']['credits']['settled'],'25');self.assertNotIn('grand_total',r)
  P['save'](self.path,self.data);loaded=P['load'](self.path);self.assertIn('costs',loaded)
  loaded['costs']['events'][0]['amount']='999';self.path.write_text(json.dumps(loaded))
  with self.assertRaises(ValueError):P['load'](self.path)

if __name__=='__main__':unittest.main()
