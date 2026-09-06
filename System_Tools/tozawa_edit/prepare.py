"""戸沢村の承認済み素材を既存の編集ツールへ対応付ける。原稿は書き換えない。"""
import argparse,json,re,shutil,sys,subprocess
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('--tools',type=Path,required=True);a=p.parse_args();w=a.work.resolve();t=a.tools.resolve();sys.path.insert(0,str(t))
 from build_shots import parse_master
 rows=parse_master(w/'Asset_Prompts_Full.md');master=parse_master(w/'Master.md')
 clean=lambda s:re.sub(r'<!--.*?-->','',s).replace('**','').strip()
 assert len(rows)==len(master)==298
 assert all(clean(x['narration'])==clean(y['narration']) for x,y in zip(rows,master))
 images=w/'画像';images.mkdir(exist_ok=True);chars=images/'キャライラスト';chars.mkdir(exist_ok=True)
 def copy(src,dst):
  if not dst.exists() or dst.stat().st_size!=src.stat().st_size:shutil.copy2(src,dst)
 for src in (w/'images').glob('*.png'):
  name=src.stem
  if name.startswith('CHAR-'):dst=chars/(name+'.png')
  elif name.endswith('_bg'):dst=images/(name[:-3]+'-1.png')
  else:dst=images/(re.sub(r'_(char|still)$','',name)+'.png')
  copy(src,dst)
 for src in (w/'動画').glob('ASSET-*.mp4'):copy(src,images/src.name)
 byid={r['asset_id']:r for r in rows}
 def background(aid,seen=()):
  if aid in seen:raise ValueError('背景の循環 '+aid)
  p=images/(aid+'-1.png')
  if p.exists():return p
  r=byid[aid];m=re.search(r'背景再使用:\s*(?:ASSET-)?(\d+)',r['block'])
  if m:return background('ASSET-'+m.group(1).zfill(3),seen+(aid,))
  p=images/(aid+'.png')
  if p.exists() and not (w/'images'/(aid+'_char.png')).exists():return p
  raise ValueError('背景未解決 '+aid)
 for r in rows:
  if (w/'images'/(r['asset_id']+'_char.png')).exists():
   copy(background(r['asset_id']),images/(r['asset_id']+'-1.png'))
 derived=[]
 for r in rows:
  kind=re.search(r'\[(.*?)\]',r['memo']).group(1)
  typ='画面エフェクト' if kind=='テキストのみ' else kind
  derived += [f"## {r['section']}",f"ナレーター: {r['narration']}",f"【制作メモ】{r['asset_id']} {r['memo']}",f'- 【{typ}】',r['block']]
 derived_path=w/'編集用素材台本.md';derived_path.write_text('\n'.join(derived))
 subprocess.run([sys.executable,str(t/'build_shots.py'),str(derived_path),str(w/'音声/仮ナレーション_Kyoko.wav'),str(images),'-o',str(w/'shots.json'),'--timings',str(w/'音声/仮音声_生成時刻.json'),'--extra-assets',str(w/'地形図'),'--tail','0','--title',w.name],check=True)
 doc=json.loads((w/'shots.json').read_text());doc['map_renderer']='tozawa_v1';doc['narration_status']='scratch_machine_voice';doc['timing_source']='measured_per_row_audio_samples';doc['source_master']='Master.md';doc['source_assets']='Asset_Prompts_Full.md'
 # 実測時刻に合わせる。素材指定の地図と25本の動画を短尺の自動併合で消さない。
 from build_shots import find_asset,CHAR_MOVES,speech_from
 charno=0
 for s,r in zip(doc['shots'],rows):
  aid=r['asset_id'];kind=re.search(r'\[(.*?)\]',r['memo']).group(1)
  own,own_kind,own_bg=find_asset(str(images),aid)
  if own:
   s.update(asset_file=str(Path(own).relative_to(w)),asset_kind=own_kind,
            background_file=str(Path(own_bg).relative_to(w)) if own_bg else s.get('background_file',''),
            same_as_prev=False,reused=False)
  if kind=='Google Earth':
   s.update(asset_file='地形図/'+aid+'.mp4',asset_kind='video',background_file='',reused=False,same_as_prev=False,pan='',telops=[])
  elif (images/(aid+'.mp4')).exists():
   s.update(asset_file='画像/'+aid+'.mp4',asset_kind='video',background_file='',reused=False,same_as_prev=False,pan='')
  elif kind=='キャラアニメーション':
   path,k,bg=find_asset(str(images),aid)
   if path:
    s.update(asset_file=str(Path(path).relative_to(w)),asset_kind=k,background_file=str(Path(bg).relative_to(w)) if bg else s['background_file'])
   if s['asset_kind']=='character':
    s['motion']=CHAR_MOVES[charno%len(CHAR_MOVES)];charno+=1
  if kind=='テキストのみ':
   s.update(asset_kind='black_card',style='black_card',asset_file='',background_file='',reused=False,same_as_prev=False)
  s['narration']=r['narration']
  # 全ての編集指示を専用画面で確認できるよう保存。発話は勝手に補わない。
  s['edit_note']=r['edit_note']
  if s['asset_kind']=='character':
   speech=speech_from(r['narration'])
   if len(speech)>24:speech=speech.split('。')[0]
   s['speech']=speech if len(speech)<=24 else ''
  if aid in ('ASSET-006','ASSET-007'):
   s['question']={'ASSET-006':'なぜ同じ村で、3度も悲劇が繰り返されたのか？','ASSET-007':'満腹なのに、なぜ人を食べたのか？'}[aid];s['telops']=[]
 # 目視で確定した表示。否定例や切替前の年を同時表示しない。
 for s in doc['shots']:
  if s['id']==27:s['telops']=['大量出血']
  if s['id']==209:s['telops']=['2026年5月3日']
  if s['id']==219:s['telops']=['通り道']
  if s['id']==243:s['telops']=['矢状稜が潰れている']
 # 台本の同一絵の連続が16秒を超える場合、当該行の元画像へ戻す。
 start=0;prev=None
 for s in doc['shots']:
  if s['asset_file']!=prev:start=s['start_frame'];prev=s['asset_file']
  if prev and (s['end_frame']-start)/doc['fps']>16:
   path,k,bg=find_asset(str(images),s['asset_id'])
   if path:s.update(asset_file=str(Path(path).relative_to(w)),asset_kind=k,background_file=str(Path(bg).relative_to(w)) if bg else '',same_as_prev=False);start=s['start_frame'];prev=s['asset_file']
 (w/'shots.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
 print('準備:',len(doc['shots']),'行、',charno,'キャラ、17地図、25動画',flush=True)
if __name__=='__main__':main()
