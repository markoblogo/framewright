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
2. Run the automated browser check below for seek,resumed playback and delivery. Manually inspect player seeking after template/player changes or a reported fault.
3. Check linked MP4/cover/subtitles/texts. Optional chapter buttons help review but
   do not replace the native timeline test.
4. Keep technical results and owner creative/listening acceptance separate.

[Worked case](../../../docs/productions/github-agentic-workflows.md) ·
[3D correction recipe](../../../docs/methods/3d-explainer-production.md).

## Standard review and publication package

Use the existing builder for every new review/package. Reuse its layout and controls. Change the film's manifest,not the page design. Existing accepted historical pages can remain available until a real update needs regeneration.

The fixed Framewright presentation uses the existing ink/ivory/amber palette,an editorial wordmark,native aspect players and visible version/status. It includes individual media downloads,cover previews and separate UTF-8 publication fields with copy buttons. One or both platforms are supported. No ZIP is required. The status is explicitly supplied and never inferred from a successful build.

Keep manifest and all linked assets in the same private delivery folder or its subfolders. Reference files by relative paths. Copy selected files byte-for-byte into that folder when sources live elsewhere. The server refuses symlinks outside its root.

~~~json
{
  "schema_version": 1,
  "title": "Film title",
  "revision": "v3",
  "state": "final",
  "note": "Both films accepted. Publication packages below.",
  "variants": [
    {
      "platform": "youtube",
      "files": {
        "video": "film-youtube-v3.mp4",
        "cover": "cover-youtube.png",
        "subtitles": "youtube.srt",
        "copy": "youtube.txt"
      }
    }
  ]
}
~~~

States are pilot,review,final,rejected. Add a tiktok variant for portrait video. Default final packages require video and cover,plus YouTube subtitles when applicable. Publication text is supplied as structured fields or a retained legacy copy file. For an instrumental/no-dialogue film,set subtitles_required to false on that variant to explicitly omit subtitle files. Review/pilot/rejected pages may omit cover,subtitles and copy. YouTube copy contains primary title,1–2 alternatives,description,tags and optional pinned comment. TikTok copy contains caption and first comment. Those are editorial checks before packaging;the builder does not invent or optimise them.

~~~sh
python3 skills/video-production-router/scripts/delivery.py /absolute/private/package/delivery.json
python3 skills/video-production-router/scripts/preview_server.py --directory /absolute/private/package --port 8871
node skills/video-production-router/scripts/delivery_check.cjs http://127.0.0.1:8871/review.html /absolute/private/package/delivery-receipt.json /absolute/existing/playwright/package.json
~~~

The Python builder uses existing ffprobe/FFmpeg. It checks nonempty local files,platform display aspect including SAR,UTF-8 text and full video/audio decode. It writes review.html and a hash receipt. It validates all assets before replacing generated outputs. Each rebuild resets browser-check status to pending.

The real-browser check uses existing Playwright and installed Chrome. It also verifies a visibly portrait TikTok stage and the copied-state confirmation on every publication button. It verifies served file hashes,response charset,metadata/frame availability,forward/backward seeking,resumed playback,browser downloads and exact clipboard contents. Complete-file HTTP verification allows180seconds per asset and disposes each response after checking,to accommodate large local masters without retaining every response body. It checks desktop/mobile overflow and retains two screenshots. Keep the current receipt with the package. Listening and creative approval remain owner decisions.

Manual player checks are template-maintenance work after a relevant change or reported fault. Ordinary per-film handoffs run the reusable automated checks. If runtime access is unavailable,record that check as pending and state the exact limitation instead of treating it as a creative failure or requiring repeated owner debugging.

Before delivery,ensure the local server is actually reachable. Give its review URL and direct individual download links. If the server later stops,restart it for the same retained package. Absolute file links are a fallback. A file existing on disk alone does not establish a working browser download.

The standard template is versioned with source. After template/player changes,inspect both viewport screenshots and manually review normal playback before adopting the revision. No film regeneration is required to check the interface.

### Initial verification —17November2026

The two accepted PAN2 aspect packages were copied byte-for-byte into the private external studio deliveries/standard-preview-demo folder. Eight source hashes match. Chrome157 passed automatic seek/resume,download,HTTP-byte/UTF-8,clipboard and desktop/mobile checks;both screenshots were inspected. Six new builder regressions and12 existing server tests passed. These software/interface checks add no film or generative-tool qualification. At that initial v1 checkpoint,owner design approval was pending;template v2 acceptance is recorded below.

### Explicit package contents

At intake,set each variant's required_files to the agreed roles,for example ["video","copy"]. Missing required assets stop the build. Unrequested absent roles produce no empty section or inactive button. Default final requirements follow the platform and supplied publication fields;new packages should declare their own list. Video remains necessary for a video-review variant.

Optional top-level extras is a list of objects with label and path,for example {"label":"Soundtrack","path":"music.wav"}. Use it for separate audio,alternative covers,standalone A/B titles,first comments or other agreed files. Extra media are individually checked downloads;extra text uses copyable fields under the additional-materials section. They receive the same path,nonempty-file,hash and real-browser download checks. Add or omit records instead of changing HTML.

### Platform-specific publication fields —template v2

Owner correction17November2026. Publication text is displayed as separate fields,each with its own Copy button. A successful clipboard write changes that button to a green checked “Скопировано” state and announces confirmation. Clipboard failure selects the field and explicitly requests manual copying.

YouTube fields are primary title,title2,title3,description and tags. Omit unused alternatives/fields. TikTok fields are caption and first_comment. TikTok has neither publication titles nor subtitle downloads. Its player stage itself is9:16,including the surrounding container. YouTube may include subtitles when needed.

Use variant.publication as an object. For YouTube,supply titles as an array of up to3strings,description as text,and tags as text or a string array. For TikTok,supply caption and first_comment as text. Unsupported platform fields are refused. All values remain plain escaped text. Buttons copy the field value only.

A retained files.copy text file can still feed older packages. Recognised legacy headings are split into the same platform fields;heading labels and alternative-title numbering are excluded from copied text. No publication text download button is rendered. Additional .txt/.md materials are copyable blocks too. Other extra media remain downloads.

Declare required_files for the actual media/file scope. A structured publication object removes the default legacy-copy-file requirement. Existing source copy files may stay in the private package as provenance. Rebuilding an interface does not change a film,cover,publication URL or creative acceptance.

### Owner acceptance —17November2026

The owner accepted template v2 with “Шаблон принимаю”. This is the default review/delivery interface for future packages. Keep the shared layout and platform rules;populate each project’s agreed fields and assets. Private deliveries/standard-preview-demo/owner-template-acceptance.json pins the selected template/page hashes and browser evidence. This acceptance covers the interface. Film,cover and soundtrack decisions stay in their production records.


### Course lesson package —template v2.1

For an actual landscape lesson,use `platform: "course"` in the same manifest and
builder. It renders **Учебный урок**,not YouTube/TikTok,and keeps the accepted
layout,player,downloads and clipboard controls. No LMS or upload adapter is added.
Course `publication` contains optional plain-text `title`, `description`,
`prerequisites` and `learning_outcomes`;social-platform fields are refused.
Declare `required_files` explicitly for the current review stage;for a complete
lesson package use video,cover and subtitles. Course video is16:9;subtitle default
is true. Add VTT,teaching ZIP,transcript or instructor materials through existing
extras. Markdown/text extras remain visible copy blocks;ZIP/VTT remain downloads.
Run the same real-browser seek/download/clipboard checks. A successful package
check is not Udemy upload,platform acceptance,owner review or learner validation.
