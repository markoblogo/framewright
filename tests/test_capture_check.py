import array
import importlib.util
from pathlib import Path
import math
import unittest

path=Path(__file__).resolve().parents[1]/'skills/video-production-router/scripts/capture_check.py'
spec=importlib.util.spec_from_file_location('capture_check',path)
cc=importlib.util.module_from_spec(spec);spec.loader.exec_module(cc)

class CaptureChecks(unittest.TestCase):
    def test_low_level_guidance(self):
        r=cc.audio_metrics([.02,-.02]*100,1,100)
        self.assertIn('low_input_raise_level_or_move_closer_and_repeat',r['channels'][0]['flags'])
        self.assertAlmostEqual(r['channels'][0]['suggested_gain_to_minus9_peak_db'],24.98,places=1)
    def test_channels_never_cancel_and_clipping_counts(self):
        r=cc.audio_metrics([1,-1]*100,2,100)
        self.assertEqual([x['samples_at_or_above_full_scale'] for x in r['channels']],[100,100])
    def test_silence_cannot_recommend_infinite_gain(self):
        r=cc.audio_metrics([0]*100,1,100)['channels'][0]
        self.assertEqual(r['flags'],['no_signal']);self.assertIsNone(r['suggested_gain_to_minus9_peak_db'])
    def test_noise_only_with_operator_intervals(self):
        samples=[.001]*100+[.1]*100
        self.assertIsNone(cc.audio_metrics(samples,1,100)['channels'][0]['declared_speech_to_room_db'])
        r=cc.audio_metrics(samples,1,100,(0,1),(1,2))
        self.assertEqual(r['channels'][0]['declared_speech_to_room_db'],40)
    def test_invalid_intervals_and_signal(self):
        for spans in [((0,1.1),(1,2)),((0,3),None)]:
            with self.assertRaises(ValueError):cc.audio_metrics([.1]*200,1,100,*spans)
        for samples in [[],[float('nan')],[float('inf')]]:
            with self.assertRaises(ValueError):cc.audio_metrics(samples,1,100)
        for text in ['nan:1','0:inf','2:1','-1:2']:
            with self.assertRaises(Exception):cc.interval(text)

if __name__=='__main__':unittest.main()
