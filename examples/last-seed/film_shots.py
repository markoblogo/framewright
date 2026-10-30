"""Manual original-scene rough-cut renderer. No providers or publishing."""
import bpy,sys,math,json,hashlib,time
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from seed_design import grain,irrigation,tube
args=sys.argv[sys.argv.index('--')+1:];base=Path(args[0]);out=Path(args[1]);controls='--controls' in args
if out.exists():raise ValueError('Use a new revision directory')
out.mkdir(parents=True)
DUR={'S01':3,'S02':4,'S03':3,'S05':5,'S06':7.5,'S07':5,'S08':5}
report={'native_canvas':[960,540],'native_fps':12,'samples':8,'manual_eevee':True,'source_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'shots':[]}
def material(name,color,alpha=1):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.27;p.inputs['Alpha'].default_value=alpha
 if alpha<1:m.surface_render_method='BLENDED'
 return m
def cube(name,loc,size,mat):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=size;o.data.materials.append(mat);return o
def cylinder(name,loc,radius,depth,mat):
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=radius,depth=depth,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(mat);return o
def aim(cam,location,target,lens):
 cam.location=location;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
started=time.monotonic()
for shot,duration in DUR.items():
 if '--only' in args and shot!=args[args.index('--only')+1]:continue
 bpy.ops.wm.open_mainfile(filepath=str(base),use_scripts=False);s=bpy.context.scene;s.frame_set(72)
 for o in s.objects:
  loc=o.location.copy();rot=o.rotation_euler.copy();scale=o.scale.copy();o.animation_data_clear();o.location=loc;o.rotation_euler=rot;o.scale=scale
  if o.type=='MESH' and o.data.shape_keys:o.data.shape_keys.animation_data_clear()
 for m in bpy.data.materials:
  if m.use_nodes:m.node_tree.animation_data_clear()
 s.world.node_tree.animation_data_clear()
 grain();cam=s.camera;cam.data.dof.use_dof=False
 young=shot in ('S01','S02','S03')
 for o in s.objects:
  if o.name.startswith(('SeedLeft','SeedRight','Stalk','Leaf')):o.hide_render=young
 brass=bpy.data.materials['OldBrass'];teal=bpy.data.materials['DeepTealSteel']
 # Four-seat cassette, three empty sockets and one physical seed above the tray.
 cassette=[]
 cassette.append(cube('SeedCassette',(-.3,0,.79),(.9,.34,.018),teal))
 dark=material('SocketDark',(.014,.024,.024))
 for x in [-.6,-.4,-.2,0]:
  cutter=cylinder('SocketCutter',(x,0,.80),.07,.16,dark);cutter.scale.y=1.8;cutter.hide_render=True
  modifier=cassette[0].modifiers.new('SocketRecess','BOOLEAN');modifier.operation='DIFFERENCE';modifier.object=cutter
  cassette.append(cylinder('SocketBottom',(x,0,.758),.074,.005,dark))
 for y in [-.155,.155]:cassette.append(cube('CassetteRail',(-.3,y,.815),(.9,.012,.018),brass))
 gate=cube('ReleaseGate',(0,0,.828),(.19,.28,.012),brass);cassette.append(gate)
 for name in ['SeedLeft','SeedRight']:
  src=bpy.data.objects[name];o=src.copy();o.data=src.data.copy();s.collection.objects.link(o);o.name='Cassette'+name;o.hide_render=not young;o.location=(0,0,.836);o.rotation_euler=(0,0,0);o.scale=(1,1,1);cassette.append(o)
 for o in cassette:o.hide_render=(not young) if o.name.startswith('CassetteSeed') else False
 tube('CassetteBracket',[(-.73,.10,-.2),(-.73,.10,.72),(-.68,.1,.79)],.010,brass)
 if not young:gate.location.y=-.19
 level=irrigation()
 lamp=bpy.data.objects['WorkingLamp'].data;sun=bpy.data.objects['DawnSun'];em=bpy.data.materials['LampEmitter'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
 maxframe=round(duration*12);s.frame_start=1;s.frame_end=maxframe;s.render.fps=12
 leafrot={o.name:o.rotation_euler.copy() for o in s.objects if o.name.startswith('Leaf') and o.parent is None}
 for f in range(1,maxframe+1):
  u=(f-1)/(maxframe-1);lamp.energy=55;sun.data.energy=.25;em.default_value=1.5
  if shot=='S01':aim(cam,(3.8-.2*u,-6.2+.7*u,2.5-.2*u),(0,.45,.65),38)
  elif shot=='S02':
   aim(cam,(.8-.18*u,-1.15+.12*u,1.46),(-.25,0,.84),55);gate.location.y=-.04*max(0,(u-.65)/.35);gate.keyframe_insert(data_path='location',frame=f)
  elif shot=='S03':
   aim(cam,(-1.38+.16*u,-.2-.15*u,1.65-.08*u),(-.58+.10*u,.59-.05*u,1.43-.03*u),48)
   level.scale.z=1-.5*u;level.location.z=1.254-.0065*u
   level.keyframe_insert(data_path='scale',frame=f);level.keyframe_insert(data_path='location',frame=f)
  elif shot=='S05':aim(cam,(1.3-.12*u,-3.5,1.8),(0,0,.85),38)
  elif shot=='S06':aim(cam,(1.25-.06*u,-2.25,1.16),(0,0,.38),55)
  elif shot=='S07':aim(cam,(3.35+.65*u,-4.85-1.65*u,2.22+.48*u),(0,.45,.65),38)
  else:aim(cam,(4+.12*u,-6.5-.2*u,2.7),(0,.45,.65),38)
  fade=max(0,min(1,(u-.3)/.65)) if shot=='S05' else (1 if shot in ('S06','S07','S08') else 0)
  dawn=(u*u*(3-2*u)) if shot=='S06' else (1 if shot in ('S07','S08') else 0)
  lamp.energy=55*(1-fade);em.default_value=1.5*(1-fade);sun.data.energy=.05+2.1*dawn if shot in ('S06','S07','S08') else .25
  for name,power in [('Key',95),('Fill',40),('BackLight',90)]:
   light=bpy.data.objects[name].data;light.energy=power*(1-.65*fade);light.keyframe_insert(data_path='energy',frame=f)
  bg=s.world.node_tree.nodes['Background'];bg.inputs[0].default_value=(.10+.22*dawn,.16+.14*dawn,.21+.02*dawn,1);bg.inputs[0].keyframe_insert(data_path='default_value',frame=f)
  sun.rotation_euler=(math.radians(62-14*dawn),math.radians(-20),math.radians(-165))
  for name,rot in leafrot.items():
   o=bpy.data.objects[name];o.rotation_euler=rot;o.rotation_euler[0]+=.015*math.sin(f/12*1.4);o.keyframe_insert(data_path='rotation_euler',frame=f)
  cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_euler',frame=f)
  sun.keyframe_insert(data_path='rotation_euler',frame=f);sun.data.keyframe_insert(data_path='energy',frame=f);lamp.keyframe_insert(data_path='energy',frame=f);em.keyframe_insert(data_path='default_value',frame=f)
 s.render.engine='BLENDER_EEVEE_NEXT';s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.eevee.taa_render_samples=8;s.render.threads_mode='FIXED';s.render.threads=2;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
 folder=out/shot;folder.mkdir();bpy.ops.wm.save_as_mainfile(filepath=str(folder/'scene.blend'))
 row={'shot':shot,'duration_seconds':duration,'frames_expected':maxframe,'scene_sha256':hashlib.sha256((folder/'scene.blend').read_bytes()).hexdigest(),'frames':[]};tic=time.monotonic()
 for f in ([1,maxframe//2,maxframe] if controls else range(1,maxframe+1)):
  s.frame_set(f);path=folder/f'frame_{f:06d}.png';s.render.filepath=str(path);bpy.ops.render.render(write_still=True);row['frames'].append({'frame':f,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'camera':list(cam.location),'lamp_energy':lamp.energy,'sun_energy':sun.data.energy})
 row['render_seconds']=time.monotonic()-tic;report['shots'].append(row);(out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
report['elapsed_seconds']=time.monotonic()-started;(out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
