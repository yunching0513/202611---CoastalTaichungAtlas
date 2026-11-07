import csv, glob, json, re, statistics, collections, sys
D8=['大甲區','大安區','外埔區','清水區','梧棲區','沙鹿區','龍井區','大肚區']
def dist(addr):
    for d in D8:
        if addr.startswith('臺中市'+d) or addr.startswith('台中市'+d): return d
    return None
crashes={}
for f in sorted(glob.glob('raw/npa114/114*.csv')):
    for row in csv.DictReader(open(f,encoding='utf-8-sig',errors='replace')):
        addr=row['發生地點']; d=dist(addr)
        if not d: continue
        key=(row['事故類別名稱'],row['發生日期'],row['發生時間'],addr,row['經度'],row['緯度'])
        c=crashes.setdefault(key,{'cls':row['事故類別名稱'],'date':row['發生日期'],'time':row['發生時間'],'addr':addr,'d':d,
            'lon':row['經度'],'lat':row['緯度'],'dh':row['死亡受傷人數'],'type':row['事故類型及型態大類別名稱']+'／'+row['事故類型及型態子類別名稱'],
            'cause':row['肇因研判子類別名稱-主要'],'parties':[]})
        c['parties'].append((row['當事者區分-類別-大類別名稱-車種'],row['當事者區分-類別-子類別名稱-車種'],row['當事者事故發生時年齡'],row['當事者行動狀態子類別名稱']))
HEAVY=('大貨車','曳引車','半聯結車','全聯結車')
def flags(c):
    big=[p[0] for p in c['parties']]; sub=[p[1] for p in c['parties']]
    moto= any('機車' in b for b in big)
    ped = any(b=='人' or '行人' in b or '行人' in s for b,s in zip(big,sub))
    heavy=any(any(h in s or h in b for h in HEAVY) for b,s in zip(big,sub))
    old=False
    for p in c['parties']:
        try:
            if int(p[2])>=65: old=True
        except: pass
    return moto,ped,heavy,old
A1=[];A2=[]
for c in crashes.values():
    m,p,h,o=flags(c)
    try: lon=float(c['lon']); lat=float(c['lat'])
    except: continue
    rec=dict(c); rec.update(moto=m,ped=p,heavy=h,old=o,lon=lon,lat=lat)
    (A1 if c['cls']=='A1' else A2).append(rec)
def pct(L,k): n=sum(1 for x in L if x[k]); return n, round(100*n/len(L),1)
print('A1',len(A1),{k:pct(A1,k) for k in ['moto','old','heavy','ped']})
print('A2',len(A2),{k:pct(A2,k) for k in ['moto','old','heavy','ped']})
print('A1 deaths', sum(int(re.search(r'死亡(\d+)',c['dh']).group(1)) for c in A1))
# party big categories sample
print(collections.Counter(p[0] for c in A1 for p in c['parties']).most_common(12))
json.dump({'A1':A1,'A2':A2},open('raw/crashes.json','w'),ensure_ascii=False)
