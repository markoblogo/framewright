"""HTTP behavior required by movie review, without media generation."""
import importlib.util
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
from email.utils import formatdate
import os
from urllib.error import HTTPError
from urllib.request import Request,urlopen

PATH=Path(__file__).resolve().parents[1]/'skills/video-production-router/scripts/preview_server.py'
spec=importlib.util.spec_from_file_location('preview_server',PATH)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class PreviewServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=TemporaryDirectory();cls.root=Path(cls.tmp.name)/'review';cls.root.mkdir()
        cls.data=bytes(range(256))*20;(cls.root/'movie.mp4').write_bytes(cls.data)
        (cls.root/'empty.mp4').write_bytes(b'');(cls.root/'index.html').write_text('review')
        (cls.root/'folder').mkdir();(cls.root/'folder/index.html').write_text('nested review')
        (cls.root/'unlisted').mkdir();outside=cls.root.parent/'private.txt';outside.write_text('private')
        (cls.root/'ambiguous-index').mkdir();(cls.root/'ambiguous-index/index.html').mkdir();(cls.root/'ambiguous-index/index.htm').symlink_to(outside);(cls.root/'unsafe-index').mkdir();(cls.root/'unsafe-index/index.html').symlink_to(outside);(cls.root/'escape.txt').symlink_to(outside);(cls.root/'escape-folder').symlink_to(cls.root.parent,target_is_directory=True)
        class Quiet(module.PreviewHandler):
            def log_message(self,*args): pass
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(cls.root)))
        cls.thread=Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.url=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join();cls.tmp.cleanup()
    def request(self,path='/movie.mp4',range_value=None,method='GET',headers=None):
        headers=dict(headers or {})
        if range_value is not None:headers['Range']=range_value
        return urlopen(Request(self.url+path,headers=headers,method=method),timeout=3)
    def test_full_get_and_head(self):
        for method in ['GET','HEAD']:
            with self.request(method=method) as r:
                self.assertEqual(r.status,200);self.assertEqual(r.headers['Accept-Ranges'],'bytes')
                self.assertEqual(int(r.headers['Content-Length']),len(self.data))
                self.assertEqual(r.read(),self.data if method=='GET' else b'')
    def test_forward_backward_and_suffix_bytes(self):
        for value,start,end in [('bytes=4000-4095',4000,4095),('bytes=10-39',10,39),('bytes=-100',5020,5119),('bytes=5100-',5100,5119),('bytes=5100-9000',5100,5119),('bytes=-9000',0,5119)]:
            with self.subTest(value=value),self.request(range_value=value) as r:
                self.assertEqual(r.status,206);self.assertEqual(r.headers['Content-Range'],f'bytes {start}-{end}/5120')
                self.assertEqual(int(r.headers['Content-Length']),end-start+1);self.assertEqual(r.read(),self.data[start:end+1])
    def test_head_range(self):
        with self.request(range_value='bytes=10-19',method='HEAD') as r:
            self.assertEqual(r.status,206);self.assertEqual(r.headers['Content-Length'],'10');self.assertEqual(r.read(),b'')
    def test_invalid_ranges_are_bounded(self):
        for value in ['bytes=5120-','bytes=9-2','bytes=-0','bytes=-','bytes=0-1,3-4','items=0-1','bytes='+'9'*1000+'-']:
            with self.subTest(value=value[:40]),self.assertRaises(HTTPError) as caught:self.request(range_value=value)
            self.assertEqual(caught.exception.code,416);self.assertEqual(caught.exception.headers['Content-Range'],'bytes */5120');caught.exception.close()
    def test_if_range_requires_matching_validator(self):
        stamp=os.stat(self.root/'movie.mp4').st_mtime
        for validator,expected in [(formatdate(stamp,usegmt=True),206),(formatdate(stamp-100,usegmt=True),200),(formatdate(stamp+100,usegmt=True),200),('"unknown-etag"',200),('invalid-date',200)]:
            with self.subTest(validator=validator),self.request(range_value='bytes=10-19',headers={'If-Range':validator}) as r:
                self.assertEqual(r.status,expected)
                self.assertEqual(r.read(),self.data[10:20] if expected==206 else self.data)
    def test_empty_file(self):
        with self.request('/empty.mp4') as r:self.assertEqual(r.read(),b'')
        with self.assertRaises(HTTPError) as caught:self.request('/empty.mp4','bytes=0-')
        self.assertEqual(caught.exception.code,416);caught.exception.close()
    def test_missing_files_do_not_become_partial_successes(self):
        for value in [None,'bytes=0-9']:
            with self.assertRaises(HTTPError) as caught:self.request('/missing.mp4',value)
            self.assertEqual(caught.exception.code,404);caught.exception.close()
    def test_index_works_but_directory_listing_is_disabled(self):
        for path in ['/','/folder/']:
            with self.request(path) as r:self.assertIn(b'review',r.read())
        with self.assertRaises(HTTPError) as caught:self.request('/unlisted/')
        self.assertEqual(caught.exception.code,403);caught.exception.close()
    def test_symlinks_cannot_escape_served_directory(self):
        for path in ['/escape.txt','/escape-folder/private.txt','/unsafe-index/','/ambiguous-index/']:
            for value in [None,'bytes=0-9']:
                with self.assertRaises(HTTPError) as caught:self.request(path,value)
                self.assertEqual(caught.exception.code,403);caught.exception.close()
    def test_foreign_host_is_rejected(self):
        with self.assertRaises(HTTPError) as caught:self.request(headers={'Host':'untrusted.example'})
        self.assertEqual(caught.exception.code,403);caught.exception.close()
    def test_changed_file_not_hidden_by_stale_cache(self):
        with self.request() as r:self.assertEqual(r.headers['Cache-Control'],'no-cache')

if __name__=='__main__':unittest.main()
