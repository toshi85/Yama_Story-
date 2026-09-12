import sys,json,urllib.request,urllib.parse,concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup
p=Path(__file__).resolve().parent
def fetch(pair):
 k,u=pair
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=25);b=r.read();pdf=b.startswith(b"%PDF");path=p/(k+(".pdf" if pdf else ".html"));path.write_bytes(b)
  if pdf:
   from pypdf import PdfReader
   d=PdfReader(path).pages;t="\n".join("\nPAGE "+str(i+1)+"\n"+pg.extract_text() for i,pg in enumerate(d));links=[]
  else:
   s=BeautifulSoup(b,"html.parser");[a.decompose() for a in s(["script","style"])];t=s.get_text(" ",strip=True);links=[(a.get_text(" ",strip=True),urllib.parse.urljoin(u,a["href"])) for a in s.select("a[href]")]
  (p/(k+".txt")).write_text(t);o={"id":k,"url":u,"bytes":len(b),"links":links};(p/(k+".json")).write_text(json.dumps(o,ensure_ascii=False,indent=2));return o
 except Exception as e:return {"id":k,"url":u,"error":str(e)}
if __name__=="__main__":
 for r in concurrent.futures.ThreadPoolExecutor(max_workers=4).map(fetch,json.loads(sys.argv[1]).items()):print(json.dumps(r,ensure_ascii=False))
