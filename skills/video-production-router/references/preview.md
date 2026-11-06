# Standard local movie preview

Use this helper for prepared film review pages and their local media. A basic
`python -m http.server` can ignore byte ranges: playback works, but dragging the
movie timeline can fail until the file is fully buffered.

```sh
python3 skills/video-production-router/scripts/preview_server.py --directory /absolute/private/review-folder --port 8871
```

Open the explicit HTML filename, for example `http://127.0.0.1:8871/review.html`.
Use an existing trusted review folder on the studio's external disk, ideally only
the intended delivery files. Do not serve the repository, home folder or volume root.
No copy, generation, upload, publication or installation occurs. Stop with Ctrl-C.

The helper binds only 127.0.0.1, rejects foreign Host headers and resolved paths
outside the chosen folder, disables directory listings and asks the browser to
revalidate cached files. Other local processes can still read the served files;
this is a trusted localhost review tool, not an authenticated public file server.
Do not edit served paths/symlinks concurrently; path checks are not OS-level isolation.

Single byte ranges support GET/HEAD with 206, bounded Content-Length and
Content-Range; invalid/unsatisfiable ranges return 416. Normal files return 200.
Multipart ranges are not supported. Keep movie filenames versioned and encode
MP4 with `-movflags +faststart`; byte-range support does not repair a corrupt file.

Before handoff:

1. Fully decode the encoded final and verify dimensions/duration/hash.
2. Open its page, drag the native timeline forward and backward **before watching
   through**, then confirm a decoded frame and continued playback.
3. Check linked MP4/cover/subtitles/texts. Optional chapter buttons help review but
   do not replace the native timeline test.
4. Keep technical results and owner creative/listening acceptance separate.

[Worked case](../../../docs/productions/github-agentic-workflows.md) ·
[3D correction recipe](../../../docs/methods/3d-explainer-production.md).
