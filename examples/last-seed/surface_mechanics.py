"""Original seed shell shader and visible mounted roof linkage; no physics claims."""
import bpy,math,bmesh
from mathutils import Vector
from recovery_design import mat,cube,line,ball

def shell_texture():
 for m in bpy.data.materials:
  if not (m.name.startswith('GrainHusk') and m.use_nodes):continue
  n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
  tex=n.new('ShaderNodeTexCoord');stretch=n.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY';stretch.inputs[1].default_value=(5,1,3)
  noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=6;noise.inputs['Detail'].default_value=4;noise.inputs['Roughness'].default_value=.8
  wave=n.new('ShaderNodeTexWave');wave.bands_direction='X';wave.inputs['Scale'].default_value=7;wave.inputs['Distortion'].default_value=8;wave.inputs['Detail Scale'].default_value=2
  pits=n.new('ShaderNodeTexVoronoi');pits.inputs['Scale'].default_value=28
  pit_ramp=n.new('ShaderNodeValToRGB');pit_ramp.color_ramp.elements[0].position=.13;pit_ramp.color_ramp.elements[0].color=(.02,.02,.02,1);pit_ramp.color_ramp.elements[1].position=.27;pit_ramp.color_ramp.elements[1].color=(1,1,1,1)
  mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.42
  multiply=n.new('ShaderNodeMixRGB');multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=.72
  color=n.new('ShaderNodeValToRGB');color.color_ramp.elements[0].position=.11;color.color_ramp.elements[0].color=(.045,.015,.004,1);color.color_ramp.elements[1].position=.76;color.color_ramp.elements[1].color=(.48,.245,.082,1)
  middle=color.color_ramp.elements.new(.44);middle.color=(.24,.105,.026,1)
  bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.78;bump.inputs['Distance'].default_value=.008
  l.new(tex.outputs['Generated'],stretch.inputs[0]);l.new(stretch.outputs[0],noise.inputs['Vector']);l.new(tex.outputs['Generated'],wave.inputs['Vector']);l.new(tex.outputs['Generated'],pits.inputs['Vector']);l.new(pits.outputs['Distance'],pit_ramp.inputs[0]);l.new(noise.outputs['Fac'],mix.inputs[1]);l.new(wave.outputs['Color'],mix.inputs[2]);l.new(mix.outputs[0],multiply.inputs[1]);l.new(pit_ramp.outputs[0],multiply.inputs[2]);l.new(multiply.outputs[0],color.inputs[0]);l.new(color.outputs[0],p.inputs['Base Color']);l.new(multiply.outputs[0],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
  p.inputs['Specular IOR Level'].default_value=.24

def cylinder_between(name,a,b,r,material,parent=None):
 a,b=Vector(a),Vector(b);bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=(b-a).length,location=(a+b)/2);o=bpy.context.object;o.name=name;o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();o.data.materials.append(material)
 for f in o.data.polygons:f.use_smooth=True
 if parent:o.parent=parent
 return o

def set_rod(o,a,b):
 a,b=Vector(a),Vector(b);o.location=(a+b)/2;o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();o.scale.z=(b-a).length

def gear_mesh(name,root,r,teeth,material):
 # Extruded tooth outline with a central bore; spokes make rotation visible.
 vertices=[];faces=[];N=teeth*4
 for x in [-.022,.022]:
  for ring in [0,1]:
   for j in range(N):
    a=j*math.tau/N;rr=(r*(1.10 if j%4 in (1,2) else .92)) if ring==0 else r*.48;vertices.append((x,rr*math.cos(a),rr*math.sin(a)))
 for j in range(N):
  k=(j+1)%N
  faces.extend([(j,k,N+k,N+j),(2*N+j,3*N+j,3*N+k,2*N+k),(j,2*N+j,2*N+k,k),(N+j,N+k,3*N+k,3*N+j)])
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update();bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();o=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(o);o.parent=root;mesh.materials.append(material)
 bevel=o.modifiers.new('Machined edges','BEVEL');bevel.width=.002;bevel.segments=2
 for i in range(4):
  a=i*math.pi/2;sp=cube(name+'Spoke',(0,.27*r*math.cos(a),.27*r*math.sin(a)),(.04,r*.50,.018),material,root);sp.rotation_euler.x=a
 cylinder_between(name+'Axle',(-.12,0,0),(.07,0,0),.024,material,root)
 return o

def mechanism():
 s=bpy.context.scene;gear=mat('BrushedGearBronze',(.47,.28,.10),.38,.65);steel=mat('MountSteel',(.13,.22,.24),.48,.6);bright=mat('LinkPolishedSteel',(.48,.56,.58),.30,.75)
 for material in [gear,steel]:
  n=material.node_tree.nodes;l=material.node_tree.links;p=n['Principled BSDF'];noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=95;bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.001;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
 for o in list(s.objects):
  if o.name.startswith(('DriveGearHub','DriveGearTooth','MotorGearHub','MotorGearTooth','RoofDriveLink')):
   o.animation_data_clear();o.hide_render=True
 gear_mesh('MountedDriveGear',bpy.data.objects['DriveGear'],.12,16,gear);gear_mesh('MountedMotorGear',bpy.data.objects['MotorGear'],.09,12,gear)
 cube('DriveBackingPlate',(1.075,-.825,2.60),(.035,.47,.37),steel)
 cylinder_between('FixedRoofSupport',(1.075,-1.96,2.66),(1.075,-.04,2.66),.025,steel)
 for y in [-1.00,-.66]:
  cylinder_between('MountHanger',(1.075,y,2.66),(1.075,y,2.45),.019,steel)
  for z in [2.46,2.73]:cylinder_between('MountBolt',(1.08,y,z),(1.125,y,z),.014,bright)
 # Visible geared crank drives a telescopic pushrod to a pin on the vent frame.
 crank=cube('CrankLever',(.058,.035,0),(.018,.095,.023),bright,bpy.data.objects['DriveGear'])
 link=cylinder_between('ActuatorSleeve',(0,0,0),(0,0,1),.024,steel);rod=cylinder_between('ActuatorPiston',(0,0,0),(0,0,1),.012,bright)
 low=ball('ActuatorLowerPin',(0,0,0),(.026,)*3,gear);high=ball('VentAttachmentPin',(0,0,0),(.025,)*3,gear)
 data=bpy.data.lights.new('MechanismSoftbox','AREA');light=bpy.data.objects.new('MechanismSoftbox',data);s.collection.objects.link(light);light.location=(1.7,-1.65,2.15);light.rotation_euler=(Vector((1.1,-.8,2.6))-light.location).to_track_quat('-Z','Y').to_euler();data.energy=40;data.shape='DISK';data.size=1.4;data.color=(.78,.88,1)
 hinge=bpy.data.objects['RoofVentHinge'];drive=bpy.data.objects['DriveGear']
 for f in range(s.frame_start,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update();a=drive.matrix_world@Vector((.065,.073,0));b=hinge.matrix_world@Vector((1.02,.86,-.34));mid=a+(b-a)*.48
  set_rod(link,a,mid);set_rod(rod,a+(b-a)*.32,b);low.location=a;high.location=b
  for o in [link,rod,low,high]:
   for key in ['location','rotation_euler','scale']:o.keyframe_insert(data_path=key,frame=f)
 return {'mount':'fixed roof support/backing plate/bolts/axles','link':'geared crank and telescoping pushrod pinned to vent','simulation':False}

def rain_spread():
 s=bpy.context.scene;drops=sorted([o for o in s.objects if o.name.startswith('ReleasedRainDrop')],key=lambda o:o.name);hinge=bpy.data.objects['RoofVentHinge'];targets=[Vector((.15,-.04,.64)),Vector((-.14,.015,.64)),Vector((.30,.07,.02))];ground=[Vector((.28,-.08,.02)),Vector((-.22,.11,.02)),Vector((.30,.07,.02))];times=[.15,1.35,2.72]
 water=bpy.data.materials['RainWater'];rings=[]
 for j in range(3):
  bpy.ops.mesh.primitive_torus_add(major_segments=24,minor_segments=6,major_radius=1,minor_radius=.06,location=ground[j]);o=bpy.context.object;o.name='RainContactRipple';o.data.materials.append(water);rings.append(o)
 for f in range(s.frame_start,s.frame_end+1):
  s.frame_set(f);t=(f-1)/12;bpy.context.view_layer.update()
  for j,o in enumerate(drops):
   dt=t-times[j];hit=targets[j];start=hinge.matrix_world@Vector((.12+.22*j,.90,-.05));o.animation_data_clear() if f==1 else None
   if 0<=dt<.70:
    u=dt/.70;o.location=start+(hit-start)*u*u;o.scale=(.014+.002*j,.014+.002*j,.027+.004*j)
   elif j<2 and .70<=dt<1.12:
    u=(dt-.70)/.42;o.location=hit+(ground[j]-hit)*Vector((u,u,u*u));o.scale=(.011,.012,.016)
   else:o.scale=(.00001,)*3
   for key in ['location','scale']:o.keyframe_insert(data_path=key,frame=f)
   impact=times[j]+(.70 if j==2 else 1.12);u=(t-impact)/.25;rings[j].location=ground[j]+Vector((0,0,.006));rings[j].scale=((.012+.045*u),(.012+.045*u),.006) if 0<=u<1 else (.00001,)*3
   rings[j].keyframe_insert(data_path='scale',frame=f)
 return [list(x) for x in targets]
