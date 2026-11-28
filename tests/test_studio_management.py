import copy,hashlib,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'skills/video-production-router/scripts/studio.py'
PROJECT=CLI.with_name('project.py');COSTS=CLI.with_name('costs.py')
class StudioManagementTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.p=self.root/'project.json';self.profile=self.root/'management.json'
  self.runcli(PROJECT,'create',self.p,'--goal','Synthetic studio','--note','No provider calls')
  self.data={'schema_version':1,'services':[{'id':'vendor','name':'Vendor','terms':'Example conditions','pools':[{'id':'restricted','unit':'vendor:restricted','opening_balance':'100','observed_at':'2026-11-27T10:00:00+00:00','expires_on':'2026-12-26','eligible_models':['Model A'],'renewal':'conditional,not guaranteed','provenance':'operator_observation'}]}],'work':[{'id':'editorial','title':'Editorial','category':'editorial','priority':1,'status':'active','deadline':None,'target_date':'2026-11-27','next_step':'Make pilot','blockers':[],'budgets':[{'unit':'vendor:restricted','amount':'60','state':'proposed'}]},{'id':'partner','title':'Partner','category':'partner','priority':3,'status':'active','deadline':'2026-11-28','target_date':None,'next_step':'Review facts','blockers':[],'budgets':[{'unit':'vendor:restricted','amount':'50','state':'proposed'}]},{'id':'paused','title':'Paused','category':'editorial','priority':1,'status':'paused','deadline':None,'target_date':None,'next_step':'Wait owner','blockers':[],'budgets':[]}]}
  self.pin()
 def runcli(self,cli,*args,ok=True):
  r=subprocess.run([sys.executable,str(cli),*map(str,args)],capture_output=True,text=True);self.assertEqual(r.returncode==0,ok,r.stderr);return r
 def pin(self):
  self.profile.write_text(json.dumps(self.data));self.runcli(PROJECT,'retain',self.p,'studio-management',self.profile,'--input','--replace')
 def view(self,*args):return json.loads(self.runcli(CLI,self.p,'--at','2026-11-27T12:00:00+00:00',*args).stdout)
 def cost(self,kind,amount,op=None):
  e={'id':kind+str(op),'kind':kind,'amount':amount,'operation':op,'supplier':'vendor','unit':'vendor:restricted','category':'generation','basis':'Synthetic test','provenance':'operator_observation'};f=self.root/'event.json';f.write_text(json.dumps(e));self.runcli(COSTS,self.p,'--event',f)
 def test_business_order_and_proposals_do_not_authorise_or_double_allocate(self):
  before=self.p.read_bytes();v=self.view();self.assertEqual([x['id'] for x in v['plan']['ready']],['partner','editorial']);self.assertEqual(v['budgets'][0]['proposed_allocations'],'110');self.assertTrue(v['budgets'][0]['overallocated']);self.assertFalse(v['execution_authorized']);self.assertEqual(before,self.p.read_bytes())
 def test_reservations_and_unknown_outcomes_reduce_shared_pool(self):
  self.cost('limit','40');self.cost('reserve','30','attempt1');self.cost('unknown',None,'attempt1');v=self.view();p=v['budgets'][0];self.assertEqual(p['forecast_remaining'],'70');self.assertEqual(p['pending_exposure'],'30');self.assertEqual(p['budget_remaining'],'10');self.assertEqual(p['unknown_operations'],1)
 def test_restricted_pool_expiry_and_unknown_balance_block_admission(self):
  self.cost('limit','40')
  for model,date,ok in [('Model A','2026-11-27T12:00:00+00:00',True),('Model B','2026-11-27T12:00:00+00:00',False),('Model A','2026-12-26T00:00:00+00:00',False)]:
   r=self.runcli(CLI,self.p,'--at',date,'--check-unit','vendor:restricted','--amount','9','--model',model,ok=ok)
   if ok:self.assertTrue(json.loads(r.stdout)['admission']['allowed'])
  self.data['services'][0]['pools'][0]['opening_balance']=None;self.pin();self.runcli(CLI,self.p,'--check-unit','vendor:restricted','--amount','9','--model','Model A',ok=False)
 def test_hash_drift_and_duplicate_work_are_rejected(self):
  self.profile.write_text('{}');self.runcli(CLI,self.p,ok=False)
  self.data['work'].append(copy.deepcopy(self.data['work'][0]));self.pin();self.runcli(CLI,self.p,ok=False)
 def test_blocked_deadlines_remain_visible_and_active_cap_is_enforced(self):
  self.data['work'][1]['blockers']=['device not delivered'];self.pin();v=self.view();self.assertEqual(v['plan']['ready'][0]['id'],'editorial');self.assertEqual(v['plan']['waiting'][0]['deadline'],'2026-11-28')
  self.data['work']+= [{**copy.deepcopy(self.data['work'][0]),'id':f'extra{i}'} for i in range(5)];self.pin();self.runcli(CLI,self.p,ok=False)
 def test_reserve_is_atomic_and_reimport_is_idempotent(self):
  self.data['services'][0]['pools'][0].update(expires_on=None,nonexpiring=True);self.pin();self.cost('limit','100')
  e={'id':'reserve-once','kind':'reserve','amount':'100','operation':'work:one:attempt1','unit':'vendor:restricted','supplier':'vendor','category':'generation','basis':'Known synthetic quote','provenance':'operator_observation'}
  f=self.root/'reserve.json';f.write_text(json.dumps(e));self.runcli(CLI,self.p,'--reserve',f,'--model','Model B',ok=False)
  before=self.p.read_bytes();self.runcli(CLI,self.p,'--reserve',f,'--model','Model A');accepted=self.p.read_bytes();self.assertNotEqual(before,accepted)
  self.runcli(CLI,self.p,'--reserve',f,'--model','Model A');self.assertEqual(accepted,self.p.read_bytes())
  e.update(id='reserve2',operation='work:one:attempt2',amount='1');f.write_text(json.dumps(e));self.runcli(CLI,self.p,'--reserve',f,'--model','Model A',ok=False);self.assertEqual(accepted,self.p.read_bytes())
 def test_conditional_topups_not_funding_and_html_escapes_owner_text(self):
  self.data['services'][0]['pools'][0]['grants']=[{'amount':'900','status':'conditional','observed_at':'2026-11-27T10:00:00+00:00'},{'amount':'50','status':'confirmed','observed_at':'2026-11-28T10:00:00+00:00'},{'amount':'10','status':'confirmed','observed_at':'2026-11-27T10:00:00+00:00'}]
  self.data['work'][0]['title']='<script>never()</script>';self.pin();out=self.root/'review.html';v=self.view('--html',out);self.assertEqual(v['budgets'][0]['forecast_remaining'],'110');self.assertNotIn('<script>never()',out.read_text());self.assertIn('&lt;script&gt;',out.read_text())
  self.runcli(CLI,self.p,'--html',self.profile,ok=False)
 def test_daily_refresh_never_manufactures_a_fresh_balance(self):
  pool=self.data['services'][0]['pools'][0];pool.update(opening_balance='7',expires_on=None,nonexpiring=True,refresh={'cadence':'daily','amount':'50','rollover':'no','next_reset_at':'2026-11-28T10:00:00+00:00'})
  self.data['services'][0]['quotes']=[{'model':'Model A','credits':'6','resolution':'540p','duration_seconds':4}];self.pin();self.cost('limit','40')
  v=self.view();self.assertEqual(v['budgets'][0]['forecast_remaining'],'7');self.assertEqual(v['budgets'][0]['refresh']['amount'],'50');self.assertEqual(v['today_options'][0]['pools'][0]['budgeted_attempts'],'1')
  self.runcli(CLI,self.p,'--at','2026-11-29T12:00:00+00:00','--check-unit','vendor:restricted','--amount','6','--model','Model A',ok=False)
if __name__=='__main__':unittest.main()
