"""Original authored drought/weather/roof rig. No physics or provider claims."""
import bpy,math,random
from mathutils import Vector,Quaternion

def mat(name,col,rough=.6,metal=0,alpha=1,emission=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=alpha
 if alpha<1:m.surface_render_method='BLENDED'
 if emission:p.inputs['Emission Color'].default_value=(*col,1);p.inputs['Emission Strength'].default_value=emission
 return m

def cracked(name,wet=False):
 m=mat(name,(.24,.13,.055) if not wet else (.075,.038,.012),.94 if not wet else .65);n=m.node_tree.nodes;l=m.node_tree.links;p=n['Principled BSDF']
 tex=n.new('ShaderNodeNewGeometry');v=n.new('ShaderNodeTexVoronoi');v.feature='DISTANCE_TO_EDGE';v.voronoi_dimensions='2D';v.inputs['Scale'].default_value=7.5;l.new(tex.outputs['Position'],v.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.012;ramp.color_ramp.elements[0].color=(.018,.006,.002,1)
 ramp.color_ramp.elements[1].position=.055;ramp.color_ramp.elements[1].color=(.075,.038,.012,1) if wet else (.25,.145,.065,1)
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.8;bump.inputs['Distance'].default_value=.009
 l.new(v.outputs['Distance'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color']);l.new(v.outputs['Distance'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
 return m

def soil():
 dry=cracked('DryCrackedEarth');wet=cracked('DampCrackedEarth',True)
 for o in bpy.context.scene.objects:
  if o.type=='MESH':
   for slot in o.material_slots:
    if slot.material and slot.material.name.startswith('DryEarth'):slot.material=dry
  if o.name=='WetPatch':o.data.materials.clear();o.data.materials.append(wet)
 # Slightly more varied husk colour; geometry is the retained pointed grain.
 for m in bpy.data.materials:
  if m.name.startswith('GrainHusk') and m.use_nodes:
   for node in m.node_tree.nodes:
    if node.type=='VALTORGB':node.color_ramp.elements[0].color=(.045,.016,.003,1);node.color_ramp.elements[1].color=(.25,.12,.026,1)

def cube(name,loc,size,material,parent=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=size;o.data.materials.append(material)
 if parent:o.parent=parent
 return o

def line(name,points,r,material,parent=None):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2
 sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for p,co in zip(sp.points,points):p.co=(*co,1)
 o=bpy.data.objects.new(name,cu);bpy.context.scene.collection.objects.link(o);cu.materials.append(material)
 if parent:o.parent=parent
 return o

def ball(name,loc,scale,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o

def empty(name,loc):
 o=bpy.data.objects.new(name,None);bpy.context.scene.collection.objects.link(o);o.location=loc;return o

def panel(name,x0,x1,y0,y1,material,parent=None,origin=None):
 points=[(x0,y0,3-x0/3),(x1,y0,3-x1/3),(x1,y1,3-x1/3),(x0,y1,3-x0/3)]
 if origin:points=[tuple(Vector(p)-Vector(origin)) for p in points]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(points,[],[(0,1,2,3)]);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(o);mesh.materials.append(material)
 if parent:o.parent=parent
 return o,points

class Rig:
 def __init__(self):
  self.s=bpy.context.scene;soil();self.brass=bpy.data.materials['OldBrass'];self.steel=bpy.data.materials['DeepTealSteel']
  glass=bpy.data.materials['CloudedGreenhouseGlass'];self.axis=Vector((1,0,-1/3)).normalized();self.hinge=empty('RoofVentHinge',(0,-.94,3))
  for o in list(self.s.objects):
   if o.name.startswith('RoofGlass') and o.type=='MESH':
    c=sum((o.matrix_world@v.co for v in o.data.vertices),Vector())/len(o.data.vertices)
    if c.x>0 and -2<c.y<0:o.hide_render=True
  panel('RoofFixedOuter',1.1,2.96,-1.96,-.04,glass);panel('RoofFixedRear',.04,1.1,-1.96,-.98,glass)
  vent,pts=panel('OpeningRoofVent',.04,1.05,-.94,-.04,glass,self.hinge,self.hinge.location)
  line('OpeningFrame',pts+[pts[0]],.014,self.brass,self.hinge)
  self.free=Vector((.15,.90,-.05));self.water=mat('RainWater',(.45,.65,.72),.12,alpha=.65)
  self.rng=random.Random(30);self.rain=[];self.beads=[]
  streak=mat('RainStreak',(.25,.40,.46),.4,emission=.3)
  for i in range(42):
   x=self.rng.uniform(-2.7,2.8);y=self.rng.choice([4.1,4.4,-2.25]);z=self.rng.uniform(.5,4.2)
   o=line('OutsideRain',[(0,0,0),(.006,0,.10)],.0015,streak);self.rain.append((o,x,y,z))
  for i in range(9):
   x=.10+.1*(i%7);y=-.85+.08*(i%5);z=3-x/3+.014
   o=ball('RoofBead',(0,0,0),(.012,.019,.008),self.water);o.parent=self.hinge;o.location=Vector((x,y,z))-self.hinge.location;self.beads.append((o,o.location.copy()))
  self.drops=[ball('ReleasedRainDrop',(0,0,0),(.001,)*3,self.water) for _ in range(3)]
  self.gear1=self.gear('DriveGear',(1.15,-.94,2.60),.12,16);self.gear2=self.gear('MotorGear',(1.15,-.71,2.60),.09,12)
  line('RoofDriveLink',[(1.15,-.94,2.60),(1.10,-.94,2.64),(1.02,-.94,2.66)],.019,self.brass)
  housing=mat('MotorHousing',(.06,.10,.11),.6,.4);cube('MotorBody',(.96,-.71,2.60),(.25,.18,.18),housing)
  cube('BatteryCase',(1.35,-.80,2.22),(.31,.10,.16),housing)
  self.led=[]
  for i in range(4):
   m=mat('BatteryLED',(.16,.45,.09),.4,emission=1);o=cube('BatteryBar',(1.235+.071*i,-.856,2.22),(.047,.008,.075),m);self.led.append(m.node_tree.nodes['Principled BSDF'])
  cube('BatteryTip',(1.53,-.80,2.22),(.025,.07,.08),self.brass)
  # Opening mechanism also parks the dead lamp clear of the rain path.
  self.lamp=[]
  for name in ['LampHousing','LampDiffuser','WorkingLamp']:
   o=bpy.data.objects.get(name)
   if o:self.lamp.append((o,o.location.copy()))
  self.cassette=[(o,o.location.copy()) for o in self.s.objects if o.name.startswith(('SeedCassette','SocketBottom','SocketCutter','CassetteRail','ReleaseGate','CassetteBracket'))]
  if 'LampCable' in bpy.data.objects:bpy.data.objects['LampCable'].hide_render=True
  line('LampSlideRail',[(-1.8,0,1.82),(.35,0,1.82)],.015,self.steel)
  self.plant=bpy.data.objects['Stalk'];self.scale=self.plant.scale.copy();self.leaves=[]
  for name in ['LeafLeft','LeafRight']:
   o=bpy.data.objects[name];self.leaves.append((o,o.location.copy(),o.rotation_euler.copy()))
  self.young=[]
  for i,(src,loc,rot) in enumerate(self.leaves):
   o=src.copy();o.data=src.data.copy();self.s.collection.objects.link(o);o.name='NewTrueLeaf';self.young.append((o,loc.copy(),rot.copy(),i))
 def gear(self,name,loc,r,n):
  root=empty(name,loc)
  bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=.035);o=bpy.context.object;o.name=name+'Hub';o.rotation_euler[1]=math.pi/2;o.parent=root;o.data.materials.append(self.brass)
  for i in range(n):
   a=i*math.tau/n;o=cube(name+'Tooth',(0,r*math.cos(a),r*math.sin(a)),(.045,.025,.025),self.brass,root);o.rotation_euler[0]=a
  return root
 @staticmethod
 def opening(t):
  if t<1.6:return .11*max(0,t)/1.6
  if t<3.1:return .11+.006*math.sin(t*32)
  if t<5.2:
   u=(t-3.1)/2.1;return .11+.53*u*u*(3-2*u)
  return .64
 def pose(self,stage,t,global_t):
  after=stage in ('water','recover','up');angle=.64 if after else (self.opening(t) if stage=='roof' else 0)
  self.hinge.rotation_mode='QUATERNION';self.hinge.rotation_quaternion=Quaternion(self.axis,angle)
  self.gear1.rotation_euler[0]=4*angle;self.gear2.rotation_euler[0]=math.pi/12-4*angle*4/3
  for i,p in enumerate(self.led):
   on=(i==0 and (stage!='roof' or t<5.2) and not after);p.inputs['Emission Strength'].default_value=1 if on else 0;p.inputs['Base Color'].default_value=(.35,.12,.015,1) if on else (.006,.008,.006,1)
  for o,loc in self.lamp:o.location=loc+Vector((-1.5*angle/.64,0,0))
  for o,loc in self.cassette:o.location=loc+Vector((-.85*angle/.64,0,0))
  for o,x,y,z in self.rain:o.location=(x+.025*global_t,y,.3+(z-global_t*2.4)%4)
  for o,base in self.beads:o.location=base+Vector((0,.015*math.sin(global_t*.7),0))
  for i,o in enumerate(self.drops):
   dt=t-(.15+i*1.25) if stage=='water' else -1
   if 0<=dt<.72:
    start=self.hinge.location+self.hinge.rotation_quaternion@self.free;u=dt/.72;hit=Vector((.13,-.035,.64));o.location=start+(hit-start)*u*u;o.scale=(.018,.018,.035)
   elif .72<=dt<1.15:
    u=(dt-.72)/.43;o.location=(.13+.13*u,-.035,.64-.62*u*u);o.scale=(.014,.014,.017)
   else:o.scale=(.00001,)*3
  grow=(t/7 if stage=='recover' else (1 if stage=='up' else 0));grow=max(0,min(1,grow))
  self.plant.scale=(self.scale.x,self.scale.y,self.scale.z*(1+.18*grow))
  for i,(o,loc,rot) in enumerate(self.leaves):
   o.location=loc+Vector((0,0,.54*.18*grow));o.rotation_euler=rot;o.rotation_euler[1]-=.28*grow;o.rotation_euler[0]+=.015*math.sin(t*2+i)
   if stage=='water':o.rotation_euler[1]+=.10*sum(math.exp(-max(0,t-(.87+j*1.25))*8)*math.sin(max(0,t-(.87+j*1.25))*22) if t>(.87+j*1.25) else 0 for j in range(3))
  for o,loc,rot,i in self.young:
   o.location=loc+Vector((0,0,.54*.18*grow));o.rotation_euler=rot;o.rotation_euler[2]+=.85;o.rotation_euler[1]-=.4;o.scale=(max(.00001,.38*grow),)*3
  wet=bpy.data.objects.get('WetPatch')
  if wet:
   wet.location.z=.003;wet.hide_render=stage in ('ground','rain');wet.scale=(.19+.20*(min(1,t/5) if stage=='water' else int(stage in ('recover','up'))),.15+.17*(min(1,t/5) if stage=='water' else int(stage in ('recover','up'))),1)
  young=stage in ('ground','rain')
  for o in self.s.objects:
   if o.name.startswith(('SeedLeft','SeedRight','Stalk','Leaf','NewTrueLeaf')):o.hide_render=young
   if o.name.startswith('CassetteSeed'):o.hide_render=not young
  gate=bpy.data.objects.get('ReleaseGate')
  if gate:gate.location.y=0 if young else -.19
  for o in self.s.objects:
   if o.name.startswith('WaterRemaining'):o.hide_render=not young
