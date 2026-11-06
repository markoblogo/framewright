#!/usr/bin/env python3
"""Serve a trusted local review directory with seekable media; loopback only."""
import argparse
from functools import partial
from datetime import timezone
from email.utils import parsedate_to_datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import re


class PreviewHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.remaining = None
        host = self.headers.get('Host', '').lower()
        allowed = {'127.0.0.1', 'localhost', f'127.0.0.1:{self.server.server_port}',
                   f'localhost:{self.server.server_port}'}
        if host not in allowed:
            self.send_error(403, 'Loopback Host required')
            return None
        path = self.translate_path(self.path)
        try:
            Path(path).resolve().relative_to(Path(self.directory).resolve())
        except (ValueError, OSError, RuntimeError):
            self.send_error(403, 'Path outside review directory')
            return None
        if os.path.isdir(path):
            # SimpleHTTPRequestHandler also follows index.html/index.htm symlinks.
            for name in ('index.html', 'index.htm'):
                candidate = Path(path) / name
                if candidate.is_file():
                    try:
                        candidate.resolve().relative_to(Path(self.directory).resolve())
                    except (ValueError, OSError, RuntimeError):
                        self.send_error(403, 'Index outside review directory')
                        return None
                    break
            return super().send_head()
        if not os.path.isfile(path):
            self.send_error(404, 'File not found')
            return None
        value = self.headers.get('Range')
        if not value:
            return super().send_head()
        try:
            stream = open(path, 'rb')
        except OSError:
            self.send_error(404, 'File not found')
            return None
        stat = os.fstat(stream.fileno())
        size = stat.st_size
        validator = self.headers.get('If-Range')
        if validator is not None:
            # We issue Last-Modified, not entity tags. Unknown or stale validators
            # must fall back to the whole representation, never mixed partial bytes.
            try:
                date = parsedate_to_datetime(validator)
                if date.tzinfo is None:
                    date = date.replace(tzinfo=timezone.utc)
                matches = int(date.timestamp()) == int(stat.st_mtime)
            except (ValueError, TypeError, OverflowError, AttributeError):
                matches = False
            if not matches:
                stream.close()
                return super().send_head()
        match = re.fullmatch(r'bytes=([0-9]{0,20})-([0-9]{0,20})', value.strip())
        try:
            if not match or not any(match.groups()):
                raise ValueError()
            a, b = match.groups()
            if a:
                start = int(a)
                end = min(int(b), size - 1) if b else size - 1
            else:
                count = int(b)
                if count <= 0:
                    raise ValueError()
                start, end = max(0, size - count), size - 1
            if start >= size or start > end:
                raise ValueError()
        except ValueError:
            stream.close()
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.send_header('Last-Modified', self.date_time_string(stat.st_mtime))
        self.end_headers()
        stream.seek(start)
        self.remaining = end - start + 1
        return stream

    def list_directory(self, path):
        self.send_error(403, 'Directory listing disabled; open the review HTML file')
        return None

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def copyfile(self, source, outputfile):
        try:
            if self.remaining is None:
                return super().copyfile(source, outputfile)
            remaining = self.remaining
            while remaining:
                chunk = source.read(min(1024 * 1024, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass  # A browser can cancel a range when the timeline is dragged again.


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True,
                        help='Explicit trusted review folder; never defaults to the repository')
    parser.add_argument('--port', type=int, default=8871)
    args = parser.parse_args()
    if not args.directory.is_dir() or not 1 <= args.port <= 65535:
        parser.error('Use an existing directory and a port from 1 to 65535')
    handler = partial(PreviewHandler, directory=str(args.directory.resolve()))
    with ThreadingHTTPServer(('127.0.0.1', args.port), handler) as server:
        print(f'Review only: http://127.0.0.1:{args.port}/ (no directory listing)', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
