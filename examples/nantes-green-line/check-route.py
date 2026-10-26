"""Offline source-to-film route coverage; does not fetch or infer missing branches."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
src=json.loads((R/'research/official-full-route.geojson').read_text())
def lines(g):
 if g.get('type')=='FeatureCollection':return [x for f in g['features'] for x in lines(f)]
 if g.get('type')=='Feature':return lines(g['geometry'])
 if g.get('type')=='LineString':return [g['coordinates']]
 if g.get('type')=='MultiLineString':return g['coordinates']
 if g.get('type')=='GeometryCollection':return [x for q in g['geometries'] for x in lines(q)]
 return []
expected=lines(src);film=json.loads((R/'film/assets/full-route.json').read_text());city=json.loads((R/'film/assets/city.json').read_text())
assert expected and expected==film['lines']==city['fullRoute'],'Route line/vertex loss between official source and film assets'
pts=[p for l in expected for p in l];xs=[p[0] for p in pts];ys=[p[1] for p in pts];bounds=[min(xs),min(ys),max(xs),max(ys)]
w=(bounds[2]-bounds[0])*75500;h=(bounds[3]-bounds[1])*111195;scale=min(1060/w,800/h)
projected=[[1180+(x-(bounds[0]+bounds[2])/2)*75500*scale,525-(y-(bounds[1]+bounds[3])/2)*111195*scale] for x,y in pts]
assert all(650<=x<=1810 and 95<=y<=950 for x,y in projected),'Full route crops outside map area'
report={'result':'pass','official_lines':len(expected),'official_vertices':len(pts),'film_lines':len(city['fullRoute']),'all_geometry_retained':True,'all_vertices_inside_map_area':True,'source_sha256':hashlib.sha256((R/'research/official-full-route.geojson').read_bytes()).hexdigest(),'scope':'Coverage and projection of the downloaded official source, not completeness of third-party OSM relation or an assertion about later route changes.'}
(R/'evidence/route-coverage.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
