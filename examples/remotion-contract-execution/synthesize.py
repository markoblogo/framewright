from pathlib import Path
import os,json,hashlib,time,sys
b=Path(__file__).parent;shared=Path(os.environ['SUPERTONIC_SOURCE_ROOT'])
os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HOME']=str(b/'cache/hf');os.environ['SUPERTONIC_CACHE_DIR']=str(b/'cache/supertonic')
manifest=json.loads((shared/'model-manifest.json').read_text());root=shared/'models/Supertonic-3'
for r in manifest['files']:
 if hashlib.sha256((root/r['file']).read_bytes()).hexdigest()!=r['sha256']:raise ValueError('Changed model/config/style:'+r['file'])
(b/'guides/model-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
import numpy as np,soundfile as sf,onnxruntime as ort
ort.disable_telemetry_events()
from supertonic import TTS
tts=TTS(model='supertonic-3',model_dir=root,auto_download=False,intra_op_num_threads=4,inter_op_num_threads=1);style=tts.get_voice_style('F1')
lines=[('opening','A signed contract is only the beginning.',.6),('control','Documents. Logistics. Inspections. Every handover needs control.',4.8),('evidence','Track responsibilities, manage exceptions, and keep the evidence together.',10.8),('closeout','From payment control to financial reconciliation and contract closeout.',16.8),('title','The Contract Execution Officer Handbook. A practical guide to physical commodity contract execution with M N seven R.',22.6)]
rows=[]
for i,(name,text,start) in enumerate(lines):
 if '--probe' in sys.argv and i:break
 target=b/'audio'/f'{name}.wav';ts=time.monotonic()
 if not target.exists():
  np.random.seed(20261017+i);wav,d=tts.synthesize(text=text,voice_style=style,lang='en',total_steps=12,speed=1.0,max_chunk_length=300,silence_duration=.25,verbose=False);tts.save_audio(wav,str(target))
 a,sr=sf.read(target)
 if not np.isfinite(a).all() or not len(a):raise ValueError('Invalid speech')
 row={'id':name,'text':text,'start':start,'seconds':len(a)/sr,'sample_rate':sr,'peak_dbfs':float(20*np.log10(max(abs(a).max(),1e-12))),'clipped_samples':int((abs(a)>=.999969).sum()),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'wall_seconds':round(time.monotonic()-ts,3)};rows.append(row);print(row,flush=True)
(b/'audio/voice-lines.json').write_text(json.dumps(rows,indent=2)+'\n')
