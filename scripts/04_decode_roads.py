import math, json, sys, gzip, collections
from pmtiles.reader import Reader, MmapSource
import mapbox_vector_tile
PM='raw/hierarchy.pmtiles'
f=open(PM,'rb'); r=Reader(MmapSource(f)); h=r.header(); print({k:h[k] for k in ['min_zoom','max_zoom','tile_compression','tile_type']})
def lon2x(lon,z): return (lon+180)/360*2**z
def lat2y(lat,z): la=math.radians(lat); return (1-math.log(math.tan(la)+1/math.cos(la))/math.pi)/2*2**z
def x2lon(x,z): return x/2**z*360-180
def y2lat(y,z): n=math.pi-2*math.pi*y/2**z; return math.degrees(math.atan(math.sinh(n)))
def decode(z,bbox,keep):
    x0,x1=int(lon2x(bbox[0],z)),int(lon2x(bbox[2],z)); y0,y1=int(lat2y(bbox[3],z)),int(lat2y(bbox[1],z))
    out=[]
    for x in range(x0,x1+1):
        for y in range(y0,y1+1):
            t=r.get(z,x,y)
            if not t: continue
            if t[:2]==b'\x1f\x8b': t=gzip.decompress(t)
            d=mapbox_vector_tile.decode(t, default_options={'y_coord_down':True})
            for lname,layer in d.items():
                ext=layer.get('extent',4096)
                for ft in layer['features']:
                    p=ft['properties']
                    if not keep(p): continue
                    g=ft['geometry']; lines=[g['coordinates']] if g['type']=='LineString' else (g['coordinates'] if g['type']=='MultiLineString' else [])
                    for ln in lines:
                        pts=[[round(x2lon(x+cx/ext,z),5),round(y2lat(y+cy/ext,z),5)] for cx,cy in ln]
                        out.append({'p':{k:p.get(k,'') for k in ['ss','sub','ref','name','link']},'c':pts})
    return out
REG=[120.25,23.78,121.45,24.75]
CORE=[120.45,24.10,120.72,24.42]
z1=int(sys.argv[1]) if len(sys.argv)>1 else 11
major=decode(z1,REG,lambda p:p.get('ss')=='T' or p.get('sub') in ('省道','縣道'))
minor=decode(12,CORE,lambda p:p.get('ss')=='D' and p.get('sub') not in ('省道','縣道'))
print('major',len(major),collections.Counter(m['p']['sub'] for m in major))
print('minor',len(minor),collections.Counter(m['p']['sub'] for m in minor))
json.dump({'major':major,'minor':minor},open('raw/roads_raw.json','w'),ensure_ascii=False)
