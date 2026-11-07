import json, statistics, math, re, collections
d=json.load(open('raw/crashes.json',encoding='utf-8'))
for c in d['A1']+d['A2']:
    c['ped']=any(p[1]=='行人' for p in c['parties'])
# A1 list
def psum(c):
    out=[]
    for big,sub,age,act in c['parties']:
        name=sub if big=='人' else (big or sub or '不明')
        name=name.replace('(含客、貨兩用)','')
        a=f'{age}歲' if age and age.isdigit() and int(age)<120 else ''
        out.append(name+(f'（{a}）' if a else ''))
    return '、'.join(out)
A1=[{'lon':c['lon'],'lat':c['lat'],'d':c['d'],'date':f"{c['date'][:4]}/{c['date'][4:6]}/{c['date'][6:]}",'time':f"{c['time'][:2]}:{c['time'][2:4]}",
     'addr':c['addr'].replace('臺中市',''),'dh':c['dh'].replace(';','，'),'type':c['type'],'cause':c['cause'],'parties':psum(c),
     'moto':c['moto'],'ped':c['ped'],'heavy':c['heavy'],'old':c['old']} for c in d['A1']]
# A2 grid
DX,DY=0.004,0.0036
g=collections.defaultdict(lambda:[0,0,0,0,0])
for c in d['A2']:
    k=(math.floor(c['lon']/DX),math.floor(c['lat']/DY))
    v=g[k]; v[0]+=1; v[1]+=c['moto']; v[2]+=c['heavy']; v[3]+=c['ped']; v[4]+=c['old']
A2=[[round((i+0.5)*DX,4),round((j+0.5)*DY,4)]+v for (i,j),v in g.items()]
print('A2 cells',len(A2),'max',max(x[2] for x in A2), 'sum',sum(x[2] for x in A2))
# road corridor: 臺灣大道
pts=[(c['lon'],c['lat']) for c in d['A1']+d['A2'] if '臺灣大道' in c['addr']]
bins=collections.defaultdict(list)
for lo,la in pts: bins[round(lo/0.006)].append((lo,la))
line=[]
for k in sorted(bins):
    b=bins[k]
    if len(b)>=3: line.append([round(statistics.median(x[0] for x in b),4),round(statistics.median(x[1] for x in b),4)])
print('taiwan blvd pts',len(pts),'line',line)
def med(pred):
    s=[(c['lon'],c['lat']) for c in d['A1']+d['A2'] if pred(c)]
    if not s: return None
    return [round(statistics.median(x[0] for x in s),4),round(statistics.median(x[1] for x in s),4),len(s)]
sites={
 'longjing_port':med(lambda c:c['heavy'] and any(r in c['addr'] for r in ['臨港路','港埠路','中航路']) and c['cls']=='A1'),
 'xinxing':med(lambda c:'龍井區' in c['addr'] and '新興路' in c['addr'] and '遊園南路' in c['addr']),
 'wuqi_zhonghua':med(lambda c:'梧棲區' in c['addr'] and '中華路一段' in c['addr'] and '臺灣大道八段' in c['addr']),
 'beishi':med(lambda c:'沙鹿區' in c['addr'] and '北勢東路' in c['addr']),
 'zhenzheng':med(lambda c:'清水區' in c['addr'] and '鎮政路' in c['addr']),
 'shuntian':med(lambda c:'大甲區' in c['addr'] and ('永順街' in c['addr'] or '新美街' in c['addr'])),
 'zhenlan':med(lambda c:'大甲區' in c['addr'] and any(r in c['addr'] for r in ['順天路','蔣公路','文武路','光明路'])),
}
print(sites)
st=json.load(open('raw/tra_stations.json',encoding='utf-8'))
want=['日南','大甲','臺中港','清水','沙鹿','龍井','大肚','追分']
S={}
for s in st:
    if s['stationName'] in want:
        la,lo=map(float,s['gps'].split()); S[s['stationName']]=[round(lo,5),round(la,5)]
print(S)
yb=json.load(open('raw/youbike_yb2.json',encoding='utf-8'))
D8=['大甲區','大安區','外埔區','清水區','梧棲區','沙鹿區','龍井區','大肚區']
Y=[[round(float(y['lng']),5),round(float(y['lat']),5),y['name_tw'].replace('YouBike2.0_',''),y['district_tw'],y['parking_spaces']] for y in yb if y.get('area_code')=='01' and y['district_tw'] in D8]
print('yb',len(Y),collections.Counter(y[3] for y in Y))
json.dump({'A1':A1,'A2':A2,'blvd':line,'sites':sites,'stations':S,'yb':Y},open('data/layers.json','w'),ensure_ascii=False)
# per-district crash counts
_c=json.load(open('raw/crashes.json',encoding='utf-8'))
_L=json.load(open('data/layers.json',encoding='utf-8'))
_L['a1d']=dict(collections.Counter(c['d'] for c in _c['A1'])); _L['a2d']=dict(collections.Counter(c['d'] for c in _c['A2']))
json.dump(_L,open('data/layers.json','w'),ensure_ascii=False)
