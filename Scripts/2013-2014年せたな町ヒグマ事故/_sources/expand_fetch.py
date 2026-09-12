import sys,json,re,urllib.request,urllib.parse,io
from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent
def redact(t):
 t=re.sub(r'[一-龥ぁ-んァ-ヶー]{2,15}(?:さん|氏)(?=[（(\s、。]|$)','[氏名省略]',t)
 t=re.sub(r'[一-龥ぁ-んァ-ヶー]{2,15}(?=[（(][0-9０-９]{2}[）)])','[氏名省略]',t)
 return t

def fetch(k,u):
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20);b=r.read()
  if b.startswith(b'%PDF'):
   import subprocess
   raw=subprocess.run(['pdftotext','-layout','-','-'],input=b,capture_output=True,check=True).stdout.decode();pages=raw.split('\f');pages=pages[:-1] if not pages[-1].strip() else pages;t='\n'.join('\nPAGE '+str(i+1)+'\n'+x for i,x in enumerate(pages));links=[];n=len(pages)
  else:
   s=BeautifulSoup(b,'html.parser');[x.decompose() for x in s(['script','style'])];t=s.get_text(' ',strip=True);links=[{'text':redact(a.get_text(' ',strip=True)),'url':urllib.parse.urljoin(u,a['href'])} for a in s.select('a[href]')];n=1
  t=redact(t);(P/(k+'.txt')).write_text(t)
  o={'url':u,'pages':n,'characters':len(t),'format':'text extraction; personal names omitted; original binary not saved','links':links};(P/(k+'.json')).write_text(json.dumps(o,ensure_ascii=False,indent=2))
  return {'id':k,'pages':n,'characters':len(t),'text':t if len(t)<13000 else t[:500],'links':[x for x in links if re.search('クマ|ヒグマ|201[345]|平成2[567]|広報|議会|年報',x['text'])]}
 except Exception as e:
  o={'url':u,'error':str(e)};(P/(k+'.json')).write_text(json.dumps(o,ensure_ascii=False));return o
if __name__=='__main__':
 for k,u in json.loads(sys.argv[1]).items():print(json.dumps(fetch(k,u),ensure_ascii=False))
