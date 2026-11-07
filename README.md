# 台中海線交通數位地圖｜Coastal Taichung Atlas

還路於民行人路權促進會（Vision Zero Taiwan）製作的互動地圖。把台中海線8區（大甲、大安、外埔、清水、梧棲、沙鹿、龍井、大肚）的交通安全、公共運輸、城鎮連接、人本交通資料疊在同一張圖上，並疊上依荷蘭Sustainable Safety分級的路網，看海線怎麼連到台中市區、苗栗與彰化。

本地圖搭配研究報告〈先補結構，再用推力：台中海線交通推力策略研究〉（2026年11月初稿）使用。

## 地圖上有什麼

- **行政區著色**：11種指標，包括2025年30日死亡率、2026年1–8月死亡、A2事故率、8年人口變化、65歲以上占比、跨區與跨縣市通勤率、YouBike密度、人行安全核定案件
- **事故**：2025年A1事故36件逐點標示（金點＝涉入重型貨車），A2事故10,034件以約400公尺網格彙整
- **公共運輸**：海線台鐵8站（大小＝2025年運量）與區域台鐵車站、臺灣大道走廊、YouBike 2.0站點405站
- **路網**：通過性道路（國道、快速公路）與集散道路（省道、縣道、鄉道、市區幹道）
- **對外連結**：國道、快速公路、省縣道與海線8區外圍行政界的15處交點，依縣市分色
- **研究建議地點**：依推力工具箱L1到L4分層標示，點開可看工具、理由、主責與時程
- **主題導覽**：交通安全、公共運輸、城鎮連接、人本交通四個主題，一鍵切換圖層組合

## 結構

```
index.html              單檔網頁（資料已內嵌，可直接部署）
data/                   處理後的地圖資料
  layers.json           事故點位、A2網格、車站、YouBike、建議地點、各區事故數
  roads.json            道路分級線形與對外連接點
  towns.json            鄉鎮市區界（台中、苗栗、彰化、南投及周邊）
  counties.json         縣市界
  stations_region.json  區域台鐵車站
scripts/                從原始資料重建的腳本，依編號執行
  template.html         網頁模板（__TOWNS__等佔位符由07_assemble.py填入）
raw/                    原始資料下載位置（不進版控）
```

## 重建步驟

1. 把原始資料放進`raw/`：
   - `raw/npa114/114*.csv`：內政部警政署114年A1、A2傷亡道路交通事故資料（data.gov.tw/dataset/177136）
   - `raw/tra_stations.json`：國營臺灣鐵路公司車站基本資料
   - `raw/youbike_yb2.json`：YouBike 2.0站點即時資料
   - `raw/hierarchy.pmtiles`：Taiwanwonnerf的道路分級圖磚
2. 安裝套件：`pip install -r requirements.txt`、`npm install`
3. 在repo根目錄依序執行：

```
python3 scripts/01_crashes.py
python3 scripts/02_layers.py
node scripts/03_boundaries.js
python3 scripts/04_decode_roads.py
python3 scripts/05_merge_roads.py
python3 scripts/06_stations_region.py
python3 scripts/07_assemble.py
```

各區人口、死亡、通勤等數字寫在`scripts/template.html`的`DIST`、`STA`常數中，來源見下方。

## 讀圖注意

- 行政區死亡數與死亡率是交通部道安資訊查詢網的「30日死亡」；A1事故點位來自警政署資料，A1是「24小時內死亡」。2025年海線30日死亡75人、24小時死亡36人，兩者不能混用。
- 大安區人口少，2025年8人死亡就讓死亡率變成45.7，單年數字要保守看。
- 海線鐵路線是依車站順序連線的示意；臺灣大道走廊是用事故地址含「臺灣大道」的點位描出的大致走向。
- 研究建議地點依事故資料地址推估，屬示意位置；市街入口gateway的實際入口點需要現勘。
- 路網為OpenStreetMap分類，不是官方道路分級；鄉道與市區幹道只畫海線範圍，也未計入對外連接點。
- 網頁沒有街道底圖。

## 資料來源

1. 交通部道安資訊查詢網：逐區30日死亡（2019–2026年8月）https://roadsafety.tw
2. 內政部警政署114年傷亡道路交通事故資料 https://data.gov.tw/dataset/177136
3. 國營臺灣鐵路公司每日各站進出站人數 https://data.gov.tw/dataset/8792 、每日時刻表、車站基本資料
4. YouBike 2.0站點資料（2026/11/6快照）
5. 內政部戶政司ODRP014村里別單一年齡人口（2018/09、2026/09）
6. 臺中市主計處109年人口及住宅普查結果分析：通勤率
7. 臺中市建設局永續提升人行安全計畫第1–3波核定案件（2026/3/19）
8. 行政區界：[taiwan-atlas](https://github.com/dkaoster/taiwan-atlas)（內政部國土測繪中心鄉鎮界，簡化版）
9. 道路功能分級：[Taiwanwonnerf](https://yunching0513.github.io/202609---Taiwanwonnerf/)，路網© OpenStreetMap contributors

## 授權

- 程式碼：MIT
- 政府開放資料依[政府資料開放授權條款第1版](https://data.gov.tw/license)使用
- 路網衍生資料（`data/roads.json`）依[ODbL](https://opendatacommons.org/licenses/odbl/)釋出，© OpenStreetMap contributors

---

還路於民行人路權促進會｜Vision Zero Taiwan｜資料截至2026年11月6日
