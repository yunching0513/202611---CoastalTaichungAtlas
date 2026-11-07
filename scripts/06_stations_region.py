import json
st=json.load(open('raw/tra_stations.json',encoding='utf-8'))
core=['日南','大甲','臺中港','清水','沙鹿','龍井','大肚','追分']
out=[]
for s in st:
    la,lo=map(float,s['gps'].split())
    if 120.25<lo<121.2 and 23.85<la<24.72 and s['stationName'] not in core:
        out.append([round(lo,5),round(la,5),s['stationName']])
json.dump(out,open('data/stations_region.json','w'),ensure_ascii=False)
