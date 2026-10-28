"""Read-only completion diagnosis from existing task, revision and review evidence."""


def diagnose(data,state,check_kind):
    steps={s['id']:s for s in data['steps']}
    latest={(r['subject'],r['kind'],r['topic']):r for r in data.get('journal',[])}
    observations={r['id']:r for r in state['observations']['effective']+state['observations']['stale']}
    blockers=[];followups=[]

    def context(subject,task):
        production=data.get('production',{})
        subjects={subject} if subject else set()
        subjects.update('output:'+i for i in steps.get(task,{}).get('required_outputs',[]))
        materials=[m['id'] for m in production.get('materials',[]) if m['subject'] in subjects]
        scenes=[s['id'] for s in production.get('scenes',[]) if set(materials).intersection(s['materials']) or
                s['narration']['material'] in materials]
        if subject and subject.startswith('output:'):
            scene=data['artifacts'][subject[7:]].get('scene')
            if scene and scene not in scenes:scenes.append(scene)
        variants=[]
        for v in production.get('variants',[]):
            report=state['production']['variants'][v['id']]
            if task in v['tasks'] or set(materials).intersection(report['used_materials']):variants.append(v['id'])
        return {'materials':materials,'scenes':scenes,'variants':variants}

    def affected(task,subject):
        roots={task} if task else set()
        if not task and subject and subject.startswith('output:'):
            roots.update(s['id'] for s in steps.values() if subject[7:] in s['required_outputs'])
        reached=set(roots)
        while True:
            expanded=reached|{s['id'] for s in steps.values() if reached.intersection(s['depends_on'])}
            if expanded==reached:break
            reached=expanded
        return sorted(reached)

    def add(kind,reason,action,task=None,subject=None,receipt=None,required=True,extra=None):
        pin=(data['inputs'].get(subject[6:]) if subject and subject.startswith('input:') else
             data['artifacts'].get(subject[7:],{}).get('file') if subject and subject.startswith('output:') else None)
        events=[{'history_index':i,'action':h['action'],'recorded_at':h['utc']} for i,h in enumerate(data['history'])
                if (task and (h.get('step')==task or any(s['id']==task for s in h.get('previous_steps',[])))) or
                   (receipt and h.get('entry')==receipt['id']) or
                   (subject and ':' in subject and h.get('identity')==subject.split(':',1)[1] and
                    h['action'] in ({'retain_input'} if subject.startswith('input:') else {'retain_output','declare_artifact'}))]
        row={'kind':kind,'reason':reason,'task':task,'subject':subject,
             'current_sha256':pin['sha256'] if pin else None,'context':context(subject,task),
             'affected_tasks':affected(task,subject),'waiting_for':steps.get(task,{}).get('waiting_for'),
             'next_action':action,'action_status':'proposal_not_execution_authority',
             'source_events':events[-3:],'receipt':None}
        if receipt:
            row['receipt']={k:receipt[k] for k in ['id','kind','result','topic','actor','provenance','note','pins','stale_reasons']}
        if extra:row.update(extra)
        (blockers if required else followups).append(row)

    for subject,reason in state['file_problems'].items():
        add('file_problem',reason,'Inspect or restore the retained source; record an intentional replacement explicitly',subject=subject,
            extra={'affects_global_readiness':True})
    for s in steps.values():
        task=s['id'];required=not s.get('optional',False)
        if s['state']=='blocked':
            add('explicit_wait' if s.get('waiting_for') else 'constraint',s['unmet'] or s['evidence'],
                'Obtain the recorded input/decision; preserve the wait until explicitly resolved' if s.get('waiting_for') else
                'Resolve the recorded constraint; a frozen unmet route needs an explicit revised plan',task=task,required=required)
        for ident in s['required_outputs']:
            if data['artifacts'][ident]['file'] is None:
                add('output_not_retained','Required output has not been retained',
                    'Obtain or produce the required material within the authorised scope, then retain it',task,'output:'+ident,required=required)
        kind=check_kind(s)
        subjects=['output:'+i for i in s['required_outputs']]
        if task=='owner-review' and 'final-video' in data['artifacts']:subjects.append('output:final-video')
        if kind:
            for subject in dict.fromkeys(subjects):
                rows=[observations[r['id']] for r in latest.values() if r['id'] in observations and r['subject']==subject and r['kind']==kind]
                if not rows and data['artifacts'][subject[7:]]['file'] is not None:
                    add('review_missing','No current '+kind+' observation recorded for this check',
                        'Perform the required check on this revision and record its result',task,subject,required=required)
        if s['state']!='done':
            unfinished=[i for i in s['depends_on'] if steps[i]['state']!='done']
            add('dependency' if unfinished else 'task_open','Dependencies are not done' if unfinished else 'Task is not recorded done',
                'Resolve the listed dependencies first' if unfinished else 'Review the recorded task and its evidence before marking completion',
                task=task,required=required,extra={'depends_on':unfinished})
    for r in latest.values():
        row=observations.get(r['id'])
        if not row:continue
        stale=bool(row['stale_reasons'])
        unresolved=row['kind'] in {'technical','listening','creative','provider','decision'} and row['result'] in {'fail','rejected','pending','deferred','proposed'}
        if not stale and not unresolved:continue
        if row['kind'] in {'publication','metrics'}:continue
        linked=[s for s in steps.values() if check_kind(s)==row['kind'] and
                (row['subject'] in ['output:'+i for i in s['required_outputs']] or
                 s['id']=='owner-review' and row['subject']=='output:final-video')]
        if not linked:
            add('stale_review' if stale else 'unscoped_review','Stale observation' if stale else 'Unresolved observation; no required check mapping recorded',
                'Review the observation and decide its relevance to completion',subject=row['subject'],receipt=row,required=False)
        for s in linked:
            add('stale_review' if stale else 'review_unresolved','Stale observation' if stale else row['kind']+': '+row['result'],
                'Inspect the exact revision/dependencies, perform the relevant review and record the outcome',s['id'],row['subject'],row,not s.get('optional',False))
    for attempt in state.get('unresolved_attempts',[]):
        add('operation_unresolved','Executor outcome unresolved: '+attempt['attempt'],
            'Inspect actual outcome and retain explicit recovery evidence; do not repeat dispatch',task=attempt['step'])
    production=state['production']
    if production:
        for variant,view in production['variants'].items():
            for reason in view['blockers']:
                add('variant_requirement',reason,'Resolve this declared variant requirement and inspect its source evidence',
                    extra={'variant':variant,'context':{'variants':[variant],
                           'scenes':list(dict.fromkeys(e['scene'] for e in view['edits'])),
                           'materials':sorted(view['used_materials'])}})
    if state['planning_sources_changed']:
        add('planning_sources_changed','Implementation/catalogue differs from the frozen planning sources',
            'Review relevance to the frozen plan; no automatic replan',required=False)
    priority={'file_problem':0,'explicit_wait':1,'constraint':2,'stale_review':3,'review_unresolved':4,'review_missing':5,'output_not_retained':6,'variant_requirement':7,'dependency':8,'task_open':9}
    blockers.sort(key=lambda r:priority.get(r['kind'],10))
    return {'schema':'framewright-completion-diagnosis-v1','goal':data.get('project',{}).get('goal',''),
            'status':'recorded_blockers' if blockers else 'no_recorded_blockers' if steps or production else 'scope_not_defined',
            'blockers':blockers,'followups':followups,'counts':{'blockers':len(blockers),'followups':len(followups)},
            'execution':'not_started','publication_authorized':False,
            'note':'Derived local/private evidence only. No recorded blockers does not establish creative approval, rights clearance or publication readiness. Unmapped observations and optional tasks are followups.'}


def markdown(view,limit=5):
    def cell(v):return str(v).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('\n',' ')
    lines=['# What prevents completion?','',cell(view['goal']), '', 'Status: '+view['status'],
           'Recorded blockers: '+str(view['counts']['blockers'])+'; followups: '+str(view['counts']['followups']),'']
    for label in ['blockers','followups']:
        lines+=['## '+label.capitalize(),'']
        for row in view[label][:limit]:
            lines.append('- '+cell(row['kind'])+' / '+cell(row['task'] or row['subject'] or row.get('variant','project'))+': '+cell(row['reason']))
            if row['waiting_for']:lines.append('  Waiting for: '+cell(row['waiting_for']))
            if row['receipt']:lines.append('  Evidence: '+cell(row['receipt']['id'])+' / '+cell(row['receipt']['result']))
            if row['affected_tasks']:lines.append('  Affected tasks: '+cell(', '.join(row['affected_tasks'])))
            lines.append('  Proposed action: '+cell(row['next_action']))
        if len(view[label])>limit:lines.append('- More: '+str(len(view[label])-limit)+'; use --json for all records.')
        if not view[label]:lines.append('- None recorded')
        lines.append('')
    return '\n'.join(lines+[view['note'],''])
