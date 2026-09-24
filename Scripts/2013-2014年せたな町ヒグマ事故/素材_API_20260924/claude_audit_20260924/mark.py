#!/usr/bin/env python3
"""修正後の目視判定を post_fix_verdicts.json に追記する。
使い方: python mark.py PASS ASSET-004 "背景: ..." ; python mark.py FAIL ASSET-xxx "理由"
"""
import sys, json
from pathlib import Path
P = Path(__file__).resolve().parent / "post_fix_verdicts.json"
d = json.load(open(P)) if P.exists() else {}
verdict, asset, evidence = sys.argv[1], sys.argv[2], " ".join(sys.argv[3:])
d[asset] = {"verdict": verdict, "evidence": evidence, "reviewer": "Claude", "stage": "修正後の合成見本を原寸相当で目視"}
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
print(asset, verdict, "| total", len(d))
