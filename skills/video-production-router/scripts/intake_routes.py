"""Offline comparison of bounded picture/voice/finishing recipes."""
import json

RECIPES=[
    ('local-authored','Locally authored motion','hyperframes',
     'Author layout, camera-like movement and graphics from supplied materials.',
     'Authoring work required; not photorealistic generative motion.'),
    ('local-montage','Local supplied-media montage','ffmpeg',
     'Arrange supplied clips or stills, then mix voice and finish.',
     'Requires suitable source media; motion from stills is limited.'),
    ('quota-generation','Quota-generated picture','pixverse',
     'Generate selected shots, then edit locally.',
     'Retries, continuity, export and actual operation affordability require a bounded trial.'),
    ('conditional-authoring','Conditional-licence authoring','remotion',
     'Author frame-driven scenes, then mix voice and finish.',
     'Confirm Free/Company eligibility and selected paid features; no price inferred.')]


def compare(p,brief,recommend):
    picture=recommend(p,brief,'video')
    finishing=recommend(p,brief,'editing')
    narration=brief.get('narration',True)
    if type(narration) is not bool:raise ValueError('narration must be boolean')
    visual_source=brief.get('visual_source','unknown')
    if visual_source not in {'supplied','generate','unknown'}:raise ValueError('visual_source must be supplied, generate or unknown')
    voices=recommend(p,brief,'narration')['candidates'] if narration and brief.get('language') else []
    preferred=brief.get('preferred_voice')
    if preferred is not None and (not isinstance(preferred,str) or not preferred.strip()):raise ValueError('preferred_voice must be a tool ID')
    if preferred:voices=[v for v in voices if v['id']==preferred]
    voice=next((v for v in voices if v['task_capabilities'].get('narration') in {'tested','documented'}),None)
    pictures={c['id']:c for c in picture['candidates']}
    finishers={c['id']:c for c in finishing['candidates']}
    questions=list(picture['questions'])
    if visual_source=='unknown':questions.append('visual_source')
    routes=[];omitted=[]
    for identity,label,tool,method,tradeoff in RECIPES:
        if tool not in pictures:
            omitted.append({'id':identity,'reason':'Picture tool excluded by policy or not indexed for task'});continue
        pic=pictures[tool];fin=finishers.get('ffmpeg');stages=[];unknowns=[];gaps=[]
        def stage(role,candidate,features):
            caps=(candidate or {}).get('task_capabilities',{})
            coverage={f:caps.get(f,'unknown') for f in features}
            item={'role':role,'tool':candidate['id'] if candidate else None,
                  'required_capabilities':coverage,'candidate':candidate}
            stages.append(item)
            if candidate is None:gaps.append(role+': no compatible candidate')
            elif any(v not in {'tested','documented'} for v in coverage.values()):
                gaps.append(role+': required capability needs a trial')
            return item
        stage('picture',pic,['video-export'])
        if narration:stage('narration',voice,['narration'])
        stage('finishing',fin,['media-mux','concat'])
        if visual_source=='generate' and tool!='pixverse':
            gaps.append('Source generation is not covered by this supplied-media recipe')
        if visual_source=='unknown':unknowns.append('Which source media exist and which need generation')
        if brief.get('source_rights') in (None,'','unknown'):unknowns.append('Source-media rights')
        if narration and voice is None:unknowns.append('Voice choice and language coverage; explicit preferences are never substituted')
        if narration and voice and voice['task_capabilities'].get('narration')!='tested':unknowns.append('Narration language requires a scoped test')
        selected=[s['candidate'] for s in stages if s['candidate']]
        cost_kinds={s['cost_kind'] for s in selected}
        local=bool(selected) and len(selected)==len(stages) and cost_kinds=={'free_local'}
        if 'free_quota' in cost_kinds:
            unknowns+=['Current plan terms and account balance','Credits per selected operation, retries and reset; calendar estimate unavailable']
        if any(c.get('account_declaration')=='unavailable' for c in selected):gaps.append('Selected provider is declared unavailable')
        if 'unknown' in cost_kinds:unknowns.append('Licence eligibility and provider fee quote')
        unknowns+=['Installed runtime, hardware fit and available disk','Asset/output rights and required attribution or disclosure',
                   'Cross-tool timing, formats and final human viewing/listening']
        routes.append({'id':identity,'label':label,'method':method,'tradeoff':tradeoff,'stages':stages,
                       'coverage':'gaps_require_resolution' if gaps else 'documented_components_only',
                       'gaps':gaps,'unknown_conditions':unknowns,
                       'cost':{'provider_fee':0 if local else None,'currency':'USD','total_project_cost':None,
                               'basis':'Local software provider fees only; labour, hardware, assets and optional services excluded' if local else 'No verified quote or affordable quota operation'},
                       'time_estimate':None,'qualification':'planning_only_requires_integration_check',
                       'execution':'not_authorized'})
    return {'schema':'framewright-intake-route-comparison-v1','questions':questions,
            'brief':{'idea':brief['idea'],'duration_seconds':brief.get('duration_seconds'),'format':brief.get('format'),
                     'language':brief.get('language'),'narration':narration,'visual_source':visual_source},
            'routes':routes,'omitted_routes':omitted,'selection_policy':p['options'],
            'execution':'not_authorized','network_calls':0,
            'scope':'Bounded recipes for picture, optional narration and finishing. No music, subtitles, delivery kit or complete creative production inferred.'}


def markdown(result):
    lines=['# Production route comparison','',result['scope'],'',
           '| Route | Picture / voice / finishing | Provider fee | Coverage | Main tradeoff |',
           '|---|---|---|---|---|']
    def cell(v):return str(v).replace('|','/').replace('\n',' ')
    for r in result['routes']:
        chain=' / '.join(s['tool'] or 'UNRESOLVED' for s in r['stages'])
        fee='0 USD local software fees; total unknown' if r['cost']['provider_fee']==0 else 'Unknown / check quota or eligibility'
        lines.append('| '+' | '.join(map(cell,[r['label'],chain,fee,r['coverage'],r['tradeoff']]))+' |')
    for r in result['routes']:
        lines+=['','## '+r['label'],'',r['method'],'']
        for s in r['stages']:lines.append('- '+cell(s['role'])+': '+cell(s['tool'] or 'unresolved')+'; '+cell(json.dumps(s['required_capabilities'],sort_keys=True)))
        lines+=['','Unresolved:']+['- '+cell(x) for x in r['gaps']+r['unknown_conditions']]
    lines+=['','Questions: '+(', '.join(result['questions']) or 'None'),
            '', 'Time and total cost remain unknown. Tool selection and execution need a separate decision.','']
    return '\n'.join(lines)
