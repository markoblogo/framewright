"""Explicit manual narrative tests/full rough renders for the rain recovery story."""
import bpy,sys,json,time,hashlib,math
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from recovery_design import Rig
args=sys.argv[sys.argv.index('--')+1:];source=Path(args[0]);out=Path(args[1]);controls='--controls' in args
if out.exists():raise ValueError('New output directory required')
out.mkdir();durations={'ground':2,'rain':2,'roof':7,'water':5,'recover':7,'up':8};starts={'ground':0,'rain':2,'roof':21.5,'water':28.5,'recover':33.5,'up':40.5}
report={'manual_eevee':True,'native_canvas':[960,540],'fps':12,'samples':8,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'shots':[]};started=time.monotonic()
for stage,duration in durations.items():
 if '--only' in args and stage not in args[args.index('--only')+1].split(','):continue
 bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False);s=bpy.context.scene;s.frame_set(36)
 for o in s.objects:
  loc=o.location.copy();rot=o.rotation_euler.copy();scale=o.scale.copy();o.animation_data_clear();o.location=loc;o.rotation_euler=rot;o.scale=scale
  if o.type=='MESH' and o.data.shape_keys:o.data.shape_keys.animation_data_clear()
 for m in bpy.data.materials:
  if m.use_nodes:m.node_tree.animation_data_clear()
 s.world.node_tree.animation_data_clear();rig=Rig();cam=s.camera;cam.data.dof.use_dof=False
 n=round(duration*12);s.frame_start=1;s.frame_end=n;s.render.fps=12;s.render.engine='BLENDER_EEVEE_NEXT';s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.render.threads_mode='FIXED';s.render.threads=2;s.eevee.taa_render_samples=8;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
 def aim(loc,target,lens):cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
 folder=out/stage;folder.mkdir();rows=[]
 # Bake all authored transforms, material controls and lamp retraction into saved scene.
 for f in range(1,n+1):
  t=(f-1)/12;u=(f-1)/(n-1);rig.pose(stage,t,starts[stage]+t)
  if stage=='ground':aim((.58-.09*u,-.9+.1*u,.5),(0,0,.015),60)
  elif stage=='rain':aim((1.6-.15*u,-2.6,3.5),(.5,-.6,2.82),46)
  elif stage=='roof':aim((2.5-.2*u,-2.8+.15*u,2.55+.13*u),(1.02,-.82,2.43+.12*u),45)
  elif stage=='water':aim((.82-.05*u,-1.55,1.05),(0,0,.4),52)
  elif stage=='recover':aim((1.1-.1*u,-1.95,1.15+.1*u),(0,0,.45+.12*u),52)
  else:
   if u<.45:
    v=u/.45;loc=(.46,-1.15+.20*v,.62+.65*v);target=(0,-.02,.30+.45*v)
   else:
    v=(u-.45)/.55;loc=(.46-.10*v,-.95+.85*v,1.27+2.15*v);target=(.20+.35*v,-.02+.22*v,.75+6.0*v)
   aim(loc,target,43)
  dawn=min(1,max(0,t/7)) if stage=='recover' else (1 if stage=='up' else 0)
  lamp=bpy.data.objects['WorkingLamp'].data;lamp.energy=0 if stage in ('roof','water','recover','up') else 55
  emitter=bpy.data.materials['LampEmitter'].node_tree.nodes['Principled BSDF'];emitter.inputs['Emission Strength'].default_value=0 if stage in ('roof','water','recover','up') else 1.5
  for name,p in [('Key',95),('Fill',40),('BackLight',90)]:bpy.data.objects[name].data.energy=p*(.30+.35*dawn if stage in ('roof','water','recover','up') else 1)
  if stage=='roof':bpy.data.objects['Fill'].data.energy=100
  sun=bpy.data.objects['DawnSun'];sun.data.energy=.08+2.2*dawn;sun.rotation_euler=(math.radians(56-9*dawn),math.radians(-20),math.radians(-165))
  bg=s.world.node_tree.nodes['Background'];bg.inputs[0].default_value=(.10+.25*dawn,.16+.25*dawn,.21+.30*dawn,1);bg.inputs[1].default_value=.5+.2*dawn
  for o in s.objects:
   for key in ('location','rotation_euler','rotation_quaternion','scale','hide_render'):o.keyframe_insert(data_path=key,frame=f)
   if o.type=='LIGHT':o.data.keyframe_insert(data_path='energy',frame=f)
  for m in bpy.data.materials:
   if m.use_nodes:
    p=m.node_tree.nodes.get('Principled BSDF')
    if p:
     for key in ['Base Color','Emission Strength']:p.inputs[key].keyframe_insert(data_path='default_value',frame=f)
  for key in [0,1]:bg.inputs[key].keyframe_insert(data_path='default_value',frame=f)
  rows.append({'frame':f,'time':t,'roof_angle':rig.opening(t) if stage=='roof' else (.64 if stage in ('water','recover','up') else 0),'lamp_energy':lamp.energy,'sun_energy':sun.data.energy,'camera':list(cam.location)})
 s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(folder/'scene.blend'));item={'shot':stage,'duration_seconds':duration,'frames_expected':n,'scene_sha256':hashlib.sha256((folder/'scene.blend').read_bytes()).hexdigest(),'frames':[]};tic=time.monotonic()
 for f in ([1,n//2,n] if controls else range(1,n+1)):
  s.frame_set(f);path=folder/f'frame_{f:06d}.png';s.render.filepath=str(path);bpy.ops.render.render(write_still=True);item['frames'].append({**rows[f-1],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 item['render_seconds']=time.monotonic()-tic;report['shots'].append(item);(out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
report['elapsed_seconds']=time.monotonic()-started;(out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
