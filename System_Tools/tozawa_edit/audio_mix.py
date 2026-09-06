"""仮ナレーションを整音し、既存の山岳用BGMと控えめな日付SEを入れる。"""
import argparse,json,sys,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('--tools',type=Path,required=True);p.add_argument('--bgm',type=Path,required=True);a=p.parse_args();w=a.work.resolve();sys.path.insert(0,str(a.tools.resolve()));import ff
j=w/'shots.json';d=json.loads(j.read_text());src=w/'音声/仮ナレーション_Kyoko.wav';end=ff.probe_duration(str(src));start=next(s['start_frame']/d['fps'] for s in d['shots'] if s['asset_id']=='ASSET-277');length=end-start
music=w/'音声/終章BGM.mp3';shutil.copy2(a.bgm,music)
cards=[(s['start_frame']/d['fps'],s['end_frame']/d['fps']) for s in d['shots'] if s['asset_kind']=='black_card']
mask='1-min(1,'+'+'.join(f'between(t,{a:.3f},{b:.3f})' for a,b in cards)+')'
ticks=[(s['start_frame']/d['fps'],s['end_frame']/d['fps']) for s in d['shots'] if '時計' in s.get('edit_note','')]
tickmask='min(1,'+'+'.join(f'between(t,{a:.3f},{b:.3f})' for a,b in ticks)+')'
filters=f"[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=24000[voice];[1:a]atrim=0:{end:.3f},asetpts=PTS-STARTPTS,loudnorm=I=-31:TP=-9:LRA=8,aresample=24000,afade=t=in:d=3,afade=t=out:st={end-5:.3f}:d=5,volume='if(lt(t,{start:.3f}),0.5,1)*({mask})':eval=frame[music];aevalsrc='0.035*sin(2*PI*900*t)*exp(-80*mod(t,1))':s=24000:d={end:.3f},volume='{tickmask}':eval=frame[clock];[voice][music][clock]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.891:level=false[out]"
out=w/'音声/編集用ミックス.wav';temp=w/'音声/編集用ミックス.new.wav';ff.run(['-i',str(src),'-stream_loop','-1','-i',str(music),'-filter_complex',filters,'-map','[out]','-t',f'{end:.6f}','-ar','24000','-ac','1','-c:a','pcm_s16le',str(temp)]);temp.replace(out)
current=json.loads(j.read_text());current['audio']='音声/編集用ミックス.wav';current['narration_audio']='音声/仮ナレーション_Kyoko.wav';j.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
(w/'音声/音響編集記録.md').write_text(f'# 確認用音響\n\n機械音声Kyoko。本文の装飾記号・HTMLコメントは発話に含めない。行別音声のサンプル数でカット時刻を作り、別途ASRで照合する。\n\nナレーションは約-16 LUFS、上限-1 dBFSで整音。既存の山岳用BGM「哀悼の意」を前半は約-37 LUFS、終章（{start:.2f}秒〜）は約-31 LUFSで使用。黒い日付・見出しカードではBGMを落とし、時計SE指定の2箇所のみ短い合成の刻み音を追加。冒頭・末尾はフェード。録音された現場音は使用していない。細かい選曲・SEの調整は本人確認用。本人の本番ナレーションへ差し替えた後は再同期が必要。\n')
print('音響保存',round(end,2),'秒',flush=True)
