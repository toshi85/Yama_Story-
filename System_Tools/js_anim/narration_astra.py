#!/usr/bin/env python3
"""鹿角60秒試作の仮ナレーション。確度Aだけを読み、各場面の尺内へ収める。"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/kazuno_astra_narr")
OUT.mkdir(parents=True, exist_ok=True)
SCRIPT = ROOT / "out" / "kazuno_astra_script.txt"
SCRIPT.parent.mkdir(parents=True, exist_ok=True)
VOICE = "Kyoko"

# (開始秒, 終了秒, 日付, 読み上げ文)。HTMLの各場面の字幕と同文。
LINES = [
    (0, 4, "5/15", "5月15日、64歳の佐藤宏さんはタケノコ採りで山に入り、行方が分からなくなりました。"),
    (4, 9, "5/15", "午前9時ごろ、知人はリュックと電子音の出る拡声器を発見。藪から返事を聞いたと語ります。"),
    (9, 13, "5/16", "16日、警察と消防が地上で交代捜索し、ヘリも使われました。"),
    (13, 17, "5/17", "17日は雨と風が強く、捜索隊は待機しました。"),
    (17, 22, "5/18", "18日午前9時半ごろ、佐藤さん発見の通報がありました。"),
    (22, 28, "5/18", "搬送中、25歳と45歳の警察官2人が相次いでクマに襲われ、作業は中断しました。"),
    (28, 33, "5/18 夜", "18日夜、県の緊急対策会議で入山禁止と捕獲用のおりの設置が報告されました。"),
    (33, 37, "5/19", "19日、ヘリと猟友会が現場を確認しましたが、クマは見つかりませんでした。"),
    (37, 41, "5/21", "21日、重機で林道を広げました。"),
    (41, 47, "5/22", "22日午前11時ごろ警察と猟友会が出発し、午後1時前に佐藤さんを運び出しました。"),
    (47, 52, "5/23", "23日の司法解剖でも死因は特定されず、失血死の可能性が報じられました。"),
    (52, 56, "5/31", "31日、現場周辺のおりで雌のクマ1頭が捕獲されました。"),
    (56, 60, "6/3", "6月3日、毛の状態が悪く、DNA鑑定ではクマかどうか特定できませんでした。"),
]


def run(args: list[str]) -> str:
    p = subprocess.run(args, check=True, capture_output=True, text=True)
    return p.stdout.strip()


def duration(path: Path) -> float:
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "default=nw=1:nk=1", str(path)]))


def speak(text: str, rate: int, path: Path) -> float:
    run(["say", "-v", VOICE, "-r", str(rate), "-o", str(path), text])
    return duration(path)


if LINES[0][0] != 0 or LINES[-1][1] != 60 or any(a[1] != b[0] for a, b in zip(LINES, LINES[1:])):
    raise ValueError("場面が60秒を隙間なく覆っていません")

SCRIPT.write_text(
    "鹿角市大平地区クマ事件｜60秒試作｜字幕・仮ナレーション全文\n"
    + "映像注記：地図は『位置関係は模式図』、クマの場面は『再現ではなく状況の図解』。\n\n"
    + "\n".join(f"{start:02d}:00–{end:02d}:00  {date}\n{text}\n"
                for start, end, date, text in LINES),
    encoding="utf-8",
)

segments = []
for i, (start, end, date, text) in enumerate(LINES):
    path = OUT / f"line_{i:02d}.aiff"
    budget = end - start - 0.12
    rate = 255
    for attempt in range(12):
        d = speak(text, rate, path)
        if d <= budget:
            break
        rate = max(rate + 15, min(900, int(rate * d / budget * 1.035)))
    else:
        raise RuntimeError(f"読み上げが収まらない: {i} {date} {d:.3f}s > {budget:.3f}s")
    if start + d > end - 0.10:
        raise RuntimeError(f"次の行と重なる: {i}")
    segments.append({"line": i, "date": date, "start": start, "end": end,
                     "duration": round(d, 3), "rate": rate, "file": str(path)})
    print(f"{i:02d} {date:6s} {start:4.0f}-{end:4.0f}s {d:5.2f}s rate={rate}", flush=True)

inputs = []
filters = []
for i, segment in enumerate(segments):
    inputs += ["-i", segment["file"]]
    ms = round(segment["start"] * 1000)
    filters.append(f"[{i}:a]aresample=48000,adelay={ms}:all=1[a{i}]")
inputs += ["-f", "lavfi", "-t", "60", "-i", "anullsrc=r=48000:cl=stereo"]
filters.append(f"[{len(segments)}:a]anull[base]")
mix = "[base]" + "".join(f"[a{i}]" for i in range(len(segments)))
filters.append(f"{mix}amix=inputs={len(segments)+1}:duration=first:normalize=0,aresample=48000[out]")
wav = OUT / "narration.wav"
run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filters),
     "-map", "[out]", "-t", "60", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(wav)])
if abs(duration(wav) - 60.0) > 0.01:
    raise RuntimeError("音声の長さが60秒ではありません")
print("DONE narration.wav 60.0s", flush=True)
