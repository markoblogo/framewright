"""Versioned correction of retained scenes: shell, mounted drive and rain spread."""
import bpy,sys,json,hashlib,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from surface_mechanics import shell_texture,mechanism,rain_spread
args=sys.argv[sys.argv.index('--')+1:];root=Path(args[0]);spec=json.loads(Path(args[1]).read_text());out=Path(args[2]);controls='--controls' in args
if out.exists():raise ValueError('New output directory required')
out.mkdir();report={'manual_eevee':True,'executor_admission':False,'shots':[]};started=time.monotonic()
for name,relative in spec.items():
 source=(root/relative).resolve();bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False);s=bpy.context.scene;s.frame_set(1);shell_texture();changes={'shell':'pitted, longitudinally grooved, varied brown husk'}
 if 'RoofVentHinge' in bpy.data.objects:
  changes['mechanism']=mechanism()
  if name!='roof':bpy.data.objects['MechanismSoftbox'].data.energy=0
 if name=='water':changes['drop_targets']=rain_spread()
 if name=='hero':s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24
 s.render.threads_mode='FIXED';s.render.threads=2;s.render.engine='BLENDER_EEVEE_NEXT';s.eevee.taa_render_samples=16 if name=='hero' else 8
 s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8'
 folder=out/name;folder.mkdir();s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(folder/'scene.blend'));n=s.frame_end;fps=s.render.fps;row={'shot':name,'duration_seconds':n/fps,'native_canvas':[s.render.resolution_x,s.render.resolution_y],'fps':fps,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scene_sha256':hashlib.sha256((folder/'scene.blend').read_bytes()).hexdigest(),'changes':changes,'frames':[]};tic=time.monotonic()
 for f in ([1,n//2,n] if controls else range(1,n+1)):
  s.frame_set(f);path=folder/f'frame_{f:06d}.png';s.render.filepath=str(path);bpy.ops.render.render(write_still=True);row['frames'].append({'frame':f,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 row['render_seconds']=time.monotonic()-tic;report['shots'].append(row);(out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
report['elapsed_seconds']=time.monotonic()-started;(out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
