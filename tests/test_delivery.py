"""Regressions for standard delivery escaping, files and platform aspect."""
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from types import SimpleNamespace

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/video-production-router/scripts/delivery.py'
spec = importlib.util.spec_from_file_location('delivery', SCRIPT)
delivery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(delivery)

class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'film #1.mp4').write_bytes(b'fixture video')
        (self.root/'copy.txt').write_text('\ufeffHello — café </pre><script>bad()</script>',encoding='utf-8')
        self.data = {'schema_version':1,'title':'A < B','revision':'v2','state':'review',
                     'note':'Explicit review','variants':[{'platform':'youtube','files':{'video':'film #1.mp4','copy':'copy.txt'}}]}
        self.manifest = self.root/'delivery.json'

    def run_build(self, width=1280, height=720, sar='1:1'):
        self.manifest.write_text(json.dumps(self.data),encoding='utf-8')
        def run(args, **kwargs):
            return SimpleNamespace(stdout=json.dumps({'streams':[{'codec_type':'video','width':width,'height':height,'sample_aspect_ratio':sar}]}))
        with patch.object(delivery.subprocess,'run',side_effect=run):
            return delivery.build(self.manifest)

    def test_escape_utf8_quoted_path_and_pending_check(self):
        receipt=self.run_build()
        page=(self.root/'review.html').read_text()
        self.assertIn('film%20%231.mp4',page)
        self.assertIn('A &lt; B',page)
        self.assertIn('Hello — café &lt;/pre&gt;&lt;script&gt;',page)
        self.assertNotIn('<script>bad()',page)
        self.assertEqual(receipt['browser_check'],'pending')
        self.assertEqual(receipt['page_sha256'],delivery.digest(self.root/'review.html'))
        self.run_build()
        self.assertEqual(receipt['files'],json.loads((self.root/'delivery-receipt.json').read_text())['files'])

    def test_youtube_legacy_copy_is_split_and_never_downloaded(self):
        (self.root/'copy.txt').write_text(
            'YOUTUBE\n\nPRIMARY TITLE\nMain\n\nALTERNATIVE TITLES FOR A/B\n'
            '1. Second\n2. Third\n\nDESCRIPTION\nA paragraph.\n'
            '\nTAGS\nart, ink\n\nOPTIONAL PINNED COMMENT\nHidden note',
            encoding='utf-8')
        self.run_build()
        page = (self.root/'review.html').read_text()
        for value in ['Main', 'Second', 'Third', 'A paragraph.', 'art, ink']:
            self.assertIn('>' + value + '</pre>', page)
        self.assertEqual(page.count('type="button" data-copy='), 5)
        self.assertNotIn('Download copy', page)
        self.assertNotIn('Hidden note', page)

    def test_tiktok_fields_and_subtitle_policy(self):
        variant = self.data['variants'][0]
        variant['platform'] = 'tiktok'
        variant['publication'] = {'caption':'Caption!', 'first_comment':'Comment!'}
        self.run_build(720,1280)
        page = (self.root/'review.html').read_text()
        self.assertIn('preview-card tiktok-preview', page)
        self.assertIn('data-field="Caption"', page)
        self.assertIn('data-field="First comment"', page)
        self.assertNotIn('Primary title', page)
        variant['publication']['titles'] = ['Wrong']
        with self.assertRaises(ValueError):
            self.run_build(720,1280)
        del variant['publication']['titles']
        (self.root/'subs.srt').write_text('captions')
        variant['files']['subtitles'] = 'subs.srt'
        with self.assertRaises(ValueError):
            self.run_build(720,1280)

    def test_structured_optional_fields_and_extra_text(self):
        variant = self.data['variants'][0]
        variant['publication'] = {'titles':['Only title'], 'tags':['ink','art']}
        self.data['extras'] = [{'label':'Extra copy','path':'copy.txt'}]
        self.run_build()
        page = (self.root/'review.html').read_text()
        self.assertNotIn('data-field="Description"', page)
        self.assertIn('>ink, art</pre>', page)
        self.assertIn('data-field="Extra copy"', page)
        self.assertNotIn('href="copy.txt" download', page)

    def test_all_downloads_precede_platform_copy_in_fixed_order(self):
        (self.root/'portrait.mp4').write_bytes(b'portrait fixture')
        (self.root/'sound.wav').write_bytes(b'original audio')
        self.data['variants'] = [
            {'platform':'tiktok','files':{'video':'portrait.mp4'},
             'publication':{'caption':'TT caption','first_comment':'TT comment'}},
            {'platform':'youtube','files':{'video':'film #1.mp4'},
             'publication':{'titles':['YT main','YT second'], 'description':'YT description'}}]
        self.data['extras'] = [{'label':'Audio','path':'sound.wav'}, {'label':'Notes','path':'copy.txt'}]
        self.manifest.write_text(json.dumps(self.data))
        def run(args, **kwargs):
            portrait = any(str(arg).endswith('portrait.mp4') for arg in args)
            return SimpleNamespace(stdout=json.dumps({'streams':[{'codec_type':'video',
                'width':720 if portrait else 1280,'height':1280 if portrait else 720}]}))
        with patch.object(delivery.subprocess,'run',side_effect=run): delivery.build(self.manifest)
        page=(self.root/'review.html').read_text()
        self.assertLess(page.index('id="youtube"'),page.index('id="tiktok"'))
        self.assertLess(page.index('id="youtube-copy"'),page.index('id="tiktok-copy"'))
        self.assertLess(page.index('href="sound.wav" download'),page.index('data-copy='))
        self.assertLess(page.index('id="tiktok"'),page.index('id="publication-texts"'))
        self.assertNotIn('Download copy',page)

    def test_missing_asset_does_not_replace_existing_page(self):
        self.run_build()
        before=(self.root/'review.html').read_bytes()
        self.data['variants'][0]['files']['copy']='missing.txt'
        with self.assertRaises(ValueError):self.run_build()
        self.assertEqual(before,(self.root/'review.html').read_bytes())

    def test_final_requires_complete_package(self):
        self.data['state']='final'
        with self.assertRaises(ValueError):self.run_build()

    def test_final_instrumental_can_explicitly_omit_subtitles(self):
        self.data['state'] = 'final'
        variant = self.data['variants'][0]
        variant['subtitles_required'] = False
        (self.root/'cover.png').write_bytes(b'cover fixture')
        variant['files']['cover'] = 'cover.png'
        self.run_build()

    def test_explicit_final_scope_and_extra_download(self):
        self.data['state'] = 'final'
        self.data['variants'][0]['required_files'] = ['video', 'copy']
        (self.root/'music.wav').write_bytes(b'music fixture')
        self.data['extras'] = [{'label':'Soundtrack <mix>', 'path':'music.wav'}]
        receipt = self.run_build()
        page = (self.root/'review.html').read_text()
        self.assertNotIn('Download cover', page)
        self.assertIn('Soundtrack &lt;mix&gt;', page)
        self.assertEqual(receipt['files'][-1]['role'], 'extra')
        self.data['variants'][0]['required_files'].append('cover')
        with self.assertRaises(ValueError):
            self.run_build()

    def test_platform_aspect_and_anamorphic_pixels(self):
        self.data['variants'][0]['platform']='tiktok'
        with self.assertRaises(ValueError):self.run_build()
        self.run_build(720,1280)
        self.data['variants'][0]['platform']='youtube'
        self.run_build(720,576,'64:45')

    def test_escape_and_duplicate_platform_refused(self):
        outside=self.root.parent/'escape-delivery-fixture.txt'
        outside.write_text('private')
        self.addCleanup(outside.unlink)
        (self.root/'outside.txt').symlink_to(outside)
        self.data['variants'][0]['files']['copy']='outside.txt'
        with self.assertRaises(ValueError):self.run_build()
        self.data['variants'][0]['files'].pop('copy')
        self.data['variants']*=2
        with self.assertRaises(ValueError):self.run_build()

    def test_course_uses_native_lesson_label_and_materials(self):
        variant = self.data['variants'][0]
        variant['platform'] = 'course'
        variant['files'].pop('copy')
        variant['publication'] = {'title': 'Make the bug fail first',
                                  'description': 'One real failing test.',
                                  'prerequisites': 'Basic Python',
                                  'learning_outcomes': 'Write a behavior test'}
        (self.root/'resources.zip').write_bytes(b'fixture resources')
        self.data['extras'] = [{'label':'Teaching files','path':'resources.zip'}]
        receipt = self.run_build()
        page = (self.root/'review.html').read_text()
        self.assertIn('id="course"', page)
        self.assertIn('Course lesson', page)
        self.assertIn('class="landscape"', page)
        self.assertIn('data-field="Learning outcomes"', page)
        self.assertNotIn('YouTube', page)
        self.assertNotIn('TikTok', page)
        self.assertEqual(receipt['files'][0]['platform'], 'course')
        self.assertIn('href="resources.zip" download', page)
        variant['publication']['caption'] = 'Wrong platform field'
        with self.assertRaises(ValueError):
            self.run_build()
        del variant['publication']['caption']
        with self.assertRaises(ValueError):
            self.run_build(720, 1280)

    def test_course_final_plain_copy_remains_visible_and_copyable(self):
        self.data['state'] = 'final'
        variant = self.data['variants'][0]
        variant['platform'] = 'course'
        (self.root/'copy.txt').write_text('A meaningful lesson description — café.', encoding='utf-8')
        (self.root/'cover.png').write_bytes(b'cover fixture')
        (self.root/'subs.srt').write_text('captions', encoding='utf-8')
        variant['files'].update(cover='cover.png', subtitles='subs.srt')
        self.run_build()
        page = (self.root/'review.html').read_text()
        self.assertIn('data-field="Lesson description"', page)
        self.assertIn('>A meaningful lesson description — café.</pre>', page)
        self.assertEqual(page.count('type="button" data-copy='), 1)
        self.assertNotIn('href="copy.txt" download', page)

    def test_invalid_utf8_refused(self):
        (self.root/'copy.txt').write_bytes(b'\xff')
        with self.assertRaises(UnicodeDecodeError):self.run_build()

if __name__=='__main__':
    unittest.main()
