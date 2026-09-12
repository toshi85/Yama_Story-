import sys,requests,json
from pathlib import Path
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
root=Path('.codex/handoff/delegations/logs/2026-09-12-topic-screening')
def search(pair):
 name,q=pair
 r=requests.get('https://search.yahoo.co.jp/search',params={'p':q},timeout=20);s=BeautifulSoup(r.content,'html.parser')
 for t in s(['script','style']):t.decompose()
 text=s.get_text(' ',strip=True)
 links=[{'text':a.get_text(' ',strip=True),'url':a['href']} for a in s.select('a[href]') if a['href'].startswith('http') and not any(d in a['href'] for d in ['yahoo.co.jp','yahoo-net.jp','lycorp.co.jp','lycbiz.com','wikipedia.org'])]
 (root/(name+'.json')).write_text(json.dumps({'query':q,'text':text,'links':links},ensure_ascii=False,indent=2))
 print(name+'\n'+text[:4300]+'\n'+json.dumps(links,ensure_ascii=False))
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(search,zip(sys.argv[1::2],sys.argv[2::2])))
