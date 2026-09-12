from pathlib import Path
import sys,json,shutil,subprocess,shlex,hashlib
sys.dont_write_bytecode=True
sys.path.insert(0,'System_Tools/edit')
import ff
from PIL import Image
import numpy as np
p=Path(__file__).resolve().parents[1];c=p/'check';g=Path('/Users/tosimasa/.codex/generated_images/01a08b08-f0c0-7a00-b8ce-01f2a7d43550')
sources={'ASSET-024_キャラ_raw.png':'exec-28c54ca6-7fdb-415f-a95e-382846115cab.png','ASSET-026-1_v2.png':'exec-655f32cd-3812-4b09-933c-df50ea1546ab.png','ASSET-031_キャラ_v2_raw.png':'exec-4dd7e56c-285a-412e-9c5f-25ed87462519.png'}
log=[]
for name,src in sources.items():
 dst=p/'画像'/name;assert not dst.exists();shutil.copy2(g/src,dst)
 log.append(dict(operation='copy2',source=str(g/src),destination=str(dst),sha256=hashlib.sha256(dst.read_bytes()).hexdigest()))
for name,out in [('ASSET-024_キャラ_raw.png','ASSET-024_キャラ.png'),('ASSET-031_キャラ_v2_raw.png','ASSET-031_キャラ_v2.png')]:
 raw=p/'画像'/name;dst=p/'画像'/out;assert not dst.exists()
 w,h=Image.open(raw).size
 cmd=['node','System_Tools/edit/character_matte.cjs',str(raw),str(dst),'',str(w),str(h),ff.ffmpeg()]
 r=subprocess.run(cmd,capture_output=True,text=True)
 item=dict(command=shlex.join(cmd),exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr);log.append(item)
 if r.returncode==0:
  image=Image.open(dst);assert image.mode=='RGBA';a=np.asarray(image)[:,:,3]
  item.update(transparent_fraction=float((a==0).mean()),opaque_fraction=float((a==255).mean()),alpha_valid=bool((a==0).mean()>=.01 and (a==255).mean()>=.01))
 print(json.dumps(item,ensure_ascii=False))
(c/'asset_commands_3.json').write_text(json.dumps(log,ensure_ascii=False,indent=1)+'\n')
