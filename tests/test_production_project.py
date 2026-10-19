"""Scene/catalogue/delivery behavior; synthetic bytes, no renderer or network."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'skills/video-production-router/scripts/project.py'

class ProductionProjectTest(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name);self.project=self.root/'project.json';self.specfile=self.root/'production.json'
        self.cli('create',self.project,'--goal','Synthetic review','--note','No real media or rights claims')
        self.clip=self.root/'clip.mp4';self.clip.write_bytes(b'not actual video; synthetic catalogue fixture')
        self.cli('asset',self.project,'clip','--kind','video-export');self.cli('retain',self.project,'clip',self.clip)

    def cli(self,*args,ok=True):
        result=subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True)
        self.assertEqual(result.returncode==0,ok,result.stderr)
        return result

    def spec(self):
        return {'schema_version':1,'materials':[{
            'id':'clip','kind':'video','subject':'output:clip','origin':'Synthetic fixture, not gameplay',
            'duration_seconds':10,'rights':{'status':'owner_authorized','basis':'Synthetic test only',
                'uses':['main','short','cover','copy'],'attribution':'','restrictions':[]}}],
            'scenes':[{'id':'demo','tell':'Explain the action','show':'Real demonstration when captured',
                'materials':['clip'],'narration':{'text':'','material':None},'missing':[],
                'claims':[{'text':'Fixture action','material':'clip'}]}],
            'variants':[{'id':name,'kind':name,'canvas':{'width':w,'height':h,'fps':30},
                'edits':[{'scene':'demo','material':'clip','source_in':start,'source_out':4,
                    'duration_seconds':4-start,'framing':frame}],
                'music':None,'tasks':[],
                'delivery':{k:None for k in ['video','thumbnail','subtitles','title','description']}}
                for name,w,h,start,frame in [('main',1920,1080,0,'Whole scene'),('short',1080,1920,2,'Keep consequence inside portrait')]]}

    def compose(self,spec,replace=False,ok=True):
        self.specfile.write_text(json.dumps(spec))
        return self.cli('compose',self.project,self.specfile,*(['--replace'] if replace else []),ok=ok)

    def board(self):
        return json.loads(self.cli('board',self.project,'--json').stdout)

    def test_material_admin_edits_do_not_reopen_video_but_rights_still_gate_kit(self):
        spec=self.complete_fixture();clip=spec['materials'][0]
        clip['origin']='Corrected source credit';clip['tags']=['reviewed']
        clip['rights']['status']='licensed';clip['rights']['basis']='Retained fixture licence'
        clip['rights']['attribution']='Corrected author credit'
        self.compose(spec,replace=True)
        board=self.board()
        self.assertEqual(board['variants']['main']['delivery']['video']['problems'],[])
        self.assertTrue(board['variants']['main']['complete_local_handoff'])
        self.assertEqual(board['materials']['clip']['rights']['attribution'],'Corrected author credit')
        clip['rights']['status']='unknown';clip['rights']['restrictions']=['Confirm reuse permission']
        self.compose(spec,replace=True);main=self.board()['variants']['main']
        self.assertEqual(main['delivery']['video']['problems'],[])
        self.assertFalse(main['complete_local_handoff'])
        self.assertTrue(any('rights unresolved' in problem for problem in main['blockers']))
        clip['duration_seconds']=9
        self.compose(spec,replace=True)
        self.assertIn('technical: no current pass receipt',self.board()['variants']['main']['delivery']['video']['problems'])

    def test_board_rejects_whitespace_and_invalid_utf8_delivery_text(self):
        spec=self.complete_fixture()
        for role,suffix in [('title','.txt'),('description','.txt'),('subtitles','.srt')]:
            f=self.root/(role+suffix);original=f.read_bytes()
            for content in [b' \n\t ',b'valid prefix\xff']:
                f.write_bytes(content);self.cli('retain',self.project,role,f,'--replace')
                self.compose(spec,replace=True)
                for kind,result in ({'technical':'pass'} if role=='subtitles' else {'creative':'accepted'}).items():
                    self.observe('output:'+role,kind,result)
                board=self.board()['variants']['main']
                self.assertFalse(board['complete_local_handoff'])
                self.assertTrue(any('text' in problem for problem in board['delivery'][role]['problems']))
                self.cli('bundle',self.project,'main','--output',self.root/('invalid-'+role),ok=False)
            f.write_bytes(original);self.cli('retain',self.project,role,f,'--replace')
            self.compose(spec,replace=True)
            for kind,result in ({'technical':'pass'} if role=='subtitles' else {'creative':'accepted'}).items():
                self.observe('output:'+role,kind,result)

    def test_delivery_metadata_and_task_changes_preserve_video_check(self):
        spec=self.complete_fixture()
        for role in ['thumbnail','subtitles','title','description']:
            changed=copy.deepcopy(spec);changed['variants'][0]['delivery'][role]=None
            self.compose(changed,replace=True)
            self.assertEqual(self.board()['variants']['main']['delivery']['video']['problems'],[])
            self.compose(spec,replace=True)
            self.assertTrue(self.board()['variants']['main']['complete_local_handoff'])
        self.cli('task',self.project,'copy-review','--label','Review updated copy')
        spec['variants'][0]['tasks']=['copy-review'];self.compose(spec,replace=True)
        self.assertEqual(self.board()['variants']['main']['delivery']['video']['problems'],[])
        self.assertFalse(self.board()['variants']['main']['complete_local_handoff'])

    def test_one_catalogue_supplies_independent_main_and_short_edits_without_execution(self):
        self.compose(self.spec())
        before=self.project.read_bytes();board=self.board()
        self.assertEqual(len(board['materials']),1)
        self.assertEqual(board['variants']['main']['duration_seconds'],4)
        self.assertEqual(board['variants']['short']['duration_seconds'],2)
        self.assertNotEqual(board['variants']['main']['edits'][0]['framing'],board['variants']['short']['edits'][0]['framing'])
        self.assertEqual(board['scenes']['demo']['tell'],'Explain the action')
        self.assertFalse(board['variants']['main']['complete_local_handoff'])
        self.assertFalse(board['publication_authorized'])
        self.assertEqual(before,self.project.read_bytes())
        self.assertIn('production',json.loads(self.cli('resume',self.project,'--json').stdout))

    def observe(self,subject,kind,result):
        self.cli('observe',self.project,subject,'--kind',kind,'--result',result,
                 '--actor','fixture operator','--provenance','operator_observation','--note','Synthetic receipt; no media decoder used')

    def complete_fixture(self):
        spec=self.spec();main=spec['variants'][0]
        for role,kind in [('video','video'),('thumbnail','image'),('subtitles','text'),('title','text'),('description','text')]:
            suffix={'video':'.mp4','thumbnail':'.png','subtitles':'.srt','title':'.txt','description':'.txt'}[role]
            f=self.root/(role+suffix);f.write_text('Fixture '+role+'; not real production')
            self.cli('asset',self.project,role,'--kind',kind);self.cli('retain',self.project,role,f)
            material=copy.deepcopy(spec['materials'][0]);material.update(id=role,kind=kind,subject='output:'+role,
                derived_from=['clip'],origin='Derived synthetic fixture, not real production')
            material.pop('duration_seconds',None)
            if role=='video':material['duration_seconds']=4
            spec['materials'].append(material);main['delivery'][role]=role
        self.compose(spec)
        for role,checks in {'video':{'technical':'pass','listening':'accepted','creative':'accepted'},
                'thumbnail':{'technical':'pass','creative':'accepted'},'subtitles':{'technical':'pass'},
                'title':{'creative':'accepted'},'description':{'creative':'accepted'}}.items():
            for kind,result in checks.items():self.observe('output:'+role,kind,result)
        return spec

    def test_bundle_copies_only_final_slots_and_keeps_publication_separate(self):
        self.complete_fixture();before=self.project.read_bytes();target=self.root/'kit'
        self.assertTrue(self.board()['variants']['main']['complete_local_handoff'])
        self.cli('bundle',self.project,'main','--output',target)
        manifest=json.loads((target/'manifest.json').read_text())
        self.assertTrue(manifest['complete_local_handoff']);self.assertFalse(manifest['publication_authorized'])
        self.assertEqual(len(manifest['files']),5)
        for row in manifest['files'].values():
            self.assertEqual(hashlib.sha256((target/row['name']).read_bytes()).hexdigest(),row['sha256'])
        self.assertFalse((target/'clip.mp4').exists())
        self.assertTrue((target/'CHECKS.md').is_file())
        self.assertEqual(before,self.project.read_bytes())
        self.cli('bundle',self.project,'main','--output',target,ok=False)
        self.assertEqual(before,self.project.read_bytes())

    def test_draft_kit_and_parent_rights_keep_unknowns_and_short_limits_visible(self):
        spec=self.spec();spec['materials'][0]['rights']['uses']=['main']
        self.compose(spec)
        board=self.board()
        self.assertTrue(any('intended uses' in p for p in board['variants']['short']['blockers']))
        target=self.root/'draft'
        self.cli('bundle',self.project,'short','--output',target,ok=False)
        self.assertFalse(target.exists())
        self.cli('bundle',self.project,'short','--output',target,'--draft')
        manifest=json.loads((target/'manifest.json').read_text())
        self.assertFalse(manifest['complete_local_handoff']);self.assertEqual(manifest['files'],{})
        spec['materials'][0]['rights']['status']='unknown'
        before=self.project.read_bytes();self.compose(spec,ok=False)
        self.assertEqual(before,self.project.read_bytes())
        self.compose(spec,replace=True)
        self.assertTrue(any('rights unresolved' in p for p in self.board()['variants']['main']['blockers']))

    def test_changed_cut_requires_new_conformance_even_with_same_final_video_bytes(self):
        spec=self.complete_fixture();self.assertTrue(self.board()['variants']['main']['complete_local_handoff'])
        spec['variants'][0]['edits'][0]['framing']='New crop; old output has not been checked against this'
        self.compose(spec,replace=True)
        self.assertFalse(self.board()['variants']['main']['complete_local_handoff'])
        self.observe('output:video','technical','pass')
        self.assertTrue(self.board()['variants']['main']['complete_local_handoff'])
        self.observe('output:clip','technical','fail')
        self.assertFalse(self.board()['variants']['main']['complete_local_handoff'])

    def test_parent_rights_and_registered_revision_changes_cannot_be_hidden_by_a_child(self):
        spec=self.spec();parent=spec['materials'][0];parent['rights']['status']='unknown'
        child=copy.deepcopy(parent);child.update(id='derived',derived_from=['clip'],origin='Derived fixture')
        child['rights']['status']='licensed';spec['materials'].append(child)
        spec['scenes'][0]['materials']=['derived'];spec['scenes'][0]['claims']=[]
        for variant in spec['variants']:variant['edits'][0]['material']='derived'
        self.compose(spec)
        self.assertTrue(any('material clip: rights unresolved' in p for p in self.board()['variants']['main']['blockers']))
        self.clip.write_bytes(b'replaced synthetic source')
        self.cli('retain',self.project,'clip',self.clip,'--replace')
        self.assertTrue(any('retained revision changed' in p for p in self.board()['variants']['main']['blockers']))

    def test_bad_specs_do_not_mutate_project_and_production_checksum_detects_manual_drift(self):
        self.compose(self.spec());before=self.project.read_bytes()
        bad=[]
        value=self.spec();value['variants'][0]['edits'][0]['duration_seconds']=True;bad.append(value)
        value=self.spec();value['variants'][0]['edits'][0]['source_out']=99;bad.append(value)
        value=self.spec();value['materials'][0]['derived_from']=['clip'];bad.append(value)
        value=self.spec();value['scenes'][0]['materials']=['unknown'];bad.append(value)
        value=self.spec();value['materials'][0]['rightz']={};bad.append(value)
        value=self.spec();value['variants'][0]['delivery']['../../bad']='clip';bad.append(value)
        for spec in bad:
            self.compose(spec,replace=True,ok=False);self.assertEqual(before,self.project.read_bytes())
        data=json.loads(before);data['production']['scenes'][0]['tell']='Changed outside the CLI'
        self.project.write_text(json.dumps(data));before=self.project.read_bytes()
        self.cli('resume',self.project,ok=False);self.assertEqual(before,self.project.read_bytes())

    def test_changed_final_bytes_are_omitted_from_draft_and_markdown_stays_literal(self):
        spec=self.complete_fixture();spec['scenes'][0]['tell']='![remote](https://example.test/pixel)'
        self.compose(spec,replace=True)
        text=self.cli('board',self.project).stdout
        self.assertNotIn('![remote](',text)
        (self.root/'video.mp4').write_bytes(b'changed final file')
        target=self.root/'draft-changed'
        self.cli('bundle',self.project,'main','--output',target,'--draft')
        result=json.loads((target/'manifest.json').read_text())
        self.assertFalse(result['complete_local_handoff']);self.assertNotIn('video',result['files'])
        self.assertTrue(any('changed' in p for p in result['report']['variants']['main']['blockers']))

    def test_copy_drift_fails_before_creating_destination(self):
        self.complete_fixture()
        import runpy
        from unittest.mock import patch
        api=runpy.run_path(str(CLI));data=api['load'](self.project);view=self.board();target=self.root/'bad-copy'
        production=api['PRODUCTION']
        def corrupt_copy(source,target):Path(target).write_bytes(b'changed during copy')
        with patch('shutil.copyfile',side_effect=corrupt_copy):
            with self.assertRaises(ValueError):
                production['build_bundle'](data,view,'main',self.root,target,'fixture-project-hash',str)
        self.assertFalse(target.exists());self.assertEqual(list(self.root.glob('.framewright-kit-*')),[])

    def test_public_template_stays_a_plan_with_shared_capture_and_separate_narration(self):
        self.cli('compose',self.project,ROOT/'examples/production/review-main-short.json')
        board=self.board()
        self.assertEqual(board['variants']['main']['edits'][0]['material'],board['variants']['short']['edits'][0]['material'])
        self.assertNotEqual(board['variants']['main']['edits'][0]['narration']['material'],board['variants']['short']['edits'][0]['narration']['material'])
        self.assertTrue(all(not v['complete_local_handoff'] for v in board['variants'].values()))
        self.assertFalse(board['publication_authorized'])
