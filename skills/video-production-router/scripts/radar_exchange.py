#!/usr/bin/env python3
"""Explicit local Radar seam. No API, rendering, publishing or scheduled hooks."""
import argparse
import copy
from datetime import datetime,timezone,timedelta
import hashlib
import json
from pathlib import Path
import runpy
from urllib.parse import urlsplit,parse_qs
import radar_wire as W

BASE=Path(__file__).resolve().parent


def apply_message(data,row):
    p=row['payload']
    if row['producer']!='radar':raise ValueError('Expected Radar')
    if row['kind']=='idea_menu':
        W.menu_payload(p);menus=data.setdefault('menus',{});old=menus.get(p['packet_sha256'])
        if old is not None and old!=p:raise ValueError('Research version conflict')
        menus[p['packet_sha256']]=copy.deepcopy(p);return 'applied','Menu cached; no project created'
    if row['kind']=='analytics_snapshot':
        W.analytics_payload(p)
        link=data.get('links',{}).get(p['project_id'])
        if link is None:return 'pending','Unknown project link'
        if p['source_kind']=='synthetic_fixture' and not data.get('allow_synthetic',False):raise ValueError('Synthetic analytics forbidden in live state')
        pubs=data.get('publications',{}).get(p['project_id'],[])
        if p['video_id'] not in [x['video_id'] for x in pubs]:raise ValueError('Video does not belong to project')
        expected=data.get('expected_channel')
        if not expected or p['channel_id']!=expected:raise ValueError('Channel not configured/mismatch')
        data.setdefault('analytics',{})[row['message_id']]=copy.deepcopy(p)
        return 'applied','Dated analytics snapshot; no causal or prospective-test claim'
    raise ValueError('Unsupported inbound kind')


def project_data(path):
    # Reuse project integrity and pinned-file validation, not an alternate journal.
    P=runpy.run_path(str(BASE/'project.py'));d=P['load'](Path(path))
    if P['file_problems'](d,Path(path).parent):raise ValueError('Project has changed/missing retained inputs')
    return d


def select(project,root,project_id,revision,idea_id,mode,owner_approved=False,before_production=False,now=None):
    if not owner_approved:raise ValueError('Explicit owner approval required')
    W.key(project_id);W.key(idea_id);W.sha(revision)
    project=Path(project);d=project_data(project);menus=W.state(root,'framewright')['data'].get('menus',{})
    menu=menus.get(revision)
    if menu is None:raise ValueError('Import menu first')
    idea=next((x for x in menu['ideas'] if x['id']==idea_id),None)
    if idea is None:raise ValueError('Unknown idea')
    now=now or datetime.now(timezone.utc).isoformat()
    if mode not in {'prospective_hypothesis','retrospective_observation'}:raise ValueError('Unknown link mode')
    p=dict(project_id=project_id,radar_idea_id=idea_id,research_revision=revision,idea_sha256=W.digest(idea),selected_at=now,link_mode=mode,owner_approval=True,timing_basis='retrospective owner link' if mode.startswith('retro') else 'owner before-production attestation; not a Radar experiment approval')
    W.association_payload(p)
    linkpath=project.parent/'radar-link.json'
    with W.locked(W.directory(root,'framewright')):
        st=W.state(root,'framewright');existing=st['data'].get('links',{}).get(project_id)
        if existing and any(existing[k]!=p[k] for k in ['project_id','radar_idea_id','research_revision','idea_sha256','link_mode']):
            raise ValueError('Project identity already associated with another idea')
        with W.locked(project.parent):
            if linkpath.exists():
                link=W.read(linkpath);old=link['association']
                if any(old[k]!=p[k] for k in ['project_id','radar_idea_id','research_revision','idea_sha256','link_mode']):raise ValueError('Frozen project association differs')
                p=old
                if existing is not None and existing!=p:raise ValueError('Project identity collision')
            else:
                if existing is not None:raise ValueError('Project identity already used at another project path')
                if mode=='prospective_hypothesis':
                    if not before_production or any(a.get('file') for a in d['artifacts'].values()):raise ValueError('Before-production owner attestation and no retained output required')
                    for s in idea['sources']:
                        if not timedelta(0)<=W.timestamp(now)-W.timestamp(s['checked_at'])<=timedelta(hours=72):raise ValueError('Refresh stale/future idea sources before new production')
                link={'association':p,'frozen_idea':idea,'export_sequence':0,'last_export_hash':None}
                W.atomic(linkpath,link,immutable=True)
        st['data'].setdefault('links',{})[project_id]=p;W.atomic(W.directory(root,'framewright')/'state.json',st)
    row=W.message('association','framewright',project_id,revision,0,p['selected_at'],p)
    W.publish(root,'framewright',row);return row


def youtube_id(url):
    p=urlsplit(url)
    if p.hostname in {'youtu.be','www.youtu.be'}:return p.path.strip('/')
    if p.hostname in {'youtube.com','www.youtube.com','m.youtube.com'}:return parse_qs(p.query).get('v',[''])[0]
    return None


def export_status(project,root):
    project=Path(project);P=runpy.run_path(str(BASE/'project.py'))
    with P['locked'](project):
        return _export_locked_status(project,root)


def _export_locked_status(project,root):
    d=project_data(project);linkpath=project.parent/'radar-link.json'
    J=runpy.run_path(str(BASE/'journal.py'));projection=J['project'](d,{});effective=projection['effective']
    latest_topics={(r['subject'],r['kind'],r['topic']):r['id'] for r in d.get('journal',[])}
    with W.locked(project.parent):
        link=W.read(linkpath);a=link['association'];outputs=[];pubs=[]
        for ident,artifact in d['artifacts'].items():
            pin=artifact.get('file')
            if not pin:continue
            subject='output:'+ident
            reviews=[r for r in effective if r['subject']==subject and r['pins'].get(subject)==pin and r['kind'] in {'creative','listening'}]
            stale_required=any(r['subject']==subject and r['kind'] in {'creative','listening'} and latest_topics.get((r['subject'],r['kind'],r['topic']))==r['id'] for r in projection['stale'])
            accepted=not stale_required and all(any(r['kind']==k for r in reviews) and all(r['result']=='accepted' for r in reviews if r['kind']==k) for k in ['creative','listening'])
            outputs.append({'id':ident,'sha256':pin['sha256'],'bytes':pin['bytes'],'accepted':accepted})
            publications={r['url']:r for r in effective if r['subject']==subject and r['pins'].get(subject)==pin and r['kind']=='publication'}
            for r in publications.values():
                vid=youtube_id(r['url'])
                if r['result']!='published' or not vid:continue
                pubs.append(dict(platform='youtube',video_id=vid,url=r['url'],output_id=ident,receipt_id=r['id'],provenance=r['provenance'],recorded_at=r['recorded_at'],master_sha256=pin['sha256']))
        status='published' if pubs else 'accepted' if any(o['accepted'] for o in outputs) else 'blocked' if any(s['state']=='blocked' and not s.get('optional') for s in d['steps']) else 'ready_for_review' if outputs else 'selected'
        payload=dict(project_id=a['project_id'],radar_idea_id=a['radar_idea_id'],research_revision=a['research_revision'],source_journal_sha256=d['journal_sha256'],status=status,outputs=outputs,publications=pubs)
        W.status_payload(payload);h=W.digest(payload)
        if h!=link['last_export_hash']:
            link['export_sequence']+=1;link['last_export_hash']=h;link['last_export_time']=datetime.now(timezone.utc).isoformat();W.atomic(linkpath,link)
        row=W.message('production_status','framewright',a['project_id'],h,link['export_sequence'],link['last_export_time'],payload)
    with W.locked(W.directory(root,'framewright')):
        st=W.state(root,'framewright');st['data'].setdefault('publications',{})[a['project_id']]=pubs;W.atomic(W.directory(root,'framewright')/'state.json',st)
    W.publish(root,'framewright',row);return row


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--exchange',type=Path,required=True);p.add_argument('--apply',action='store_true')
    sub=p.add_subparsers(dest='action',required=True)
    q=sub.add_parser('receive');q.add_argument('message',type=Path)
    q=sub.add_parser('select');q.add_argument('project',type=Path);q.add_argument('--project-id',required=True);q.add_argument('--research-revision',required=True);q.add_argument('--idea-id',required=True);q.add_argument('--mode',choices=['retrospective_observation','prospective_hypothesis'],required=True);q.add_argument('--owner-approved',action='store_true');q.add_argument('--before-production',action='store_true')
    q=sub.add_parser('export-status');q.add_argument('project',type=Path)
    q=sub.add_parser('configure');q.add_argument('--channel-id',required=True)
    q=sub.add_parser('enable-auto');q.add_argument('project',type=Path)
    sub.add_parser('status')
    args=p.parse_args()
    if args.action=='status':print(json.dumps(W.state(args.exchange,'framewright'),ensure_ascii=False));return
    if not args.apply:print(json.dumps({'status':'PREVIEW_NO_WRITES','action':args.action}));return
    if args.action=='enable-auto':
        from radar_auto import enable
        enable(args.project,args.exchange);print(json.dumps({'result':'auto_checkpoint_enabled'}));return
    if args.action=='configure':
        import re
        if not re.fullmatch(r'UC[A-Za-z0-9_-]{22}',args.channel_id):raise ValueError('Invalid channel')
        with W.locked(W.directory(args.exchange,'framewright')):
            st=W.state(args.exchange,'framewright');old=st['data'].get('expected_channel')
            if old and old!=args.channel_id:raise ValueError('Channel change requires explicit migration')
            st['data']['expected_channel']=args.channel_id;W.atomic(W.directory(args.exchange,'framewright')/'state.json',st)
        result={'result':'configured'}
    elif args.action=='receive':result=W.receive(args.exchange,'framewright',W.read(args.message),apply_message)
    elif args.action=='select':result=select(args.project,args.exchange,args.project_id,args.research_revision,args.idea_id,args.mode,args.owner_approved,args.before_production)
    else:result=export_status(args.project,args.exchange)
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
