#!/usr/bin/env python3
"""サンプル用の機械音声ナレーションを作る（macOS の say コマンド）。
各行は開始秒と持ち時間を持ち、枠に収まるよう読速を自動調整する。
本番のナレーションは本人の声。これは試作の仮置き。
"""
import json, subprocess, sys, os

OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/narr"
VOICE = os.environ.get("VOICE", "Kyoko")
os.makedirs(OUT, exist_ok=True)

# (開始秒, 与えられる秒数, 読み上げ文)  ※事実は Fact_Sheet_鹿角2024.md の確度Aのみ
LINES = [
    (5.6,  7.0, "二千二十四年五月十五日、秋田県鹿角市大平。佐藤宏さん六十四歳は、タケノコを採りに入山したまま、戻りませんでした。"),
    (13.6, 5.2, "午前九時ごろ、知人がリュックと拡声器を見つけます。藪の奥から返事が聞こえた、と語っています。"),
    (19.8, 6.8, "この山では、クマの目撃が相次いでいました。ただ、佐藤さんに何が起きたのかは、確認されていません。"),
    (27.4, 6.2, "十六日、警察と消防が交代で捜索し、ヘリも出ました。十七日は雨と風が強く、隊は待機します。"),
    (34.4, 3.4, "十八日午前九時半ごろ、斜面の上で佐藤さんが見つかります。"),
    (38.6, 7.0, "ところが運び出そうとしたとき、警察官二人が相次いでクマに襲われました。二十五歳と四十五歳。作業は中断します。"),
    (46.4, 4.4, "その夜、現場付近の入山禁止と、おりの設置が決まりました。"),
    (51.4, 4.4, "二十一日、重機で林道を広げ、二十二日、佐藤さんは運び出されました。"),
    (56.2, 3.6, "死因は特定されず、毛からも個体は分かりませんでした。"),
]


def dur(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path], capture_output=True, text=True).stdout.strip()
    return float(out)


def synth(text, rate, path):
    subprocess.run(["say", "-v", VOICE, "-r", str(int(rate)), "-o", path, text], check=True)
    return dur(path)


segments = []
for i, (start, budget, text) in enumerate(LINES):
    path = f"{OUT}/n{i:02d}.aiff"
    rate = 240
    d = synth(text, rate, path)
    # 枠に収まらなければ読速を上げる（最大 1.6 倍まで）。余っても遅くはしない
    if d > budget:
        rate = min(rate * d / budget * 1.02, rate * 1.4)
        d = synth(text, rate, path)
    segments.append({"file": path, "start": start, "dur": round(d, 2), "rate": int(rate)})
    print(f"{i:02d} start={start:5.1f} budget={budget:4.1f} dur={d:5.2f} rate={int(rate)}")

json.dump(segments, open(f"{OUT}/segments.json", "w"), ensure_ascii=False, indent=1)

# 1本のトラックへ合成（開始位置へ遅延させて重ねる）
inputs, filters, mixes = [], [], []
for i, s in enumerate(segments):
    inputs += ["-i", s["file"]]
    ms = int(s["start"] * 1000)
    filters.append(f"[{i}:a]aresample=48000,adelay={ms}|{ms},volume=1.0[a{i}]")
    mixes.append(f"[a{i}]")
fc = ";".join(filters) + ";" + "".join(mixes) + f"amix=inputs={len(segments)}:normalize=0:duration=longest[out]"
inputs += ["-f", "lavfi", "-t", "60",
           "-i", "anoisesrc=color=brown:sample_rate=48000:amplitude=0.30"]
n = len(segments)
fc = (";".join(filters) + ";"
      + f"[{n}:a]lowpass=f=320,highpass=f=40,tremolo=f=0.12:d=0.6,volume=0.24,"
        "afade=t=in:st=0:d=3,afade=t=out:st=56:d=4[amb];"
      + "".join(mixes) + "[amb]"
      + f"amix=inputs={n+1}:normalize=0:duration=longest[mx];"
        "[mx]alimiter=limit=0.94,aresample=48000[out]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs,
                "-filter_complex", fc, "-map", "[out]",
                "-t", "60", "-ar", "48000", "-ac", "2", f"{OUT}/narration.wav"], check=True)
print("wrote", f"{OUT}/narration.wav", dur(f"{OUT}/narration.wav"))
