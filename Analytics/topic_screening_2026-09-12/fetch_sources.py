import sys,requests,json
from pathlib import Path
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
root=Path(__file__).parent
def fetch(pair):
 name,url=pair
 try:
  r=requests.get(url,timeout=25);r.raise_for_status()
  (root/(name+'.html')).write_bytes(r.content)
  s=BeautifulSoup(r.content,'html.parser')
  for t in s(['script','style']):t.decompose()
  text=s.get_text('\n',strip=True)
  (root/(name+'.txt')).write_text(url+'\n'+text)
  links=[{'text':a.get_text(' ',strip=True),'url':requests.compat.urljoin(url,a['href'])} for a in s.select('a[href]')]
  (root/(name+'-links.json')).write_text(json.dumps(links,ensure_ascii=False,indent=2))
  print(name,r.status_code,len(text))
 except Exception as e: print(name,type(e).__name__,str(e))
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(fetch,zip(sys.argv[1::2],sys.argv[2::2])))
