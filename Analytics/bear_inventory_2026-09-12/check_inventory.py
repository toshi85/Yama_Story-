from pathlib import Path
import json,re,hashlib,collections
P=Path(__file__).parent
rs=json.loads((P/'incidents.json').read_text());ss=json.loads((P/'sources.json').read_text());env=json.loads((P/'_sources/env_deaths_by_pref_year.json').read_text())
def deaths(r):
 if 'dead' in r:return r['dead']
 m=re.search(r'死亡(\d+)人',r['outcome'])
 return int(m.group(1)) if m else int('死亡' in r['outcome'])
def fy(r):
 m=re.match(r'(\d{4})-(\d{2})',r['date']);return int(m[1])-(int(m[2])<4) if m else int(r['date'][:4])
coverage=[]
for e in env:
 hits=[r for r in rs if r['prefecture'].startswith(e['prefecture']) and fy(r)==e['fiscal_year'] and deaths(r)]
 n=sum(map(deaths,hits));coverage.append({**e,'inventory_deaths':n,'incident_ids':[r['id'] for r in hits],'status':'不足' if n<e['deaths'] else '人数一致' if n==e['deaths'] else '集計範囲の差の確認が必要'})
(P/'fatal_coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2))
required=['date','prefecture','location','terrain','species','victims','activity','outcome','A','B','C','overall','source_refs','published','competition','competition_views']
missing=[(r['id'],k) for r in rs for k in required if k not in r or (isinstance(r[k],str) and not r[k])]
source_ids={s['id'] for s in ss};badrefs=[r['id'] for r in rs if any(s['id'] not in source_ids for s in r['source_refs'])]
badfiles=[s['id'] for s in ss if not Path(s['path']).exists()]
text=(P.parent/'Bear_Incident_Inventory_2026-09-12.md').read_text()
forbidden=re.findall(r'おすすめ|推奨|優先順位|ランキング|狙い目',text)
duplicates=[]
by=collections.defaultdict(list)
for r in rs:by[(r['date'],r['prefecture'],r['location'])].append(r['id'])
duplicates=[dict(key=k,ids=v) for k,v in by.items() if len(v)>1]
checks={'records':len(rs),'missing_required_fields':missing,'bad_source_refs':badrefs,'missing_source_files':badfiles,'forbidden_word_hits':forbidden,'same_date_place_review':duplicates,'jbn_records':sum(any(s['id']=='S1' for s in r['source_refs']) for r in rs),'non_jbn_records':sum(not any(s['id']=='S1' for s in r['source_refs']) for r in rs),'years_descending':all(rs[i]['date'][:4]>=rs[i+1]['date'][:4] for i in range(len(rs)-1)),'unmatched_fatal_pref_years':[c for c in coverage if c['status']=='不足'],'all_national_fatalities_verified':False,'output_sha256':hashlib.sha256(text.encode()).hexdigest()}
(P/'checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in checks.items() if k not in ['same_date_place_review','unmatched_fatal_pref_years']},ensure_ascii=False))
print('不足県年度',[(c['prefecture'],c['fiscal_year'],c['deaths']-c['inventory_deaths']) for c in coverage if c['status']=='不足'])
