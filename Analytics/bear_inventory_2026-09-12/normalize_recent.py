"""Normalize the downloaded prefectural incident tables; retain source row references."""
from pathlib import Path
import re,json,unicodedata
P=Path(__file__).parent
def norm(t):return unicodedata.normalize('NFKC',t)
records=[]
def add(date,pref,location,terrain,victims,activity,outcome,name,page,n=1,notes='',key=''):
 records.append(dict(date=date,prefecture=pref,location=location,terrain=terrain,species='ツキノワグマ',victims=f'{n}人：{victims}／職業不明（当該表・記録に職業欄なし）',activity=activity,outcome=outcome,n=n,source_name=name,pdf_page=page,notes=notes,key=key))
# Iwate: single-person rows are regular; merged cells are transcribed separately below.
for r in json.loads((P/'iwate_table_rows.json').read_text()):
 c=r['cells'];m=re.search(r'(令和|平成)(\d+|元)年(\d+)月(\d+)日',c[1])
 if not m:continue
 era,y,mo,d=m.groups();date=f'{(2018 if era=="令和" else 1988)+(1 if y=="元" else int(y)):04}-{int(mo):02}-{int(d):02}'
 if (date,int(c[0])) in [('2020-09-19',21),('2019-05-04',2)]:continue
 try: j=next(i for i,v in enumerate(c) if re.fullmatch(r'.+[市町村]',v))
 except StopIteration:continue
 rest=c[j+2:]
 if len(rest)<5 or not re.fullmatch(r'\d+代|不明',rest[1]) or rest[2] not in ['男性','女性','不明']:continue
 activity,age,sex,outcome=rest[:4]
 if not any(v in outcome for v in ['重傷','死亡']):continue
 if activity.endswith('途'):activity='作業小屋に向かう途中'
 terrain='里（県区分。詳しい地形未記載）' if '里' in rest[4:] else '山（県区分。詳しい地形未記載）'
 notes=''
 if '※' in c[1] or '※' in outcome:notes='日付は遺体発見日。県警がクマによる被害の可能性が高いと判断し計上。'
 if date=='2024-05-16':notes='5月13日遭難、5月16日付で被害計上。県警はクマ関与が非常に高いと判断。'
 if date=='2025-10-17':notes+='環境省の事故概要は10月16日。日付不一致を保持。'
 add(date,'岩手県',c[j]+c[j+1],terrain,age+sex,activity,outcome,'iwate_2026_incidents',r['page'],notes=notes)
for date,loc,act,victims,outcome,n,page,terrain in [
 ('2025-05-05','八幡平市松尾','山菜・きのこ採り','20代男性・30代男性','重傷1人・軽傷1人',2,2,'山'),
 ('2023-04-27','八幡平市野駄','山菜・きのこ採り','70代男性・70代女性','軽傷2人',2,4,'山'),
 ('2023-10-15','花巻市大迫町','シカ有害捕獲作業','70代男性2人','重傷2人',2,4,'山'),
 ('2023-10-19','八幡平市兄川','山菜・きのこ採り','70代男性・70代女性','男性重傷・女性死亡',2,4,'山'),
 ('2022-05-23','岩泉町釜津田','山菜・きのこ採り','70代男性2人','重傷2人',2,5,'山'),
 ('2020-08-13','釜石市栗林町','物音の確認','60代男性2人','重傷1人・軽傷1人',2,6,'里'),
 ('2020-09-19','花巻市太田','女性は農作業、男性はクマの勢子','70代女性・70代男性','重傷2人',2,6,'山'),
 ('2019-05-04','岩手町一方井','山菜採り','60代男性2人','重傷1人・軽傷1人',2,6,'山')]:
 add(date,'岩手県',loc,terrain+'（県区分）',victims,act,outcome,'iwate_2026_incidents',page,n)
# Akita 2025/2026: single-person entries and explicit multi-person blocks.
for year in [2025,2026]:
 name=f'akita_{year}_incidents'
 for l in norm((P/'_sources'/f'{name}.txt').read_text()).splitlines():
  m=re.match(r'^\s*(\d+)\s+1\s+(\d{4}/\d+/\d+)\s+(.+)',l)
  if not m:continue
  seq,date,body=m.groups()
  a=re.match(r'.*?\s+(.+?)\s+(山|里)\s+(.+?)\s+(\d+代)\s+(男性|女性)\s+(.+?)\s*$',body)
  if not a:continue
  loc,terrain,act,age,sex,outcome=a.groups()
  if '重傷' not in outcome and '死亡' not in outcome:continue
  notes='県表は11月2日、環境省の死亡事故概要は11月3日。日付不一致。' if date=='2025/11/02' else ''
  add(date.replace('/','-'),'秋田県',re.sub(r'\s+','',loc),terrain+'（県区分）',age+sex,act,outcome,name,1,notes=notes)
for date,loc,act,vic,out,n,key in [
 ('2025-09-18','鹿角市八幡平坂比平','配電線設備の点検','50代男性・20代男性','軽傷2人',2,''),
 ('2025-10-20','湯沢市清水町・表町・材木町','買い物帰り、犬の散歩、施設巡回、自宅敷地','60代男性2人・50代男性・70代男性','重傷3人・軽傷1人',4,''),
 ('2025-10-24','東成瀬村田子内字田子内','70代男女は畑作業、60代・30代男性は救助','70代男女、60代男性、30代男性','30代男性死亡・他3人重傷',4,'東成瀬'),
 ('2025-11-09','五城目町馬場目字中村','自宅敷地内','70代女性・50代女性','重傷2人',2,'')]:
 add(date,'秋田県',loc,'里（県区分）',vic,act,out,'akita_2025_incidents',1,n,key=key)
# Detailed official accident sheets (all extracted text reviewed).
for year in [2020,2022]:
 name=f'akita_{year}_incidents'
 for page,t in enumerate((P/'_sources'/f'{name}.txt').read_text().split('\f'),1):
  if not t.strip():continue
  def field(label):
   m=re.search(label+r'\s+([^\n]+)',t);return m.group(1).strip() if m else '不明'
  dm=re.search(r'年月日\s+令和(\d+)年(\d+)月(\d+)日',t)
  if not dm:continue
  y,mo,d=map(int,dm.groups());date=f'{y+2018:04}-{mo:02}-{d:02}'
  vic=field('年齢・性別');n=2 if 'Ａ：' in vic else 1
  out=field('被害状況')
  add(date,'秋田県',field('住所'),field('山/里の別')+'（詳細は出典の環境欄）',vic,field('行動目的'),out,name,page,n)
(P/'recent_records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print(json.dumps({'records':len(records),'death_records':sum('死亡' in r['outcome'] for r in records)},ensure_ascii=False))
