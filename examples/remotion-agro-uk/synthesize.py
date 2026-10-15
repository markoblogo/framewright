"""Synthesize the retained script only after verifying both pinned voice files."""
from pathlib import Path
import hashlib
import json
import time
import wave

MODEL_FILES = {
    'tetiana.onnx': '1206d8447b99632badeb63d6132241f76cf551874e5254eb8836db36aed7c85c',
    'tetiana.onnx.json': '12de3568ea07f32b4ad922667b27c01ac3da9aeeb04f62a0036f9b32a2eb6aee',
}
LINES = [
    ('grain', 'Ринок починається із зерна. Але угода — це значно більше.'),
    ('route', 'Якість, ціна, логістика. І люди, які з’єднують усе.'),
    ('deal', 'Від офера до контракту та виконання.'),
    ('book', 'Брокеридж на ринках зернових та олійних.'),
    ('cta', 'Безкоштовний практичний гід українською. Завантажуйте та читайте.'),
]


def verify_voice_files(base):
    for name, expected in MODEL_FILES.items():
        path = base / 'models' / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Voice file hash mismatch: {name}')
    return base / 'models/tetiana.onnx', base / 'models/tetiana.onnx.json'


def main(base=None):
    base = Path(base) if base is not None else Path(__file__).parent
    model, config = verify_voice_files(base)
    # No runtime load or synthesis is attempted with unverified files.
    import onnxruntime as ort
    from piper import PiperVoice, SynthesisConfig
    ort.disable_telemetry_events()
    voice = PiperVoice.load(str(model), config_path=str(config))
    rows = []
    for name, text in LINES:
        started = time.monotonic()
        path = base / 'audio' / f'{name}.wav'
        with wave.open(str(path), 'wb') as wav:
            voice.synthesize_wav(text, wav, syn_config=SynthesisConfig(length_scale=1.0))
        with wave.open(str(path)) as wav:
            seconds = wav.getnframes() / wav.getframerate()
        rows.append({'id': name, 'text': text, 'duration': seconds,
                     'synthesis_sec': round(time.monotonic() - started, 3)})
        print(name, seconds, flush=True)
    (base / 'audio/voice-lines.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
