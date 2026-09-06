"""戸沢村用の実座標地形映像。地区の代表点を事故現場のピンにしない。"""
import argparse,functools,json,math,os,re,sys,subprocess,shutil,hashlib
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
_sibling=Path(__file__).resolve().parents[1]/'edit'
TOOLS=Path(os.environ.get('YAMA_EDIT_TOOLS',str(_sibling if _sibling.exists() else Path(__file__).resolve().parents[3]/'System_Tools/edit')))
sys.path.insert(0,str(TOOLS))
import make_map,make_map3d,ff,fonts_setup
from build_shots import parse_master
from PIL import Image,ImageDraw,ImageFont
make_map3d._grid=functools.lru_cache(maxsize=3)(make_map3d._grid)
W,H,FPS=1280,720,15
make_map3d.W,make_map3d.H=W,H

def spec_of(r):
 b=r['block'];aid=r['asset_id'];m=re.search(r'検索座標:\s*([\d.]+),\s*([\d.]+)',b)
 if not m:raise ValueError('中心座標なし '+aid)
 lat,lon=map(float,m.groups());pins=[]
 for label,la,lo in re.findall(r'地点[A-Z]（([^）]+)）:\s*(?:約\s*)?([\d.]+),\s*([\d.]+)',b):
  pins.append((float(la),float(lo),label))
 secret='非公表' in b or 'ピンは打たない' in b
 if secret:pins=[]
 if aid=='ASSET-205':pins=[(38.7376,140.1436,'戸沢村・1988年の3件')]
 altline=re.search(r'カメラ高度:\s*(.+)',b).group(1)
 nums=[float(x.replace(',','')) for x in re.findall(r'[\d,]+',altline)]
 if 'km' in altline:nums=[x*1000 for x in nums]
 a0=max(nums);a1=min(nums)
 if a0==a1:a1=a0*.72
 wide=a0>=100000
 a0=max(a0,1000);a1=max(a1,700)
 if a0/a1<1.25:a1=a0*.7
 radius=re.search(r'半径(\d+)m',b)
 labels={'008':'戸沢村','009':'山形県北部・戸沢村 / 人口 約4,300人','021':'神田地区から約500〜600m上流','051':'神田地区と周辺の山林','059':'集落から約400m / 権現山の山裾','071':'1件目と2件目は約200m','072':'1件目：砂防ダムの裏 / 2件目：家の裏山','100':'十和利山 / 2016年','101':'戸沢村でも近い範囲で被害','107':'神田地区と古口地区 / 約5km','147':'1件目と2件目は約200m','148':'直線 約4〜5km / 起伏を入れて約10km','154':'尾根で隔てられた別の山','205':'1977年〜2020年の記録','273':'角川地区から約10km / 別の集落・別の山系','279':'最上川','295':'集落のすぐ近くまで山林が迫る'}
 return dict(id=aid,lat=lat,lon=lon,pins=pins,secret=secret,alt0=a0,alt1=a1,wide=wide,radius=int(radius.group(1)) if radius else None,label=labels[aid[-3:]],source_note=r['edit_note'])

def zoom(s):
 if s['wide']:return s.get('tile_zoom',8)
 return max(8,min(14,int(round(math.log2(156543*math.cos(math.radians(s['lat']))*1000/(s['alt0']*3))))))

def frame(job):
 s,i,n,cache,tmp=job;p=Path(tmp)/f'f{i:05d}.jpg'
 if p.exists():return str(p)
 q=i/max(n-1,1);u=q*q*(3-2*q);alt=s['alt0']*(s['alt1']/s['alt0'])**u;z=zoom(s)
 if s['wide']:
  im,origin=make_map.build(s['lat'],s['lon'],z,cache,relief=0 if s['id']=='ASSET-008' else .25)
  im=make_map.draw_overlays(im,z,origin,s['pins'],False)
  # 広域は俯瞰で寄る。図の実縮尺は衛星タイルの縮尺で決まる。
  scale=1-.35*u;cw,ch=int(im.width*scale),int(im.height*scale);x,y=(im.width-cw)//2,(im.height-ch)//2
  im=im.crop((x,y,x+cw,y+ch)).resize((W,H),Image.Resampling.LANCZOS)
 else:
  circle=(s['lat'],s['lon'],s['radius']) if s['radius'] else None
  im=make_map3d.render(s['lat'],s['lon'],z,8,heading=s.get('heading',350)+20*u,pitch=max(15,min(65,58-15*u+s.get('pitch_delta',0))),cam_h=alt,far=max(alt*7,18000),cache=cache,src='s2',pins=s['pins'],circle=circle,gain=(1.05,1.15,1.12))
 d=ImageDraw.Draw(im);font=ImageFont.truetype(str(Path(fonts_setup.font_dir())/'MPLUSRounded1c-Bold.ttf'),30);small=ImageFont.truetype(str(Path(fonts_setup.font_dir())/'MPLUSRounded1c-Bold.ttf'),20)
 d.text((32,30),s['label'],font=font,fill='white',stroke_width=3,stroke_fill='black')
 if s['secret']:d.text((32,78),'地区の代表点を中心とした図 / 正確な現場位置は非公表',font=small,fill='white',stroke_width=2,stroke_fill='black')
 d.text((20,H-28),'Sentinel-2 cloudless / EOX / Copernicus · Terrain: Mapzen',font=small,fill='white',stroke_width=2,stroke_fill='black')
 im.save(p,quality=91);return str(p)

def apply_overrides(spec,ov):
 s=dict(spec)
 if s['id'] in ('ASSET-009','ASSET-205'):s['tile_zoom']=10
 pref=ov.get('map_zoom',1)
 scale={'near':.55,'far':1.7}.get(str(pref),pref)
 scale=max(.2,min(3,float(scale or 1)))
 s['alt0']*=scale;s['alt1']*=scale
 if ov.get('map_heading') not in (None,''):s['heading']=float(ov['map_heading'])%360
 if ov.get('map_pitch') not in (None,''):s['pitch_delta']=max(-20,min(20,float(ov['map_pitch'])))
 edits=ov.get('map_pins') or {};pins=[]
 for la,lo,label in s['pins']:
  e=edits.get(label) or {}
  if e.get('hide'):continue
  pins.append((la+float(e.get('dn') or 0)/110540,lo+float(e.get('de') or 0)/(111320*math.cos(math.radians(la))),e.get('label') or label))
 s['pins']=pins
 return s

def preview(work,shot_id,override):
 w=Path(work);doc=json.loads((w/'shots.json').read_text());sh=next(s for s in doc['shots'] if s['id']==shot_id)
 row=next(r for r in parse_master(w/'Asset_Prompts_Full.md') if r['asset_id']==sh['asset_id'])
 spec=apply_overrides(spec_of(row),dict(sh,**override));tmp=w/'check/preview'/('.tozawa_'+str(shot_id));shutil.rmtree(tmp,ignore_errors=True);tmp.mkdir(parents=True)
 cache=w/'.map_tiles';cache.mkdir(exist_ok=True);src=frame((spec,1,3,str(cache),str(tmp)));dst=w/'check/preview'/f'{shot_id:04d}_map.jpg';shutil.copy2(src,dst);return str(dst)

def main():
 p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('--jobs',type=int,default=3);p.add_argument('--only');p.add_argument('--force',action='store_true');p.add_argument('--overrides',type=Path);p.add_argument('--out',type=Path);a=p.parse_args();w=a.work.resolve();out=a.out or w/'地形図';out.mkdir(exist_ok=True,parents=True);cache=w/'.map_tiles';cache.mkdir(exist_ok=True)
 doc=json.loads((w/'shots.json').read_text());dur={s['asset_id']:(s['end_frame']-s['start_frame'])/doc['fps'] for s in doc['shots']}
 specs=[spec_of(r) for r in parse_master(w/'Asset_Prompts_Full.md') if '[Google Earth]' in r['memo']]
 settings={s['asset_id']:s for s in doc['shots']}
 if a.overrides:
  for ov in json.loads(a.overrides.read_text()).get('shots',{}).values():
   if ov.get('asset_id'):settings[ov['asset_id']]=dict(settings.get(ov['asset_id'],{}),**ov)
 specs=[apply_overrides(s,settings.get(s['id'],{})) for s in specs]
 (out/'map_specs.json').write_text(json.dumps(specs,ensure_ascii=False,indent=2))
 for s in specs:
  aid=s['id']
  if a.only and aid!=a.only:continue
  target=out/(aid+'.mp4');seconds=dur[aid]
  if not a.force and target.exists() and abs(ff.probe_duration(str(target))-seconds)<.15:continue
  tmp=out/('.frames_'+aid);tmp.mkdir(exist_ok=True);n=max(2,round(seconds*FPS))
  if a.force:shutil.rmtree(tmp);tmp.mkdir()
  # 必要な衛星・標高を先に取得。欠けた地図を完成扱いにしない。
  z=zoom(s);cx,cy=make_map.deg2num(s['lat'],s['lon'],z);todo=[]
  size=10 if s['wide'] else 8
  for x in range(int(cx)-size//2,int(cx)+size//2):
   for y in range(int(cy)-size//2,int(cy)+size//2):todo.append((x,y))
  def fetch(xy):
   x,y=xy;ok=bool(make_map.fetch(z,x,y,str(cache)))
   if not s['wide']:
    tp=cache/f'terr_{z}_{x}_{y}.png'
    ok=ok and (tp.exists() or make_map.download(make_map3d.TERRAIN.format(z=z,x=x,y=y),str(tp),300))
   return ok
  with ThreadPoolExecutor(max_workers=8) as pool:checks=list(pool.map(fetch,todo))
  if not all(checks):raise RuntimeError(f'{aid}:地図タイル取得不足 {sum(checks)}/{len(checks)}')
  print(f'{aid}: {seconds:.2f}秒 / 座標{s["lat"]},{s["lon"]} / {n}フレーム',flush=True)
  with ProcessPoolExecutor(max_workers=a.jobs) as pool:list(pool.map(frame,[(s,i,n,str(cache),str(tmp)) for i in range(n)],chunksize=4))
  temp_video=target.with_suffix('.new.mp4')
  ff.run(['-framerate',str(FPS),'-i',str(tmp/'f%05d.jpg'),'-vf','minterpolate=fps=30:mi_mode=blend','-t',str(seconds),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',str(temp_video)])
  if abs(ff.probe_duration(str(temp_video))-seconds)>.15:raise RuntimeError('地形動画の尺が合わない '+aid)
  os.replace(temp_video,target)
  (out/(aid+'.pins.json')).write_text(json.dumps({'pins':[p[2] for p in s['pins']],'heading':s.get('heading',350)},ensure_ascii=False))
  print('保存',aid,flush=True)
 print('地形図17本の処理終了',flush=True)
if __name__=='__main__':main()
