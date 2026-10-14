from pathlib import Path
import runpy
import shutil
import subprocess

here = Path(__file__).resolve().parent
assert Path.cwd().resolve() == here, 'Run this command from the example directory'
(here/'public').mkdir(exist_ok=True)
(here/'outputs').mkdir(exist_ok=True)
shutil.copy2(here.parents[1]/'assets/framewright-cover.png', here/'public/framewright-cover.png')
runpy.run_path(str(here/'generate-score.py'), run_name='__main__')
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i','outputs/framewright-score-original.wav','-af','loudnorm=I=-18:TP=-1.5:LRA=7','-ar','48000','public/framewright-score.wav'],check=True)
