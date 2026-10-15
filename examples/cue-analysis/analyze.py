import argparse
from pathlib import Path
import json,time,hashlib,csv
import numpy as np,soundfile as sf
import librosa
from scenedetect import detect,ContentDetector
parser=argparse.ArgumentParser(description='Analyze a local music stem and encoded video against predeclared sparse landmarks. No rendering or providers.')
parser.add_argument('--music',type=Path,required=True)
parser.add_argument('--video',type=Path,required=True)
parser.add_argument('--reference',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
r=args.output
ref=json.loads(args.reference.read_text())
for key,tol in [('target_music_accents_seconds',ref['accent_tolerance_seconds']),('expected_all_hard_cuts_seconds',ref['cut_tolerance_seconds'])]:
 values=ref[key]
 if not values or any(type(v) not in (int,float) or not np.isfinite(v) or v<0 for v in values) or any(b-a<=2*tol for a,b in zip(sorted(values),sorted(values)[1:])):
  raise ValueError('Reference markers must be nonempty, finite, nonnegative and separated by more than twice tolerance: '+key)
r.mkdir(parents=True,exist_ok=False)
start=time.monotonic()
music=args.music;video=args.video
y,sr=sf.read(music);y=librosa.to_mono(y.T);y=librosa.resample(y,orig_sr=sr,target_sr=22050)
onsets=librosa.onset.onset_detect(y=y,sr=22050,hop_length=256,backtrack=False,units='time')
tempo,beat=librosa.beat.beat_track(y=y,sr=22050,hop_length=256,units='time')
scenes=detect(str(video),ContentDetector(threshold=27,min_scene_len=15),start_in_scene=True)
cuts=[s[0].get_seconds() for s in scenes[1:]]
rows=[]
for kind,targets,candidates,tolerance in [('music-accent',ref['target_music_accents_seconds'],onsets,ref['accent_tolerance_seconds']),('all-cut',ref['expected_all_hard_cuts_seconds'],cuts,ref['cut_tolerance_seconds'])]:
 for t in targets:
  nearest=min(candidates,key=lambda x:abs(x-t)) if len(candidates) else None
  delta=abs(float(nearest)-t) if nearest is not None else None
  rows.append({'kind':kind,'reference_seconds':t,'detected_seconds':float(nearest) if nearest is not None else None,'absolute_error_seconds':delta,'matched':delta is not None and delta<=tolerance+1e-7})
allcutmatched=sum(x['matched'] for x in rows if x['kind']=='all-cut');accentmatched=sum(x['matched'] for x in rows if x['kind']=='music-accent')
result={'reference_sha256':hashlib.sha256(args.reference.read_bytes()).hexdigest(),'parameter_adjustments':0,'rows':rows,'cuts_seconds':cuts,'onsets_seconds':onsets.tolist(),'exploratory_beats_seconds':beat.tolist(),'exploratory_tempo_bpm':np.atleast_1d(tempo).tolist(),'accent_matches':accentmatched,'accent_targets':len(ref['target_music_accents_seconds']),'cut_matches':allcutmatched,'cut_targets':len(ref['expected_all_hard_cuts_seconds']),'cut_recall':allcutmatched/len(ref['expected_all_hard_cuts_seconds']),'cut_precision':allcutmatched/len(cuts) if cuts else 0,'extra_cut_candidates':len(cuts)-allcutmatched,'onset_precision':'NOT_ESTIMABLE from sparse accent annotations; other musical attacks are not labelled false positives','passed_authored_reference_tolerances':accentmatched>=ref['minimum_accent_matches'] and allcutmatched==len(ref['expected_all_hard_cuts_seconds']),'independent_human_listening':'pending','duration_seconds':round(time.monotonic()-start,3),'versions':{'librosa':librosa.__version__}}
(r/'comparison.json').write_text(json.dumps(result,indent=2)+'\n');(r/'cue-sheet.json').write_text(json.dumps({'onsets_seconds':onsets.tolist(),'beats_seconds':beat.tolist(),'picture_cuts_seconds':cuts,'reference_sha256':result['reference_sha256']},indent=2)+'\n')
with (r/'cuts.csv').open('w') as f:
 writer=csv.writer(f);writer.writerow(['scene','start_frame','end_frame_exclusive','start_seconds','end_seconds'])
 for i,(a,z) in enumerate(scenes,1):writer.writerow([i,a.get_frames(),z.get_frames(),a.get_seconds(),z.get_seconds()])
print(json.dumps({k:v for k,v in result.items() if k not in ['onsets_seconds','exploratory_beats_seconds']},indent=2),flush=True)
