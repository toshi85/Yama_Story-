from pathlib import Path
import csv,json,re,hashlib
P=Path(__file__).parent
ROOT=P.parents[2]
def read(n):return json.loads((P/n).read_text())
def save(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
sources=read('reviewed_sources.json')[:2]
sources[0].update(title='日本クマネットワーク『人身事故情報のとりまとめに関する報告書』2011',name='jbn')
sources[1].update(title='山形県第4期ツキノワグマ管理計画',name='yamagata')
for name,sid in [('hokkaido_history','S3'),('hokkaido_2025','S4'),('hokkaido_2026','S5')]:
 d=next(x for x in read('_sources/hokkaido_downloads.json') if Path(x['pdf']).stem==name)
 sources.append(dict(id=sid,name=name,title=d['name'],path=d['pdf'],url=d['url'],sha256=d['sha256'],read='全ページの抽出本文・表・注記を確認'))
scopes={
 'hokkaido_plan':'人身被害・管理計画の概要部分。個別事故は別表S3を使用',
 'hokkaido_plan_appendix':'PDF8–10、PDF11は一部。個別事例の重複はS3へ統合',
 'aomori_plan':'PDF16（印刷12）の人身事故集計、PDF19（印刷15）の死亡言及。ブラウザでも本文確認',
 'iwate_plan':'PDF9・12・13、人身事故推移・状況',
 'akita_plan':'PDF6–10・15、人身被害集計',
 'akita_plan_appendix':'PDF4・7・9–11・13。市町村別年度集計は個別事故として数えない',
 'miyagi_plan':'PDF36–39（印刷32–35）。個別事故49件の表と被害程度の集計',
 'fukushima_plan':'PDF7・28（印刷5・26）。年度別死亡件数を確認',
 'niigata_plan':'PDF5・23。人身被害集計部分',
 'toyama_plan_current':'PDF5・11・20・30。人身被害はPDF11（印刷7）',
 'nagano_plan':'PDF13–14（印刷10–11）。人身被害集計',
 'nagano_plan_appendix':'PDF9–10の様式。個別事例データではない',
 'gifu_plan':'人身被害を記載する箇所の所在確認。個別事故は別添資料を使用',
 'gifu_plan_appendix':'PDF15–17（印刷13–15）。2004–2023年の個別事故表56件',
 'gunma_plan':'人身被害表の所在確認。個別事故は資料編を使用',
 'gunma_plan_appendix':'PDF8（印刷7）。2011–2020年35件38人の表',
 'tochigi_plan':'PDF26–28。PDF27（印刷25）の個別事故表',
 'ishikawa_plan':'PDF18–20（印刷16–18）。年度集計',
 'fukui_plan':'PDF18–20（印刷16–18）。年度・市町村集計',
 'hiroshima_plan':'PDF11–12（印刷8–9）。西中国3県地域の集計',
 'shimane_plan':'PDF12–13（印刷8–9）。西中国3県地域の集計',
 'env_injury':'PDF1–2の死亡人数列を全県・全年度確認。年度区切り。個別事故の出典にはしない',
 'env_2025_overview':'PDF1全体。2025年度死亡事故13件の日付・市町村',
 'env_2026_overview':'PDF1全体。2026年度死亡事故6件の日付・市町村',
 'iwate_2026_incidents':'PDF1–7全表・脚注。2018–2026年度。重傷・死亡・複数被害を抽出',
 'akita_2025_incidents':'PDF1全表・脚注。59件67人',
 'akita_2026_incidents':'PDF1全表・脚注。7件7人',
 'akita_2020_incidents':'PDF1–6全抽出本文。事故番号2–7の6件',
 'akita_2022_incidents':'PDF1–6全抽出本文。事故番号1–6の6件',
 'aomori_death2024':'2024年6月25日公開の記事本文全段落。2021年10月事故への言及も確認',
 'aomori_death2026':'2026年7月1日記事の見出し・冒頭段落（続きは未確認）',
 'fukushima_death2010':'2010年7月21日記事本文、喜多方市の死亡事例を記載する第2段落',
 'fukushima_death2024':'2024年10月2日記事本文全3段落',
 'fukushima_death2022':'2022年7月27日記事の公開部分第1–2段落。以降は有料で未確認',
 'aizumisato2013_yomiuri':'2017年5月11日・第4ページ本文。現地調査を行った研究者本人の報告',
 'towari_expert1':'2017年5月11日・第1ページ本文全体。現地関係者への聞き取り調査報告',
 'towari_expert2':'同第2ページ本文全体。死亡事例に関する個体同定の推論は断定に用いない',
 'towari_expert3':'同第3ページ本文全体。2016年5月25日の負傷事例と現地状況',
 'akita_death2017':'2017年5月27日記事の公開第1段落。以降有料部分は未確認',
 'toyama_death2023':'2023年10月18日記事本文全段落。県警・現地取材',
 'nagano_death2023':'2023年10月17日記事本文全段落。わなと現場確認者への取材',
 'nagano_death2025':'2025年6月23日記事本文全段落。負傷した同行者への直接取材',
 'miyagi_death2025':'2025年10月3日県発表本文全体。発表時点は負傷表記、死亡は環境省概要で補完',
 'yamagata_death2026':'2026年5月25日県発表本文全体。県警の調査結果で死亡原因を確認',
 'yamagata_death2026_news_full':'2026年5月8日記事第1ページ全体。男性78歳の身元確認。第2–4ページは未確認',
 'sankebetsu_official':'苫前町郷土資料館ページ「三毛別（三渓）ヒグマ事件」全文',
 'niigata_death2020_mainichi':'2020年10月13日記事の公開本文2段落。以降の有料部分は未確認',
 'expert_kako2':'2011年7月23日付「福島県西会津町での死亡事故について」全文。具体的な事故年月日・年齢・性別・活動は記載なし',
 'niigata_death2020':'2020年10月21日記事第1ページ全文、19年ぶりの死者の項。第2ページは未確認',
 'akita_expert2018':'2018年5月11日・第3ページ本文全体。現地調査者本人の報告。1983・1993・2000・2007年死亡事例を確認',
}
for name,scope in scopes.items():
 f=P/'_sources'/f'{name}_retrieval.json'
 if not f.exists():continue
 d=json.loads(f.read_text())
 if 'file' not in d:continue
 sources.append(dict(id=f'S{len(sources)+1}',name=name,title=name,path=d['file'],url=d['url'],sha256=d['sha256'],read=scope))
for name,title,path,url,scope in [
 ('hachimantai_fire','鹿角広域行政組合消防年報（平成24年）','Yama_Story/Scripts/2012年八幡平クマ牧場事件/research/fire2012.txt','https://www.fdkazuno.jp/img/nenpou24.pdf','PDF75（印刷62）災害記録2012年4月20日の項'),
 ('hachimantai_news','秋田魁新報・2012年4月20日の報道説明文保存資料','Yama_Story/Scripts/2012年八幡平クマ牧場事件/research/sakigake_20120420_description.txt','https://www.youtube.com/watch?v=H5HNvZ0ywL4','保存された説明欄本文全体を確認。映像は今回の確認範囲に含まない')]:
 sources.append(dict(id=f'S{len(sources)+1}',name=name,title=title,path=path,url=url,read=scope,sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest()))
ids={s['name']:s['id'] for s in sources}
records=read('hokkaido_records.json')
for r in records:r['source_refs'][0]['name']='hokkaido_history'
# Merge JBN/Hokkaido repetitions, preserving the conflicts between sources.
for a in csv.DictReader((P/'jbn_records.psv').open(),delimiter='|'):
 r=dict(date=a['年月日'],prefecture=a['都道府県'],location=a['市町村・場所'],terrain=a['場所の性格'],species='ヒグマ' if a['都道府県']=='北海道' else 'ツキノワグマ',victims=a['被害者'],activity=a['行動'],outcome=a['結果'],B=a['B根拠'],C=a['C根拠'],source_refs=[dict(id='S1',name='jbn',range=a['JBN冊子ページ・節'])],key=a['照合キー'],notes='')
 if r['prefecture']=='北海道':
  year=r['date'][:4];town=r['location'].split('町')[0]+'町'
  matches=[x for x in records if x['date'].startswith(year) and (town in x['location'] or (year=='1970' and '登山' in x['activity']) or (year=='2010' and '帯広' in x['location']))]
  if len(matches)!=1:raise ValueError(('hokkaido merge',r['date'],len(matches)))
  dst=matches[0];dst['source_refs']+=r['source_refs'];dst['terrain']=r['terrain'];dst['location']=r['location'];dst['activity']=r['activity'];dst['key']=r['key']
  if year in ['2004','2006','2008']:dst['notes']+=f"S1では日付{r['date']}・結果{r['outcome']}。S3との相違を保持。"
  continue
 records.append(r)
# Yamagata victim rows: merge only explicit paired/linked incidents.
ys=read('yamagata_rows.json');skip={4,5,6,63,71,73,74,108}
groups={62:[62,63],70:[70,71],72:[72,73,74]}
days={35:18,49:21,52:29,70:12,72:14,80:18}
for i,a in enumerate(ys):
 if i in skip:continue
 group=[ys[j] for j in groups.get(i,[i])];content=a['content'];loc=content.split('(')[0].strip();activity=content[len(loc):].strip('() ') or '不明（S2の当該行に活動記載なし）'
 pref='山形県'
 for pr in ['秋田県','新潟県','宮城県']:
  if loc.startswith(pr):pref=pr;loc=loc[len(pr):]
 if i==62:activity='クリ拾いと同伴'
 if i==70:activity='夫婦が自宅玄関に出た際'
 if i==72:activity='自宅玄関、農作業、中学校敷地内の用務員への連続被害'
 date=f"{a['year']:04}-{a['month']:02}"+(f'-{days[i]:02}' if i in days else '（日不明）')
 records.append(dict(date=date,prefecture=pref,location=loc,terrain='不明（S2は地名・活動まで。詳細地形なし）',species='ツキノワグマ',victims=f"{len(group)}人："+'・'.join(x['sex'] for x in group)+'／年齢・職業不明（S2表に欄なし）',activity=activity,outcome='・'.join(x['result'] for x in group),n=len(group),source_refs=[dict(id='S2',name='yamagata',pdf_pages=[a['pdf_page']],range=f"印刷p.{a['printed_page']}の当該年月・場所の行")],notes='同年月・同所の男女の被害は連続事件か未確定のため別行を保持。' if i in [105,106] else '',key=''))
for r in records:
 if r['prefecture']=='山形県' and r['date'].startswith('1988'):
  r['source_refs'].append(dict(id='S2',name='yamagata',pdf_pages=[42],range='印刷p.40の1988年の行'))
for r in read('recent_records.json'):
 r['location']=r['location'].replace('雫石町雫石町','雫石町')
 if r['date']=='2023-08-19' and '雫石町' in r['location']:r['notes']+='県表の別事故番号17（男性・5時10分）と18（女性・5時20分）を別行で保持。同一個体の確証は当該表にない。'
 if r['date']=='2026-04-21' and '紫波町' in r['location']:r['notes']+='県表の事故番号1（捜索者負傷）と2（女性遺体発見）を別行で保持。関連性の確定には追加資料が必要。'
 r['source_refs']=[dict(id=ids[r['source_name']],name=r['source_name'],pdf_pages=[r['pdf_page']],range='当該年月日・場所の行／事故記録')];records.append(r)
for a in csv.DictReader((P/'plan_supplement.psv').open(),delimiter='|'):
 a['n']=int(a['n']);a['species']='ツキノワグマ';a['victims']=str(a['n'])+'人：'+a['victims']+('' if re.search('会社員|飼育員|看護助手|無職|自営業',a['victims']) else '／職業不明（当該出典に記載なし）')
 a['source_refs']=[dict(id=ids[a['source_name']],name=a['source_name'],pdf_pages=[int(a['pdf_page'])] if int(a['pdf_page']) else [],range='当該事故の記述')]
 if a['key'] in ['三毛別','八幡平クマ牧場']:a['species']='ヒグマ'
 if a['key']=='八幡平クマ牧場':a['source_refs'].append(dict(id=ids['hachimantai_fire'],name='hachimantai_fire',pdf_pages=[75],range='印刷p.62・2012年4月20日'))
 if a['source_name']=='yamagata_death2026_news_full':a['source_refs'].append(dict(id=ids['yamagata_death2026'],name='yamagata_death2026',range='2026年5月25日県発表本文'))
 if a['source_name']=='miyagi_death2025':a['source_refs'].append(dict(id=ids['env_2025_overview'],name='env_2025_overview',pdf_pages=[1],range='10月3日栗原市の行'))
 records.append(a)
def classify(r):
 act=r['activity'].replace('<調査中>','不明（調査中）');where=r['terrain'];vic=r['victims']
 r['A']='○：1960年以降' if int(r['date'][:4])>=1960 else '×：1960年より前'
 b=r.get('B');c=r.get('C')
 # Occupation alone is not a reason to exclude an ordinary visitor.
 if b and b.startswith('不明') and re.search('職業(記載)?なし|職業不明|職業記載なし',b):b=None
 if b is None:
  if '不明' in act:b='不明：当該出典で現場にいた役割を確認できない'
  elif re.search('狩猟|駆除|有害.*捕獲|シカ猟|クマ.*捕獲|捕獲わな|わなの確認|止め刺し|勢子|調査|捜索|パトロール|放獣|捕獲活動',act):b='×：捕獲・調査・捜索等の役割で現場にいた'
  elif '不明' in act:b='不明：当該出典で現場にいた役割を確認できない'
  else:b='○：記録上は一般の利用者・住民としての行動。職業自体は未確認'
 if c is None:
  if act=='不明（調査中）':c='不明：被害時の活動は行政資料で調査中'
  elif re.search('自宅|台所|農作業|栽培|作業|通学|登校|下校|通勤|帰宅|配達|駆除|狩猟|捕獲|調査|捜索|パトロール|放獣|見回り|確認|精米|戸締|掃除|草|庭|墓参|ゴミ|水口|水位|施設|配電線',act):c='×：仕事・日常生活・施設等での被害'
  elif re.search('登山|山行|沢登り|釣り|つり|山菜|タケノコ|キノコ|きのこ|コゴミ|フキ|ワラビ|クリ拾|クルミ|ギョウジャ|ネマガリ|キャンプ',act):c='○：任意の登山・採取・釣り等で訪れた'
  elif re.search('集落|市街|住宅|自宅|施設|生活圏',where):c='×：生活圏・施設での被害'
  else:c='不明：任意の対象活動・場所かを当該出典から確定できない'
 if r.get('key')=='乗鞍岳':b='○：中心となる一般観光客を基準。従業員の被害も併記';c='○：一般観光客が登山口・遊歩道を訪問'
 if '卒論' in act:b='×：野生動物の研究調査で現場にいた'
 if '新聞配達' in act:b='○：報道取材ではなく通常の配達業務'
 if '女性は農作業、男性はクマの勢子'==act:b='○：一般の農作業者への被害を中心とする'
 if r['date']=='2013-05-27・28' and r['prefecture']=='福島県':b='○：中心は一般の山菜採り男性。警官等の続発被害も併記';c='○：最初の被害者は任意の山菜採り'
 if r.get('source_name')=='fukushima_death2024':c='不明：今回もキノコ採りだったかは確認した記事で未確定'
 if r.get('key')=='八幡平クマ牧場':b='×：飼育員として現場にいた';c='×：飼育施設内での業務'
 if r.get('key')=='三毛別':b='○：開拓地の一般住民';c='×：生活する開拓地の住宅での被害'
 r['B'],r['C']=b,c
 r['overall']='除外' if any(x.startswith('×') for x in [r['A'],b,c]) else '条件合致' if all(x.startswith('○') for x in [r['A'],b,c]) else '不明'
for r in records:
 if r['date'].startswith('1983') and r['prefecture']=='秋田県':
  r['notes']+='S1の引用新聞年月は1992年だが、現地調査者の2018年報告は1983年6月24日と記述。資料間の記載差を保持。'
  r['source_refs'].append(dict(id=ids['akita_expert2018'],name='akita_expert2018',range='第3ページ〈1〉旧田沢湖町玉川地区'))
 if r['date'].startswith('2007-06') and r['prefecture']=='秋田県' and '死亡' in r['outcome']:
  r['date']='2007-06-13（研究者報告）';r['victims']='1人：男性63歳／職業不明（確認資料に記載なし）';r['activity']='タケノコ採り';r['terrain']='鳥海山北麓の山中'
  r['source_refs'].append(dict(id=ids['akita_expert2018'],name='akita_expert2018',range='第3ページ〈3〉鳥海山北麓'))
 if r.get('source_name')=='miyagi_plan' and r['date']=='2019-07-11':r['source_refs'].append(dict(id='S2',name='yamagata',pdf_pages=[43],range='印刷p.41・県外参考2019年7月蔵王町の行'))
 classify(r)
views={'福岡大':2292947,'大千軒':2164129,'羅臼':979136,'星野':659365,'三毛別':499414,'乗鞍岳':446685,'太郎平':275240}
published={'福岡大','大千軒','羅臼','星野','三毛別','乗鞍岳','朱鞠内','風不死','東成瀬','十和利','石狩沼田','丘珠','熊倉山'}
draft={'戸沢村','八幡平クマ牧場','立山'}
for r in records:
 key=r.get('key','');t=r['location'];year=r['date'][:4]
 for y,term,k in [('1970','日高','福岡大'),('1976','千歳','風不死'),('2023','幌加内','朱鞠内'),('2023','福島','大千軒'),('2025','斜里','羅臼')]:
  if year==y and term in t:key=k
 r['key']=key;r['published']='●既出（投稿実績）' if key in published else '●既出（Scripts）' if key in draft else '―（指定資料に一致なし）'
 r['competition']='◆競合既出' if key in views else '―（指定142タイトルに一致なし）';r['competition_views']=views.get(key,0)
records.sort(key=lambda r:tuple(int(x) for x in re.findall(r'\d+',r['date'])[:3])+(-1,),reverse=True)
for i,r in enumerate(records,1):r['id']=f'B{i:04}'
save('sources.json',sources);save('incidents.json',records)
stats=dict(total=len(records),eligible=sum(r['overall']=='条件合致' for r in records),excluded=sum(r['overall']=='除外' for r in records),unknown=sum(r['overall']=='不明' for r in records),jbn=sum(any(s['id']=='S1' for s in r['source_refs']) for r in records),non_jbn=sum(not any(s['id']=='S1' for s in r['source_refs']) for r in records),competition_absent=sum(not r['competition_views'] for r in records),death_records=sum('死亡' in r['outcome'] for r in records))
save('counts.json',stats)
out=['# クマ人身事故一覧（2026年9月12日調査）','', '**照合作業中。全国の死亡事例の全件収録は未確認。** 年度別死亡統計に対する不足と未確認範囲は[未完了表](bear_inventory_2026-09-12/unresolved.md)と[死亡照合表](bear_inventory_2026-09-12/fatal_coverage.json)に記載する。','',f"収録{stats['total']}件／条件合致{stats['eligible']}件／除外{stats['excluded']}件／不明{stats['unknown']}件。S1掲載{stats['jbn']}件、S1以外{stats['non_jbn']}件。",'',
 'A＝1960年以降。B＝中心となる一般被害者を基準とし、捕獲・研究・捜索等の役割で現場にいた場合を区別する。C＝任意の登山・採取・釣り・沢登り・キャンプ等。仕事・通勤通学・市街地・自宅敷地・施設内等は除外。職業不明と現場での役割不明は区別する。','',
 '被害者数は負傷・死亡した人数。同行者数とは分ける。資料の重傷・軽傷区分を保持し、診断から独自に変更しない。遺体発見日、疑い例、資料間の日付・人数の差も記載する。同一個体の確証がない事例は、年月・地域が同じという理由だけでは統合しない。','',
 '●既出は Video_Performance_Log.md と Scripts の照合。◆競合既出は Next_Topic_Candidates_2026-09-12.md の142タイトルとの一致。同一事件の一致動画は再生数を合算する。「一致なし」はこの資料範囲に限る。YouTube全体の不存在や動画内容の確認を意味しない。','',
 '以下は新しい年順。各資料のページはPDFページを原則とし、S1は冊子の印刷ページを併記する。個別行の不明項目は当該出典の確認範囲に値がないもの。','']
last=None
for r in records:
 if r['date'][:4]!=last:last=r['date'][:4];out+=['## '+last+'年','']
 refs=[]
 for s in r['source_refs']:
  refs.append(s['id']+(' PDF '+','.join(map(str,s.get('pdf_pages',[]))) if s.get('pdf_pages') else '')+' '+s.get('range',''))
 out+=[f"### {r['id']}　{r['date']}　{r['prefecture']} {r['location']}",'',f"- 場所：{r['terrain']}。種類：{r['species']}。",f"- 被害者：{r['victims']}。行動：{r['activity']}。結果：{r['outcome']}。",f"- A {r['A']}／B {r['B']}／C {r['C']}。総合：**{r['overall']}**。",f"- {r['published']}／{r['competition']}／一致動画の合計再生数：{r['competition_views']:,}。",f"- 出典：{'；'.join(refs)}。"]
 if r.get('notes'):out+=['- 注記：'+r['notes']]
 out+=['']
out+=['## 出典と確認範囲','']
for s in sources:
 out+=[f"### {s['id']}　{s['title']}",'',f"- 確認範囲：{s['read']}。",f"- 保存資料：`{s['path']}`。"]
 if s.get('url'):out+=['- URL：'+s['url']]
 out+=['']
(P.parent/'Bear_Incident_Inventory_2026-09-12.md').write_text('\n'.join(out))
print(json.dumps(stats,ensure_ascii=False))
