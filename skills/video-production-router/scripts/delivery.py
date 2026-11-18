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

VERSION = '2'
STATES = {'pilot': 'Проба', 'review': 'На просмотр', 'final': 'Финальный пакет',
          'rejected': 'Отклонённая проба'}
LABELS = {'video': 'Скачать видео', 'cover': 'Скачать обложку',
          'subtitles': 'Скачать субтитры', 'copy': 'Скачать тексты'}
CSS = """
:root{color-scheme:dark;--ink:#101d24;--paper:#f6efdb;--amber:#e7ba6a;--muted:#aec0c6}
*{box-sizing:border-box}body{margin:0;background:var(--ink);color:var(--paper);font:17px/1.6 system-ui,sans-serif}
header,main,footer{max-width:1200px;margin:auto;padding:24px}
header{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #39505b}
.wordmark{font:28px Georgia,serif;letter-spacing:-1px}nav{display:flex;gap:22px}
a{color:var(--paper);text-underline-offset:5px}a:hover{color:var(--amber)}
h1{font:clamp(36px,6vw,64px)/1.1 Georgia,serif;margin:20px 0}
h2{font-size:26px;margin:0}h3{font-size:17px;margin:24px 0 8px}
.status{color:var(--amber)}.intro{max-width:780px}.muted,footer{color:var(--muted)}
.variant{margin-top:48px;padding-top:22px;border-top:1px solid #39505b;scroll-margin-top:20px}
.variant-head{display:flex;gap:20px;align-items:baseline;justify-content:space-between}
.layout{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(260px,1fr);gap:30px;margin-top:18px}
.stage{background:#080e12;border:1px solid #344953;display:flex;align-items:center;justify-content:center;min-width:0}
video{display:block;width:100%;max-height:70vh;object-fit:contain}
.tiktok-layout{grid-template-columns:minmax(0,360px) minmax(260px,1fr);align-items:start}
.tiktok-layout .stage{width:100%;aspect-ratio:9/16;align-self:start}
.portrait{aspect-ratio:9/16;width:100%;height:100%;max-height:none;margin:0}
button[data-copied=true]{background:#173f36;border-color:#86d3b2;color:#ccf4df}
.copy-head{flex-wrap:wrap}.copy-head h3{margin:0}.copy-head button{margin-left:auto}.copy-status{flex-basis:100%}.copy-status:empty{display:none}.copy-status{color:#ccf4df;font-size:14px}
@media(max-width:760px){.layout.tiktok-layout{grid-template-columns:1fr}.tiktok-layout .stage{max-width:360px;justify-self:center}.tiktok-layout video{max-height:none}}
.landscape{aspect-ratio:16/9}
.files{display:flex;gap:10px;flex-direction:column}.download,button{font:inherit;border:1px solid #53646b;background:transparent;color:var(--paper);padding:10px 15px;text-decoration:none;border-radius:4px;text-align:left}
.download.primary{background:var(--amber);color:#101d24;border-color:var(--amber);font-weight:650}
button{cursor:pointer;padding:6px 12px;font-size:14px}button:hover{border-color:var(--amber)}
:focus-visible{outline:3px solid #80d3c2;outline-offset:4px}
.cover{display:block;max-width:100%;max-height:210px;object-fit:contain;margin:20px 0}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font:15px/1.65 system-ui,sans-serif;margin:12px 0 0}
.copy{margin-top:24px;padding:22px;background:#192b34;border:1px solid #39505b;border-radius:4px}
.copy-head{display:flex;align-items:center;justify-content:space-between;gap:12px}
.media-error{color:#ffb2a6;padding:12px;border:1px solid #bb766d}footer{font-size:14px;border-top:1px solid #39505b;margin-top:50px}
@media(max-width:760px){header,main,footer{padding:18px}.layout{grid-template-columns:1fr}.variant-head{display:block}nav{gap:14px;font-size:14px}video{max-height:65vh}.copy{padding:16px}}
"""
JS = """
document.querySelectorAll('video').forEach(v=>{
 v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()}));
 v.addEventListener('error',()=>{const p=document.createElement('p');p.className='media-error';
 p.textContent='Видео не загрузилось. Попробуйте прямое скачивание.';v.after(p)},{once:true});
});
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{
 const text=document.getElementById(b.dataset.copy).textContent;
 try{await navigator.clipboard.writeText(text);b.textContent='✓ Скопировано';b.dataset.copied='true';b.parentElement.querySelector('.copy-status').textContent='В буфере обмена'}
 catch{const s=window.getSelection(),r=document.createRange();r.selectNodeContents(document.getElementById(b.dataset.copy));
 s.removeAllRanges();s.addRange(r);b.textContent='Текст выделен — скопируйте'}
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
    allowed = {'titles', 'description', 'tags'} if platform == 'youtube' else {'caption', 'first_comment'}
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
            data['description' if platform == 'youtube' else 'caption'] = legacy.strip()
    if platform == 'youtube':
        titles = data.get('titles', [])
        if not isinstance(titles, list) or len(titles) > 3 or any(not isinstance(t, str) for t in titles):
            raise ValueError('YouTube titles must be a list of at most three strings')
        fields = list(zip(['Основной заголовок', 'Заголовок 2', 'Заголовок 3'], titles))
        tags = data.get('tags', '')
        if isinstance(tags, list) and all(isinstance(t, str) for t in tags):
            tags = ', '.join(tags)
        fields += [('Описание', data.get('description', '')), ('Теги', tags)]
    else:
        fields = [('Кэпшн', data.get('caption', '')), ('Первый комментарий', data.get('first_comment', ''))]
    if any(not isinstance(value, str) for _, value in fields):
        raise ValueError('Publication fields must contain text')
    return [(label, value.strip()) for label, value in fields if value.strip()]

def copy_section(identity, label, value):
    return (
        f'<section class="copy" data-field="{escape(label)}">'
        f'<div class="copy-head"><h3>{escape(label)}</h3>'
        f'<button type="button" data-copy="{identity}">Копировать</button>'
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
    seen, records, sections = set(), [], []
    for variant in variants:
        platform = variant.get('platform')
        if platform not in {'youtube', 'tiktok'} or platform in seen:
            raise ValueError('Each platform must be youtube or tiktok, once')
        seen.add(platform)
        assets = variant.get('files', {})
        if not isinstance(assets, dict) or 'video' not in assets or set(assets) - LABELS.keys():
            raise ValueError('Expected video and supported file roles')
        if platform == 'tiktok' and 'subtitles' in assets:
            raise ValueError('TikTok packages do not include subtitles')
        subtitles_required = variant.get('subtitles_required', platform == 'youtube')
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
                            'bytes': p.stat().st_size, 'sha256': digest(p)})
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
                expected = 16 / 9 if platform == 'youtube' else 9 / 16
                if abs(ratio / expected - 1) > .02:
                    raise ValueError('Video does not match platform aspect: ' + platform)
                subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(p),
                                '-f', 'null', '-'], check=True, capture_output=True)
                info = f'{width} × {height}'
        name = 'YouTube' if platform == 'youtube' else 'TikTok'
        aspect = 'landscape' if platform == 'youtube' else 'portrait'
        downloads = ''.join(
            f'<a class="download {"primary" if role == "video" else ""}" href="{escape(url)}" download>{LABELS[role]} · {size_label(p.stat().st_size)}</a>'
            for role, (url, p, _) in checked.items() if role != 'copy')
        cover = f'<img class="cover" src="{escape(checked["cover"][0])}" alt="Обложка {name}" loading="lazy">' if 'cover' in checked else ''
        fields = publication_fields(platform, variant.get('publication'),
                                    checked.get('copy', (None, None, ''))[2])
        copy_block = ''.join(copy_section(f'copy-{platform}-{i}', label, value)
                             for i, (label, value) in enumerate(fields))
        sections.append(f'''<section class="variant" id="{platform}">
<div class="variant-head"><h2>{name}</h2><span class="muted">{info} · {escape(data["revision"])}</span></div>
<div class="layout {platform}-layout"><div class="stage"><video class="{aspect}" controls playsinline preload="metadata" src="{escape(checked["video"][0])}"></video></div>
<div><div class="files">{downloads}</div>{cover}</div></div>{copy_block}</section>''')
    extra_html = []
    extras = data.get('extras', [])
    if not isinstance(extras, list):
        raise ValueError('extras must be a list')
    for extra in extras:
        if not isinstance(extra, dict) or not isinstance(extra.get('label'), str) or not extra['label'].strip():
            raise ValueError('Each extra needs a label and relative path')
        value = extra.get('path')
        p = local_file(root, value)
        records.append({'platform': 'common', 'role': 'extra', 'path': value,
                        'bytes': p.stat().st_size, 'sha256': digest(p)})
        if p.suffix.lower() in {'.txt', '.md'}:
            text = p.read_text(encoding='utf-8-sig')
            extra_html.append(copy_section(f'copy-extra-{len(extra_html)}', extra['label'], text))
        else:
            extra_html.append(f'<a class="download" href="{escape(quote(value, safe="/"))}" download>{escape(extra["label"])} · {size_label(p.stat().st_size)}</a>')
    additional = '<section class="variant"><h2>Дополнительные материалы</h2><div class="files">' + ''.join(extra_html) + '</div></section>' if extra_html else ''
    nav = ''.join(f'<a href="#{p}">{"YouTube" if p == "youtube" else "TikTok"}</a>'
                  for p in ('youtube', 'tiktok') if p in seen)
    page = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(data["title"])} · Framewright</title><style>{CSS}</style></head>
<body><header><span class="wordmark">Framewright</span><nav aria-label="Версии">{nav}</nav></header>
<main><div class="intro"><p class="status">{STATES[data["state"]]} · {escape(data["revision"])}</p><h1>{escape(data["title"])}</h1><p>{escape(data["note"])}</p></div>{''.join(sections)}{additional}</main>
<footer>Framewright Studio · Версия шаблона {VERSION}. Ссылки работают, пока запущен локальный сервер.</footer><script>{JS}</script></body></html>'''
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
