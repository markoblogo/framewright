"""Original revised grain and smooth irrigation props; no external assets."""
import bpy,math
from mathutils import Vector

def mat(name,col,rough=.5,alpha=1,metal=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=alpha
 if alpha<1:m.surface_render_method='BLENDED'
 return m

def grain(bake=False):
 m=mat('GrainHusk',(.23,.12,.035),.68);nodes=m.node_tree.nodes;links=m.node_tree.links;p=nodes['Principled BSDF']
 tex=nodes.new('ShaderNodeTexCoord');scale=nodes.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(16,1.5,8)
 noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3;noise.inputs['Detail'].default_value=2
 ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.10,.042,.009,1);ramp.color_ramp.elements[1].color=(.39,.24,.065,1)
 bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.0014
 links.new(tex.outputs['Generated'],scale.inputs[0]);links.new(scale.outputs[0],noise.inputs['Vector']);links.new(noise.outputs['Fac'],ramp.inputs[0]);links.new(ramp.outputs[0],p.inputs['Base Color']);links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs[0],p.inputs['Normal'])
 seeds=[]
 for name,side in [('SeedLeft',-1),('SeedRight',1)]:
  o=bpy.data.objects[name];verts=[];faces=[];nu=28;nv=24
  for i in range(nu+1):
   theta=math.pi*i/nu;w=math.sin(theta)*(.82+.18*math.cos(theta))
   for j in range(nv+1):
    phi=-math.pi/2+math.pi*j/nv;verts.append((side*.075*w*math.cos(phi),.145*math.cos(theta),.037*w*math.sin(phi)))
  for i in range(nu):
   for j in range(nv):
    a=i*(nv+1)+j;faces.append((a,a+1,a+nv+2,a+nv+1))
  mesh=bpy.data.meshes.new(name+'PointedGrain');mesh.from_pydata(verts,[],faces);mesh.update();o.data=mesh;mesh.materials.append(m)
  for f in mesh.polygons:f.use_smooth=True
  seeds.append(o)
 if bake:
  s=bpy.context.scene
  for f in range(1,181):
   s.frame_set(f)
   for o in seeds:o.location.z-=.032;o.keyframe_insert(data_path='location',frame=f)
   for i in range(3):
    o=bpy.data.objects.get('Runoff'+str(i));u=((f-1)/24-2.83-i*.035)/.42
    if o and 0<=u<=1:
     angle=u*math.pi*.68;o.location=(.022*(i-1)+.060*math.sin(angle),-.025-.06*math.sin(angle),.025+.037*math.cos(angle));o.keyframe_insert(data_path='location',frame=f)
   t=(f-1)/24;wet=max(0,min(1,(t-2.83)/.08))*(1-max(0,min(1,(t-3.5)/.25)))
   for key,value in [('Roughness',.68-.32*wet),('Coat Weight',.3*wet)]:p.inputs[key].default_value=value;p.inputs[key].keyframe_insert(data_path='default_value',frame=f)
 else:
  for o in seeds:o.location.z-=.032
 return seeds

def cylinder(name,loc,r,depth,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(m)
 for p in o.data.polygons:p.use_smooth=True
 return o

def tube(name,points,r,m):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=3;cu.resolution_u=16
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for p,co in zip(sp.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,cu);bpy.context.scene.collection.objects.link(o);cu.materials.append(m);return o

def irrigation():
 for name in ['Nozzle','NozzleLip','Feed','Supply']:
  if name in bpy.data.objects:bpy.data.objects[name].hide_render=True
 brass=bpy.data.materials['OldBrass'];teal=bpy.data.materials['DeepTealSteel'];glass=mat('ClearReserveGlass',(.7,.85,.86),.12,.09);blue=mat('LastWaterBlue',(.055,.28,.34),.12,.75)
 cx,cy=-.6,.65;verts=[];faces=[];profile=[(1.22,.10),(1.24,.15),(1.56,.15),(1.60,.13),(1.63,.10)]
 for z,r in profile:
  for j in range(48):a=j*math.tau/48;verts.append((cx+r*math.cos(a),cy+r*math.sin(a),z))
 for i in range(len(profile)-1):
  for j in range(48):a=i*48+j;b=i*48+(j+1)%48;faces.append((a,b,b+48,a+48))
 mesh=bpy.data.meshes.new('RoundedReserve');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('RoundedGlassReservoir',mesh);bpy.context.scene.collection.objects.link(o);mesh.materials.append(glass)
 for p in mesh.polygons:p.use_smooth=True
 cylinder('ReservoirCap',(cx,cy,1.64),.108,.035,brass);cylinder('ReservoirFoot',(cx,cy,1.225),.112,.022,brass)
 water=cylinder('WaterRemaining',(cx,cy,1.254),.14,.026,blue)
 for z in [1.27,1.51]:
  bpy.ops.mesh.primitive_torus_add(major_radius=.154,minor_radius=.006,major_segments=48,minor_segments=8,location=(cx,cy,z));bpy.context.object.name='ReservoirCollar';bpy.context.object.data.materials.append(brass)
 tube('ReservoirStand',[(-.82,.85,-.2),(-.82,.85,1.18),(-.78,.74,1.27),(-.754,.65,1.27)],.012,teal)
 cylinder('StandFoot',(-.82,.85,-.21),.075,.025,teal)
 tube('CurvedWaterFeed',[(cx,cy,1.22),(-.6,.65,1.13),(-.48,.5,1.10),(-.3,.3,1.10),(-.12,.12,1.08),(-.1,.025,.98)],.012,brass)
 cylinder('DripNozzle',(-.1,.025,1.005),.021,.05,brass);cylinder('NozzleOpening',(-.1,.025,.979),.010,.002,mat('DripOpening',(.009,.012,.012)))
 cylinder('ValveBody',(-.3,.3,1.1),.023,.05,brass);cylinder('ValveStem',(-.3,.3,1.145),.006,.055,brass)
 tube('TapHandle',[(-.34,.3,1.175),(-.3,.3,1.175),(-.26,.3,1.175)],.009,teal)
 return water
