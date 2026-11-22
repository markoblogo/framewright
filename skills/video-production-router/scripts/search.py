#!/usr/bin/env python3
"""Offline arsenal discovery and compatible proposed chains; never executes tools."""
import argparse
import copy
import hashlib
from collections import Counter
import json
import re
from pathlib import Path
import runpy

BASE=Path(__file__).resolve().parent
REFS=BASE.parent/'references'
LEVEL={'unknown':0,'failed':0,'documented':1,'tested':2}
RANKING=runpy.run_path(str(BASE/'ranking.py'))


QUALITY_AXES=('readability','motion','drawing_stability','artifacts','controllability')

def application_matches(app, query):
    """All requested discovery facets must describe the SAME retained application."""
    if query['task']!='all' and query['task'] not in app['tasks']: return False
    if query.get('style') and query['style'] not in app['styles']: return False
    if query.get('input') and query['input'] not in app['inputs']: return False
    if query.get('technique') and query['technique'] not in app['techniques']: return False
    if LEVEL.get(app['evidence'],0)<{'any':0,'documented':1,'tested':2}[query['evidence']]: return False
    words=[w for w in re.findall(r'\w+',query.get('text','').casefold()) if w not in {'с','и','для','with','and','for'}]
    hay=json.dumps(app,ensure_ascii=False).casefold()
    return all(w in hay for w in words)


def validate_applications(facets, source_root=None):
    """Validate discovery evidence without promoting it to an executable provider."""
    ids=set();root=Path(source_root).resolve() if source_root is not None else None
    for tool,tag in facets['tools'].items():
        for app in tag.get('applications',[]):
            if app['id'] in ids: raise ValueError('Duplicate application ID: '+app['id'])
            ids.add(app['id'])
            if app['evidence'] not in LEVEL: raise ValueError('Invalid application evidence')
            for key in ('tasks','styles','inputs','techniques','sources','examples','limitations','alternatives','search_terms'):
                if not isinstance(app[key],list): raise ValueError('Application list required: '+key)
            if not app['tasks'] or not set(app['tasks']).issubset(tag['tasks']): raise ValueError('Application task outside tool scope: '+tool)
            if not app['sources']: raise ValueError('Application needs retained sources')
            for source in app['sources']:
                path=Path(source)
                if path.is_absolute() or '..' in path.parts or '://' in source: raise ValueError('Invalid application source: '+source)
                if root is not None:
                    f=(root/path).resolve()
                    if not f.is_relative_to(root) or not f.is_file(): raise ValueError('Invalid application source: '+source)
            if set(app['quality'])!=set(QUALITY_AXES): raise ValueError('Missing application quality axis')
            for assessment in app['quality'].values():
                if assessment['status'] not in {'not_assessed','observed','limitation_observed'}: raise ValueError('Invalid quality status')
                if assessment['provenance'] not in {'not_assessed','operator_observation','retained_report'}: raise ValueError('Invalid quality provenance')
            if app['owner_evaluation']['status'] not in {'not_recorded','accepted','rejected','mixed','accepted_retained_scope'}: raise ValueError('Invalid owner evaluation')
            if app['technical']['status'] not in {'recorded_execution','passed','failed','partial'}: raise ValueError('Invalid technical observation')
            for key in ('version','scope','resources','owner_evaluation','technical'):
                if not app[key]: raise ValueError('Missing application field: '+key)
            for alternative in app['alternatives']:
                if alternative['tool_id'] not in facets['tools']: raise ValueError('Unknown application alternative')
                if alternative['comparison']!='not_compared': raise ValueError('Unqualified comparative claim')


def inventory(registry,ledger,facets):
    if facets.get('schema_version')!=1:
        raise ValueError('Unsupported arsenal facets')
    validate_applications(facets)
    RANKING['validate_rankings'](facets)
    rows={}
    aliases=facets['aliases']
    for tool in ledger['tools']:
        identity=aliases.get(tool['id'],tool['id'])
        rows[identity]={'id':identity,'name':tool['name'],'profile':None,'review':tool}
    for tool in registry['tools']:
        row=rows.setdefault(tool['id'],{'id':tool['id'],'review':None})
        row.update(name=tool['name'],profile=tool)
    if rows.keys()!=facets['tools'].keys():
        raise ValueError('Arsenal facets differ from registry/review ledger; index new or removed IDs explicitly')
    for identity,row in rows.items():
        row['facets']=facets['tools'][identity]
        if row['facets']['rights_class'] not in {'conditional','noncommercial_only','unknown'}:
            raise ValueError('Unknown rights classification: '+identity)
    return rows


def rights(row,purpose):
    note=(row['profile'] or row['review'])['licence_note']
    current=hashlib.sha256(note.encode()).hexdigest()==row['facets'].get('licence_note_sha256')
    classification=row['facets']['rights_class'] if current else 'unknown'
    eligible=(purpose=='any' or classification=='conditional' or
              (purpose=='noncommercial' and classification=='noncommercial_only'))
    return {'matches_filter':eligible,'classification':classification,
            'status':'conditional_review_required' if eligible and classification!='unknown' else 'unknown_or_excluded',
            'classification_matches_retained_note':current,'asset_clearance':False,'publication_authorized':False,'retained_terms':note,
            'scope':'Historical discovery eligibility,not a current licence/account/asset grant'}


def fact(tool,feature,query,planner):
    cap=next((f for f in tool['features'] if f['id']==feature),None)
    if not cap:return None
    result=copy.deepcopy(cap)
    if cap['status'] in {'tested','documented'}:
        language=query['language'] or next(iter(cap.get('tested_languages') or cap.get('documented_languages') or ['en']))
        result.update(planner['capability'](tool,feature,language,query['allow_paid'],query['canvas']) or {'status':'unavailable','evidence':'unavailable'})
        if result.get('evidence')!='unavailable':
            result['status']=result['evidence']
    return result


def search(query,registry,ledger,facets):
    planner=runpy.run_path(str(BASE/'plan.py'))
    rows=inventory(registry,ledger,facets)
    task=query['task']; requested=query['features']; minimum=query['evidence']
    threshold={'any':0,'documented':1,'tested':2}[minimum]
    results=[];excluded=[];primary=[]
    for identity,row in sorted(rows.items()):
        tool=row['profile'];review=row['review'];tag=row['facets']
        applications=[a for a in tag.get('applications',[]) if application_matches(a,query)]
        reasons=[];policy=rights(row,query['rights'])
        if task!='all' and task not in tag['tasks']:reasons.append('task does not match')
        if query['tool'] and identity!=facets['aliases'].get(query['tool'],query['tool']):reasons.append('explicit tool filter')
        if query['text'] and not applications and query['text'].casefold() not in (identity+' '+row['name']+' '+str([k for k,v in facets['aliases'].items() if v==identity])+' '+str(tag['tasks'])+' '+str((review or {}).get('scope_and_findings',''))).casefold():reasons.append('text does not match')
        if query['style'] and not applications and query['style'] not in (tool or {}).get('styles',[]):reasons.append('style not indexed for this tool')
        if query.get('technique') and not applications:reasons.append('technique not indexed for this application')
        if query['input']:
            inputs=tool['inputs'] if tool else tag.get('inputs')
            if inputs is None or (inputs and query['input'] not in inputs):reasons.append('input kind does not match or is unindexed')
        if not policy['matches_filter']:reasons.append('retained rights classification excluded or unknown for requested use')
        if tool and tool.get('default_narration_eligible') is False and not query['include_fallbacks'] and query['tool']!=identity:reasons.append('low-quality explicit fallback;enable --include-fallbacks to inspect')
        relevant=facets['task_features'].get(task,[])
        facts=[f for name in relevant if tool and (f:=fact(tool,name,query,planner))]
        if not relevant and tool:facts=[fact(tool,f['id'],query,planner) for f in tool['features']]
        if tool:
            evidence=max((f.get('status','unknown') for f in facts),key=lambda x:LEVEL.get(x,0),default='unknown')
        else:
            evidence='tested' if review['disposition'] in {'supported_scoped','component_used','tested_scoped','owner_accepted_scoped_voice'} else 'unknown'
        if LEVEL.get(evidence,0)<threshold:reasons.append('task evidence below requested level')
        coverage=[]
        if query['language']:
            voice=next((f for f in (tool or {}).get('features',[]) if f['id']=='narration'),None)
            languages=(voice or {}).get('tested_languages' if minimum=='tested' else 'documented_languages',tag.get('declared_languages',[]) if minimum!='tested' else [])
            if query['language'] not in languages:reasons.append('requested speech language not indexed at this evidence level')
        for feature in requested:
            f=fact(tool,feature,query,planner) if tool else None
            if f is None or f.get('status')=='unavailable' or LEVEL.get(f['status'],0)<threshold:
                reasons.append('feature unavailable or below level: '+feature)
            else:coverage.append(f)
        if coverage:
            evidence=min([evidence,*[f['status'] for f in coverage]],key=lambda x:LEVEL.get(x,0))
        if reasons:
            excluded.append({'id':identity,'reasons':reasons})
        else:
            results.append({'id':identity,'name':row['name'],'tasks':tag['tasks'],
                'role':tool['role'] if tool else 'manual_or_review_record',
                'mode':('independent_music_profile' if tool['role']=='music-provider' else 'preproduction_profile' if tool['role']=='preproduction' else 'planner_profile') if tool else 'retained_manual_or_review_record',
                'evidence':evidence,'evidence_scope':'requested component features only' if tool else 'retained method/component only;no structured feature coverage',
                'disposition':review['disposition'] if review else 'profile_only',
                'coverage':coverage,'task_capabilities':{f['id']:f['status'] for f in facts},
                'eligible_for_feature_planning':bool(tool and all(f['status'] in {'tested','documented'} for f in coverage) and LEVEL.get(evidence,0)>0),
                'inputs':tool['inputs'] if tool else tag.get('inputs','unindexed'),'styles':sorted(set((tool or {}).get('styles',[]))|{s for a in applications for s in a['styles']}),
                'applications':copy.deepcopy(applications),
                'languages':next(({'tested':f.get('tested_languages',[]),'documented':f.get('documented_languages',[])} for f in (tool or {}).get('features',[]) if f['id']=='narration'),{'declared':tag.get('declared_languages',[])}),
                'rights':policy,'limits':(tool or {}).get('limitations',[])+([review['scope_and_findings']] if review else []),
                'reference':(review or {}).get('evidence',[]),
                'experiment_ids':sorted({e for f in facts+coverage for e in f.get('experiments',[])}),
                'requires_account_check':bool(tool and tool['role']=='music-provider'),
                'requires_feature_test':any(f.get('status')!='tested' for f in coverage)})
        # Combo primaries use task/style/input/rights only. Companions cover requested features/language.
        if tool and tool['role'] in planner['MAIN_ROLES']:
            independent=[r for r in reasons if not (r.startswith('feature unavailable') or r.startswith('requested speech language') or r.startswith('task evidence'))]
            gate=tool.get('activation')
            active=query['tool']==identity or not gate or bool(set(requested).intersection(gate['features'])) or query['style'] in gate['styles']
            contributes=any((c:=fact(tool,f,query,planner)) and c['status'] in {'tested','documented'} for f in ['video-export',*requested])
            if not independent and active and contributes:primary.append(tool)
    results.sort(key=lambda x:(-LEVEL.get(x['evidence'],0),x['id']))
    chains=[];blocked=[]
    if query['combinations']:
        subset=copy.deepcopy(registry)
        subset['tools']=[t for t in subset['tools'] if rights(rows[t['id']],query['rights'])['matches_filter']]
        outputs=list(dict.fromkeys(['video-export',*requested]))
        for tool in primary:
            block={'id':'search','input':query['input'],'preferred_tool':tool['id'],
                   'style':query['style'] or '', 'effects':requested,'deliverables':outputs}
            if query['voice']:block['preferred_voice']=query['voice']
            brief={'blocks':[block],'minimum_evidence':'tested' if minimum=='tested' else 'documented',
                   'language':query['language'] or 'en','allow_paid':query['allow_paid'],'canvas':query['canvas']}
            # Preserve explicit voice and report its rights/input issue, never silently substitute.
            if query['voice'] and not any(t['id']==query['voice'] for t in subset['tools']):
                blocked.append({'primary':tool['id'],'unmet':['explicit voice excluded by rights filter']});continue
            plan=planner['plan'](brief,subset);b=plan['blocks'][0]
            item={'primary':tool['id'],'tools':b['tools'],'coverage':b['coverage'],'unmet':b['unmet'],
                  'requires_feature_test':b['requires_feature_test'],'limits':b['known_limits'],
                  'rights':{t:rights(rows[t],query['rights']) for t in b['tools']},
                  'qualification':'proposed_chain_requires_integration_check','execution':'not_started',
                  'related_component_experiments':sorted({e for c in b['coverage'] for t in subset['tools'] if t['id']==c['tool'] for f in t['features'] if f['id']==c['feature'] for e in f.get('experiments',[])})}
            (blocked if b['unmet'] else chains).append(item)
        if query['tool'] and not primary:
            blocked.append({'primary':query['tool'],'tools':[],'unmet':['explicit tool has no compatible automatic picture route for these filters;inspect its manual record or exclusions']})
        chains.sort(key=lambda c:(len(c['requires_feature_test']),len(c['tools']),c['primary']))
    return {'schema_version':1,'execution':'not_started','query':query,'result_count':len(results),
            'results':results[:query['limit']],'combinations':chains[:query['limit']],
            'combination_count':len(chains),'blocked_combinations':blocked[:query['limit']],
            'excluded':excluded if query['explain'] else [r for r in excluded if r['id']==facets['aliases'].get(query['tool'],query['tool'])],
            'excluded_summary':dict(Counter(reason for row in excluded for reason in row['reasons'])),
            'notes':['Task/style tags are discovery facets,not creative quality guarantees.',
                     'Conditional rights still require current model/build/account,asset and intended-use review.',
                     'Component evidence never qualifies a new combination. Inspect the retained recipes and final handoff.',
                     'Cloud music needs the independent music.py plan and rights/account gates;not a picture-chain extra.',
                     'Manual/candidate records can be discovered but are not automatically executable providers.']}


def markdown(result):
    cell=runpy.run_path(str(BASE/'packet.py'))['cell']
    lines=['# Arsenal search','', 'Offline discovery only;no execution or rights clearance.',
           f"Matching individual records: {result['result_count']};complete proposed chains: {result['combination_count']}. Display limit: {result['query']['limit']}.", '',
           '| Tool | Tasks | Evidence | Disposition | Rights |','| --- | --- | --- | --- | --- |']
    for row in result['results']:
        lines.append('| '+' | '.join(cell(x) for x in [row['id'],', '.join(row['tasks']),row['evidence'],row['disposition'],row['rights']['status']])+' |')
    for row in result['results']:
        lines+=['', '## '+cell(row['name']), '',
                'Mode: '+cell(row['mode'])+'. Evidence scope: '+cell(row['evidence_scope'])+'.',
                'Task feature facts: '+cell(json.dumps(row['task_capabilities'],ensure_ascii=True))+'.',
                'Retained experiments: '+cell(', '.join(row['experiment_ids']) or 'see manual/review record')+'.',
                'References: '+cell(', '.join(row['reference']) or 'tools.json source keys')+'.',
                'Rights: '+cell(row['rights']['retained_terms'])+'. No asset clearance/publication authority inferred.']
        apps=row.get('applications',[])
        for app in apps if result['query'].get('details') else apps[:2]:
            if not result['query'].get('details') and app.get('granularity')!='specific_production_application':
                lines+=['', 'Application: '+cell(app['id'])+'; version: '+cell(app['version']),
                        'Retained scope: '+cell(app['scope'][:260]),
                        'Technical: '+cell(app['technical']['status'])+'; owner evaluation: '+cell(app['owner_evaluation']['status'])+'; per-axis assessment: see JSON/--details.',
                        'Sources: '+cell(', '.join(app['sources'][:2]))]
                continue
            lines+=['', '### Application: '+cell(app['id']),
                    'Version: '+cell(app['version'])+'. Scope: '+cell(app['scope']),
                    'Styles: '+cell(', '.join(app['styles']) or 'not indexed')+'; techniques: '+cell(', '.join(app['techniques']) or 'not indexed'),
                    'Technical: '+cell(json.dumps(app['technical'],ensure_ascii=False)),
                    'Owner evaluation: '+cell(json.dumps(app['owner_evaluation'],ensure_ascii=False)),
                    'Quality observations: '+cell(json.dumps(app['quality'],ensure_ascii=False)),
                    'Resources: '+cell(json.dumps(app['resources'],ensure_ascii=False)),
                    'Examples: '+cell(json.dumps(app['examples'],ensure_ascii=False)),
                    'Sources: '+cell(', '.join(app['sources'])),
                    'Application limits: '+cell('; '.join(app['limitations'])),
                    'Alternatives (not compared): '+cell(json.dumps(app['alternatives'],ensure_ascii=False))]
        if len(apps)>2 and not result['query'].get('details'):lines.append('More application records retained;use --details or JSON to inspect all.')
        lines.extend('- '+cell(limit) for limit in row['limits'])
    if not result['results'] and result['combinations']:
        lines+=['','No single tool covers all requested filters/features;matching chains follow.']
    lines+=['','## Proposed combinations','']
    for chain in result['combinations']:
        lines+=['### '+cell(' + '.join(chain['tools'])),'', 'Integration check required. Related component records: '+cell(', '.join(chain['related_component_experiments']) or 'none')+'.',
                    'Component capabilities:']
        lines.extend('- '+cell(f"{c['feature']}: {c['tool']} ({c['evidence']}) — {c['note']}") for c in chain['coverage'])
        for tool,limits in chain['limits'].items():
            lines.extend('- '+cell(tool+': '+limit) for limit in limits)
            lines.append('- '+cell(tool+' rights: '+chain['rights'][tool]['retained_terms']))
    if not result['combinations']:lines.append('No complete combination selected. Inspect blocked requirements/filters.')
    if result['blocked_combinations']:
        lines+=['','Blocked combinations:']
        lines.extend('- '+cell(c['primary']+': '+', '.join(c['unmet'])) for c in result['blocked_combinations'])
    lines+=['','## Filter diagnostics','', '```json',json.dumps({'query':result['query'],'excluded_summary':result['excluded_summary'],'excluded':result['excluded']},ensure_ascii=True,indent=2),'```', 'Use --explain for all per-tool exclusions.','']
    lines.extend('- '+cell(note) for note in result['notes'])
    return '\n'.join(lines)


def main():
    registry=json.loads((REFS/'tools.json').read_text())
    ledger=json.loads((REFS/'review-ledger.json').read_text())
    facets=json.loads((REFS/'arsenal-facets.json').read_text())
    tasks=sorted({t for row in facets['tools'].values() for t in row['tasks']})
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task',choices=['all',*tasks],default='all')
    input_kinds = set(runpy.run_path(str(BASE/'plan.py'))['DEFAULTS']) | {kind for row in facets['tools'].values() for kind in (row.get('inputs') or [])}
    parser.add_argument('--input',choices=sorted(input_kinds))
    parser.add_argument('--details',action='store_true',help='Expand all retained application observations in Markdown');parser.add_argument('--technique');parser.add_argument('--style');parser.add_argument('--language');parser.add_argument('--rights',choices=['any','commercial','noncommercial'],default='any')
    parser.add_argument('--evidence',choices=['tested','documented','any'],default='documented')
    parser.add_argument('--feature',action='append',default=[]);parser.add_argument('--query',default='')
    parser.add_argument('--explain',action='store_true',help='Include per-tool exclusions,not just counts');parser.add_argument('--tool');parser.add_argument('--voice');parser.add_argument('--include-fallbacks',action='store_true')
    parser.add_argument('--allow-paid',action='store_true');parser.add_argument('--combinations',action='store_true')
    parser.add_argument('--list-filters',action='store_true');parser.add_argument('--format',choices=['json','markdown'],default='json')
    parser.add_argument('--limit',type=int,default=10)
    parser.add_argument('--width',type=int,default=1920);parser.add_argument('--height',type=int,default=1080);parser.add_argument('--fps',type=int,default=30)
    ranking_mode=parser.add_mutually_exclusive_group()
    ranking_mode.add_argument('--list-rankings',action='store_true',help='List scoped decision profiles')
    ranking_mode.add_argument('--rank-profile',choices=['all',*sorted(facets.get('rankings',{}))],help='Compare tools for a named production use or show every profile')
    parser.add_argument('--unavailable',action='append',default=[],metavar='TOOL',help='Exclude a tool for this project only')
    parser.add_argument('--confirmed',action='append',default=[],metavar='TOOL',help='Confirm current access and setup for a tool')
    args=parser.parse_args()
    try:
        rows=inventory(registry,ledger,facets)
        if args.list_rankings or args.rank_profile:
            if (args.list_filters or args.task!='all' or args.input or args.details or args.technique or args.style
                or args.language or args.evidence!='documented' or args.feature or args.query or args.explain
                or args.tool or args.voice or args.combinations or args.limit!=10 or (args.width,args.height,args.fps)!=(1920,1080,30)):
                raise ValueError('Ranking profiles define their own scope; use ordinary discovery for ad hoc filters')
            if args.list_rankings:
                listing=[{'id':key,'title':value['title'],'scope':value['scope']} for key,value in facets.get('rankings',{}).items()]
                print('\n'.join(f"- `{row['id']}` — {row['title']}. {row['scope']}" for row in listing)
                      if args.format=='markdown' else json.dumps(listing,ensure_ascii=True,indent=2))
                return
            unavailable={facets['aliases'].get(tool,tool) for tool in args.unavailable}
            confirmed={facets['aliases'].get(tool,tool) for tool in args.confirmed}
            unknown=(unavailable | confirmed)-rows.keys()
            if unknown:
                raise ValueError('Unknown tool IDs: '+', '.join(sorted(unknown)))
            profiles=facets['rankings']
            selected=profiles if args.rank_profile=='all' else {args.rank_profile:profiles[args.rank_profile]}
            results=[]
            for key, profile in selected.items():
                result=RANKING['ranked_profile'](profile,rows,rights,args.rights,unavailable,confirmed,args.allow_paid,args.include_fallbacks)
                results.append(dict(profile=key, **result))
            if args.format=='markdown':
                print('\n---\n\n'.join(RANKING['markdown'](result) for result in results))
            else:
                print(json.dumps(results if args.rank_profile=='all' else results[0],ensure_ascii=True,indent=2))
            return
        if args.unavailable or args.confirmed:
            raise ValueError('--unavailable and --confirmed require --rank-profile')
        if args.list_filters:
            print(json.dumps({'tasks':tasks,'styles':sorted({s for t in registry['tools'] for s in t['styles']} | {s for row in facets['tools'].values() for a in row.get('applications',[]) for s in a['styles']}),
                              'techniques':sorted({t for row in facets['tools'].values() for a in row.get('applications',[]) for t in a['techniques']}),
                              'speech_languages':sorted({lang for t in registry['tools'] for f in t['features'] for lang in f.get('documented_languages',[])}),
                              'rights':['any','commercial','noncommercial'],'evidence':['tested','documented','any'],'tool_ids':sorted(rows),'records':len(rows)},indent=2));return
        features=runpy.run_path(str(BASE/'terms.py'))['normalize_effects'](args.feature)
        if args.limit<1 or args.limit>50 or min(args.width,args.height,args.fps)<1:raise ValueError('Positive canvas/fps and limit 1..50 required')
        if args.tool and facets['aliases'].get(args.tool,args.tool) not in rows:raise ValueError('Unknown explicit tool')
        voices={t['id'] for t in registry['tools'] if t['role']=='voice'}
        if args.voice and args.voice not in voices:raise ValueError('Unknown explicit voice')
        if args.language and args.task not in {'narration','transcription','speaker-analysis','song'} and 'narration' not in features:raise ValueError('--language filters speech;request narration or a speech task explicitly')
        if args.combinations and (not args.input or args.task not in {'video','graphics','montage','software','interface','3d','diagram','editing','all'}):raise ValueError('Picture combinations require --input and a picture/editing task;use independent music.py for songs/music')
        if args.combinations and ('narration' in features or args.voice) and not args.language:raise ValueError('Narrated combinations require an explicit --language')
        if args.voice and not args.combinations:raise ValueError('--voice is a combination choice;use --tool for individual voice discovery')
        if args.voice and 'narration' not in features:raise ValueError('--voice requires --feature narration')
        if args.combinations:
            features=list(dict.fromkeys([{'interface':'camera-travel','3d':'staged-3d','diagram':'workflow-diagram','graphics':'typography','montage':'image-pan-zoom'}.get(args.task,'video-export'),*features]))
        query={'task':args.task,'input':args.input,'style':args.style,'details':args.details,'technique':args.technique,'language':args.language,'rights':args.rights,
               'evidence':args.evidence,'features':list(dict.fromkeys(features)),'text':args.query,'tool':args.tool,'voice':args.voice,
               'include_fallbacks':args.include_fallbacks,'allow_paid':args.allow_paid,'combinations':args.combinations,'limit':args.limit,'explain':args.explain,
               'canvas':{'width':args.width,'height':args.height,'fps':args.fps}}
        result=search(query,registry,ledger,facets)
        print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=True,indent=2))
    except (ValueError,KeyError,TypeError) as exc:parser.error(str(exc))


if __name__=='__main__':main()
