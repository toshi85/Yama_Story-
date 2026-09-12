from pathlib import Path
import re,json,unicodedata
p=Path(__file__).parent
ps=(p/'_sources/hokkaido_history.txt').read_text().split('\f')
records=[]
pat=re.compile(r'(\d{4})\.\s*(\d{1,2})\.\s*(\d{1,2})\s+(\S+)\s+(\S+)\s+(\S+)\s+([男女])\s+(\S+)\s+(死亡|重傷|負傷|軽傷)')
for page,t in enumerate(ps,1):
 for line in t.splitlines():
  s=unicodedata.normalize('NFKC',line);m=pat.search(s)
  if not m:continue
  y,mo,day,region,city,act,sex,age,out=m.groups()
  records.append({'date':f'{int(y):04}-{int(mo):02}-{int(day):02}','prefecture':'北海道','location':city,'terrain':'不明（S3は市町村・活動内容まで）','species':'ヒグマ','victims':f'1人：{sex}性{age}／職業不明（S3に職業欄なし）','activity':act,'outcome':out,'n':1,'dead':int(out=='死亡'),'injured':int(out!='死亡'),'source_refs':[{'id':'S3','pdf_pages':[page],'range':'当該年月日・市町村の行'}],'raw':line,'notes':'','key':''})
# Merged-cell entries are transcribed separately. All 3 PDF pages were read.
special=[
('1964-09-30','白滝村','2人：男性64歳死亡・男性27歳重傷／クマ駆除従事','クマ駆除','死亡1人・重傷1人',2,1,1,1,''),
('1970-07-26・27','中札内村・日高山脈','3人：男性18歳・19歳・20歳／大学生（S1）','縦走登山','死亡3人',3,3,0,1,'福岡大'),
('1976-06-04～09','千歳市・風不死岳（照合名称）','5人：男性56歳・53歳・26歳負傷、男性58歳・54歳死亡／職業不明','4日山林作業、5・9日山菜採り','死亡2人・負傷3人',5,2,3,1,'風不死岳'),
('1999-05-08・11','木古内町大川・チリチリ川（詳細S1）','3人：男性47歳、女性39歳・50歳／職業不明','8日川釣り、11日山菜採り','死亡1人・負傷2人（S3）；S1は女性2人を重傷と記載',3,1,2,2,'木古内'),
('2004-11-26','新冠町岩清水（詳細S1）','2人：男性67歳重傷・男性65歳軽傷／狩猟者（S1）','S3クマ駆除；S1送電線点検同行後の捕獲','重傷1人・軽傷1人（S3）；S1は重傷2人',2,0,2,2,''),
('2005-10-04','穂別町','2人：男性58歳重傷・男性71歳軽傷／狩猟者','狩猟','重傷1人・軽傷1人',2,0,2,2,''),
('2006-10-14','浜中町','2人：男性62歳・59歳／クマ狩猟者','クマ狩猟','死亡2人（S3）；S1 p31は死亡1人・負傷1人',2,2,0,2,''),
('2011-08-24','遠軽町','2人：男性61歳2人／駆除従事','クマ駆除','軽傷1人・重傷1人',2,0,2,2,''),
('2021-06-18','札幌市東区','4人：男性75歳軽傷・女性80代負傷（ごみ出し）、男性40代重傷（歩行）、男性43歳負傷（自衛隊警備）／他職業不明','市街地のごみ出し・歩行・自衛隊警備','重傷1人・軽傷1人・負傷2人',4,0,4,3,''),
('2021-08-07','津別町','2人：女性66歳・39歳／職業不明','農作業','負傷2人',2,0,2,3,''),
('2022-03-31','札幌市','2人：男性47歳・58歳／冬眠穴調査従事','冬眠穴調査','負傷2人',2,0,2,3,''),
('2022-07-15','松前町','2人：男性81歳・女性78歳／職業不明','農作業','負傷2人',2,0,2,3,''),
('2023-10-13','阿寒町（S3表記）','1人：男性52歳／職業不明','林道を自転車で走行','負傷',1,0,1,3,''),
('2023-10-29・31','福島町・大千軒岳（照合名称）','3人：男性22歳死亡、男性41歳2人負傷／職業はS3未記載','登山','死亡1人・負傷2人',3,1,2,3,'大千軒岳'),
('2023-11-21','滝上町','2人：男性49歳・女性58歳／狩猟者','狩猟','負傷2人',2,0,2,3,''),
('2025-10-04','小樽市桃内（S4）','2人：男性75歳・68歳／捕獲従事者','シカ用くくりわなのヒグマ錯誤捕獲への対処','負傷2人',2,0,2,3,''),
]
# Single-line members of the explicitly merged groups must not be counted twice.
replace_dates={'1964-09-30','1970-07-26','1970-07-27','1976-06-04','1976-06-05','1976-06-09','1999-05-08','1999-05-11','2004-11-26','2005-10-04','2006-10-14','2011-08-24','2021-06-18','2021-08-07','2022-03-31','2022-07-15','2023-10-13','2023-10-29','2023-10-31','2023-11-21','2025-10-04'}
# 1970-07-27 Shibetsu is a separate ordinary row.
records=[r for r in records if r['date'] not in replace_dates or (r['date']=='1970-07-27' and r['location']=='士別市')]
for date,loc,victims,act,out,n,d,inj,page,key in special:
 records.append(dict(date=date,prefecture='北海道',location=loc,terrain='不明（S3は市町村・活動内容まで）',species='ヒグマ',victims=victims,activity=act,outcome=out,n=n,dead=d,injured=inj,source_refs=[{'id':'S3','pdf_pages':[page],'range':'当該年月日・市町村の行'}],raw='',notes='同一事故・連続事案を1件にまとめた行。公式の発生件数とは集計単位が異なる場合がある。' if n>1 else '',key=key))
for r in records:
 if r['date'] in ['2020-05-15','2021-07-12','2021-11-24']:r['notes']+='S3はヒグマによる可能性が極めて高い事例として記載。原因確定とは区別。'
 if r['date']=='2026-07-17':r['notes']+='活動はS3の2026-08-04時点で調査中。'
(p/'hokkaido_records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
summary={'rows':len(records),'victims':sum(r['n'] for r in records),'deaths':sum(r['dead'] for r in records),'injured':sum(r['injured'] for r in records),'official_deaths':61,'official_victims':188}
(p/'hokkaido_parse_check.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary))
