"""戸沢村の承認済み素材を既存の編集ツールへ対応付ける。原稿は書き換えない。"""
import argparse,json,re,shutil,sys,subprocess
from pathlib import Path

def main():
 p=argparse.ArgumentParser()
 p.add_argument('work',type=Path);p.add_argument('--tools',type=Path,required=True)
 # 🚨 2026-09-11: 音声が仮ナレーション（行ごとに生成＝実測時刻あり）で直書きされていた。
 #    本番音声は通しの1本なので実測時刻が無く、ASRで行を割り当てる。両方を受け付ける。
 p.add_argument('--audio',default='音声/仮ナレーション_Kyoko.wav',help='素材フォルダからの相対パス')
 p.add_argument('--timings',default='音声/仮音声_生成時刻.json',help='行別に生成したときの実測時刻。本番音声では使わない')
 p.add_argument('--asr',default='',help='通しの音声を文字起こししたJSON。--timings の代わりに使う')
 p.add_argument('-o','--out',default='shots.json',help='書き出すカット表')
 p.add_argument('--keep-from',default='',help='確定済みの表示（テロップ・文字サイズ・地形図のカメラ）を引き継ぐ元のカット表')
 a=p.parse_args();w=a.work.resolve();t=a.tools.resolve();sys.path.insert(0,str(t))
 if a.asr and a.timings=='音声/仮音声_生成時刻.json':a.timings=''
 if not a.asr and not a.timings:sys.exit('--asr か --timings のどちらかが要ります')
 out_path=w/a.out
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
 cmd=[sys.executable,str(t/'build_shots.py'),str(derived_path),str(w/a.audio),str(images),'-o',str(out_path),'--extra-assets',str(w/'地形図'),'--tail','0','--title',w.name]
 cmd += ['--asr',str(w/a.asr)] if a.asr else ['--timings',str(w/a.timings)]
 subprocess.run(cmd,check=True)
 doc=json.loads(out_path.read_text());doc['map_renderer']='tozawa_v1'
 doc['narration_status']='final_voice' if a.asr else 'scratch_machine_voice'
 doc['timing_source']='asr_alignment' if a.asr else 'measured_per_row_audio_samples'
 doc['narration_audio']=a.audio
 doc['source_master']='Master.md';doc['source_assets']='Asset_Prompts_Full.md'
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
 # 🚨 2026-09-12: この道具は素材の対応付けをゼロから作り直すので、本人が確定させた
 #    表示（テロップ・黒カードの文字サイズ・地形図のカメラ・実写への差し替え）が消える。
 #    音声を差し替えたとき、9月7日に削除したはずの左上テロップが138カットで復活した。
 #    → 前のカット表があれば、確定済みの表示だけを戻す。
 KEEP=('telops','question','card_font_size','map_zoom','map_heading','map_pitch','map_camera','map_pins')
 prev=w/(a.keep_from or '')
 if a.keep_from and prev.is_file():
  before={s['id']:s for s in json.loads(prev.read_text())['shots']};n=0
  for s in doc['shots']:
   o=before.get(s['id'])
   if not o:continue
   for k in KEEP:
    if o.get(k)!=s.get(k):s[k]=o.get(k) if o.get(k) is not None else ([] if k=='telops' else None);n+=1
  print('確定済みの表示を戻した:',n,'項目（',prev.name,'）',flush=True)
 elif a.keep_from:
  sys.exit('--keep-from のカット表が見つかりません: '+str(prev))
 out_path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
 print('準備:',len(doc['shots']),'行、',charno,'キャラ、17地図、25動画',flush=True)
if __name__=='__main__':main()
