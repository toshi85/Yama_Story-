"""県域のカットだけ縮尺を細かくし、東北全体の画角から寄せる。"""
import argparse,sys,shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import maps
p=argparse.ArgumentParser();p.add_argument('work',type=Path);a=p.parse_args();w=a.work.resolve();temp=w/'.editing/wide_maps';temp.mkdir(exist_ok=True,parents=True)
for name in ('shots.json','Asset_Prompts_Full.md'):shutil.copy2(w/name,temp/name)
if not(temp/'.map_tiles').exists():(temp/'.map_tiles').symlink_to(w/'.map_tiles',target_is_directory=True)
maps.zoom=lambda s:10
maps.ProcessPoolExecutor=ThreadPoolExecutor
for aid in ('ASSET-009','ASSET-205'):
 sys.argv=['maps.py',str(temp),'--only',aid,'--jobs','2'];maps.main()
 src=temp/'地形図'/(aid+'.mp4');dst=w/'地形図'/(aid+'.mp4');shutil.copy2(src,dst)
 print('県域の画角を修正',aid,flush=True)
