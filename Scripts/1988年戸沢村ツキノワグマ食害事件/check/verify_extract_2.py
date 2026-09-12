import sys,json,pathlib,hashlib,subprocess,shlex
sys.dont_write_bytecode=True
sys.path.insert(0,'System_Tools/edit')
import ff
p=pathlib.Path(__file__).resolve().parents[1];c=p/'check';frames=c/'frames_2';frames.mkdir(exist_ok=True)
before=json.loads((c/'shots_修正前_20260910_2回目.json').read_text());after=json.loads((p/'shots.json').read_text())
lines=[]
for b,a in zip(before['shots'],after['shots']):
 assert b['id']==a['id']
 keys=[k for k in dict.fromkeys([*b,*a]) if (k in b)!=(k in a) or b.get(k)!=a.get(k)]
 if b['id'] in [23,27,30]:
  lines.append(f"カット{b['id']}の変更キー一覧: {', '.join(keys)}")
  for k in keys:lines.append(f"  {k}: {json.dumps(b.get(k,'<キーなし>'),ensure_ascii=False)} → {json.dumps(a.get(k,'<キーなし>'),ensure_ascii=False)}")
  for k in ['start_frame','end_frame','narration','subtitle_segments']:assert (k in b)==(k in a) and b.get(k)==a.get(k)
 else:assert not keys
assert len(before['shots'])==len(after['shots'])==298
assert before.keys()==after.keys()
assert {k:v for k,v in before.items() if k!='shots'}=={k:v for k,v in after.items() if k!='shots'}
# Exact serialized blocks of all unrelated cuts must remain byte-for-byte present.
rawb=(c/'shots_修正前_20260910_2回目.json').read_text();rawa=(p/'shots.json').read_text()
for s in before['shots']:
 if s['id'] not in [23,27,30]:
  block='\n'.join('  '+l for l in json.dumps(s,ensure_ascii=False,indent=1).splitlines());assert rawb.count(block)==rawa.count(block)==1
lines+=['3カットとも start_frame / end_frame / narration / subtitle_segments が不変（キーの有無も含む）: PASS','他の295カットは全フィールド一致: PASS（JSON文字列も一致）','トップレベルの全キー・値が一致: PASS（shots配列の指定3要素の変更を除く。shotsキーの存在・298要素の順序も不変）']
(c/'shots_diff_20260910_2回目.txt').write_text('\n'.join(lines)+'\n')
log=[]
asset=p/'地形図/ASSET-009.mp4'; h=hashlib.sha256(asset.read_bytes()).hexdigest()
for name,path in [(f'cut{i}',c/('preview_2_adjusted' if i==23 else 'preview_2')/f'{i:04}.mp4') for i in [23,27,30]]+[('asset009',asset)]:
 duration=ff.probe_duration(str(path));assert duration>0
 for label,t in zip('abc',[.5,duration/2,duration-.3]):
  out=frames/f'{name}_{label}.png'
  cmd=[ff.ffmpeg(),'-hide_banner','-nostdin','-y','-i',str(path),'-ss',f'{t:.6f}','-frames:v','1',str(out)]
  r=subprocess.run(cmd,capture_output=True,text=True);log.append(dict(command=shlex.join(cmd),exit_code=r.returncode,time=t,duration=duration,output=str(out)))
  assert r.returncode==0 and out.stat().st_size>0,r.stderr
assert hashlib.sha256(asset.read_bytes()).hexdigest()==h
(c/'extract_commands_2.json').write_text(json.dumps(dict(commands=log,asset009_sha256=h,asset009_unchanged=True),ensure_ascii=False,indent=1)+'\n')
print('\n'.join(lines[::1]));print('12 frames extracted; all exit 0; ASSET-009 unchanged')
