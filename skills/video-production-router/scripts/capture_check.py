#!/usr/bin/env python3
"""Local short recording calibration; measurements are not perceptual approval."""
import argparse
import array
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

MAX_SECONDS = 60
MAX_BYTES = 100 * 1024 * 1024


def interval(value):
    try:
        start, end = map(float, value.split(':'))
        if not (math.isfinite(start) and math.isfinite(end) and 0 <= start < end):
            raise ValueError()
        return (start, end)
    except ValueError:
        raise argparse.ArgumentTypeError('Use finite START:END seconds, 0 <= START < END')


def db(value):
    return round(20 * math.log10(value), 2) if value > 0 else None


def audio_metrics(samples, channels, rate, room=None, speech=None):
    if not samples or channels < 1 or len(samples) % channels:
        raise ValueError('Empty or malformed decoded audio')
    if any(not math.isfinite(v) for v in samples):
        raise ValueError('Non-finite audio samples')
    duration = len(samples) / channels / rate
    for span in (room, speech):
        if span and not (0 <= span[0] < span[1] <= duration):
            raise ValueError('Declared interval is outside decoded audio')
    if room and speech and max(room[0], speech[0]) < min(room[1], speech[1]):
        raise ValueError('Room-tone and speech intervals must not overlap')
    rows = []
    for ch in range(channels):
        data = samples[ch::channels]
        peak = max(map(abs, data))
        rms = math.sqrt(sum(v*v for v in data) / len(data))
        def level(span):
            if span is None:
                return None
            part = data[int(span[0]*rate):int(span[1]*rate)]
            if not part:
                raise ValueError('Interval contains no decoded samples')
            return math.sqrt(sum(v*v for v in part)/len(part))
        noise, voice = level(room), level(speech)
        snr = db(voice/noise) if voice and noise else None
        flags = []
        if peak == 0:
            flags.append('no_signal')
        elif peak >= 10**(-0.5/20):
            flags.append('near_full_scale_reduce_input_and_repeat')
        elif peak < 10**(-18/20):
            flags.append('low_input_raise_level_or_move_closer_and_repeat')
        if speech is not None and voice == 0:
            flags.append('no_signal_in_declared_speech_interval_repeat')
        if snr is not None and snr < 20:
            flags.append('low_declared_speech_to_room_ratio_quieten_room_and_repeat')
        rows.append({'channel':ch+1,'sample_peak_dbfs':db(peak),'rms_dbfs':db(rms),
                     'samples_at_or_above_full_scale':sum(abs(v)>=1 for v in data),
                     'room_rms_dbfs':db(noise) if noise is not None else None,
                     'speech_rms_dbfs':db(voice) if voice is not None else None,
                     'declared_speech_to_room_db':snr,
                     'suggested_gain_to_minus9_peak_db':round(-9-db(peak),2) if peak else None,
                     'flags':flags})
    return {'decoded_seconds':duration,'channels':rows,'room_interval':room,'speech_interval':speech,
            'scope':'Sample peaks, not true peaks. Whole-clip peak may be handling noise. Intervals are operator-labelled, not detected speech. Gain is an estimate to test, never an automatic setting.'}


def command(args):
    try:
        return subprocess.run(args,capture_output=True,check=True,timeout=45)
    except subprocess.TimeoutExpired as exc:
        raise ValueError('Local check timed out; use a shorter calibration clip') from exc
    except subprocess.CalledProcessError as exc:
        raise ValueError('Media inspection failed: '+exc.stderr.decode(errors='replace')[-1200:]) from exc


def inspect(path, room=None, speech=None):
    path=Path(path).resolve(strict=True)
    if not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError('Use a regular local calibration file no larger than 100 MiB')
    for tool in ('ffmpeg','ffprobe'):
        if not shutil.which(tool):
            raise ValueError(tool+' is not installed; nothing will be downloaded')
    before=hashlib.sha256(path.read_bytes()).hexdigest()
    probe=json.loads(command(['ffprobe','-v','error','-protocol_whitelist','file,pipe','-show_format','-show_streams','-of','json',str(path)]).stdout)
    duration=float(probe.get('format',{}).get('duration',0))
    if not math.isfinite(duration) or not 0 < duration <= MAX_SECONDS:
        raise ValueError('Use a calibration recording with a known duration of 0–60 seconds')
    report={'schema_version':1,'source':str(path),'sha256':before,'duration_seconds':duration,
            'publication_authorized':False,'perceptual_review':'not_performed','audio':None,'video':None,
            'manual_checks':['Listen for pronunciation, delivery, room echo and distortion.',
                             'For video inspect framing, focus, lighting and lip sync in actual playback.']}
    audio=next((s for s in probe['streams'] if s['codec_type']=='audio'),None)
    video=next((s for s in probe['streams'] if s['codec_type']=='video' and not s.get('disposition',{}).get('attached_pic')),None)
    common=['ffmpeg','-v','error','-nostdin','-protocol_whitelist','file,pipe','-i',str(path)]
    if audio:
        channels=int(audio['channels'])
        if not 1 <= channels <= 8:
            raise ValueError('Calibration supports 1–8 audio channels')
        data=command(common+['-map',f"0:{audio['index']}",'-t','60','-ar','48000','-c:a','pcm_f32le','-f','f32le','-']).stdout
        samples=array.array('f');samples.frombytes(data)
        if sys.byteorder!='little':samples.byteswap()
        report['audio']=audio_metrics(samples,channels,48000,room,speech)
        report['audio']['input_sample_rate']=audio.get('sample_rate')
    elif room or speech:
        raise ValueError('Declared audio intervals but no audio stream')
    if video:
        # Sampled luma is only an exposure clue, never proof of focus, framing or motion.
        proc=command(common+['-map',f"0:{video['index']}",'-t','60','-an','-vf','fps=2,scale=320:-2,signalstats,metadata=print:file=-','-f','null','-'])
        values=[float(x) for x in re.findall(r'lavfi.signalstats.YAVG=([0-9.]+)',proc.stdout.decode(errors='replace'))]
        report['video']={'width':video.get('width'),'height':video.get('height'),'average_frame_rate':video.get('avg_frame_rate'),
                         'sampled_luma_frames':len(values),'sampled_luma_average':round(sum(values)/len(values),2) if values else None,
                         'scope':'2 fps resized luma samples; no visual/temporal/audio-sync evaluation; intentional dark scenes may be valid.',
                         'flags':['very_dark_samples_check_lighting_manually'] if values and sum(values)/len(values)<30 else []}
    if not audio and not video:
        raise ValueError('No audio or video stream found')
    if hashlib.sha256(path.read_bytes()).hexdigest()!=before:
        raise ValueError('Source changed during inspection; repeat on stable file')
    report['source_unchanged']=True
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file')
    parser.add_argument('--room-tone',type=interval,help='Known quiet interval START:END')
    parser.add_argument('--speech',type=interval,help='Known speech interval START:END')
    args=parser.parse_args()
    try:
        result=inspect(args.file,args.room_tone,args.speech)
    except (ValueError,OSError,KeyError) as exc:
        parser.exit(2,str(exc)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))


if __name__=='__main__':main()
