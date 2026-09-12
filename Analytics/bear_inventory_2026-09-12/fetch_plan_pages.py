from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,requests,bs4
p=Path(__file__).parent/'_sources'
names=['北海道','青森','岩手','秋田','宮城','福島','新潟','富山','長野','岐阜','群馬','栃木','石川','福井','広島','島根']
links=json.loads((p/'plan_links.json').read_text())
def fetch(item):
 name=next(n for n in names if n in item['title']);u=item['url'];result={'prefecture':name,'url':u}
 try:
  r=requests.get(u,timeout=15);r.raise_for_status();r.encoding=r.apparent_encoding;s=bs4.BeautifulSoup(r.text,'html.parser');(p/(name+'_plan_page.html')).write_text(r.text);(p/(name+'_plan_page.txt')).write_text(s.get_text('\n',strip=True))
  result['links']=[{'title':a.get_text(' ',strip=True),'url':requests.compat.urljoin(u,a['href'])} for a in s.select('a[href]') if any(w in a.get_text() for w in ['クマ','ヒグマ','鳥獣保護','特定鳥獣','人身','管理計画']) or a['href'].lower().endswith('.pdf')]
 except Exception as e:result['error']=str(e)
 return result
items=[i for i in links if any(n in i['title'] for n in names)]
with ThreadPoolExecutor(max_workers=8) as pool:res=list(pool.map(fetch,items))
(p/'plan_page_results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
for r in res:print(json.dumps(r,ensure_ascii=False))
