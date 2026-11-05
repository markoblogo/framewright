"""Opt-in sync on saved checkpoints; no scheduler, selection or remote calls."""
from pathlib import Path
import radar_wire as W
import radar_exchange as E


def enable(project,root):
    project=Path(project);E.project_data(project)
    link=W.read(project.parent/'radar-link.json')['association']
    if W.state(root,'framewright')['data'].get('links',{}).get(link['project_id'])!=link:
        raise ValueError('Existing project/exchange link required')
    W.atomic(project.parent/'radar-auto.json',{'version':1,'enabled':True,'exchange_root':str(Path(root).absolute())})


def checkpoint(project):
    project=Path(project);config=project.parent/'radar-auto.json'
    if not config.exists():return {'result':'disabled'}
    try:
        c=W.read(config)
        if not isinstance(c,dict):raise ValueError('Invalid auto configuration')
        if c!={'version':1,'enabled':True,'exchange_root':c.get('exchange_root')} or not isinstance(c['exchange_root'],str):raise ValueError('Invalid auto configuration')
        root=Path(c['exchange_root']);state=W.state(root,'framewright')['data'];link=W.read(project.parent/'radar-link.json')['association']
        if state.get('links',{}).get(link['project_id'])!=link:raise ValueError('Existing project/exchange link required')
        incoming=W.drain(root,'framewright',E.apply_message)
        row=E.export_status(project,root)
        result={'result':'synced','message_id':row['message_id'],'incoming':[r['result'] for r in incoming]}
    except (OSError,ValueError,TypeError,KeyError,ImportError) as exc:
        result={'result':'pending','reason':type(exc).__name__}
    # Optional seam failure must not invalidate a successful project save.
    try:W.atomic(project.parent/'radar-auto-last.json',result)
    except OSError:pass
    return result
