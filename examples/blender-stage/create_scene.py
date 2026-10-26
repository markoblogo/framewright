"""Original self-contained Blender fixture; no external media, add-ons or simulation."""
import json
from pathlib import Path
import sys
import bpy
from mathutils import Vector

dest=Path(sys.argv[sys.argv.index('--')+1]);dest.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene;scene.render.fps=12;scene.frame_start=1;scene.frame_end=36
world=bpy.data.worlds.new('StudioWorld');world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.035,0.05,0.08,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=0.3;scene.world=world
def material(name,color,metal=0,roughness=.45):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=roughness;return m
floor=material('Slate',(0.045,0.065,0.1),.15,.55)
amber=material('Amber',(0.8,0.23,0.025),.6,.28)
steel=material('Steel',(0.1,0.16,0.2),.5,.3)
bpy.ops.mesh.primitive_plane_add(size=200);bpy.context.object.name='Floor';bpy.context.object.data.materials.append(floor)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=.45,location=(-1.3,0,.65))
actor=bpy.context.object;actor.name='Actor';actor.data.materials.append(amber)
for polygon in actor.data.polygons:polygon.use_smooth=True
for frame,x in [(1,-1.3),(36,1.3)]:
    actor.location=(x,0,.65);actor.rotation_euler=(0,x*.5,0)
    actor.keyframe_insert(data_path='location',frame=frame);actor.keyframe_insert(data_path='rotation_euler',frame=frame)
actor.animation_data.action.name='Glide'
for x in [-1.8,1.8]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.09,depth=1.9,location=(x,.55,.95))
    bpy.context.object.data.materials.append(steel)
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,.55,1.95));o=bpy.context.object;o.scale=(3.8,.18,.18);o.data.materials.append(steel)
bpy.ops.object.text_add(location=(-1.35,.8,.03));label=bpy.context.object;label.name='Label';label.data.body='FRAMEWRIGHT';label.data.size=.25;label.data.extrude=.002;label.data.materials.append(steel)
cam_data=bpy.data.cameras.new('Camera');camera=bpy.data.objects.new('Camera',cam_data);scene.collection.objects.link(camera)
camera.location=(3.8,-6,3.2);camera.rotation_euler=(Vector((0,.1,.8))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=48;scene.camera=camera
lights={}
for name,energy,color,location,size in [('Key',700,(1,.72,.45),(-2,-3,4),4),('Fill',180,(.42,.65,1),(3,1,3),3)]:
    data=bpy.data.lights.new(name,'AREA');obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj)
    obj.location=location;obj.rotation_euler=(Vector((0,0,.5))-obj.location).to_track_quat('-Z','Y').to_euler()
    data.energy=energy;data.color=color;data.size=size
    lights[name]={'energy':energy,'color':list(color),'location':list(location),'size':size}
scene.view_settings.view_transform='AgX';scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str((dest/'stage.blend').resolve()))
spec={'id':'stage','version':'v1','scene':'input:scene','resources':[],
      'canvas':{'width':480,'height':270,'fps':12},'frames':{'start':0,'end':36},
      'engine':{'name':'CYCLES','device':'CPU','samples':8,'seed':7},
      'settings':{'camera':{'object':'Camera','location':list(camera.location),'rotation_euler':list(camera.rotation_euler),'lens':camera.data.lens},
                  'actions':{'Actor':'Glide'},'lights':lights},
      'audio':{'subject':'input:sound','gain_db':-6,'offset_seconds':0},'bindings':[]}
(dest/'shot-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
print('Original test scene saved:',dest/'stage.blend')
