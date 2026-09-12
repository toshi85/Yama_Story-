from pathlib import Path
import sys,json,subprocess,shlex
sys.dont_write_bytecode=True
sys.path.insert(0,'System_Tools/edit');import ff
p=Path(__file__).resolve().parents[1];c=p/'check';out=c/'frames_3';out.mkdir(exist_ok=True)
b=json.loads((c/'shots_修正前_20260910_3回目.json').read_text());a=json.loads((p/'shots.json').read_text());lines=[]
rb=(c/'shots_修正前_20260910_3回目.json').read_text();ra=(p/'shots.json').read_text()
for old,new in zip(b['shots'],a['shots']):
 assert old['id']==new['id'];sid=old['id']
 keys=[k for k in dict.fromkeys([*old,*new]) if (k in old)!=(k in new) or old.get(k)!=new.get(k)]
 if sid in [24,26,31]:
  lines.append(f'カット{sid}の変更キー一覧: '+(', '.join(keys) if keys else '変更なし（生成画像の条件不一致で反映停止）'))
  for k in keys:lines.append(f'  {k}: {json.dumps(old.get(k),ensure_ascii=False)} → {json.dumps(new.get(k),ensure_ascii=False)}')
  for k in ['start_frame','end_frame','narration','subtitle_segments']:assert (k in old)==(k in new) and old.get(k)==new.get(k)
 else:assert not keys
 if sid in [24,31]:
  for s,is_before in [(old,True),(new,False)]:
   block='\n'.join('  '+l for l in json.dumps(s,ensure_ascii=False,indent=1).splitlines())
   if is_before:assert rb.count(block)==1;rb=rb.replace(block,f'CUT{sid}')
   else:assert ra.count(block)==1;ra=ra.replace(block,f'CUT{sid}')
assert len(a['shots'])==len(b['shots'])==298 and rb==ra
assert a.keys()==b.keys() and {k:v for k,v in a.items() if k!='shots'}=={k:v for k,v in b.items() if k!='shots'}
lines+=['3カットの start_frame / end_frame / narration / subtitle_segments が不変（キーの有無も含む）: PASS','他の295カットが全フィールド一致: PASS。未反映の26も一致、実際には計296カット不変。','トップレベルの全キー・値が一致: PASS（shots配列内の指定変更を除く。キー・配列長・順序も不変）。','24・31のJSONブロックを除くファイル全体の文字列が一致: PASS。']
ob=json.loads((c/'overrides_修正前_20260910_3回目.json').read_text());oa=json.loads((c/'overrides.json').read_text())
for sid,patch in ob['shots'].items():
 for k,v in patch.items():assert oa['shots'][sid][k]==v
for sid,keys in [(24,['asset_file','asset_kind','background_file','motion','drift','base_x']),(31,['asset_file'])]:
 shot=next(s for s in a['shots'] if s['id']==sid)
 for k in keys:assert shot[k]==oa['shots'][str(sid)][k]
lines.append('overrides既存キー保持・今回の変更値の一致: PASS。26の上書き項目追加なし。')
(c/'shots_diff_20260910_3回目.txt').write_text('\n'.join(lines)+'\n')
log=[]
for sid in [24,31]:
 video=c/'preview_3'/f'{sid:04}.mp4';duration=ff.probe_duration(str(video))
 for label,t in zip('abc',[.5,duration/2,duration-.3]):
  dst=out/f'cut{sid}_{label}.png';cmd=[ff.ffmpeg(),'-hide_banner','-nostdin','-y','-i',str(video),'-ss',f'{t:.6f}','-frames:v','1',str(dst)]
  r=subprocess.run(cmd,capture_output=True,text=True);log.append(dict(command=shlex.join(cmd),exit_code=r.returncode,time=t,duration=duration,output=str(dst)))
  assert r.returncode==0 and dst.stat().st_size>0,r.stderr
(c/'extract_commands_3.json').write_text(json.dumps(log,ensure_ascii=False,indent=1)+'\n')
print('\n'.join(lines));print('6 frames extracted, all exit 0. Cut26 stopped before adoption/preview.')
