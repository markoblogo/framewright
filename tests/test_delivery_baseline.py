"""Shared player proof must not suppress regression after a contract/scope change."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

CHECKER=Path(__file__).resolve().parents[1]/'skills/video-production-router/scripts/delivery_check.cjs'
@unittest.skipUnless(shutil.which('node'),'Node is optional for browser delivery checks')
class PlayerBaselineTests(unittest.TestCase):
    def check_reuse(self,entry,key='current',platforms=None,copy=True):
        payload={'entry':entry,'key':key,'scope':{'platforms':platforms or ['youtube','tiktok'],'copy':copy}}
        script="const {reusable}=require(process.argv[1]);const p=JSON.parse(process.argv[2]);console.log(JSON.stringify(reusable(p.entry,p.key,p.scope)));"
        p=subprocess.run(['node','-e',script,str(CHECKER),json.dumps(payload)],capture_output=True,text=True,check=True)
        return json.loads(p.stdout)
    def baseline(self):
        return {'state':'passed','key':'current','checked_at':'2026-11-20','platforms':['youtube','tiktok'],'copy':True}
    def test_matching_proof_reused_across_new_package(self):
        self.assertTrue(self.check_reuse(self.baseline()))
    def test_template_server_browser_or_checker_change_invalidates(self):
        self.assertFalse(self.check_reuse(self.baseline(),key='changed-contract'))
    def test_landscape_only_proof_cannot_qualify_portrait(self):
        entry=self.baseline();entry['platforms']=['youtube'];self.assertFalse(self.check_reuse(entry))
    def test_missing_clipboard_proof_cannot_qualify_copy_fields(self):
        entry=self.baseline();entry['copy']=False;self.assertFalse(self.check_reuse(entry))
    def test_failed_corrupt_or_missing_proof_is_not_reused(self):
        for entry in [None,{},dict(self.baseline(),state='failed'),dict(self.baseline(),platforms='youtube')]:
            with self.subTest(entry=entry):self.assertFalse(self.check_reuse(entry))
