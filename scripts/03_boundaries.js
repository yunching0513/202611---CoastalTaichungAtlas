const topo=require('./node_modules/topojson-client');
const t=require('./node_modules/taiwan-atlas/towns-10t.json');
const D8=['大甲區','大安區','外埔區','清水區','梧棲區','沙鹿區','龍井區','大肚區'];
const r=a=>Array.isArray(a[0])?a.map(r):[+a[0].toFixed(4),+a[1].toFixed(4)];
const KEEP=['台中市','苗栗縣','彰化縣','南投縣','新竹縣','雲林縣'];
function bb(g){let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;const w=a=>{if(typeof a[0]==='number'){x0=Math.min(x0,a[0]);x1=Math.max(x1,a[0]);y0=Math.min(y0,a[1]);y1=Math.max(y1,a[1]);}else a.forEach(w)};w(g.coordinates);return [x0,y0,x1,y1]}
const towns=topo.feature(t,t.objects.towns).features.filter(f=>{const b=bb(f.geometry);return KEEP.includes(f.properties.COUNTYNAME)&&b[2]>120.1&&b[0]<121.6&&b[3]>23.6&&b[1]<24.9})
 .map(f=>({type:'Feature',properties:{c:f.properties.COUNTYNAME,t:f.properties.TOWNNAME,core:f.properties.COUNTYNAME==='台中市'&&D8.includes(f.properties.TOWNNAME)},geometry:{type:f.geometry.type,coordinates:r(f.geometry.coordinates)}}));
const counties=topo.feature(t,t.objects.counties).features.filter(f=>KEEP.slice(0,4).includes(f.properties.COUNTYNAME)).map(f=>({type:'Feature',properties:{c:f.properties.COUNTYNAME},geometry:{type:f.geometry.type,coordinates:r(f.geometry.coordinates)}}));
console.log(towns.length, counties.map(c=>c.properties.c).join(','));
require('fs').writeFileSync('data/towns.json',JSON.stringify({type:'FeatureCollection',features:towns}));
require('fs').writeFileSync('data/counties.json',JSON.stringify({type:'FeatureCollection',features:counties}));
