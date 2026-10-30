"""Explicit manual Eevee pilot fallback; not an admitted Framewright worker."""
import bpy
import hashlib
import json
from pathlib import Path
import sys
import time

args=sys.argv[sys.argv.index('--')+1:];out=Path(args[0]);frames=[int(x) for x in args[1].split(',')]
if out.exists():raise ValueError('Use new render output directory')
if not frames or len(frames)>180 or min(frames)<1 or max(frames)>180:raise ValueError('Only explicit pilot frames1–180')
out.mkdir(parents=True)
scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE_NEXT'
scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.render.fps=24;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.render.image_settings.color_depth='8';scene.render.film_transparent=False
scene.render.threads_mode='FIXED';scene.render.threads=2
if hasattr(scene,'eevee') and hasattr(scene.eevee,'taa_render_samples'):scene.eevee.taa_render_samples=32
report={'engine':'BLENDER_EEVEE_NEXT','executor_admission':False,'reason':'Measured Cycles CPU frame cost and noisy preview; owner-authorised local pilot fallback',
 'blender':bpy.app.version_string,'source_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'frames':[]}
started=time.monotonic()
for f in frames:
 scene.frame_set(f);scene.render.filepath=str(out/f'frame_{f:06d}.png')
 start=time.monotonic();bpy.ops.render.render(write_still=True)
 path=Path(scene.render.filepath)
 report['frames'].append({'frame':f,'seconds':time.monotonic()-start,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
   'camera':list(scene.camera.location),'seed':list(bpy.data.objects['SeedLeft'].location),'tip':list(bpy.data.objects['LeafLeft'].location)})
report['elapsed_seconds']=time.monotonic()-started
(out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
