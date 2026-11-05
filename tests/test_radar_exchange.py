"""Synthetic exchange behaviour; no live project/API/scheduler mutations."""
import importlib.util
import sys
from pathlib import Path
import tempfile
import unittest
SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/video-production-router/scripts'
sys.path.insert(0, str(SCRIPTS))
import radar_wire as wire

class WireTest(unittest.TestCase):
    def test_retry_after_commit_does_not_apply_twice(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            msg = wire.message('idea_menu', 'radar', 'menu:fixture', 'a'*64, 1,
                               '2026-11-05T12:00:00+00:00', {'fixture': True})
            calls=[]
            def apply(state, message):
                calls.append(message['message_id']);state['count']=state.get('count',0)+1
                return 'applied','stored'
            first=wire.receive(root,'framewright',msg,apply)
            second=wire.receive(root,'framewright',msg,apply)
            self.assertEqual(first['result'],'applied')
            self.assertEqual(second['result'],'duplicate')
            self.assertEqual(len(calls),1)
            self.assertEqual(wire.state(root,'framewright')['data']['count'],1)


class StudioAdapterTest(unittest.TestCase):
    def test_menu_import_does_not_create_production(self):
        import radar_exchange as studio
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            msg=wire.message('idea_menu','radar','menu:fixture','a'*64,0,
                 '2026-11-05T12:00:00+00:00',{'packet_sha256':'a'*64,'as_of':'2026-11-05','ideas':[{'id':'idea-1','title':'A question','question':'Why?','hypothesis':'May help','format':'horizontal','sources':[],'constraints':[]} ]})
            result=wire.receive(root,'framewright',msg,studio.apply_message)
            self.assertEqual(result['result'],'applied')
            self.assertEqual(list(wire.state(root,'framewright')['data']['menus']),['a'*64])
            self.assertFalse(list(root.rglob('project.json')))

class TransportFailureTest(unittest.TestCase):
    def msg(self):return wire.message('idea_menu','radar','fixture','a'*64,0,'2026-11-05T12:00:00+00:00',{'safe':True})
    def test_corruption_is_rejected_without_application(self):
        with tempfile.TemporaryDirectory() as t:
            msg=self.msg();msg['payload']['safe']=False
            result=wire.receive(Path(t),'framewright',msg,lambda *_:self.fail('Must not apply'))
            self.assertEqual(result['result'],'rejected');self.assertFalse(wire.state(Path(t),'framewright')['processed'])
    def test_retry_after_ack_failure_applies_once(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);calls=[]
            def apply(data,_):calls.append(1);data['n']=1;return 'applied','one'
            with patch.object(wire,'publish',side_effect=OSError('synthetic ack failure')):
                with self.assertRaises(OSError):wire.receive(root,'framewright',self.msg(),apply)
            self.assertEqual(wire.receive(root,'framewright',self.msg(),apply)['result'],'duplicate');self.assertEqual(calls,[1])
    def test_pending_cannot_partially_mutate_or_block_retry(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            def pending(data,_):data['bad']=1;return 'pending','dependency absent'
            self.assertEqual(wire.receive(root,'framewright',self.msg(),pending)['result'],'pending')
            self.assertNotIn('bad',wire.state(root,'framewright')['data'])
            self.assertEqual(wire.receive(root,'framewright',self.msg(),lambda d,m:('applied','now present'))['result'],'applied')
    def test_missing_volume_creates_no_tree(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'absent-volume'/'exchange'
            with self.assertRaises(ValueError):wire.publish(root,'radar',self.msg())
            self.assertFalse(root.exists())
    def test_unknown_version_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            row=self.msg();row['schema_version']='future/v9';self.assertEqual(wire.receive(Path(t),'framewright',row,lambda *_:self.fail())['result'],'rejected')
    def test_symlink_root_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);(root/'link').symlink_to(root,target_is_directory=True)
            with self.assertRaises(ValueError):wire.publish(root/'link','radar',self.msg())
    def test_status_read_does_not_initialise_folders(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);self.assertEqual(wire.state(root,'framewright')['data'],{});self.assertEqual(list(root.iterdir()),[])
    def test_receipts_do_not_generate_receipt_loops(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);msg=self.msg();wire.publish(root,'radar',msg);wire.receive(root,'framewright',msg,lambda *_:('applied','yes'))
            ack=wire.read(next((root/'framewright/outbox').glob('*.json')))
            self.assertEqual(wire.receive(root,'radar',ack,lambda *_:self.fail())['result'],'applied')
            self.assertEqual(len(list((root/'radar/outbox').glob('*.json'))),1)

class StudioWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.exchange=self.root/'exchange';self.exchange.mkdir();self.project=self.root/'film'/'project.json';self.project.parent.mkdir()
        import json,hashlib
        def oldhash(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=True).encode()).hexdigest()
        d={'schema_version':2,'project':{'goal':'fixture'},'brief':{'blocks':[]},'plan':{'blocks':[]},'production_packet':'fixture','inputs':{},'artifacts':{},'steps':[],'journal':[],'history':[],'planning_sources':{}}
        for name,key in [('brief','brief_sha256'),('plan','plan_sha256'),('production_packet','packet_sha256'),('journal','journal_sha256')]:d[key]=oldhash(d[name])
        self.project.write_text(json.dumps(d));self.original=self.project.read_bytes()
        self.idea={'id':'idea-1','title':'A question','question':'Why?','hypothesis':'May help','format':'horizontal','sources':[],'constraints':[]}
        payload={'packet_sha256':'a'*64,'as_of':'2026-11-05','ideas':[self.idea]};self.menu=wire.message('idea_menu','radar','menu:fixture','a'*64,0,'2026-11-05T12:00:00+00:00',payload)
        import radar_exchange as studio
        self.studio=studio;wire.receive(self.exchange,'framewright',self.menu,studio.apply_message)
    def select(self,**kwargs):return self.studio.select(self.project,self.exchange,'framewright:fixture','a'*64,'idea-1','retrospective_observation',owner_approved=True,**kwargs)
    def test_selection_freezes_card_and_leaves_project_bytes_unchanged(self):
        import json
        msg=self.select();self.assertEqual(self.project.read_bytes(),self.original)
        self.assertEqual(json.loads((self.project.parent/'radar-link.json').read_text())['frozen_idea'],self.idea)
        self.assertEqual(self.select()['message_id'],msg['message_id'])
        second=dict(self.idea,title='Changed title');new=wire.message('idea_menu','radar','menu:new','b'*64,0,'2026-11-06T12:00:00+00:00',{'packet_sha256':'b'*64,'as_of':'2026-11-06','ideas':[second]});wire.receive(self.exchange,'framewright',new,self.studio.apply_message)
        self.assertEqual(json.loads((self.project.parent/'radar-link.json').read_text())['frozen_idea'],self.idea)
    def test_selection_requires_owner_and_known_card(self):
        with self.assertRaises(ValueError):self.studio.select(self.project,self.exchange,'framewright:fixture','a'*64,'idea-1','retrospective_observation')
        with self.assertRaises(ValueError):self.studio.select(self.project,self.exchange,'framewright:fixture','a'*64,'absent','retrospective_observation',owner_approved=True)
        self.assertFalse((self.project.parent/'radar-link.json').exists())
    def test_unchanged_status_exports_have_same_identity(self):
        self.select();a=self.studio.export_status(self.project,self.exchange);b=self.studio.export_status(self.project,self.exchange)
        self.assertEqual(a['message_id'],b['message_id']);self.assertEqual(a['payload']['status'],'selected');self.assertFalse(a['payload']['publications'])
    def metrics(self,**changes):
        p=dict(project_id='framewright:fixture',video_id='abcdefghijk',channel_id='UC'+'a'*22,as_of='2026-11-14T12:00:00+00:00',published_at='2026-11-05T12:00:00+00:00',period_start='2026-11-06',period_end='2026-11-12',timezone='America/Los_Angeles',window='calendar_report',availability='REPORTED',metrics={'views':5,'average_view_duration_seconds':None,'average_percentage_viewed':None,'impressions_ctr_percent':None,'estimated_revenue':None},currency=None,source_sha256='c'*64,source_kind='retained_youtube_api',report_label='videos_7d');p.update(changes);return p
    def test_nullable_metrics_and_channel_identity(self):
        self.select();folder=wire.directory(self.exchange,'framewright');s=wire.state(self.exchange,'framewright');s['data']['expected_channel']='UC'+'a'*22;s['data']['publications']={'framewright:fixture':[{'video_id':'abcdefghijk'}]};wire.atomic(folder/'state.json',s)
        payload=self.metrics();msg=wire.message('analytics_snapshot','radar','framewright:fixture','c'*64,0,payload['as_of'],payload)
        self.assertEqual(wire.receive(self.exchange,'framewright',msg,self.studio.apply_message)['result'],'applied')
        stored=wire.state(self.exchange,'framewright')['data']['analytics'][msg['message_id']];self.assertIsNone(stored['metrics']['estimated_revenue'])
        wrong=self.metrics(channel_id='UC'+'z'*22);row=wire.message('analytics_snapshot','radar','framewright:fixture','d'*64,1,wrong['as_of'],wrong)
        self.assertEqual(wire.receive(self.exchange,'framewright',row,self.studio.apply_message)['result'],'rejected')
    def test_synthetic_analytics_cannot_enter_live_state(self):
        self.select();p=self.metrics(source_kind='synthetic_fixture');row=wire.message('analytics_snapshot','radar','framewright:fixture','c'*64,0,p['as_of'],p)
        self.assertEqual(wire.receive(self.exchange,'framewright',row,self.studio.apply_message)['result'],'rejected')
    def test_zero_revenue_requires_currency_and_unavailable_is_not_zero(self):
        p=self.metrics();p['metrics']['estimated_revenue']=0
        with self.assertRaises(ValueError):wire.analytics_payload(p)
        p['currency']='EUR';wire.analytics_payload(p)
        p['availability']='ACCESS_FAILED'
        with self.assertRaises(ValueError):wire.analytics_payload(p)

    def test_project_identity_cannot_be_reused_at_another_path(self):
        self.select()
        other=self.project.parent/'other';other.mkdir();project=other/'project.json';project.write_bytes(self.original)
        with self.assertRaises(ValueError):self.studio.select(project,self.exchange,'framewright:fixture','a'*64,'idea-1','retrospective_observation',owner_approved=True)
        self.assertFalse((other/'radar-link.json').exists())
    def test_prospective_requires_attestation_and_fresh_sources(self):
        with self.assertRaises(ValueError):self.studio.select(self.project,self.exchange,'framewright:fixture','a'*64,'idea-1','prospective_hypothesis',owner_approved=True)
        self.idea['sources']=[{'url':'https://example.com','checked_at':'2026-10-01T12:00:00+00:00','supports':'fixture'}]
        folder=wire.directory(self.exchange,'framewright');state=wire.state(self.exchange,'framewright');state['data']['menus']['a'*64]['ideas']=[self.idea];wire.atomic(folder/'state.json',state)
        with self.assertRaises(ValueError):self.studio.select(self.project,self.exchange,'framewright:fixture','a'*64,'idea-1','prospective_hypothesis',owner_approved=True,before_production=True,now='2026-11-05T12:00:00+00:00')

class StaleDependencyTest(unittest.TestCase):
    setUp=StudioWorkflowTest.setUp
    select=StudioWorkflowTest.select
    def test_stale_dependency_cannot_export_acceptance_or_publication(self):
        import json,copy,runpy
        from unittest.mock import patch
        self.select();d=json.loads(self.project.read_text())
        out={'path':'final.mp4','sha256':'b'*64,'bytes':1};old={'path':'source.png','sha256':'c'*64,'bytes':1};new={**old,'sha256':'d'*64}
        d['inputs']={'source':new};d['artifacts']={'final':{'file':out}}
        for i,(kind,result) in enumerate([('creative','accepted'),('listening','accepted'),('publication','published')]):
            d['journal'].append(dict(id='e'+str(i),subject='output:final',kind=kind,topic=kind,result=result,pins={'output:final':out,'input:source':old},url='https://youtu.be/abcdefghijk',provenance='owner_report',recorded_at='2026-11-05T12:00:00+00:00'))
        J=runpy.run_path(str(SCRIPTS/'journal.py'));self.assertEqual(len(J['project'](d,{})['stale']),3)
        with patch.object(self.studio,'project_data',return_value=d):row=self.studio.export_status(self.project,self.exchange)
        self.assertEqual(row['payload']['status'],'ready_for_review');self.assertFalse(row['payload']['outputs'][0]['accepted']);self.assertFalse(row['payload']['publications'])

class PublicationIdentityTest(unittest.TestCase):
    def test_publication_url_must_identify_same_video(self):
        p=dict(project_id='fixture',radar_idea_id='idea',research_revision='a'*64,source_journal_sha256='b'*64,status='published',outputs=[dict(id='final',sha256='c'*64,bytes=1,accepted=True)],publications=[dict(platform='youtube',video_id='abcdefghijk',url='https://youtu.be/zzzzzzzzzzz',output_id='final',receipt_id='e1',provenance='owner_report',recorded_at='2026-11-05T12:00:00+00:00',master_sha256='c'*64)])
        with self.assertRaises(ValueError):wire.status_payload(p)

class GitHubFollowupTest(unittest.TestCase):
    setUp=StudioWorkflowTest.setUp
    select=StudioWorkflowTest.select
    def test_unrelated_review_topic_cannot_erase_rejection(self):
        import json
        from unittest.mock import patch
        self.select();d=json.loads(self.project.read_text());pin={'path':'final.mp4','sha256':'b'*64,'bytes':1};d['artifacts']={'final':{'file':pin}}
        for i,(kind,topic,result) in enumerate([('creative','facts','rejected'),('creative','style','accepted'),('listening','audio','accepted')]):
            d['journal'].append(dict(id='e'+str(i),subject='output:final',kind=kind,topic=topic,result=result,pins={'output:final':pin}))
        with patch.object(self.studio,'project_data',return_value=d):row=self.studio.export_status(self.project,self.exchange)
        self.assertFalse(row['payload']['outputs'][0]['accepted']);self.assertEqual(row['payload']['status'],'ready_for_review')
    def test_snapshot_read_holds_the_actual_project_writer_lock(self):
        import runpy,json
        from unittest.mock import patch
        self.select();P=runpy.run_path(str(SCRIPTS/'project.py'));d=json.loads(self.project.read_text())
        def snapshot(path):
            with self.assertRaises(ValueError):
                with P['locked'](path):pass
            return d
        with patch.object(self.studio,'project_data',side_effect=snapshot):self.studio.export_status(self.project,self.exchange)
    def test_null_timestamp_peer_does_not_block_valid_menu_or_status(self):
        import json
        self.select();good=self.menu.copy();bad={**good,'occurred_at':None}
        folder=wire.directory(self.exchange,'radar')/'outbox'
        (folder/(bad['message_id']+'.json')).write_text(json.dumps(bad))
        other={**self.menu['payload'],'packet_sha256':'f'*64};msg=wire.message('idea_menu','radar','menu:other','f'*64,0,'2026-11-05T12:00:00+00:00',other);wire.publish(self.exchange,'radar',msg)
        results=wire.drain(self.exchange,'framewright',self.studio.apply_message)
        self.assertIn('rejected',[r['result'] for r in results]);self.assertIn('f'*64,wire.state(self.exchange,'framewright')['data']['menus'])
        row=self.studio.export_status(self.project,self.exchange);self.assertEqual(row['kind'],'production_status')

class RecoveryFollowupTest(unittest.TestCase):
    setUp=StudioWorkflowTest.setUp
    select=StudioWorkflowTest.select
    def test_stale_topic_is_not_removed_from_required_acceptance(self):
        import json
        from unittest.mock import patch
        self.select();d=json.loads(self.project.read_text());out={'path':'final.mp4','sha256':'b'*64,'bytes':1};old={'path':'voice.wav','sha256':'c'*64,'bytes':1};d['inputs']={'voice':{**old,'sha256':'d'*64}};d['artifacts']={'final':{'file':out}}
        for i,(kind,topic,result) in enumerate([('creative','facts','rejected'),('creative','style','accepted'),('listening','audio','accepted')]):
            pins={'output:final':out}
            if i==0:pins['input:voice']=old
            d['journal'].append(dict(id='e'+str(i),subject='output:final',kind=kind,topic=topic,result=result,pins=pins))
        with patch.object(self.studio,'project_data',return_value=d):row=self.studio.export_status(self.project,self.exchange)
        self.assertFalse(row['payload']['outputs'][0]['accepted'])
    def test_invalid_receipt_does_not_prevent_next_checkpoint_export(self):
        self.select();row=wire.message('receipt','radar','ack:fixture','e'*64,0,'2026-11-05T12:00:00+00:00',{});wire.publish(self.exchange,'radar',row)
        results=wire.drain(self.exchange,'framewright',self.studio.apply_message);self.assertEqual(results[0]['result'],'rejected')
        self.assertEqual(self.studio.export_status(self.project,self.exchange)['kind'],'production_status')
    def test_frozen_prospective_retry_ignores_new_selection_freshness(self):
        from unittest.mock import patch
        args=(self.project,self.exchange,'framewright:fixture','a'*64,'idea-1','prospective_hypothesis')
        with patch.object(wire,'publish',side_effect=OSError('outbox unavailable')):
            with self.assertRaises(OSError):self.studio.select(*args,owner_approved=True,before_production=True,now='2026-11-05T12:00:00+00:00')
        row=self.studio.select(*args,owner_approved=True,now='2026-11-10T12:00:00+00:00')
        self.assertEqual(row['payload']['selected_at'],'2026-11-05T12:00:00+00:00')

if __name__=='__main__':unittest.main()
