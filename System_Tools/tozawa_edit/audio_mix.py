"""仮ナレーション・時計SEを保ち、BGMは末尾の指定秒数だけに入れる。"""
import argparse
import json
import shutil
import sys
from pathlib import Path


def music_filter(end, seconds=25, source='[1:a]', output='[music]'):
    length = min(seconds, end)
    start = end - length
    music = (f'{source}atrim=0:{length:.6f},asetpts=PTS-STARTPTS,'
             'loudnorm=I=-31:TP=-9:LRA=8,aresample=24000,aformat=channel_layouts=mono,'
             f'afade=t=in:d={min(3,length/2):.6f},'
             f'afade=t=out:st={max(0,length-5):.6f}:d={min(5,length):.6f},asetpts=PTS-STARTPTS')
    if start <= 0:
        return music + output
    return (music + '[tail_music];'
            f'anullsrc=r=24000:cl=mono,atrim=end_sample={round(start*24000)},asetpts=PTS-STARTPTS[quiet];'
            f'[quiet][tail_music]concat=n=2:v=0:a=1{output}')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('work', type=Path)
    p.add_argument('--tools', type=Path, required=True)
    p.add_argument('--bgm', type=Path, required=True)
    p.add_argument('--ending-seconds', type=float, default=25)
    a = p.parse_args()
    if not 0 < a.ending_seconds <= 120:
        p.error('末尾のBGMは0秒より長く120秒以下で指定してください')
    w = a.work.resolve()
    sys.path.insert(0, str(a.tools.resolve()))
    import ff
    j = w/'shots.json'
    d = json.loads(j.read_text())
    src = w/'音声/仮ナレーション_Kyoko.wav'
    end = ff.probe_duration(str(src))
    start = max(0, end-a.ending_seconds)
    music = w/'音声/終章BGM.mp3'
    if a.bgm.resolve() != music.resolve():
        shutil.copy2(a.bgm, music)
    ticks = [(s['start_frame']/d['fps'], s['end_frame']/d['fps']) for s in d['shots'] if '時計' in s.get('edit_note', '')]
    tickmask = 'min(1,' + ('+'.join(f'between(t,{a:.3f},{b:.3f})' for a,b in ticks) or '0') + ')'
    filters = (f'[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=24000[voice];'
               f'{music_filter(end,a.ending_seconds)};'
               f"aevalsrc='0.035*sin(2*PI*900*t)*exp(-80*mod(t,1))':s=24000:d={end:.6f},"
               f"volume='{tickmask}':eval=frame[clock];"
               '[voice][music][clock]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.891:level=false[out]')
    out = w/'音声/編集用ミックス.wav'
    temp = out.with_name('編集用ミックス.new.wav')
    ff.run(['-i',str(src),'-stream_loop','-1','-i',str(music),'-filter_complex',filters,
            '-map','[out]','-t',f'{end:.6f}','-ar','24000','-ac','1','-c:a','pcm_s16le',str(temp)])
    if out.exists():
        backup = out.with_name('編集用ミックス_BGM変更前.wav')
        if not backup.exists():
            shutil.copy2(out, backup)
    temp.replace(out)
    current = json.loads(j.read_text())
    current.update(audio='音声/編集用ミックス.wav', narration_audio='音声/仮ナレーション_Kyoko.wav',
                   bgm={'file':'音声/終章BGM.mp3','start':start,'end':end,'ending_seconds':a.ending_seconds})
    j.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
    (w/'音声/音響編集記録.md').write_text(
        f'# 確認用音響\n\n機械音声Kyoko。ナレーション約-16 LUFS、時計SE指定箇所を維持。\n\n'
        f'本人指定：BGM「哀悼の意」は最後の{a.ending_seconds:g}秒だけ（{start:.3f}〜{end:.3f}秒）。'
        'それより前はBGMなし。約-31 LUFS、入り3秒・末尾5秒のフェード。\n')
    print(json.dumps({'duration':end,'bgm_start':start,'bgm_end':end,'audio':str(out)},ensure_ascii=False),flush=True)


if __name__ == '__main__':
    main()
