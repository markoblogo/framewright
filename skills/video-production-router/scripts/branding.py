#!/usr/bin/env python3
"""Freeze selected local brand references and export renderer-neutral assets/CSS. No rendering or upload."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import shutil

SCHEMA='framewright-brand-profile-v1'
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def file_hash(path):
 h=hashlib.sha256()
 with path.open('rb') as stream:
  for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def load(path):return json.loads(path.read_text())
def write(path,value):
 with path.open('x') as stream:json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')
def exact(value,keys,label):
 if not isinstance(value,dict) or set(value)!=set(keys):raise ValueError('Invalid '+label+' fields')
def text(value,label):
 if not isinstance(value,str) or not value.strip():raise ValueError('Missing '+label)
 return value
def number(value,label,low,high):
 if type(value) not in (int,float) or not math.isfinite(value) or not low<=value<=high:raise ValueError('Invalid '+label)
def design(spec):
 exact(spec,{'id','palette','typography','layout','motion','assets','sources'},'brand')
 if not isinstance(spec['id'],str) or not re.fullmatch('[a-z][a-z0-9-]{0,63}',spec['id']):raise ValueError('Invalid brand id')
 exact(spec['palette'],{'paper','ink','accent','muted','negative'},'palette')
 for colour in spec['palette'].values():
  if not isinstance(colour,str) or not re.fullmatch('#[A-Fa-f0-9]{6}',colour):raise ValueError('Colours need six-digit hex values')
 t=spec['typography'];exact(t,{'family','heading_px','hero_px','body_px','meta_px','heading_weight'},'typography')
 if not isinstance(t['family'],str) or not re.fullmatch('[A-Za-z][A-Za-z0-9 -]{0,79}',t['family']):raise ValueError('Invalid font-family label')
 for key in ['heading_px','hero_px','body_px','meta_px']:number(t[key],key,8,1024)
 number(t['heading_weight'],'heading weight',100,900)
 l=spec['layout'];exact(l,{'width','height','margin_x','content_top','content_bottom','logo_width'},'layout')
 for key in ['width','height']:
  if type(l[key]) is not int:raise ValueError('Canvas dimensions must be integers')
  number(l[key],key,16,8192)
 number(l['margin_x'],'horizontal margin',0,l['width']/2-1)
 number(l['logo_width'],'logo width',1,l['width']-2*l['margin_x'])
 number(l['content_top'],'content top',0,l['height']-1)
 number(l['content_bottom'],'content bottom',l['content_top']+1,l['height'])
 motion=spec['motion'];required={'enter_seconds','chart_seconds'}
 if not isinstance(motion,dict) or not required<=set(motion)<=required|{'settled_hold_seconds'}:raise ValueError('Invalid motion fields')
 for key,value in motion.items():number(value,key,0 if key=='settled_hold_seconds' else .01,10)
 exact(spec['assets'],{'logo','font','licence'},'assets')
 for role,asset in spec['assets'].items():
  exact(asset,{'path','origin','rights_status','rights_evidence'},role)
  text(asset['path'],'local asset path');text(asset['origin'],'asset origin')
  if '://' in asset['path']:raise ValueError('Only selected local files; no fetching')
  if asset['rights_status'] not in {'granted','unknown','noncommercial_only','denied'}:raise ValueError('Invalid rights status')
  if asset['rights_status']=='denied':raise ValueError('Denied brand asset')
  if asset['rights_status'] in {'granted','noncommercial_only'}:text(asset['rights_evidence'],'rights evidence')
  elif not isinstance(asset['rights_evidence'],str):raise ValueError('Rights evidence must be text')
  suffix=Path(asset['path']).suffix.lower()
  if role=='logo' and suffix not in {'.png','.jpg','.jpeg'}:raise ValueError('Use an inspected PNG/JPEG logo')
  if role=='font' and suffix not in {'.ttf','.otf','.woff','.woff2'}:raise ValueError('Use an inspected local font')
 if not isinstance(spec['sources'],list) or not 1<=len(spec['sources'])<=20:raise ValueError('Select1–20local reference sources')
 for source in spec['sources']:
  exact(source,{'path','note'},'source');text(source['path'],'source path');text(source['note'],'source note')
  if '://' in source['path']:raise ValueError('Retain remote references locally before freezing')
 digest(spec)
def pin(path):
 path=path.resolve()
 if not path.is_file():raise ValueError('Missing selected file: '+str(path))
 return {'path':str(path),'sha256':file_hash(path),'bytes':path.stat().st_size}
def freeze(source,output):
 spec=load(source);design(spec)
 value={'schema':SCHEMA,'design':spec,'assets':{},'sources':[],
        'selection':'Explicitly selected reference values; not automatic brand inference or owner film acceptance',
        'creative_review':'pending','publication_authorized':False}
 for role,asset in spec['assets'].items():value['assets'][role]={**asset,**pin(source.parent/asset['path'])}
 for item in spec['sources']:value['sources'].append({**item,**pin(source.parent/item['path'])})
 value['publication_blockers']=[role+': resolve rights for intended use' for role,a in value['assets'].items() if a['rights_status']!='granted']
 value['profile_sha256']=digest(value);write(output,value);return value
def checked(path):
 value=load(path)
 if value.get('schema')!=SCHEMA or value.get('profile_sha256')!=digest({k:v for k,v in value.items() if k!='profile_sha256'}):raise ValueError('Profile changed; freeze a new revision')
 design(value['design'])
 for item in [*value['assets'].values(),*value['sources']]:
  file=Path(item['path'])
  if not file.is_file() or file_hash(file)!=item['sha256']:raise ValueError('Pinned brand source changed or missing: '+str(file))
 return value
def export(profile,output):
 value=checked(profile);s=value['design'];files={role:role+Path(a['path']).suffix.lower() for role,a in value['assets'].items()}
 # Everything is checked before a new output directory is created. Existing bundles are never overwritten.
 output.mkdir()
 for role,a in value['assets'].items():shutil.copyfile(a['path'],output/files[role])
 rules=["@font-face{font-family:FWBrand;src:url('"+files['font']+"');font-style:normal;font-weight:100 900}"]
 tokens={'font':'FWBrand'}
 tokens.update({k:v for k,v in s['palette'].items()})
 for k,v in s['typography'].items():
  if k=='family':continue
  tokens[k.replace('_px','').replace('_','-')]=str(v)+('px' if k.endswith('_px') else '')
 for k,v in s['layout'].items():tokens[k.replace('_','-')]=str(v)+'px'
 for k,v in s['motion'].items():tokens[k.replace('_seconds','').replace('_','-')]=str(v)+'s'
 rules.append(':root{'+''.join('--brand-'+k+':'+v+';' for k,v in tokens.items())+'}')
 (output/'brand.css').write_text('\n'.join(rules)+'\n')
 # Exported bundles are independently usable after the original source files move; their origin remains explicit.
 bundle={k:value[k] for k in ['profile_sha256','selection','creative_review','publication_authorized','publication_blockers']}
 bundle['schema']='framewright-brand-bundle-v1';bundle['design']=copy.deepcopy(s)
 for role in bundle['design']['assets']:bundle['design']['assets'][role]['path']=files[role]
 bundle['design']['sources']=[{'path':Path(item['path']).name,'note':item['note'],'sha256':item['sha256']} for item in value['sources']]
 bundle['files']={role:{'file':files[role],'sha256':a['sha256'],'origin':a['origin'],'rights_status':a['rights_status'],'rights_evidence':a['rights_evidence']} for role,a in value['assets'].items()}
 bundle['css_sha256']=file_hash(output/'brand.css');write(output/'brand.json',bundle)
 return bundle
def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
 for name in ['create','export']:
  a=sub.add_parser(name);a.add_argument('source',type=Path);a.add_argument('--output',type=Path,required=True)
 a=sub.add_parser('check');a.add_argument('source',type=Path);args=parser.parse_args()
 try:
  result=freeze(args.source,args.output) if args.command=='create' else export(args.source,args.output) if args.command=='export' else checked(args.source)
  print(json.dumps({'ok':True,'command':args.command,'profile_sha256':result['profile_sha256'],'publication_authorized':False,'publication_blockers':result['publication_blockers']}))
 except (ValueError,OSError,KeyError,TypeError) as exc:parser.exit(1,str(exc)+'\n')
if __name__=='__main__':main()
