"""把scripts/template.html與data/*.json組成單檔index.html"""
rd=lambda f: open(f,encoding='utf-8').read()
s=rd('scripts/template.html')
s=(s.replace('__TOWNS__',rd('data/towns.json')).replace('__COUNTIES__',rd('data/counties.json'))
    .replace('__ROADS__',rd('data/roads.json')).replace('__REGSTA__',rd('data/stations_region.json'))
    .replace('__LAYERS__',rd('data/layers.json')))
open('index.html','w',encoding='utf-8').write(s)
print('index.html', len(s))
