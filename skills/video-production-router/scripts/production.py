"""Local scene/cut/catalogue and delivery bookkeeping; never renders or publishes."""
import copy
import hashlib
import json
import math
from pathlib import Path
import shutil
import tempfile

ROLES = {'video':'video', 'thumbnail':'image', 'subtitles':'text', 'title':'text', 'description':'text'}
EXTENSIONS = {'video':{'.mp4','.mov','.webm'},'thumbnail':{'.png','.jpg','.jpeg','.webp'},
              'subtitles':{'.srt','.vtt'},'title':{'.txt'},'description':{'.txt'}}
CHECKS = {'video':{'technical':'pass','listening':'accepted','creative':'accepted'},
          'thumbnail':{'technical':'pass','creative':'accepted'}, 'subtitles':{'technical':'pass'},
          'title':{'creative':'accepted'}, 'description':{'creative':'accepted'}}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def shape(value, required, optional=(), label='record'):
    if not isinstance(value,dict) or set(required)-value.keys() or value.keys()-set(required)-set(optional):
        raise ValueError(label+': missing or unsupported fields')


def text(value, empty=False):
    if not isinstance(value,str) or (not empty and not value.strip()):raise ValueError('Expected text')


def strings(value):
    if not isinstance(value,list) or any(not isinstance(x,str) or not x.strip() for x in value):
        raise ValueError('Expected a list of nonempty strings')


def number(value, zero=False):
    if type(value) not in {int,float} or not math.isfinite(value) or value < 0 or (not zero and value==0):
        raise ValueError('Expected a finite positive number' if not zero else 'Expected finite nonnegative time')


def index(rows, label):
    if not isinstance(rows,list):raise ValueError(label+': expected a list')
    result={}
    for row in rows:
        if not isinstance(row,dict):raise ValueError(label+': expected objects')
        text(row.get('id'))
        if row['id'] in result:raise ValueError(label+': duplicate ID '+row['id'])
        result[row['id']]=row
    return result


def subject_pin(data, subject):
    if subject is None:return None
    text(subject)
    kind,sep,identity=subject.partition(':')
    if sep and kind=='input' and identity in data['inputs']:return copy.deepcopy(data['inputs'][identity])
    if sep and kind=='output' and identity in data['artifacts']:return copy.deepcopy(data['artifacts'][identity]['file'])
    raise ValueError('Unknown material subject: '+subject)


def validate_spec(spec, data):
    shape(spec, ['schema_version','materials','scenes','variants'],label='production')
    if type(spec['schema_version']) is not int or spec['schema_version']!=1:raise ValueError('Unsupported production format')
    materials=index(spec['materials'],'materials');scenes=index(spec['scenes'],'scenes');variants=index(spec['variants'],'variants')
    def ref(identity, allow_none=False):
        if identity is None and allow_none:return
        if not isinstance(identity,str) or identity not in materials:raise ValueError('Unknown material ID')
    def narration(row):
        shape(row,['text','material'],label='narration');text(row['text'],empty=True);ref(row['material'],True)
        if row['material'] is not None and materials[row['material']]['kind']!='audio':raise ValueError('Narration needs an audio material')
    for row in materials.values():
        shape(row,['id','kind','subject','origin','rights'],['tags','duration_seconds','derived_from','capture_mode','disclosure'],'material')
        if row['kind'] not in {'video','audio','image','text','project'}:raise ValueError('Unknown material kind')
        text(row['origin']);subject_pin(data,row['subject'])
        if 'duration_seconds' in row:number(row['duration_seconds'])
        strings(row.get('tags',[]));strings(row.get('derived_from',[]))
        for parent in row.get('derived_from',[]):ref(parent)
        if row.get('capture_mode','not_applicable') not in {'not_applicable','human_gameplay','scripted_gameplay','screen_capture','authored','generated'}:
            raise ValueError('Unknown capture mode')
        if 'disclosure' in row:text(row['disclosure'],empty=True)
        rights=row['rights'];shape(rights,['status','basis','uses','attribution','restrictions'],label='rights')
        if rights['status'] not in {'unknown','owner_authorized','licensed','restricted'}:raise ValueError('Unknown rights status')
        text(rights['basis'],empty=rights['status']=='unknown');text(rights['attribution'],empty=True)
        strings(rights['uses']);strings(rights['restrictions'])
        if set(rights['uses'])-{'main','short','other','cover','copy'}:raise ValueError('Unknown intended use')
    visiting=set();done=set()
    def walk(identity):
        if identity in visiting:raise ValueError('Material derivation cycle')
        if identity in done:return
        visiting.add(identity)
        for parent in materials[identity].get('derived_from',[]):walk(parent)
        visiting.remove(identity);done.add(identity)
    for identity in materials:walk(identity)
    for row in scenes.values():
        shape(row,['id','tell','show','materials','narration','missing'],['claims'],'scene')
        text(row['tell'],empty=True);text(row['show'],empty=True);strings(row['materials']);strings(row['missing'])
        for identity in row['materials']:ref(identity)
        narration(row['narration'])
        if not isinstance(row.get('claims',[]),list):raise ValueError('Claims must be a list')
        for claim in row.get('claims',[]):
            shape(claim,['text','material'],label='claim');text(claim['text']);ref(claim['material'],True)
    for row in variants.values():
        shape(row,['id','kind','canvas','edits','music','tasks','delivery'],label='variant')
        if row['kind'] not in {'main','short','other'}:raise ValueError('Unknown variant kind')
        shape(row['canvas'],['width','height','fps'],label='canvas')
        for value in row['canvas'].values():
            if type(value) is not int or value<=0:raise ValueError('Canvas values must be positive integers')
        if not isinstance(row['edits'],list) or not row['edits']:raise ValueError('Variant needs at least one edit')
        strings(row['tasks'])
        if set(row['tasks'])-{s['id'] for s in data['steps']}:raise ValueError('Unknown variant task ID')
        ref(row['music'],True)
        if row['music'] is not None and materials[row['music']]['kind']!='audio':raise ValueError('Music needs an audio material')
        shape(row['delivery'],list(ROLES),label='delivery')
        for role,identity in row['delivery'].items():
            ref(identity,True)
            if identity is not None and materials[identity]['kind']!=ROLES[role]:raise ValueError('Wrong material kind for delivery role '+role)
        for edit in row['edits']:
            shape(edit,['scene','material','duration_seconds','framing'],['source_in','source_out','narration'],'edit')
            if edit['scene'] not in scenes:raise ValueError('Unknown scene ID')
            ref(edit['material'],True);number(edit['duration_seconds']);text(edit['framing'])
            if edit['material'] is not None and materials[edit['material']]['kind'] not in {'video','image'}:raise ValueError('Picture edit requires video/image')
            if ('source_in' in edit)!=('source_out' in edit):raise ValueError('Provide both source range bounds')
            if 'source_in' in edit:
                number(edit['source_in'],True);number(edit['source_out'])
                if edit['source_out']<=edit['source_in']:raise ValueError('Empty/reversed source range')
                if abs(edit['source_out']-edit['source_in']-edit['duration_seconds'])>1e-6:raise ValueError('Only normal-speed source ranges are supported')
                if edit['material'] is None or materials[edit['material']]['kind']!='video':raise ValueError('Source range requires a video material')
                duration=materials[edit['material']].get('duration_seconds')
                if duration is not None and edit['source_out']>duration:raise ValueError('Source range exceeds declared duration')
            if 'narration' in edit:narration(edit['narration'])
    return materials,scenes,variants


def compile_project(data,spec):
    validate_spec(spec,data)
    result=copy.deepcopy(spec)
    for row in result['materials']:row['_pin']=subject_pin(data,row['subject'])
    return result


def validate_stored(data):
    if 'production' not in data:return
    if data.get('production_sha256')!=digest(data['production']):raise ValueError('Production composition integrity mismatch')
    spec=copy.deepcopy(data['production'])
    for row in spec['materials']:row.pop('_pin')
    validate_spec(spec,data)


def nonempty_utf8(path):
    has_text=False
    with path.open(encoding='utf-8') as stream:
        for line in stream:has_text=bool(line.strip()) or has_text
    return has_text


def report(data,problems,observations,root):
    if 'production' not in data:return None
    stored=data['production'];materials=index(stored['materials'],'materials');scenes=index(stored['scenes'],'scenes')
    material_view={}
    for identity,row in materials.items():
        subject=row['subject'];pin=subject_pin(data,subject);issues=[]
        if pin is None:issues.append('material not retained')
        elif pin!=row['_pin']:issues.append('retained revision changed; recompose explicitly')
        if subject in problems:issues.append(problems[subject])
        material_view[identity]={**{k:v for k,v in row.items() if k!='_pin'},'available':not issues,'problems':issues,
                                 'retained_sha256':row['_pin']['sha256'] if row['_pin'] else None,
                                 'observations':[{k:r[k] for k in ['id','kind','result','actor','provenance','note']} for r in observations['effective'] if r['subject']==subject]}
    latest={(r['subject'],r['kind'],r['topic']):r['id'] for r in data.get('journal',[])}
    latest_stale=[r for r in observations['stale'] if r['id']==latest[(r['subject'],r['kind'],r['topic'])]]
    variants={}
    for variant in stored['variants']:
        issues=[];used={};edits=[];clock=0
        def use(identity,purpose):
            if identity is None:return
            if purpose in used.setdefault(identity,set()):return
            used[identity].add(purpose)
            for parent in materials[identity].get('derived_from',[]):use(parent,purpose)
        for edit in variant['edits']:
            scene=scenes[edit['scene']];scope='scene '+scene['id'];narr=edit.get('narration',scene['narration'])
            if not scene['tell'].strip():issues.append(scope+': missing script point')
            if not scene['show'].strip():issues.append(scope+': missing visual plan')
            issues.extend(scope+': '+need for need in scene['missing'])
            for identity in scene['materials']:use(identity,variant['kind'])
            for claim in scene.get('claims',[]):
                if claim['material'] is None:issues.append(scope+': claim lacks a demonstration/source reference: '+claim['text'])
                use(claim['material'],variant['kind'])
            use(edit['material'],variant['kind']);use(narr['material'],variant['kind'])
            if edit['material'] is None:issues.append(scope+': picture take missing')
            else:
                material=materials[edit['material']]
                if material['kind']=='video' and ('source_in' not in edit or 'duration_seconds' not in material):
                    issues.append(scope+': bounded source range/duration missing')
                if material.get('capture_mode')=='scripted_gameplay' and not material.get('disclosure','').strip():
                    issues.append(scope+': scripted gameplay disclosure missing')
            if narr['text'].strip() and narr['material'] is None:issues.append(scope+': narration recording missing')
            edits.append({**edit,'timeline_in':clock,'timeline_out':clock+edit['duration_seconds'],'narration':narr})
            clock+=edit['duration_seconds']
        use(variant['music'],variant['kind'])
        slots={}
        for role,identity in variant['delivery'].items():
            slot={'material':identity,'required_checks':CHECKS[role],'problems':[]}
            if identity is None:slot['problems'].append('delivery material missing')
            else:
                row=materials[identity];use(identity,variant['kind'] if role=='video' else 'cover' if role=='thumbnail' else 'copy')
                slot['problems'].extend(material_view[identity]['problems'])
                for kind,expected in CHECKS[role].items():
                    receipts=[r for r in observations['effective'] if r['subject']==row['subject'] and r['kind']==kind]
                    if not receipts or any(r['result']!=expected for r in receipts) or any(r['subject']==row['subject'] and r['kind']==kind for r in latest_stale):
                        slot['problems'].append(kind+': no current '+expected+' receipt')
                if row['_pin'] and row['_pin']['bytes']<=0:slot['problems'].append('empty delivery file')
                if row['_pin'] and Path(row['_pin']['path']).suffix.lower() not in EXTENSIONS[role]:
                    slot['problems'].append('unsupported filename extension for delivery role')
                if role in {'subtitles','title','description'} and row['_pin'] and not material_view[identity]['problems']:
                    try:
                        if not nonempty_utf8(root/row['_pin']['path']):
                            slot['problems'].append('empty delivery text')
                    except (OSError, UnicodeError):
                        slot['problems'].append('delivery text is not readable UTF-8')
                if role=='video' and row.get('duration_seconds') is not None and abs(row['duration_seconds']-clock)>1/variant['canvas']['fps']:
                    slot['problems'].append('declared final duration differs from cut')
            issues.extend(role+': '+p for p in slot['problems']);slots[role]=slot
        for identity,purposes in used.items():
            row=materials[identity];rights=row['rights']
            issues.extend('material '+identity+': '+p for p in material_view[identity]['problems'])
            if rights['status'] not in {'owner_authorized','licensed'}:issues.append('material '+identity+': rights unresolved or restricted')
            if not purposes.issubset(rights['uses']):issues.append('material '+identity+': intended uses not authorised in retained rights note')
            if rights['restrictions']:issues.append('material '+identity+': restrictions require resolution in rights note')
            for receipt in observations['effective']+latest_stale:
                if receipt['subject']==row['subject'] and receipt['kind'] in {'technical','listening','creative'} and (
                        receipt['stale_reasons'] or receipt['result'] in {'fail','rejected','pending'}):
                    issues.append('material '+identity+': unresolved '+receipt['kind']+' receipt '+receipt['id'])
        steps={s['id']:s for s in data['steps']}
        for identity in variant['tasks']:
            if steps[identity]['state']!='done':issues.append('task '+identity+': '+steps[identity]['state'])
        variants[variant['id']]={'kind':variant['kind'],'canvas':variant['canvas'],'edits':edits,
            'duration_seconds':clock,'used_materials':{k:sorted(v) for k,v in used.items()},'delivery':slots,
            'blockers':list(dict.fromkeys(issues)),'complete_local_handoff':not issues,'publication_authorized':False}
    return {'materials':material_view,'scenes':scenes,'variants':variants,'publication_authorized':False,
            'open_tasks':[{ 'id':s['id'],'state':s['state'],'label':s['label'],'reason':s['evidence']} for s in data['steps'] if s['state']!='done'],
            'note':'Local declared plan and manually attributed checks only. No semantic fact-check, media decode, rights verification or publishing performed.'}


def markdown(view,cell):
    lines=['# Production board','','Local plan and recorded checks; no execution/publication authority.','',
           '| Scene | Tell | Show | Materials | Narration | Still needed |','| --- | --- | --- | --- | --- | --- |']
    for row in view['scenes'].values():
        lines.append('| '+' | '.join(cell(x) for x in [row['id'],row['tell'],row['show'],', '.join(row['materials']),row['narration']['text'],'; '.join(row['missing'])])+' |')
    for identity,row in view['variants'].items():
        lines+=['','## '+cell(identity),'',cell(str(row['canvas']))+'; '+cell(row['duration_seconds'])+'s. Local handoff complete: '+cell(row['complete_local_handoff'])+'.','']
        lines.extend('- '+cell(f"{e['timeline_in']}–{e['timeline_out']}: {e['scene']}; {e['material']}; source {e.get('source_in','n/a')}–{e.get('source_out','n/a')}; {e['framing']}; narration: {e['narration']['text']} [{e['narration']['material']}]") for e in row['edits'])
        lines+=['','Remaining checks:']
        lines.extend('- '+cell(p) for p in row['blockers'])
        if not row['blockers']:lines.append('- None recorded; manual attestations remain scoped, publication is separate.')
    lines+=['','## Catalogue','']
    for identity,row in view['materials'].items():
        lines+=['- '+cell(identity)+': '+cell(row['kind'])+'; '+cell(row['origin'])+'; rights: '+cell(row['rights']['status'])+'; uses: '+cell(', '.join(row['rights']['uses']))+'; basis: '+cell(row['rights']['basis'])+'; attribution: '+cell(row['rights']['attribution'])+'; checks: '+cell(', '.join(r['kind']+':'+r['result'] for r in row['observations']))+'.']
    lines+=['','## Other recorded project work','','Only tasks explicitly attached to a variant block that variant; all remaining project work is disclosed here.']
    lines.extend('- '+cell(f"{s['id']}: {s['state']}; {s['label']}; {s['reason']}") for s in view['open_tasks'])
    return '\n'.join(lines)+'\n'


def variant_bases(production):
    """Hash media/cut conformance independently of catalogue administration."""
    materials=index(production['materials'],'materials');scenes=index(production['scenes'],'scenes');result={}
    for variant in production['variants']:
        used=set();selected={}
        def use(identity):
            if identity is None or identity in used:return
            used.add(identity)
            for parent in materials[identity].get('derived_from',[]):use(parent)
        use(variant['music'])
        use(variant['delivery']['video'])
        for edit in variant['edits']:
            scene=scenes[edit['scene']];selected[scene['id']]=scene
            for identity in scene['materials']:use(identity)
            for claim in scene.get('claims',[]):use(claim['material'])
            use(edit['material']);use(edit.get('narration',scene['narration'])['material'])
        video_variant={k:v for k,v in variant.items() if k not in {'tasks','delivery'}}
        video_variant['delivery']={'video':variant['delivery']['video']}
        result[variant['id']]=digest({'variant':video_variant,'scenes':selected,
                                     'materials':{k:{field:value for field,value in materials[k].items()
                                         if field in {'kind','subject','_pin','duration_seconds','capture_mode','disclosure'}}
                                                  for k in sorted(used)}})
    return result


def build_bundle(data,view,variant_id,root,output,project_sha256,cell,draft=False):
    if variant_id not in view['variants']:raise ValueError('Unknown delivery variant')
    variant=view['variants'][variant_id]
    if not variant['complete_local_handoff'] and not draft:
        raise ValueError('Unresolved delivery checks; inspect board or explicitly export --draft')
    if output.exists() or output.is_symlink():raise ValueError('Bundle destination exists; refusing to overwrite')
    output=output.resolve()
    if not output.parent.is_dir():raise ValueError('Create the bundle parent directory explicitly')
    materials=index(data['production']['materials'],'materials')
    stage=Path(tempfile.mkdtemp(prefix='.framewright-kit-',dir=output.parent))
    try:
        files={}
        for role,slot in variant['delivery'].items():
            identity=slot['material']
            if identity is None or not view['materials'][identity]['available']:continue
            pin=materials[identity]['_pin'];source=root/pin['path'];suffix=source.suffix.lower()
            if suffix not in EXTENSIONS[role]:continue
            name=role+suffix;target=stage/name
            shutil.copyfile(source,target)
            h=hashlib.sha256()
            with target.open('rb') as stream:
                for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
            if target.stat().st_size!=pin['bytes'] or h.hexdigest()!=pin['sha256']:
                raise ValueError('Source changed during bundle copy: '+role)
            if role in {'subtitles','title','description'}:
                if not nonempty_utf8(target):raise ValueError('Empty delivery text: '+role)
            files[role]={'name':name,'bytes':pin['bytes'],'sha256':pin['sha256'],
                         'material':identity,'subject':materials[identity]['subject']}
        # The manifest is the last completion marker; an interrupted export cannot claim completion.
        manifest={'schema_version':1,'variant':variant_id,'project_sha256':project_sha256,
                  'production_sha256':data['production_sha256'],'complete_local_handoff':variant['complete_local_handoff'],
                  'publication_authorized':False,'files':files,'report':view,
                  'verification':'Copied hashes checked; QA/rights are scoped manual records, no media decoder or uploader run.'}
        (stage/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=True,indent=2)+'\n')
        report_view={**view,'variants':{variant_id:variant}}
        (stage/'CHECKS.md').write_text(markdown(report_view,cell),encoding='utf-8')
        output.mkdir(mode=0o700)  # Exclusive creation, including when another process created the target meanwhile.
        for source in sorted(stage.iterdir(),key=lambda p:p.name=='manifest.json'):
            source.rename(output/source.name)
        return {'output':str(output),'complete_local_handoff':manifest['complete_local_handoff'],
                'publication_authorized':False,'files':files}
    finally:
        shutil.rmtree(stage)
