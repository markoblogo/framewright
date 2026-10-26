import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1] / 'skills/video-production-router/scripts'


class EnvironmentTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.spec = self.root/'requirements.json'; self.out = self.root/'readiness.json'
        self.payload = {'id':'local-sample','platforms':[], 'architectures':[],
            'min_memory_gib':0, 'min_free_disk_gib':0, 'programs':[], 'models':[],
            'manual_checks':[], 'rights':{'status':'unknown','basis':'Not reviewed'},
            'cost':{'status':'unknown','amount':None,'currency':'USD','basis':'No quote'}}

    def cli(self, *args, ok=True):
        self.spec.write_text(json.dumps(self.payload))
        r = subprocess.run([sys.executable,str(BASE/'environment.py'),str(self.spec),*map(str,args)],
                           capture_output=True,text=True,timeout=25)
        self.assertEqual(r.returncode==0,ok,r.stderr)
        return json.loads(r.stdout) if ok else r

    def test_readiness_keeps_technical_rights_cost_and_authority_separate(self):
        r=self.cli()
        self.assertEqual(r['technical_status'],'ready')
        self.assertEqual(r['next_step'],'review_rights_and_cost')
        self.assertFalse(r['execution_authorized'])
        self.assertEqual(r['rights']['status'],'unknown')
        self.assertEqual(r['cost']['amount'],None)
        self.assertEqual(r['executed_probes'],[])
        self.assertEqual(r['manifest_sha256'],hashlib.sha256(self.spec.read_bytes()).hexdigest())

    def test_version_probe_is_explicit_and_export_is_not_inferred(self):
        self.payload['programs']=[{'name':'python3','minimum_version':'3.0'}]
        self.payload['manual_checks']=[{'id':'video-export','status':'unknown','basis':'Export not tested'}]
        r=self.cli();self.assertEqual(r['technical_status'],'unknown');self.assertEqual(r['executed_probes'],[])
        r=self.cli('--probe-versions')
        self.assertEqual(r['technical_status'],'unknown')
        self.assertEqual(len(r['executed_probes']),1)
        self.assertTrue(any(c['id']=='program:python3' and c['status']=='pass' for c in r['checks']))
        self.assertTrue(any(c['id']=='manual:video-export' and c['status']=='unknown' for c in r['checks']))

    def test_missing_models_and_platform_mismatch_need_preparation(self):
        self.payload['platforms']=['ImaginaryOS']
        self.payload['models']=[{'id':'voice','path':'absent.bin','sha256':None}]
        r=self.cli();self.assertEqual(r['technical_status'],'needs_preparation')
        self.assertFalse((self.root/'absent.bin').exists())

    def test_model_hash_and_no_overwrite(self):
        model=self.root/'model.bin';model.write_bytes(b'local fixture')
        self.payload['models']=[{'id':'voice','path':'model.bin','sha256':'0'*64}]
        r=self.cli('--output',self.out)
        self.assertEqual(r['technical_status'],'needs_preparation')
        before=self.out.read_bytes();self.cli('--output',self.out,ok=False)
        self.assertEqual(before,self.out.read_bytes())
        link=self.root/'alias.json';link.symlink_to(self.spec)
        original=self.spec.read_bytes();self.cli('--output',link,ok=False)
        self.assertEqual(original,self.spec.read_bytes())

    def test_arbitrary_commands_nonfinite_values_and_unbased_clearance_rejected(self):
        for key,value in [('programs',[{'name':'sh','minimum_version':None}]),
                          ('min_memory_gib',float('nan')),('min_free_disk_gib',True),
                          ('rights',{'status':'allowed','basis':''})]:
            original=self.payload[key];self.payload[key]=value
            self.cli('--output',self.out,ok=False);self.assertFalse(self.out.exists())
            self.payload[key]=original

    def test_gpu_is_not_inferred_from_a_program_or_platform_name(self):
        self.payload['backends']=['cuda']
        r=self.cli()
        self.assertNotEqual(r['technical_status'],'ready')
        self.assertEqual(r['executed_probes'],[])
        self.payload['backends']=['invented-backend'];self.cli(ok=False)

    def test_empty_model_file_does_not_pass_presence_check(self):
        (self.root/'empty.bin').touch()
        self.payload['models']=[{'id':'empty','path':'empty.bin','sha256':None}]
        self.assertEqual(self.cli()['technical_status'],'needs_preparation')


if __name__=='__main__': unittest.main()
