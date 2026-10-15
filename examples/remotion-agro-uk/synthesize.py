from pathlib import Path
import wave,json,time,hashlib
import onnxruntime as ort
ort.disable_telemetry_events()
from piper import PiperVoice,SynthesisConfig
b=Path(__file__).parent
model=b/'models/tetiana.onnx'
if hashlib.sha256(model.read_bytes()).hexdigest()!='1206d8447b99632badeb63d6132241f76cf551874e5254eb8836db36aed7c85c':raise ValueError('Model hash mismatch')
v=PiperVoice.load(str(model));rows=[]
lines=[('grain','Ринок починається із зерна. Але угода — це значно більше.'),('route','Якість, ціна, логістика. І люди, які з’єднують усе.'),('deal','Від офера до контракту та виконання.'),('book','Брокеридж на ринках зернових та олійних.'),('cta','Безкоштовний практичний гід українською. Завантажуйте та читайте.')]
for name,text in lines:
 t=time.monotonic()
 with wave.open(str(b/'audio'/f'{name}.wav'),'wb') as w:v.synthesize_wav(text,w,syn_config=SynthesisConfig(length_scale=1.0))
 with wave.open(str(b/'audio'/f'{name}.wav')) as w:seconds=w.getnframes()/w.getframerate()
 rows.append({'id':name,'text':text,'duration':seconds,'synthesis_sec':round(time.monotonic()-t,3)})
 print(name,seconds,flush=True)
(b/'audio/voice-lines.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
