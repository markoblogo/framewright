#!/usr/bin/env python3
"""Build one standard local review/delivery page from an explicit package manifest."""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import subprocess
from urllib.parse import quote

VERSION = '2.2'
PLATFORMS = {'youtube': 'YouTube', 'tiktok': 'TikTok', 'course': 'Course lesson'}
STATES = {'pilot': 'Preview', 'review': 'For review', 'final': 'Publication package',
          'rejected': 'Rejected preview'}
LABELS = {'video': 'Download video', 'cover': 'Download cover',
          'subtitles': 'Download subtitles', 'copy': 'Download copy'}
CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{color-scheme:dark;--bg:#070808;--fg:#f0f0eb;--muted:#939999;--line:#272b2b;--accent:#b5d4c4;--columns:minmax(0,256fr) minmax(0,81fr) minmax(240px,120fr)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 'DM Sans',Arial,sans-serif;-webkit-font-smoothing:antialiased}
header,main,footer{width:min(1320px,calc(100% - 80px));margin:auto}header{height:78px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line)}main{padding-top:30px}
.wordmark{font:800 18px Manrope,Arial,sans-serif;letter-spacing:-.7px;display:flex;gap:8px;align-items:center}.brand-dot{width:5px;height:5px;background:var(--accent);border-radius:50%}
nav{display:flex;gap:26px;font-size:13px;color:#bbc0bd}a{color:inherit;text-decoration:none}a:hover{color:white}h1,h2,h3,p{overflow-wrap:anywhere}h1,h2,h3{font-family:Manrope,Arial,sans-serif}h1{font-size:clamp(28px,3.2vw,42px);font-weight:500;line-height:1.15;letter-spacing:-1.5px;margin:12px 0 16px;max-width:none}h2{font-size:20px;line-height:1.35;font-weight:600;letter-spacing:-.5px;margin:0}h3{font-size:13px;font-weight:600;margin:0}
.intro{width:100%;margin-bottom:30px}.intro p{margin:0;color:var(--muted);font-size:14px}.intro .status{font-size:11px;letter-spacing:.8px;color:var(--accent)}
.media-grid,.publication-grid{display:grid;grid-template-columns:var(--columns);gap:24px;align-items:start}.media-grid{padding-top:24px;border-top:1px solid var(--line)}.preview-card,.download-card{min-width:0;display:flex;flex-direction:column;gap:12px}.download-card{align-self:stretch}.stage{min-width:0;background:#000;border:1px solid var(--line);overflow:hidden}.landscape{aspect-ratio:16/9}.portrait{aspect-ratio:9/16}video{display:block;width:100%;height:100%;max-height:none;object-fit:contain}.youtube-preview .stage,.course-preview .stage{aspect-ratio:16/9}.tiktok-preview .stage{aspect-ratio:9/16}
.files{display:grid;grid-auto-rows:minmax(42px,1fr);gap:10px;flex:1}.download,button{font:inherit;border:1px solid #454d49;background:transparent;color:var(--fg);border-radius:3px;text-align:left}.download{display:flex;align-items:center;padding:10px 14px;font-size:14px;line-height:1.35}.download.primary{background:#e4e9e1;color:#121613;border-color:#dce0d9;font-weight:600}.download:hover{border-color:#dce0d9}.download.primary:hover{background:white}
.publication-grid{margin-top:32px;padding-top:26px;border-top:1px solid var(--line)}.publication{min-width:0}.publication-youtube,.publication-course{grid-column:1/3}.publication-tiktok{grid-column:3}.copy{margin-top:14px;padding:18px;border:1px solid var(--line);border-radius:3px;background:#0c1010}.copy-head{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.copy-head button{margin-left:auto}.copy-status{flex-basis:100%;font-size:12px;color:var(--accent)}.copy-status:empty{display:none}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.65 'DM Sans',Arial,sans-serif;margin:12px 0 0;color:#d5dcd7}
button{cursor:pointer;padding:5px 10px;font-size:12px;line-height:1.5}button:hover{border-color:var(--accent)}button[data-copied=true]{background:#14231c;border-color:#789c87;color:#d0e8da}:focus-visible{outline:2px solid var(--accent);outline-offset:4px}.media-error{color:#efb4a8;padding:12px;border:1px solid #8a5d55}.extra-text{margin-top:24px}footer{font-size:12px;color:var(--muted);border-top:1px solid var(--line);margin-top:40px;padding:24px 0}
.single-landscape{grid-template-columns:minmax(0,1fr) minmax(240px,320px)}.single-portrait{grid-template-columns:minmax(0,240px) minmax(240px,1fr)}.publication-grid.single-landscape,.publication-grid.single-portrait{grid-template-columns:1fr}.publication-grid.single-landscape>.publication,.publication-grid.single-portrait>.publication{grid-column:1}
@media(max-width:900px) and (min-width:761px){:root{--columns:minmax(0,256fr) minmax(0,81fr) minmax(210px,150fr)}header,main,footer{width:calc(100% - 48px)}.media-grid,.publication-grid{gap:16px}.download{font-size:12px;padding:8px}.copy{padding:14px}}
@media(max-width:760px){header,main,footer{width:calc(100% - 32px)}header{height:68px}main{padding-top:22px}nav{gap:18px}h1{font-size:29px;letter-spacing:-1px}.intro{margin-bottom:24px}.media-grid,.publication-grid{display:flex;flex-direction:column;gap:24px}.preview-card,.download-card,.publication{width:100%}.tiktok-preview{width:min(100%,280px);align-self:center}.files{display:flex;flex-direction:column}.download{min-height:46px}.publication-grid{margin-top:28px}.copy{padding:16px}}
"""
JS = """
document.querySelectorAll('video').forEach(v=>{
 v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()}));
 v.addEventListener('error',()=>{const p=document.createElement('p');p.className='media-error';
 p.textContent='Video could not load. Use the download link.';v.after(p)},{once:true});
});
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{
 const text=document.getElementById(b.dataset.copy).textContent;
 try{await navigator.clipboard.writeText(text);b.textContent='✓ Copied';b.dataset.copied='true';b.parentElement.querySelector('.copy-status').textContent='Copied to clipboard'}
 catch{const s=window.getSelection(),r=document.createRange();r.selectNodeContents(document.getElementById(b.dataset.copy));
 s.removeAllRanges();s.addRange(r);b.textContent='Text selected — copy manually'}
}));
"""
def escape(value):
    return html.escape(str(value), quote=True)

def local_file(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError('Asset path must be relative to the package')
    p = (root / value).resolve()
    if not p.is_relative_to(root) or not p.is_file() or p.stat().st_size == 0:
        raise ValueError('Missing, empty or escaping package file: ' + value)
    if p.name in {'review.html', 'delivery-receipt.json'}:
        raise ValueError('Asset conflicts with generated output')
    return p

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def size_label(size):
    return f"{size / 1048576:.2f} MB" if size >= 1048576 else f"{max(1, round(size / 1024))} KB"


def publication_fields(platform, supplied, legacy):
    allowed = ({'title', 'description', 'prerequisites', 'learning_outcomes'} if platform == 'course'
               else {'titles', 'description', 'tags'} if platform == 'youtube'
               else {'caption', 'first_comment'})
    if supplied is not None:
        if not isinstance(supplied, dict) or set(supplied) - allowed:
            raise ValueError('Unsupported publication fields for ' + platform)
        data = dict(supplied)
    else:
        # Read retained publication text files without copying their headings or
        # numbering into the actual publication fields.
        import re
        headings = {
            'PRIMARY TITLE': 'title', 'ALTERNATIVE TITLES FOR A/B': 'alternatives',
            'DESCRIPTION': 'description', 'TAGS': 'tags',
            'OPTIONAL PINNED COMMENT': 'ignored', 'PINNED COMMENT': 'ignored',
            'CAPTION': 'caption', 'FIRST COMMENT': 'first_comment',
            'COVER TEXT': 'ignored',
        }
        sections, current, found = {}, None, False
        for line in (legacy or '').splitlines():
            heading = line.strip()
            if heading in headings:
                current = headings[heading]
                sections.setdefault(current, [])
                found = True
            elif current:
                sections[current].append(line)
        data = {k: '\n'.join(v).strip() for k, v in sections.items()}
        if platform == 'youtube':
            titles = [data.get('title', '')]
            titles += [re.sub(r'^\s*\d+[.)]\s*', '', line).strip()
                       for line in data.get('alternatives', '').splitlines() if line.strip()]
            data['titles'] = [title for title in titles if title][:3]
        if legacy and not found:
            data['description' if platform in {'youtube', 'course'} else 'caption'] = legacy.strip()
    if platform == 'course':
        fields = [(label, data.get(key, '')) for key, label in [
            ('title', 'Lesson title'), ('description', 'Lesson description'),
            ('prerequisites', 'Prerequisites'), ('learning_outcomes', 'Learning outcomes')]]
    elif platform == 'youtube':
        titles = data.get('titles', [])
        if not isinstance(titles, list) or len(titles) > 3 or any(not isinstance(t, str) for t in titles):
            raise ValueError('YouTube titles must be a list of at most three strings')
        fields = list(zip(['Primary title', 'Title 2', 'Title 3'], titles))
        tags = data.get('tags', '')
        if isinstance(tags, list) and all(isinstance(t, str) for t in tags):
            tags = ', '.join(tags)
        fields += [('Description', data.get('description', '')), ('Tags', tags)]
    else:
        fields = [('Caption', data.get('caption', '')), ('First comment', data.get('first_comment', ''))]
    if any(not isinstance(value, str) for _, value in fields):
        raise ValueError('Publication fields must contain text')
    return [(label, value.strip()) for label, value in fields if value.strip()]

def copy_section(identity, label, value):
    return (
        f'<section class="copy" data-field="{escape(label)}">'
        f'<div class="copy-head"><h3>{escape(label)}</h3>'
        f'<button type="button" data-copy="{identity}">Copy</button>'
        '<span class="copy-status" role="status" aria-live="polite"></span></div>'
        f'<pre id="{identity}">{escape(value)}</pre></section>'
    )

def build(manifest):
    manifest = Path(manifest).resolve()
    root = manifest.parent
    data = json.loads(manifest.read_text(encoding='utf-8'))
    if data.get('schema_version') != 1 or data.get('state') not in STATES:
        raise ValueError('Expected schema_version 1 and a supported state')
    for key in ('title', 'revision', 'note'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError('Required text: ' + key)
    variants = data.get('variants')
    if not isinstance(variants, list) or not 1 <= len(variants) <= 2:
        raise ValueError('Provide one or two platform variants')
    seen, records, sections, publication, download_buttons = set(), [], [], [], []
    # Platform order is a presentation contract,not caller insertion order.
    order = {"youtube": 0, "course": 1, "tiktok": 2}
    variants = sorted(variants, key=lambda v: order.get(v.get("platform"), 99))
    for variant in variants:
        platform = variant.get('platform')
        if platform not in PLATFORMS or platform in seen:
            raise ValueError('Each platform must be youtube, tiktok or course, once')
        seen.add(platform)
        assets = variant.get('files', {})
        if not isinstance(assets, dict) or 'video' not in assets or set(assets) - LABELS.keys():
            raise ValueError('Expected video and supported file roles')
        if platform == 'tiktok' and 'subtitles' in assets:
            raise ValueError('TikTok packages do not include subtitles')
        subtitles_required = variant.get('subtitles_required', platform in {'youtube', 'course'})
        if not isinstance(subtitles_required, bool):
            raise ValueError('subtitles_required must be boolean')
        default_required = ['video', 'cover']
        if variant.get('publication') is None:
            default_required.append('copy')
        if subtitles_required:
            default_required.append('subtitles')
        required = variant.get('required_files', default_required if data['state'] == 'final' else ['video'])
        if not isinstance(required, list) or any(role not in LABELS for role in required):
            raise ValueError('required_files must list supported roles')
        if not set(required) <= set(assets):
            raise ValueError('Final variant is missing required publication files')
        checked, info = {}, None
        for role, value in assets.items():
            p = local_file(root, value)
            copy = p.read_text(encoding='utf-8-sig') if role in {'copy', 'subtitles'} else None
            checked[role] = (quote(value, safe='/'), p, copy)
            records.append({'platform': platform, 'role': role, 'path': value,
                            'bytes': p.stat().st_size, 'sha256': digest(p),
                            'identity': {'mtime_ns': str(p.stat().st_mtime_ns), 'inode': str(p.stat().st_ino), 'device': str(p.stat().st_dev)}})
            if role == 'video':
                probe = subprocess.run(['ffprobe', '-v', 'error', '-show_streams',
                                        '-of', 'json', str(p)], check=True,
                                       capture_output=True, text=True)
                streams = json.loads(probe.stdout)['streams']
                video = next((s for s in streams if s['codec_type'] == 'video'), None)
                if video is None:
                    raise ValueError('No video stream')
                width, height = video['width'], video['height']
                # SAR matters: encoded pixels alone can hide an anamorphic mismatch.
                sar = video.get('sample_aspect_ratio', '1:1')
                sn, sd = (1, 1) if sar in {'N/A', '0:1'} else map(int, sar.split(':'))
                ratio = width * sn / (height * sd)
                expected = 9 / 16 if platform == 'tiktok' else 16 / 9
                if abs(ratio / expected - 1) > .02:
                    raise ValueError('Video does not match platform aspect: ' + platform)
                subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(p),
                                '-f', 'null', '-'], check=True, capture_output=True)
                info = f'{width} × {height}'
        name = PLATFORMS[platform]
        aspect = 'portrait' if platform == 'tiktok' else 'landscape'
        for role in ['video', 'cover', 'subtitles']:
            if role not in checked:
                continue
            url, file, _ = checked[role]
            label = ('YouTube video' if platform == 'youtube' else 'TikTok video' if platform == 'tiktok' else 'Lesson video') if role == 'video' else ('YouTube cover' if platform == 'youtube' else 'TikTok cover' if platform == 'tiktok' else 'Lesson cover') if role == 'cover' else 'Subtitles'
            download_buttons.append(f'<a class="download {"primary" if role == "video" else ""}" href="{escape(url)}" download>Download {label} · {size_label(file.stat().st_size)}</a>')
        fields = publication_fields(platform, variant.get('publication'),
                                    checked.get('copy', (None, None, ''))[2])
        copy_block = ''.join(copy_section(f'copy-{platform}-{i}', label, value)
                             for i, (label, value) in enumerate(fields))
        sections.append(f'''<section class="preview-card {platform}-preview" id="{platform}">
<h2>{name}</h2><div class="stage"><video class="{aspect}" aria-label="{name} preview" controls playsinline preload="metadata" src="{escape(checked["video"][0])}"></video></div></section>''')
        if copy_block:
            publication.append(f'<section class="publication publication-{platform}" id="{platform}-copy"><h2>{name} copy</h2>{copy_block}</section>')
    extra_downloads, extra_text = [], []
    extras = data.get('extras', [])
    if not isinstance(extras, list):
        raise ValueError('extras must be a list')
    for extra in extras:
        if not isinstance(extra, dict) or not isinstance(extra.get('label'), str) or not extra['label'].strip():
            raise ValueError('Each extra needs a label and relative path')
        value = extra.get('path')
        p = local_file(root, value)
        records.append({'platform': 'common', 'role': 'extra', 'path': value,
                        'bytes': p.stat().st_size, 'sha256': digest(p),
                            'identity': {'mtime_ns': str(p.stat().st_mtime_ns), 'inode': str(p.stat().st_ino), 'device': str(p.stat().st_dev)}})
        if p.suffix.lower() in {'.txt', '.md'}:
            text = p.read_text(encoding='utf-8-sig')
            extra_text.append(copy_section(f'copy-extra-{len(extra_text)}', extra['label'], text))
        else:
            extra_downloads.append(f'<a class="download" href="{escape(quote(value, safe="/"))}" download>{escape(extra["label"])} · {size_label(p.stat().st_size)}</a>')
    mode = 'dual' if 'tiktok' in seen and ('youtube' in seen or 'course' in seen) else 'single-portrait' if 'tiktok' in seen else 'single-landscape'
    buttons = ''.join(download_buttons + extra_downloads)
    media = f'<section class="media-grid {mode}" id="downloads">' + ''.join(sections) + f'<section class="download-card" id="download-links"><h2>Downloads</h2><div class="files">{buttons}</div></section></section>'
    texts = f'<section class="publication-grid {mode}" id="publication-texts">' + ''.join(publication) + '</section>' if publication else ''
    if extra_text:
        texts += '<section class="extra-text">' + ''.join(extra_text) + '</section>'
    nav = ''.join(f'<a href="#{p}">{PLATFORMS[p]}</a>' for p in PLATFORMS if p in seen)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(data["title"])} · Framewright</title><style>{CSS}</style></head>
<body><header><span class="wordmark"><span class="brand-dot" aria-hidden="true"></span>FRAMEWRIGHT</span><nav aria-label="Formats">{nav}</nav></header>
<main><div class="intro"><p class="status">{STATES[data["state"]]} · {escape(data["revision"])}</p><h1>{escape(data["title"])}</h1><p>{escape(data["note"])}</p></div>{media}{texts}</main>
<footer>Framewright Studio · Files are available while this local page is running.</footer><script>{JS}</script></body></html>'''
    receipt = {'schema_version': 1, 'template_version': VERSION,
               'template_sha256': digest(Path(__file__)), 'manifest_sha256': digest(manifest),
               'state': data['state'], 'files': records,
               'page_sha256': hashlib.sha256(page.encode('utf-8')).hexdigest(),
               'file_checks': 'present_nonempty_hashed;video_aspect_and_full_decode;utf8_text',
               'browser_check': 'pending', 'owner_approval': 'not_inferred'}
    # Finish all validation before replacing any generated delivery output.
    for filename, content in [('review.html', page), ('delivery-receipt.json', json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')]:
        target = root / filename
        if target.is_symlink():
            raise ValueError('Refuse symlink output: ' + filename)
        temp = root / ('.' + filename + '.tmp')
        # Exclusive creation avoids following a pre-existing temporary symlink.
        with temp.open('x', encoding='utf-8') as f:
            f.write(content)
        os.replace(temp, target)
    return receipt

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    try:
        receipt = build(args.manifest)
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as e:
        parser.exit(1, f'Delivery build failed: {e}\n')
    print(f'Built {args.manifest.parent / "review.html"}; checked {len(receipt["files"])} files')

if __name__ == '__main__':
    main()
