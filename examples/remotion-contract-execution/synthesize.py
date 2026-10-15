"""Reproduce this pinned voice trial; existing WAV files are regenerated."""
from pathlib import Path
import hashlib
import json
import os
import sys
import time

BASE = Path(__file__).resolve().parent
LINES = [
    ('opening', 'A signed contract is only the beginning.', .6),
    ('control', 'Documents. Logistics. Inspections. Every handover needs control.', 4.8),
    ('evidence', 'Track responsibilities, manage exceptions, and keep the evidence together.', 10.8),
    ('closeout', 'From payment control to financial reconciliation and contract closeout.', 16.8),
    ('title', 'The Contract Execution Officer Handbook. A practical guide to physical commodity contract execution with M N seven R.', 22.6),
]


def verify_model(shared, manifest_path):
    # Trust the committed pin, never a self-consistent manifest beside the weights.
    manifest = json.loads(manifest_path.read_text())
    root = shared / 'models/Supertonic-3'
    for row in manifest['files']:
        relative = Path(row['file'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe pinned model path')
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Changed model/config/style:' + row['file'])
    return manifest, root


def generate_line(tts, style, text, target, seed, set_seed):
    # A filename is not provenance: never relabel a cached WAV with new inputs.
    set_seed(seed)
    wav, _ = tts.synthesize(text=text, voice_style=style, lang='en', total_steps=12,
                          speed=1.0, max_chunk_length=300, silence_duration=.25,
                          verbose=False)
    tts.save_audio(wav, str(target))


def invalidate_previous_run(base):
    # Fail closed before any WAV can be replaced, including import/runtime failure.
    for name in ["voice-lines.json", "voice-lines-timed.json"]:
        (base / "audio" / name).unlink(missing_ok=True)


def reject_clipping(count):
    if count:
        raise ValueError("Clipped raw speech: " + str(count) + " samples")


def main(base=BASE, shared=None, probe=False):
    shared = Path(shared) if shared is not None else Path(os.environ['SUPERTONIC_SOURCE_ROOT'])
    manifest, root = verify_model(shared, base / 'model-manifest.json')
    for folder in ['audio', 'guides', 'cache']:
        (base / folder).mkdir(parents=True, exist_ok=True)
    invalidate_previous_run(base)
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['HF_HOME'] = str(base / 'cache/hf')
    os.environ['SUPERTONIC_CACHE_DIR'] = str(base / 'cache/supertonic')
    (base / 'guides/model-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    import numpy as np
    import soundfile as sf
    import onnxruntime as ort
    ort.disable_telemetry_events()
    from supertonic import TTS
    tts = TTS(model='supertonic-3', model_dir=root, auto_download=False,
              intra_op_num_threads=4, inter_op_num_threads=1)
    style = tts.get_voice_style('F1')
    rows = []
    for i, (name, text, start) in enumerate(LINES):
        if probe and i:
            break
        target = base / 'audio' / f'{name}.wav'
        started = time.monotonic()
        generate_line(tts, style, text, target, 20261017 + i, np.random.seed)
        audio, sr = sf.read(target)
        if not np.isfinite(audio).all() or not len(audio):
            raise ValueError('Invalid speech')
        clipped = int((abs(audio) >= .999969).sum())
        reject_clipping(clipped)
        row = {'id': name, 'text': text, 'start': start, 'seconds': len(audio) / sr,
               'sample_rate': sr,
               'peak_dbfs': float(20 * np.log10(max(abs(audio).max(), 1e-12))),
               'clipped_samples': clipped,
               'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
               'wall_seconds': round(time.monotonic() - started, 3)}
        rows.append(row)
        print(row, flush=True)
    (base / 'audio/voice-lines.json').write_text(json.dumps(rows, indent=2) + '\n')


if __name__ == '__main__':
    main(probe='--probe' in sys.argv)
