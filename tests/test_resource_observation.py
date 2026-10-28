import runpy
from pathlib import Path
from types import SimpleNamespace as NS
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'skills/video-production-router/scripts/resources.py'

class ResourceObservationTest(unittest.TestCase):
 def module(self): return runpy.run_path(str(SCRIPT))
 def test_unavailable_memory_stays_null_and_does_not_claim_host_fit(self):
  r=self.module()['snapshot']([Path.cwd()],backend=None)
  self.assertIsNone(r['memory']['available_bytes'])
  self.assertEqual(r['memory']['status'],'unavailable')
  self.assertFalse(r['workload_qualified'])
  self.assertEqual(len(r['volumes']),1)
 def test_available_memory_is_distinct_from_total_and_disk_errors_are_explicit(self):
  backend=NS(__version__='fixture',virtual_memory=lambda:NS(total=100,available=30),swap_memory=lambda:NS(total=50,used=10))
  r=self.module()['snapshot']([Path('/not/a/real/volume')],backend=backend)
  self.assertEqual(r['memory']['total_bytes'],100)
  self.assertEqual(r['memory']['available_bytes'],30)
  self.assertIsNone(r['volumes'][0]['free_bytes'])
 def test_denied_child_tree_still_samples_the_owned_root(self):
  class Process:
   pid=123
   def create_time(self):return 10
   def children(self,recursive=True):raise PermissionError('denied')
   def cpu_percent(self,interval=None):return 5
   def memory_info(self):return NS(rss=4096)
  b=NS(__version__='fixture',Process=lambda pid:Process())
  sampler=self.module()['OwnedSampler'](123,backend=b,max_samples=1)
  sampler.sample();sampler.sample();r=sampler.report()
  self.assertEqual(r['samples'],1)
  self.assertEqual(r['sampled_peak_rss_bytes'],4096)
  self.assertTrue(r['partial_coverage'])

 def test_owned_sampler_rejects_pid_reuse_and_bounds_samples(self):
  m=self.module(); calls=[10,11]
  class Process:
   pid=123
   def create_time(self):return calls.pop(0) if calls else 11
   def children(self,recursive=True):return []
   def cpu_percent(self,interval=None):return 0
   def memory_info(self):return NS(rss=1234)
  b=NS(__version__='fixture',Process=lambda pid:Process())
  s=m['OwnedSampler'](123,backend=b,max_samples=2)
  s.sample();r=s.report()
  self.assertEqual(r['samples'],0)
  self.assertTrue(r['errors'])
  self.assertIsNone(r['sampled_peak_rss_bytes'])

if __name__=='__main__':unittest.main()
