"""Two original local Eevee staging tests; explicit manual execution, no publishing."""
import bpy,math,json,sys,hashlib,time
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];out=Path(args[0]);mode=args[1]
if mode not in ('wide','dawn') or out.exists():raise ValueError('New output directory and wide/dawn mode required')
out.mkdir(parents=True)
s=bpy.context.scene;s.frame_set(171)
# Freeze accepted mature pose before creating new independent camera/light tests.
for o in list(s.objects):
 loc=o.location.copy();rot=o.rotation_euler.copy();scale=o.scale.copy();o.animation_data_clear();o.location=loc;o.rotation_euler=rot;o.scale=scale
 if o.type=='MESH' and o.data.shape_keys:o.data.shape_keys.animation_data_clear()
for m in bpy.data.materials:
 if m.use_nodes:m.node_tree.animation_data_clear()
for o in list(s.objects):
 if o.name.startswith(('Frame','Crossbar')) or o.name in ('RearGlass','Bench'):o.hide_render=True
s.world.node_tree.nodes['Background'].inputs[1].default_value=.5

def mat(name,col,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=.6;p.inputs['Metallic'].default_value=metal;return m
teal=bpy.data.materials['DeepTealSteel'];brass=bpy.data.materials['OldBrass'];earth=bpy.data.materials['DryEarth'];dry=mat('DryStalk',(.19,.14,.065));floor=mat('Floor',(.10,.13,.12));glass=mat('DawnGlass',(.09,.19,.20))
def cube(name,loc,scale,material):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(material);return o

def beam(name,a,b,r=.035,material=teal):
 d=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=r,depth=d.length,location=(Vector(a)+Vector(b))/2);o=bpy.context.object;o.name=name;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(material);return o
cube('Floor',(0,1,-.85),(7,10,.1),floor)
cube('CentralBench',(0,.2,-.3),(1.65,2.5,.14),teal)
for x in [-.62,.62]:
 for y in [-.65,1]:beam('BenchLeg',(x,y,-.8),(x,y,-.3),.04)
for y in [-2,0,2,4]:
 for side in [-1,1]:
  x=side*3;beam('Pillar',(x,y,-.8),(x,y,2));beam('Rafter',(x,y,2),(0,y,3))
 beam('CrossTie',(-3,y,2),(3,y,2),.022)
beam('RoofRidge',(0,-2,3),(0,4,3))
for x in [-3,3]:beam('Eave',(x,-2,2),(x,4,2))
# Framed rear windows; dawn light travels through their open apertures.
for x in [-3,-1.5,0,1.5,3]:beam('WindowMullion',(x,4,-.8),(x,4,2))
for z in [-.7,.7,2]:beam('WindowCross',(-3,4,z),(3,4,z))
cube('RearSill',(0,4,-.7),(6,.16,.12),teal)
# Owner revision: lightly cloudy glazing, front entry deliberately open.
if mode=='wide':
 # Actual alpha-transmitting glass; low rough surface opacity retains the view outside.
 g=mat('CloudedGreenhouseGlass',(.33,.44,.43),0)
 g.surface_render_method='BLENDED'
 if hasattr(g,'use_transparent_shadow'):g.use_transparent_shadow=False
 shader=g.node_tree.nodes['Principled BSDF'];shader.inputs['Roughness'].default_value=.24;shader.inputs['Coat Weight'].default_value=.32
 shader.inputs['Alpha'].default_value=.16;shader.inputs['IOR'].default_value=1.45
 noise=g.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=4;noise.inputs['Detail'].default_value=2
 opacity=g.node_tree.nodes.new('ShaderNodeMapRange');opacity.inputs['To Min'].default_value=.10;opacity.inputs['To Max'].default_value=.23
 g.node_tree.links.new(noise.outputs['Fac'],opacity.inputs['Value']);g.node_tree.links.new(opacity.outputs[0],shader.inputs['Alpha'])
 def pane(name,points):
  mesh=bpy.data.meshes.new(name);mesh.from_pydata(points,[],[(0,1,2,3)]);mesh.update();o=bpy.data.objects.new(name,mesh);s.collection.objects.link(o);o.data.materials.append(g)
 for side in [-1,1]:
  x=side*3
  for z in [-.7,.7]:beam('SideWindowRail',(x,-2,z),(x,4,z),.025)
  for y0,y1 in [(-2,0),(0,2),(2,4)]:
   for z0,z1 in [(-.7,.7),(.7,2)]:pane('SideGlass',[(x,y0+.04,z0+.04),(x,y1-.04,z0+.04),(x,y1-.04,z1-.04),(x,y0+.04,z1-.04)])
   pane('RoofGlass',[(side*.04,y0+.04,2.987),(side*2.96,y0+.04,2.013),(side*2.96,y1-.04,2.013),(side*.04,y1-.04,2.987)])
 for x0,x1 in [(-3,-1.5),(-1.5,0),(0,1.5),(1.5,3)]:
  for z0,z1 in [(-.7,.7),(.7,2)]:pane('RearGlassPanel',[(x0+.04,4,z0+.04),(x1-.04,4,z0+.04),(x1-.04,4,z1-.04),(x0+.04,4,z1-.04)])
 for side in [-1,1]:pane('RearGableGlass',[(side*.04,4,2.04),(side*2.85,4,2.04),(side*.04,4,2.97),(side*.04,4,2.97)])

for side in [-1,1]:
 x=2.1*side;cube('SideBench',(x,1,-.3),(1.15,4,.12),teal)
 for dx in [-.42,.42]:
  for yleg in [-.7,2.7]:beam('SideLeg',(x+dx,yleg,-.8),(x+dx,yleg,-.3),.035)
 for y in [-.2,1.15,2.5]:
  bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.41,depth=.12,location=(x,y,-.18));o=bpy.context.object;o.name='EmptyTray';o.data.materials.append(brass)
  bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.39,depth=.015,location=(x,y,-.11));bpy.context.object.data.materials.append(earth)
  for k in range(3):beam('DryStem',(x+.07*k,y,-.1),(x+.07*k+.08,y+.03,.15+.07*k),.008,dry)
# Restrained background gradient, no generated scenery.
back=mat('Horizon',(.12,.24,.27));cube('DistantBackground',(0,7,-.65),(24,.1,.3),back)
# Original low-detail exterior: distant relief and tree silhouettes, not an opaque wall.
if mode=='wide':
 outside=mat('NightSilhouette',(.035,.065,.073));pb=outside.node_tree.nodes['Principled BSDF'];pb.inputs['Emission Color'].default_value=(.035,.065,.073,1);pb.inputs['Emission Strength'].default_value=.65
 for layer,y in enumerate([12,18]):
  verts=[(-20,y,-2),(20,y,-2)]+[(x,y,1.1+layer*.35+.55*math.sin(x*.34+layer)+.25*math.sin(x*.71)) for x in range(20,-21,-1)]
  mesh=bpy.data.meshes.new('DistantRelief');mesh.from_pydata(verts,[],[tuple(range(len(verts)))]);mesh.update();o=bpy.data.objects.new('DistantRelief',mesh);s.collection.objects.link(o);o.data.materials.append(outside)
 for i,(x,y,h) in enumerate([(-6,8,4),(-3.9,9,3.6),(-1.7,11,4.3),(1.4,10,3.7),(4.8,9,4.5),(7,11,4),(-6,-.4,3.8)]):
  beam('ExteriorTrunk',(x,y,-.8),(x,y,h-.8),.045,outside)
  for k in range(3):
   z=-.3+h*(.38+.18*k);bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=h*(.21-.035*k),radius2=0,depth=h*.55,location=(x,y,z));bpy.context.object.name='ExteriorTree';bpy.context.object.data.materials.append(outside)
 s.world.node_tree.nodes['Background'].inputs[0].default_value=(.10,.16,.21,1)
# Clearly visible hanging lamp associated with working station.
lampmat=mat('LampEmitter',(.9,.7,.35));bs=lampmat.node_tree.nodes['Principled BSDF'];bs.inputs['Emission Color'].default_value=(1,.62,.22,1)
cube('LampHousing',(0,.0,1.72),(.8,.35,.10),teal);cube('LampDiffuser',(0,0,1.66),(.68,.26,.025),lampmat)
beam('LampCable',(0,0,1.77),(0,0,3),.012)
data=bpy.data.lights.new('WorkingLamp','AREA');lamp=bpy.data.objects.new('WorkingLamp',data);s.collection.objects.link(lamp);lamp.location=(0,-.1,1.62);data.shape='DISK';data.size=.65;data.color=(1,.65,.3)
sun_data=bpy.data.lights.new('DawnSun','SUN');sun=bpy.data.objects.new('DawnSun',sun_data);s.collection.objects.link(sun);sun_data.angle=.06;sun_data.color=(1,.68,.32)
cam=s.camera;cam.data.dof.use_dof=False;cam.data.lens=38 if mode=='wide' else 55
s.frame_start=1;s.frame_end=72;s.render.fps=24
for f in range(1,73):
 t=(f-1)/71
 if mode=='wide':
  cam.location=(3.6-.25*t,-5.5+.65*t,2.3-.08*t);target=Vector((0,.45,.65));data.energy=55;sun_data.energy=.25;bs.inputs['Emission Strength'].default_value=1.5
 else:
  cam.location=(1.25-.06*t,-2.25,1.16);target=Vector((0,0,.38))
  fade=max(0,min(1,(t-.12)/.25));dawn=max(0,min(1,(t-.35)/.6));dawn=dawn*dawn*(3-2*dawn)
  data.energy=55*(1-fade);bs.inputs['Emission Strength'].default_value=1.5*(1-fade)
  for name in ['Key','Fill','BackLight']:bpy.data.objects[name].data.energy=({'Key':45,'Fill':15,'BackLight':25}[name])*(1-.65*fade)
  sun_data.energy=.05+2.1*dawn
  bg=s.world.node_tree.nodes['Background'];bg.inputs[0].default_value=(.055+.25*dawn,.085+.20*dawn,.11+.12*dawn,1);bg.inputs[0].keyframe_insert(data_path='default_value',frame=f)
  for name in ['Key','Fill','BackLight']:bpy.data.objects[name].data.keyframe_insert(data_path='energy',frame=f)
 cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();sun.rotation_euler=(math.radians(62-14*t),math.radians(-20),math.radians(-165))
 for obj in (cam,sun):
  for prop in ('location','rotation_euler'):obj.keyframe_insert(data_path=prop,frame=f)
 data.keyframe_insert(data_path='energy',frame=f);sun_data.keyframe_insert(data_path='energy',frame=f);bs.inputs['Emission Strength'].keyframe_insert(data_path='default_value',frame=f)
s.render.engine='BLENDER_EEVEE_NEXT';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.threads_mode='FIXED';s.render.threads=2
s.eevee.taa_render_samples=16;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'))
frames=[36] if '--still' in args else ([1,36,72] if '--controls' in args else list(range(1,73)))
report={'mode':mode,'seconds':3,'fps':24,'executor_admission':False,'sound':'intentionally silent light/camera test','scene_sha256':hashlib.sha256((out/'scene.blend').read_bytes()).hexdigest(),'frames':[]};start=time.monotonic()
for f in frames:
 s.frame_set(f);p=out/f'frame_{f:06d}.png';s.render.filepath=str(p);bpy.ops.render.render(write_still=True);report['frames'].append({'frame':f,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lamp_energy':data.energy,'sun_energy':sun_data.energy,'camera':list(cam.location)})
report['render_seconds']=time.monotonic()-start;(out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
