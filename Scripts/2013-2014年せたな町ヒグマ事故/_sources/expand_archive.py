import json,sys,re,concurrent.futures,datetime
from pathlib import Path
from expand_fetch import fetch,P

def collect(year):
 key=f'expand_archive{year}_oldest';hits=[];visited=[]
 for step in range(22):
  d=json.loads((P/(key+'.json')).read_text());t=(P/(key+'.txt')).read_text();visited.append(d['url'])
  for x in d['links']:
   if re.search('ヒグマ|クマ|せたな|今金|太田|新成',x['text']) and '_msg' in x['url']:
    if x['url'] not in [h['url'] for h in hits]:
     article_key=f"expand_news_{year}_"+re.search(r'/(\d+)_',x['url'])[1];out=fetch(article_key,x['url']);hits.append({'title':x['text'],'url':x['url'],'file':article_key+'.txt','error':out.get('error')})
  dates=re.findall(r'\.\.\.(\d{4})/(\d{1,2})/(\d{1,2})',t)
  if dates and max(tuple(map(int,x)) for x in dates)>=(year,5,1):break
  nxt=next((x['url'] for x in d['links'] if '次の一覧' in x['text']),None)
  if not nxt:break
  key=f'expand_archive{year}_{step:02}';out=fetch(key,nxt)
  if 'error' in out:break
 result={'year':year,'indexes':len(visited),'visited':visited,'candidates':hits};(P/f'expand_archive{year}_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));return result
if __name__=='__main__':
 for x in concurrent.futures.ThreadPoolExecutor(2).map(collect,[2013,2014]):print(json.dumps(x,ensure_ascii=False))
