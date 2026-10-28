#!/usr/bin/env python3
"""Allowlisted worker with inherited exclusion and a parent-independent deadline."""
import math
import os
from pathlib import Path
import runpy
import signal
import sys
import threading


def main():
    descriptor, seconds, mode, *arguments = sys.argv[1:]
    descriptor = int(descriptor); seconds = float(seconds)
    if not math.isfinite(seconds) or not 1 <= seconds <= 180:
        raise ValueError('Invalid worker deadline')
    scripts = {'local-media-review': 'media_review.py', 'review-clip': 'executor_clip_worker.py'}
    if mode not in scripts:
        raise ValueError('Unsupported worker')
    os.fstat(descriptor)  # Keep the inherited host-lock description open until exit.
    if os.getpgrp() != os.getpid():
        raise ValueError('Worker requires its own process group')
    def expire():
        os.killpg(os.getpgrp(), signal.SIGKILL)
    watchdog = threading.Timer(seconds, expire)
    watchdog.daemon = True; watchdog.start()
    script = Path(__file__).with_name(scripts[mode])
    sys.argv = [str(script), *arguments]
    try:
        runpy.run_path(str(script), run_name='__main__')
    finally:
        watchdog.cancel()


if __name__ == '__main__':
    main()
