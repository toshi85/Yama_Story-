from pathlib import Path
import requests,subprocess,hashlib,json,bs4,sys
from concurrent.futures import ThreadPoolExecutor
p=Path(__file__).parent/'_sources'
def fetch(item):
 name,u=item;result={'name':name,'url':u}
 try:
  r=requests.get(u,timeout=20);r.raise_for_status()
  if r.content.startswith(b'%PDF'):
   f=p/(name+'.pdf');f.write_bytes(r.content);subprocess.run(['pdftotext','-layout',str(f),str(p/(name+'.txt'))],check=True,timeout=15,capture_output=True);result['pages']=len((p/(name+'.txt')).read_text().split('\f'))-1
  else:
   r.encoding=r.apparent_encoding;f=p/(name+'.html');f.write_text(r.text);s=bs4.BeautifulSoup(r.text,'html.parser');(p/(name+'.txt')).write_text(s.get_text('\n',strip=True));ls=[{'title':a.get_text(' ',strip=True),'url':requests.compat.urljoin(u,a['href'])} for a in s.select('a[href]') if ('.pdf' in a['href'].lower() and any(w in a.get_text() for w in ['クマ','ヒグマ','資料','本文','計画'])) or any(w in a.get_text() for w in ['人身','ツキノワグマ'])];(p/(name+'_links.json')).write_text(json.dumps(ls,ensure_ascii=False,indent=2));result['links']=ls
  result['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();result['file']=str(f)
 except Exception as e:result['error']=str(e)
 (p/(name+'_retrieval.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2));return result
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=6) as ex:
  for r in ex.map(fetch,json.loads(Path(sys.argv[1]).read_text())):print(json.dumps(r,ensure_ascii=False))
