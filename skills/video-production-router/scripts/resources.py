"""Optional bounded host/owned-process observations. No installations or fit claims."""
from datetime import datetime, timezone
import math
import os
from pathlib import Path
import platform
import shutil
import threading
import time

AUTO=object()

def optional_backend():
 try:
  import psutil
  return psutil
 except ImportError:return None

def snapshot(volumes, backend=AUTO):
 backend=optional_backend() if backend is AUTO else backend
 memory={'status':'unavailable','total_bytes':None,'available_bytes':None,'swap_total_bytes':None,'swap_used_bytes':None}
 if backend is not None:
  try:
   vm=backend.virtual_memory();memory.update(status='observed',total_bytes=vm.total,available_bytes=vm.available)
  except Exception:memory['status']='unavailable'
  try:
   swap=backend.swap_memory();memory.update(swap_total_bytes=swap.total,swap_used_bytes=swap.used)
  except Exception:pass
 rows=[]
 if len(volumes)>8:raise ValueError('At most eight explicitly selected volumes')
 for path in dict.fromkeys(map(str,volumes)):
  try:free=shutil.disk_usage(path).free;status='observed'
  except OSError:free=None;status='unavailable'
  rows.append({'path':path,'status':status,'free_bytes':free})
 return {'schema':'framewright-resource-snapshot-v1','observed_at':datetime.now(timezone.utc).isoformat(),
         'platform':platform.system(),'architecture':platform.machine(),
         'backend_version':getattr(backend,'__version__',None),'memory':memory,'volumes':rows,
         'workload_qualified':False,'scope':'Time-bound host snapshot; no GPU/model/codec, storage speed or internet-fit inference'}

class OwnedSampler:
 """Only attach to a Popen child owned by the caller; never arbitrary system discovery."""
 def __init__(self,pid,backend=AUTO,interval=0.25,max_samples=720):
  if not math.isfinite(interval) or not 0.1<=interval<=5 or type(max_samples)!=int or not 1<=max_samples<=720:
   raise ValueError('Bound observation interval/samples')
  self.backend=optional_backend() if backend is AUTO else backend
  self.pid=pid;self.interval=interval;self.maximum=max_samples;self.started=time.monotonic()
  self.rows=[];self.errors=[];self.process=None;self.identity=None;self.known={};self.stop_event=threading.Event();self.thread=None
  if self.backend is not None:
   try:
    self.process=self.backend.Process(pid);self.identity=self.process.create_time()
    self.known[(pid,self.identity)]=self.process;self.process.cpu_percent(interval=None)
   except Exception:self.errors.append('Owned worker unavailable at attachment')
 def sample(self):
  if self.process is None or len(self.rows)>=self.maximum:return
  try:
   if self.backend.Process(self.pid).create_time()!=self.identity:raise ValueError('PID identity changed')
   try:children=self.process.children(recursive=True)
   except Exception:
    children=[];self._error('Child tree unavailable; root-only coverage')
   if len(children)>128:raise ValueError('Child coverage exceeds bounded limit')
   processes=[self.process,*children];rss=0;cpu=0;coverage=0;cpu_coverage=0
   for p in processes:
    try:
     key=(p.pid,p.create_time())
     if key not in self.known:
      self.known[key]=p;p.cpu_percent(interval=None) # discard meaningless first CPU sample
     else:
      cpu+=self.known[key].cpu_percent(interval=None);cpu_coverage+=1
     rss+=p.memory_info().rss;coverage+=1
    except Exception:self._error('Exited/inaccessible child; partial coverage')
   if coverage:self.rows.append({'rss':rss,'cpu':cpu if cpu_coverage else None,'processes':coverage,'expected':len(processes)})
  except Exception:self._error('Worker exited/inaccessible or PID identity changed; partial coverage')
 def _error(self,msg):
  if msg not in self.errors:self.errors.append(msg)
 def start(self):
  if self.process is None:return self
  def loop():
   while not self.stop_event.wait(self.interval):
    self.sample()
    if len(self.rows)>=self.maximum:return
  self.thread=threading.Thread(target=loop,daemon=True);self.thread.start();return self
 def finish(self):
  self.stop_event.set()
  if self.thread:self.thread.join(timeout=6)
  return self.report()
 def report(self):
  return {'schema':'framewright-owned-worker-resources-v1','backend_version':getattr(self.backend,'__version__',None),
   'status':'observed' if self.rows else 'unavailable','pid':self.pid,'process_created_at':self.identity,
   'sample_interval_seconds':self.interval,'samples':len(self.rows),'sample_limit':self.maximum,
   'elapsed_seconds':time.monotonic()-self.started,
   'sampled_peak_rss_bytes':max((r['rss'] for r in self.rows),default=None),
   'sampled_peak_cpu_percent':max((r['cpu'] for r in self.rows if r['cpu'] is not None),default=None),
   'partial_coverage':bool(self.errors) or any(r['processes']!=r['expected'] for r in self.rows),'errors':self.errors,
   'scope':'Owned worker plus observed children only; sampled RSS may double-count shared pages; CPU convention 100% per core. Not a guaranteed peak, hard memory cap or workload qualification.'}
