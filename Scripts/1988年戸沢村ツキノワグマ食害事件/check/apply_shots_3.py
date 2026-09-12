from pathlib import Path
import json
p=Path(__file__).resolve().parents[1];c=p/'check'
f=p/'shots.json';raw=f.read_text();d=json.loads(raw);o=json.loads((c/'overrides.json').read_text())
patch={24:dict(asset_file='画像/ASSET-024_キャラ.png',asset_kind='character',background_file='画像/ASSET-022-1.png',motion='still',drift=[0,0],base_x=0),31:dict(asset_file='画像/ASSET-031_キャラ_v2.png')}
for s in d['shots']:
 if s['id'] in patch:
  b='\n'.join('  '+l for l in json.dumps(s,ensure_ascii=False,indent=1).splitlines());s.update(patch[s['id']])
  a='\n'.join('  '+l for l in json.dumps(s,ensure_ascii=False,indent=1).splitlines());assert raw.count(b)==1;raw=raw.replace(b,a,1)
  o['shots'].setdefault(str(s['id']),{}).update(patch[s['id']])
f.write_text(raw);(c/'overrides.json').write_text(json.dumps(o,ensure_ascii=False,indent=1)+'\n')
# Keep original tools unchanged. Reuse the already-reviewed check-only/no-deletion wrapper.
s=(c/'preview_safe_2.py').read_text().replace("work=CHECK/'preview_work_2'","work=CHECK/'preview_work_3'").replace("outdir=CHECK/('preview_2_adjusted' if sid==23 else 'preview_2')","outdir=CHECK/'preview_3'")
(c/'preview_safe_3.py').write_text(s)
print('Updated cuts 24 and 31; cut26 not applied (four-toe requirement failed)')
