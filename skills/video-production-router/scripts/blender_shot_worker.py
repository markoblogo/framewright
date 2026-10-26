"""Trusted Blender-side worker. Invoked only by shots.py with disabled auto-execution."""
import json
import math
from pathlib import Path
import sys
import bpy


def main():
    job_path=Path(sys.argv[sys.argv.index('--')+1]);job=json.loads(job_path.read_text())
    spec=job['spec'];out=Path(job['output']);scene=bpy.context.scene
    if Path(bpy.data.filepath).resolve()!=Path(job['scene']).resolve():raise ValueError('Wrong saved scene loaded')
    allowed={str(Path(p).resolve()) for p in job['resources']}
    # No hidden relative image/audio/font/library dependency may silently change a shot.
    for collection in [bpy.data.images,bpy.data.sounds,bpy.data.fonts,bpy.data.libraries,bpy.data.movieclips]:
        for item in collection:
            path=getattr(item,'filepath','')
            if not path or path=='<builtin>' or getattr(item,'packed_file',None) or getattr(item,'packed_files',None):continue
            resolved=str(Path(bpy.path.abspath(path)).resolve())
            if resolved not in allowed:raise ValueError('External scene resource not retained: '+item.name)
    for obj in scene.objects:
        if obj.particle_systems or obj.rigid_body:
            raise ValueError('Particle/rigid-body simulation needs a separate baked-state adapter')
        if any(m.type in {'CLOTH','SOFT_BODY','FLUID','DYNAMIC_PAINT','NODES'} for m in obj.modifiers):
            raise ValueError('Simulation/geometry-node state not qualified by this adapter')
    for binding in spec['bindings']:
        if binding['object'] is not None and binding['object'] not in scene.objects:raise ValueError('Passport-bound object missing')
    scene.render.engine='CYCLES';scene.cycles.device='CPU'
    scene.cycles.samples=spec['engine']['samples'];scene.cycles.seed=spec['engine']['seed']
    scene.cycles.use_animated_seed=False;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=spec['canvas']['width'];scene.render.resolution_y=spec['canvas']['height'];scene.render.resolution_percentage=100
    scene.render.fps=spec['canvas']['fps'];scene.render.fps_base=1.0
    scene.render.use_sequencer=False;scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8'
    scene.render.film_transparent=False
    controls=spec['settings'];cam=bpy.data.objects.get(controls['camera']['object'])
    if cam is None or cam.type!='CAMERA':raise ValueError('Explicit camera missing')
    scene.camera=cam;cam.animation_data_clear()
    for name,action_name in controls['actions'].items():
        obj=bpy.data.objects.get(name);action=bpy.data.actions.get(action_name)
        if obj is None or action is None:raise ValueError('Named action/object missing')
        obj.animation_data_create().action=action
        if hasattr(action,'slots') and action.slots and obj.animation_data.action_slot is None:
            obj.animation_data.action_slot=action.slots[0]
    states=[]
    for frame in range(job['start'],job['end']):
        scene.frame_set(frame+1)
        c=controls['camera'];cam.location=c['location'];cam.rotation_euler=c['rotation_euler'];cam.data.lens=c['lens']
        for name,value in controls['lights'].items():
            light=bpy.data.objects.get(name)
            if light is None or light.type!='LIGHT' or light.data.type!='AREA':raise ValueError('Explicit area light missing')
            light.location=value['location'];light.data.energy=value['energy'];light.data.color=value['color'];light.data.size=value['size']
        bpy.context.view_layer.update()
        states.append({'frame':frame,'camera':{'object':cam.name,'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'lens':cam.data.lens},
            'actions':{name:{'action':bpy.data.objects[name].animation_data.action.name,
                              'world_location':list(bpy.data.objects[name].matrix_world.translation)} for name in controls['actions']},
            'lights':{name:{'energy':bpy.data.objects[name].data.energy,'color':list(bpy.data.objects[name].data.color),
                             'location':list(bpy.data.objects[name].location),'size':bpy.data.objects[name].data.size} for name in controls['lights']}})
        scene.render.filepath=str(out/f'frame_{frame+1:06d}.png')
        bpy.ops.render.render(write_still=True)
    report={'blender_version':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode(),
            'public_frames':'zero-based end-exclusive; Blender frame=public frame+1','states':states,
            'color_management':{'view_transform':scene.view_settings.view_transform,'look':scene.view_settings.look,
                                'exposure':scene.view_settings.exposure,'gamma':scene.view_settings.gamma},
            'scene_saved_by_worker':False,'audio_owner':'shots.py explicit pinned-source mix'}
    (out/'state.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
