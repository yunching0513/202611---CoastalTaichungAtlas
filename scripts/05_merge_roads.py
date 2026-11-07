import json, collections
from shapely.geometry import shape, LineString, MultiLineString, Point
from shapely.ops import linemerge, unary_union
R=json.load(open('raw/roads_raw.json',encoding='utf-8'))
T=json.load(open('data/towns.json',encoding='utf-8'))
def merge(items,tol):
    grp=collections.defaultdict(list)
    for it in items:
        p=it['p']
        if str(p.get('link'))=='1': continue
        grp[(p['sub'],p['ref'],p['name'])].append(LineString(it['c']))
    out=[]
    for (sub,ref,name),ls in grp.items():
        u=unary_union(ls)
        m=(linemerge(u) if u.geom_type=='MultiLineString' else u).simplify(tol,preserve_topology=False)
        geoms=[m] if m.geom_type=='LineString' else list(getattr(m,'geoms',[]))
        cs=[[[round(x,4),round(y,4)] for x,y in g.coords] for g in geoms if g.length>0]
        cs=[c for c in cs if len(c)>=2]
        if cs: out.append({'sub':sub,'ref':ref,'name':name,'c':cs})
    return out
major=merge(R['major'],0.0006); minor=merge(R['minor'],0.0003)
print(len(major),len(minor), sum(len(c) for m in major for c in m['c']), sum(len(c) for m in minor for c in m['c']))
# connection points
core=[shape(f['geometry']) for f in T['features'] if f['properties']['core']]
others=[(shape(f['geometry']),f['properties']) for f in T['features'] if not f['properties']['core']]
cu=unary_union(core).buffer(0); bd=cu.boundary
pts=[]
for m in major:
    for c in m['c']:
        ln=LineString(c); x=ln.intersection(bd)
        if x.is_empty: continue
        for pt in ([x] if x.geom_type=='Point' else [g for g in getattr(x,'geoms',[]) if g.geom_type=='Point']):
            nb=None
            for poly,pr in others:
                if poly.distance(pt)<0.0015: nb=pr; break
            if not nb: continue
            side=nb['c'] if nb['c']!='台中市' else '台中市'+nb['t']
            pts.append({'xy':[round(pt.x,4),round(pt.y,4)],'sub':m['sub'],'ref':m['ref'],'name':m['name'],'to':side,'county':nb['c']})
# dedupe within ~400m same road
ded=[]
for p in pts:
    if any(abs(p['xy'][0]-q['xy'][0])<0.012 and abs(p['xy'][1]-q['xy'][1])<0.012 and (p['sub'],p['ref'],p['to'])==(q['sub'],q['ref'],q['to']) for q in ded): continue
    ded.append(p)
for p in sorted(ded,key=lambda p:(p['county'],p['sub'])): print(p['county'],p['to'],p['sub'],p['ref'],p['name'],p['xy'])
print(collections.Counter((p['county'],p['sub']) for p in ded))
json.dump({'major':major,'minor':minor,'gates':ded},open('data/roads.json','w'),ensure_ascii=False,separators=(',',':'))
import os; print(os.path.getsize('data/roads.json'))
