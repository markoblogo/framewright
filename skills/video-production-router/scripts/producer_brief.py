"""Read-only producer proposal joining existing intake routes and source evidence."""
from pathlib import Path
import hashlib
import json
import math
import runpy

BASE=Path(__file__).resolve().parent


def validate(brief):
    if not isinstance(brief,dict):raise ValueError('Brief must be an object')
    duration=brief.get('duration_seconds')
    if duration is not None and (type(duration) not in (int,float) or not math.isfinite(duration) or duration<=0):
        raise ValueError('duration_seconds must be a finite positive number')
    for key in ('idea','format','language','deadline','budget','source_rights','preferred_route'):
        if brief.get(key) is not None and (not isinstance(brief[key],str) or not brief[key].strip()):
            raise ValueError(key+' must be nonempty text when provided')
    constraints=brief.get('constraints',{})
    if not isinstance(constraints,dict) or set(constraints)-{'allow_uploads','allow_installation'}:
        raise ValueError('Supported constraints: allow_uploads, allow_installation')
    if any(type(v) is not bool for v in constraints.values()):raise ValueError('Constraints must be boolean')
    scenes=brief.get('scenes')
    if scenes is not None:
        if not isinstance(scenes,list) or not 1<=len(scenes)<=30:raise ValueError('Provide 1–30 scenes')
        seen=set()
        for row in scenes:
            if not isinstance(row,dict) or set(row)-{'id','purpose','query'} or not {'id','purpose'}<=set(row):
                raise ValueError('Scene requires id, purpose and optional material query')
            if any(not isinstance(v,str) or not v.strip() for v in row.values()):raise ValueError('Scene fields must be nonempty text')
            if row['id'] in seen:raise ValueError('Duplicate scene id')
            seen.add(row['id'])


def project_view(path):
    path=path.resolve();raw=path.read_bytes()
    project=runpy.run_path(str(BASE/'project.py'))
    data=project['load'](path);state=project['summary'](data,path.parent)
    module=runpy.run_path(str(BASE/'project_summary.py'))
    sha=hashlib.sha256(raw).hexdigest()
    files=module['project'](data,path.parent,state['file_problems'],project['JOURNAL'],sha)
    view=module['working_brief'](data,state,files)
    if raw!=path.read_bytes():raise ValueError('Project changed during proposal; retry')
    return dict(view,checkpoint_sha256=sha,files=files['files'])


def build(profile,brief,recommend,source_index=None,project=None):
    validate(brief)
    routing=runpy.run_path(str(BASE/'intake_routes.py'))
    comparison=routing['compare'](profile,brief,recommend)
    preferred=brief.get('preferred_route')
    if preferred and preferred not in {r[0] for r in routing['RECIPES']}:raise ValueError('Unknown preferred_route')
    supplied=brief.get('visual_source')=='supplied'
    constraints=brief.get('constraints',{})
    order=['local-montage','local-authored'] if supplied else ['quota-generation']
    if supplied and profile['options']=='both':order.append('conditional-authoring')
    if brief.get('visual_source','unknown')=='unknown' and not preferred:order=[]
    if preferred:order=[preferred]
    by_id={r['id']:r for r in comparison['routes']};routes=[];excluded=[]
    for identity in order:
        if identity not in by_id:
            excluded.append({'id':identity,'reason':'Excluded by policy or missing indexed capabilities'});continue
        row=by_id[identity]
        stages=[s['candidate'] for s in row['stages'] if s['candidate']]
        if any(s.get('account_declaration')=='unavailable' or profile['subscriptions'].get(s['id'])=='unavailable' for s in stages):
            excluded.append({'id':identity,'reason':'Provider declared unavailable'});continue
        if constraints.get('allow_uploads') is False and any(s['cost_kind']!='free_local' for s in stages):
            excluded.append({'id':identity,'reason':'No-upload constraint: this route has no confirmed local-only execution profile'});continue
        row=dict(row,selection_basis='explicit_preference' if preferred else 'proposed_from_declared_visual_source')
        row['human_work']='Review material relevance and rights, refine scene intent, author/edit the shot, and view/listen to the result.'
        row['fallback']='If prerequisites cannot be met, reduce the scene to supplied-media editing; a changed route needs a new explicit decision.' if identity!='local-montage' else 'If no suitable clip exists, propose a simpler still-based composition or request new material; do not invent a source.'
        row['pilot']='After selecting the route and clearing prerequisites, prepare one short representative shot for human review.'
        if constraints.get('allow_installation') is False:
            row['unknown_conditions']=row['unknown_conditions']+['Installation forbidden: verify all required runtimes are already present; do not install']
        routes.append(row)
    questions=list(comparison['questions'])
    declared_scenes=brief.get('scenes')
    scenes=[dict(r,basis='declared') for r in declared_scenes] if declared_scenes else [
        {'id':'opening','purpose':'Establish the subject and why the viewer should care','basis':'proposed'},
        {'id':'demonstration','purpose':'Show concrete evidence or the central action','basis':'proposed'},
        {'id':'ending','purpose':'Resolve the idea and leave a clear takeaway','basis':'proposed'}]
    if declared_scenes is None:questions.append('scene_purposes')
    materials={'status':'declared_not_inspected','source_rights':brief.get('source_rights'),
               'rights_basis':'declared_not_verified','sources':[],'missing':[]}
    search=None;index=None
    if source_index:
        raw=source_index.read_bytes();index=json.loads(raw)
        search=runpy.run_path(str(BASE/'source_search.py'))['search']
        search(index,'framewright revision validation')  # Existing full pin validation, no semantic inference.
        materials.update(status='checked_file_revisions_only',index_sha256=index['index_sha256'],
                         sources=[{k:r[k] for k in ('id','kind','sha256','annotation_provenance')} for r in index['sources']])
    else:materials['missing'].append('source_index')
    for scene in scenes:
        scene.update(material_status='not_searched',candidates=[],candidate_count=0)
        if not scene.get('query'):
            materials['missing'].append('material_query:'+scene['id'])
        elif search:
            found=search(index,scene['query']);scene['candidates']=found['results'][:3]
            scene['candidate_count']=len(found['results'])
            scene['material_status']='candidates_require_review' if found['results'] else 'not_found_in_index'
            if not found['results']:materials['missing'].append('indexed_match:'+scene['id'])
    if source_index and raw!=source_index.read_bytes():raise ValueError('Source index changed during proposal; retry')
    materials['note']='Only retained file revisions and supplied annotations are checked. Search is lexical; no hit is not proof the material does not exist. Candidates need human viewing and rights review.'
    journal=project_view(project) if project else None
    if (preferred and not routes) or (routes and all(r['gaps'] for r in routes)):
        kind,label='resolve_route_gaps','Resolve the requested route constraints or choose another approach; no substitute has been selected.'
    elif questions:kind,label='clarify_brief','Resolve: '+', '.join(questions)+'.'
    elif not routes:kind,label='resolve_route_gaps','No supported route fits; revise the scope or investigate a bounded alternative.'
    elif materials['missing']:kind,label='material_review','Resolve the material gaps, or explicitly plan their creation: '+', '.join(materials['missing'])+'.'
    else:kind,label='choose_route','Review the material candidates and select a proposed route; then validate concrete prerequisites before a bounded pilot.'
    if journal and journal['proposed_next']['kind'] in {'file_review','evidence_review','operation_recovery','waiting','blocked'}:
        kind,label=journal['proposed_next']['kind'],journal['proposed_next']['label']
    return {'schema':'framewright-producer-brief-v1',
            'task':dict(comparison['brief'],basis='declared',deadline=brief.get('deadline'),budget=brief.get('budget')),
            'materials':materials,'scenes':scenes,'routes':routes,'route_exclusions':excluded,'questions':questions,
            'constraints':{'selection_policy':profile['options'],**constraints,
                           'machine':'unknown; not inspected by this command','scope':comparison['scope']},
            'project':journal,
            'next_step':{'kind':kind,'label':label,'status':'proposal_not_execution_authority'},
            'execution':'not_authorized','network_calls':0,'automatic_model_calls':0}


def markdown(view):
    def text(value):
        return str(value if value is not None else 'unknown').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('\n',' ').replace('\r',' ')
    task=view['task'];materials=view['materials']
    lines=['# Production proposal','','## Task','',text(task['idea']),'',
           '- Duration: '+text(task['duration_seconds'])+' seconds; format: '+text(task['format'])+'; language: '+text(task['language'])+' [declared].',
           '- Deadline: '+text(task['deadline'])+'; budget instruction: '+text(task['budget'])+' [declared, not a quote].',
           '', '## Materials','',
           'Local file revisions checked; content and rights still need review.' if materials['sources'] else 'Materials declared, not inspected.',
           '', 'Rights: '+text(materials['source_rights'])+' [declared, not verified].','',
           'Missing: '+(', '.join(map(text,materials['missing'])) or 'None identified within supplied index; candidate review still required.'),
           '', materials['note']]
    if materials['sources']:
        lines+=['', 'Indexed sources ('+str(len(materials['sources']))+'):','']
        for source in materials['sources']:
            lines+=['- '+text(source['id'])+' — '+text(source['kind'])+'; annotation basis: '+text(source['annotation_provenance'])]
    lines+=['', '### Scene purposes','']
    for scene in view['scenes']:
        lines+=['- '+text(scene['id'])+': '+text(scene['purpose'])+' ['+scene['basis']+']; '+scene['material_status']]
        if scene['candidate_count']:lines+=['  - Showing '+str(len(scene['candidates']))+' of '+str(scene['candidate_count'])+' matches.']
        for candidate in scene['candidates']:
            span=('; '+text(candidate['start'])+'–'+text(candidate['end'])+' seconds') if candidate.get('start') is not None else '; still image, no time range'
            lines+=['  - '+text(candidate['source'])+' / '+text(candidate.get('evidence_id'))+span+': '+text(candidate.get('text'))+
                    '; provenance: '+text(candidate['annotation_provenance'])]
    lines+=['', '## Routes','']
    if not view['routes']:lines+=['No route proposed under the current inputs and constraints.','']
    for exclusion in view['route_exclusions']:lines+=['- '+exclusion['id']+': '+exclusion['reason']]
    for r in view['routes']:
        lines += ['', '### '+r['label'],'',r['method'],'',
                  '- Tools: '+' → '.join(s['tool'] or 'UNRESOLVED' for s in r['stages']),
                  '- Why shown: '+('your explicit route preference' if r['selection_basis']=='explicit_preference' else 'matches the declared source approach; a proposal, not a selected route'),
                  '- Tradeoff: '+r['tradeoff'],
                  '- Provider fee: '+text(r['cost']['provider_fee'])+' USD; total cost and working time: unknown.',
                  '- Cost basis: '+r['cost']['basis'],
                  '- Coverage: '+('required capabilities have unresolved gaps' if r['gaps'] else 'component evidence only; complete route not qualified'),
                  '', 'Prerequisites and unresolved checks:','']
        lines+=['- '+text(item) for item in r['gaps']+r['unknown_conditions']]
        lines+=['', 'Human work: '+r['human_work'],'',
                'Pilot: '+r['pilot'],'','Fallback (proposal): '+r['fallback'],'', 'Component evidence and terms:','']
        for stage in r['stages']:
            candidate=stage['candidate']
            if candidate:
                coverage=', '.join(k+': '+v for k,v in stage['required_capabilities'].items())
                lines+=['- '+stage['role']+' ('+candidate['id']+'): '+coverage+'; '+candidate['evidence_scope']+'. '+text(candidate['retained_rights_note'])]
    lines+=['', '## Constraints','', '- Preference: '+view['constraints']['selection_policy'],
            '- Machine: '+view['constraints']['machine'],
            '- Uploads allowed: '+text(view['constraints'].get('allow_uploads'))+'; installation allowed: '+text(view['constraints'].get('allow_installation')),
            '',view['constraints']['scope'],'',
            'Questions: '+(', '.join(view['questions']) or 'None recorded'),
            '', '## Next step','',view['next_step']['label']+' [proposed].',
            '', 'Planning only. No execution, account checks, spending, approval or publication authorized.','']
    if view['project']:
        lines+=['## Recorded project state','',runpy.run_path(str(BASE/'project_summary.py'))['brief_markdown'](view['project'])]
    return '\n'.join(lines)
