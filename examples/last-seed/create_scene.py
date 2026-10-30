"""Original Last Seed pilot. Baked object transforms, no simulation or external assets."""
import bpy
import json
import math
from mathutils import Vector
from pathlib import Path
import random
import sys

out=Path(sys.argv[sys.argv.index('--')+1]);out.mkdir(parents=True,exist_ok=True)
if (out/'last-seed.blend').exists():raise ValueError('Use a new scene revision directory; never overwrite retained scenes')
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=180;scene.render.fps=24
random.seed(24)
world=bpy.data.worlds.new('Dusk');world.use_nodes=True;scene.world=world
world.node_tree.nodes['Background'].inputs[0].default_value=(.055,.085,.11,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.35

def mat(name,color,rough=.45,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
 p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 return m
soil=mat('DryEarth',(.075,.041,.019),.94)
p=soil.node_tree.nodes.get('Principled BSDF');n=soil.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=48;n.inputs['Detail'].default_value=3
b=soil.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.6;b.inputs['Distance'].default_value=.035
soil.node_tree.links.new(n.outputs['Fac'],b.inputs['Height']);soil.node_tree.links.new(b.outputs['Normal'],p.inputs['Normal'])
seedmat=mat('OchreSeed',(.3,.105,.025),.33)
wet=mat('WetEarth',(.032,.017,.008),.3)
steel=mat('DeepTealSteel',(.032,.095,.103),.32,.65)
brass=mat('OldBrass',(.32,.19,.055),.33,.72)
stone=mat('EarthGrain',(.13,.075,.036),.9)
green=mat('LivingGreen',(.055,.24,.008),.48)
p=green.node_tree.nodes.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.025
veinmat=mat('LeafVeins',(.27,.46,.048),.4)
water=mat('Water',(.34,.68,.8),.045)
p=water.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.68;p.inputs['IOR'].default_value=1.333

def finish(o,name,material):
 o.name=name;o.data.materials.append(material)
 if hasattr(o.data,'polygons'):
  for f in o.data.polygons:f.use_smooth=True
 return o

def ball(name,loc,scale,material,ico=False):
 if ico:bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=loc)
 else:bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=1,location=loc)
 o=finish(bpy.context.object,name,material);o.scale=scale;return o

def cyl(name,loc,radius,depth,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=radius,depth=depth,location=loc)
 return finish(bpy.context.object,name,material)

def cube(name,loc,scale,material):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=finish(bpy.context.object,name,material);o.scale=scale;return o

def torus(name,loc,major,minor,material):
 bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=12,location=loc,major_radius=major,minor_radius=minor)
 return finish(bpy.context.object,name,material)

cyl('Tray',(0,0,-.12),.66,.2,steel)
cyl('Soil',(0,0,-.037),.615,.07,soil)
torus('Rim',(0,0,-.018),.645,.018,brass)
cube('Bench',(0,.3,-.3),(4,2.5,.14),steel)
for i in range(160):
 r=random.uniform(.06,.60);a=random.random()*math.tau;x,y=r*math.cos(a),r*math.sin(a)
 if abs(x)<.16 and abs(y)<.18:continue
 size=random.uniform(.007,.022)
 o=ball('Grain%03d'%i,(x,y,.003),(size,size*.75,size*.45),stone,True);o.rotation_euler[2]=a
for i,x in enumerate([-1.4,-.7,.7,1.4]):cube('Frame%d'%i,(x,1.6,.9),(.045,.05,2.5),brass)
for z in [.2,1,1.8]:cube('Crossbar'+str(z),(0,1.6,z),(4,.05,.025),steel)
back=mat('GreenhouseGlass',(.04,.11,.13),.25,.15)
cube('RearGlass',(0,1.7,1),(5,.025,3),back)
# A visibly grounded nozzle over the growing tray; no floating prop.
cyl('Nozzle',(-.10,.025,1.18),.028,.4,brass)
torus('NozzleLip',(-.10,.025,.98),.028,.006,steel)
cube('Supply',(0,1.1,1.39),(2.5,.07,.07),steel)
cube('Feed',(-.10,.55,1.39),(.055,1.15,.06),brass)
# Seed halves form a closed continuous shell before germination.
seeds=[]
for side in [-1,1]:
 vertices=[];faces=[];nu=16;nv=20
 for i in range(nu+1):
  theta=math.pi*i/nu
  for j in range(nv+1):
   phi=-math.pi/2+math.pi*j/nv
   vertices.append((side*.087*math.sin(theta)*math.cos(phi),.14*math.sin(theta)*math.sin(phi),.071*math.cos(theta)))
 for i in range(nu):
  for j in range(nv):
   a=i*(nv+1)+j;faces.append((a,a+1,a+nv+2,a+nv+1))
 mesh=bpy.data.meshes.new('SeedShell');mesh.from_pydata(vertices,[],faces);mesh.update()
 o=bpy.data.objects.new('SeedLeft' if side<0 else 'SeedRight',mesh);scene.collection.objects.link(o);finish(o,o.name,seedmat);seeds.append((o,side))
# Baked impact patch, displaced soil and runoff: no physics/fluid solver.
bpy.data.objects['Soil'].hide_render=True
verts=[(0,0,.002)];faces=[];rings=32;segments=64
for ring in range(1,rings+1):
 r=.615*ring/rings
 for j in range(segments):
  a=j*math.tau/segments;verts.append((r*math.cos(a),r*math.sin(a),.002))
for j in range(segments):faces.append((0,1+j,1+(j+1)%segments))
for ring in range(1,rings):
 for j in range(segments):
  a=1+(ring-1)*segments+j;b=1+(ring-1)*segments+(j+1)%segments
  faces.append((a,a+segments,b+segments,b))
mesh=bpy.data.meshes.new('ImpactSoil');mesh.from_pydata(verts,[],faces);mesh.update()
impact=bpy.data.objects.new('ImpactSoil',mesh);scene.collection.objects.link(impact);finish(impact,'ImpactSoil',soil)
impact.shape_key_add(name='Basis');dent=impact.shape_key_add(name='Impact')
for v in dent.data:
 r=math.hypot(v.co.x,v.co.y);v.co.z+=-.028*math.exp(-(r/.095)**2)+.012*math.exp(-((r-.13)/.035)**2)
dust=[ball('Dust%02d'%i,(0,0,0),(.001,)*3,stone,True) for i in range(18)]
runoff=[ball('Runoff%d'%i,(0,0,0),(.001,)*3,water) for i in range(3)]
drop=ball('Drop',(-.10,.025,.95),(.001,.001,.001),water)
patch=cyl('WetPatch',(-.08,.02,-.0005),1,.0015,wet);patch.scale=(.001,.001,1)
ripple=torus('Ripple',(-.1,.025,.008),1,.013,water)
splashes=[ball('Splash%d'%i,(0,0,0),(.001,)*3,water) for i in range(7)]
cu=bpy.data.curves.new('ContinuousStem','CURVE');cu.dimensions='3D';cu.bevel_depth=.011;cu.bevel_resolution=3
sp=cu.splines.new('POLY');sp.points.add(60)
for i in range(61):
 u=i/60;sp.points[i].co=(.045*math.sin(u*math.pi),.024*math.sin(u*4),.54*u,1)
stalk=bpy.data.objects.new('Stalk',cu);scene.collection.objects.link(stalk);cu.materials.append(green)
stems=[stalk]

def leaf(name):
 verts=[];faces=[];n=18
 for i in range(n+1):
  u=i/n;w=.12*math.sin(math.pi*u)**.85
  for v in [-1,-.5,0,.5,1]:verts.append((.34*u,w*v,.045*math.sin(math.pi*u)-.027*v*v*math.sin(math.pi*u)))
 for i in range(n):
  for j in range(4):a=i*5+j;faces.append((a,a+5,a+6,a+1))
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
 o=bpy.data.objects.new(name,mesh);scene.collection.objects.link(o);finish(o,name,green)
 # vein follows leaf coordinates and is carried by its parent.
 cu=bpy.data.curves.new(name+'Vein','CURVE');cu.dimensions='3D';cu.bevel_depth=.002;cu.bevel_resolution=2
 sp=cu.splines.new('POLY');sp.points.add(n)
 for i in range(n+1):u=i/n;sp.points[i].co=(.34*u,0,.045*math.sin(math.pi*u)+.002,1)
 vein=bpy.data.objects.new(name+'Vein',cu);scene.collection.objects.link(vein);vein.parent=o;cu.materials.append(veinmat)
 return o
leaves=[leaf('LeafLeft'),leaf('LeafRight')]

def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def stempoint(u,g,t):
 return Vector((.045*math.sin(u*math.pi)*g, .024*math.sin(u*4)*g, .055+.54*g*u))
animated=[o for o,_ in seeds]+[drop,patch,ripple]+splashes+stems+leaves+dust+runoff
contact=[]
for f in range(1,181):
 t=(f-1)/24;fall=ease((t-.15)/.85);growth=ease((t-3.25)/3.6)
 for o,side in seeds:
  split=ease((t-3.3)/2.4)
  o.location=(side*.035*split,0,.075+.72*(1-fall)-.025*split-.018*ease((t-.97)/.13)*(1-ease((t-3.25)/.45)))
  o.rotation_euler=(.16*(1-fall),side*.28*split,.25*(1-fall))
 if t<2.15:
  d=ease((t-1.2)/.95);drop.location=(-.1,.025,.946-.015*d);drop.scale=(.044*d,.044*d,.062*d)
 elif t<2.83:
  u=(t-2.15)/.68;drop.location=(-.10*(1-u),.025-.045*u,.931-.795*u*u);drop.scale=(.044,.044,.062+.035*u)
 else:drop.scale=(.00001,)*3
 wetness=ease((t-3.16)/.65);patch.scale=(.19*wetness+.001,.15*wetness+.001,1)
 r=ease((t-3.16)/.42);visible=1 if 3.16<=t<3.58 else .00001
 ripple.scale=((.02+.17*r)*visible,(.02+.17*r)*visible,(1-r)*visible)
 for i,o in enumerate(splashes):
  dt=t-3.16;a=i*math.tau/7
  if 0<=dt<.38:
   o.location=(-.1+.35*dt*math.cos(a),.025+.35*dt*math.sin(a),.012+.85*dt-2.3*dt*dt)
   o.scale=(.008*(1-dt/.38),)*3
  else:o.scale=(.00001,)*3
 dent.value=ease((t-.97)/.13)*(1-ease((t-3.25)/.45));dent.keyframe_insert(data_path='value',frame=f)
 for i,o in enumerate(dust):
  dt=t-.97;a=i*2.399963
  if 0<=dt<.48:
   o.location=((.10+.23*dt)*math.cos(a),(.10+.23*dt)*math.sin(a),.01+(.35+.08*(i%3))*dt-.8*dt*dt)
   size=(.005+.001*(i%4))*math.sin(math.pi*dt/.48);o.scale=(size,)*3
  else:o.scale=(.00001,)*3
 for i,o in enumerate(runoff):
  u=(t-2.83-i*.035)/.42
  if 0<=u<=1:
   angle=u*math.pi*.68;o.location=(.025*(i-1)+.079*math.sin(angle),-.025-.06*math.sin(angle),.057+.076*math.cos(angle))
   o.scale=(.014*(1-.45*u),.010,.023*(1-.4*u))
  else:o.scale=(.00001,)*3
 shader=seedmat.node_tree.nodes.get('Principled BSDF');wetfilm=ease((t-2.83)/.08)*(1-ease((t-3.5)/.25))
 for key,value in [('Roughness',.33-.2*wetfilm),('Coat Weight',.65*wetfilm)]:
  shader.inputs[key].default_value=value;shader.inputs[key].keyframe_insert(data_path='default_value',frame=f)
 stalk.location=(0,0,.055);stalk.scale=(max(.0001,growth),)*3
 tip=stempoint(1,growth,t)
 for i,o in enumerate(leaves):
  open_=ease((t-4.05)/2.9);o.location=tip
  o.scale=(max(.0001,open_),max(.0001,open_),max(.0001,open_))
  o.rotation_euler=(.05*math.sin(t*2+i),-.95*(1-open_)-.13*open_,math.pi*i+.13*math.sin(t*1.1+i)*open_)
 for o in animated:
  for prop in ('location','rotation_euler','scale'):o.keyframe_insert(data_path=prop,frame=f)
 if f in [25,69,90,130,180]:contact.append({'frame':f,'seed_center_z':seeds[0][0].location.z,'growth':growth,'tip':list(tip)})
actions={}
for o in animated:o.animation_data.action.name=o.name+'Action';actions[o.name]=o.animation_data.action.name
camdata=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',camdata);scene.collection.objects.link(cam)
cam.location=(1.10,-1.85,1.05);cam.rotation_euler=(Vector((0,0,.35))-cam.location).to_track_quat('-Z','Y').to_euler();camdata.lens=55;scene.camera=cam
camdata.dof.use_dof=True;camdata.dof.focus_distance=(cam.location-Vector((0,0,.25))).length;camdata.dof.aperture_fstop=5.6
lights={}
for name,loc,power,color,size in [('Key',(-1.5,-2,2.5),95,(1,.78,.49),2.2),('Fill',(1.5,-.3,1.8),40,(.42,.74,1),1.6),('BackLight',(-.5,1.1,1.8),90,(.8,1,.58),1.2)]:
 data=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.2))-o.location).to_track_quat('-Z','Y').to_euler();data.energy=power;data.color=color;data.size=size
 lights[name]={'location':list(loc),'energy':power,'color':list(color),'size':size}
scene.view_settings.view_transform='AgX';scene.cycles.max_bounces=5;scene.cycles.transmission_bounces=3
scene.render.engine='CYCLES'
scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(out/'last-seed.blend'))
spec={'id':'last-seed','version':'v1','scene':'input:scene','resources':[],
 'canvas':{'width':960,'height':540,'fps':24},'frames':{'start':0,'end':180},
 'engine':{'name':'CYCLES','device':'CPU','samples':24,'seed':24},
 'settings':{'camera':{'object':'Camera','location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'lens':camdata.lens},'actions':actions,'lights':lights},
 'audio':{'subject':'input:sound','gain_db':0,'offset_seconds':0},'bindings':[]}
(out/'shot-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
(out/'motion-checkpoints.json').write_text(json.dumps(contact,indent=2)+'\n')
print('Saved original scene and explicit actions:',len(actions))
