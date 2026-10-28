"""Bounded optional OTIO export; no implicit installation or paid/model calls."""
import importlib.util
import json
from pathlib import Path
import runpy
import tempfile
import unittest
import wave

ROOT=Path(__file__).resolve().parents[1]
M=runpy.run_path(str(ROOT/'skills/video-production-router/scripts/otio_export.py'))
HAS_OTIO=importlib.util.find_spec('opentimelineio') is not None


class OtioExportTest(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name)
        self.media=self.root/'voice space.wav'
        with wave.open(str(self.media),'wb') as f:f.setparams((1,2,8000,0,'NONE',''));f.writeframes(b'\0\0'*8000)
        self.spec=self.root/'spec.json'
        self.data={'schema':'framewright-otio-export-v1','name':'test','rate':30,'duration_frames':21,
                   'media':[{'id':'voice','path':self.media.name,'sha256':M['E']['file_hash'](self.media)}],
                   'tracks':[{'id':'voice','kind':'audio','items':[{'id':'lead','type':'gap','duration_frames':3},{'id':'spoken','type':'clip','media':'voice','in_frames':4,'duration_frames':18}]}]}
        self.write()
    def write(self):self.spec.write_text(json.dumps(self.data))

    def test_explicit_timing_and_identity_preflight(self):
        result=M['inspect_spec'](self.spec)
        self.assertEqual(result['spec']['duration_frames'],21)
        self.assertEqual(result['media']['voice']['sha256'],M['E']['file_hash'](self.media))

    def test_exact_audio_extent_does_not_use_rounded_format_duration(self):
        self.assertEqual(M['available_frames']({'codec_type':'audio','duration_ts':2046400,'time_base':'1/48000'},30),1279)
        with self.assertRaises(ValueError):M['available_frames']({'codec_type':'audio','duration':'42.633333'},30)

    def test_missing_and_replaced_media_rejected(self):
        self.media.rename(self.root/'gone.wav')
        with self.assertRaises(OSError):M['inspect_spec'](self.spec)
        (self.root/'gone.wav').rename(self.media)
        with self.media.open('ab') as f:f.write(b'changed')
        with self.assertRaises(ValueError):M['inspect_spec'](self.spec)

    def test_no_silent_effect_drop(self):
        for row in [self.data,self.data['tracks'][0],self.data['tracks'][0]['items'][1]]:
            row['effects']=['crop']
            self.write()
            with self.assertRaises(ValueError):M['inspect_spec'](self.spec)
            del row['effects']

    def test_out_of_bounds_and_track_duration_rejected(self):
        self.data['tracks'][0]['items'][1]['in_frames']=20;self.write()
        with self.assertRaises(ValueError):M['inspect_spec'](self.spec)
        self.data['tracks'][0]['items'][1]['in_frames']=0;self.data['duration_frames']=30;self.write()
        with self.assertRaises(ValueError):M['inspect_spec'](self.spec)

    def test_remote_absolute_and_traversal_refs_rejected(self):
        for value in ['https://example.com/voice.wav',str(self.media),'../voice.wav']:
            self.data['media'][0]['path']=value;self.write()
            with self.assertRaises(ValueError):M['inspect_spec'](self.spec)

    def test_invalid_ids_and_rates_rejected(self):
        self.data['rate']=29.97;self.write()
        with self.assertRaises(ValueError):M['inspect_spec'](self.spec)
        self.data['rate']=30;self.data['tracks'][0]['items'][1]['id']='lead';self.write()
        with self.assertRaises(ValueError):M['inspect_spec'](self.spec)

    @unittest.skipUnless(HAS_OTIO,'Optional OTIO library not installed')
    def test_official_roundtrip_gaps_ranges_urls_and_no_overwrite(self):
        out=self.root/'timeline.otio';r=M['export'](self.spec,out)
        self.assertEqual(r['roundtrip']['duration_frames'],21)
        clip=r['roundtrip']['tracks'][0]['items'][1]
        self.assertEqual((clip['timeline_start'],clip['source_in'],clip['duration']),(3,4,18))
        self.assertEqual(clip['target_url'],'voice%20space.wav')
        self.assertEqual(r['editor_import'],'not_tested')
        with self.assertRaises(ValueError):M['export'](self.spec,out)

    @unittest.skipUnless(HAS_OTIO,'Optional OTIO library not installed')
    def test_export_stays_with_media_package(self):
        with self.assertRaises(ValueError):M['export'](self.spec,self.root.parent/'outside.otio')


if __name__=='__main__':unittest.main()
