#!/usr/bin/env python3
"""Yama 素材プロンプトの「生成前の関所」＝3本の検査を1本の入口で走らせ、合格票を出す。

2026-09-25 新設（せたな町で、必読を読まず・検査を1本しか走らせず・警告を無視したまま
「検査を通った」と報告し、生成に進もうとした事故を受けて）。

使い方:
  python System_Tools/check_prompts_all.py <プロンプト.md> [--master <Master.md>] [--skip-precheck-reason "理由"]

合格の条件（全部満たしたときだけ PASS）:
  1. validate_phase2_assets.py --prompts … FAIL 0件・WARN 0件
  2. validate_yama_prompts.py            … 「❌ FAIL」0件
  3. imagegen/precheck_subjects.py       … 全ASSETが PASS（Codex でナレーションの主題が絵に描かれているかを判定）
  4. 「要設定・TBD・仮置き・TODO」0件

合格すると .claude/yama_gate/prompt_checks/<sha256>.json に合格票を書き、git で別のPCへ共有する。
生成の関所（.claude/hooks/guard-yama-generation-gate.sh と imagegen/regen.py）は、
この合格票がプロンプトの「今の中身」と一致するときだけ生成を通す。中身を1字でも変えたら取り直し。
報告するときは、最後に出る「総合判定」の行をそのまま貼る（自分の言葉で要約しない）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]  # D:\0
sys.path.insert(0, str(HERE))
import generation_gate  # noqa: E402  合格票は PC 間で共有する（generation_gate.STAMPS）
STAMPS = generation_gate.STAMPS
TODO = re.compile(r"（要設定）|要設定|TBD|仮置き|後で埋める|TODO")


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def asset_ids(text):
    return sorted(set(re.findall(r"【制作メモ】(ASSET-\d+)", text)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("prompts", type=Path)
    ap.add_argument("--master", type=Path)
    ap.add_argument("--skip-precheck-reason", default="")
    ap.add_argument("--excerpt", action="store_true",
                    help="作り直し分だけを抜き出したファイル。隣のカットとの並び（GE連続・静止画連続・読点分割の連続）は本編で見るので除外し、その旨を票に残す")
    ap.add_argument("--accept", action="append", default=[],
                    help="'ASSET-209:単数なのに複数:理由' の形。判断して受け入れる警告。票と最終行に必ず出る")
    a = ap.parse_args()
    path = a.prompts.resolve()
    text = path.read_text(encoding="utf-8")
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    results, problems = {}, []

    code, out = run([sys.executable, str(HERE / "validate_phase2_assets.py"), "--prompts", str(path)])
    ADJ = ("Google Earthが3回以上連続", "読点で分割された連続ナレーション", "キャラアニメーションが4回以上連続", "静止画が3", "文字カードが連続")
    fails = [l.strip() for l in out.splitlines() if "FAIL ❌" in l and not (a.excerpt and any(k in l for k in ADJ))]
    warns = [l.strip() for l in out.splitlines() if "WARN ⚠" in l and not (a.excerpt and any(k in l for k in ADJ))]
    accepted = []
    for acc in a.accept:
        aid, key, reason = (acc.split(":", 2) + ["", ""])[:3]
        if not reason.strip():
            raise SystemExit(f"--accept には理由が要る: {acc}")
        idre = re.compile(r"\b" + re.escape(aid) + r"\b,?\s*")
        for l in list(warns):
            if key in l and idre.search(l):
                rest = idre.sub("", l).rstrip(", ")
                warns.remove(l)
                if re.search(r"ASSET-\d+", rest.split("件", 1)[-1]):
                    warns.append(rest)
                accepted.append(f"{aid} {key}: {reason}")
    results["validate_phase2_assets"] = {"fail": len(fails), "warn": len(warns)}
    problems += [f"[lint] {l}" for l in fails + warns]

    cmd = [sys.executable, str(HERE / "validate_yama_prompts.py"), str(path)]
    if a.master:
        cmd.append(str(a.master.resolve()))
    code, out = run(cmd)
    vfails = [l.strip() for l in out.splitlines() if l.strip().startswith("❌ FAIL")
              and not (a.excerpt and re.search(r"3連続|静止画連続", l))]
    results["validate_yama_prompts"] = {"fail": len(vfails)}
    problems += [f"[validate_yama_prompts] {l}" for l in vfails]

    if a.skip_precheck_reason:
        results["precheck_subjects"] = {"skipped": a.skip_precheck_reason}
        problems.append(f"[precheck_subjects] 省略（理由: {a.skip_precheck_reason}）→ 合格票は出さない")
    else:
        pre_out = path.parent / ".imagegen" / f"precheck_{sha[:12]}"
        code, out = run([sys.executable, str(HERE / "imagegen" / "precheck_subjects.py"), str(path), "--out", str(pre_out)])
        results["precheck_subjects"] = {"exit": code, "out": str(pre_out)}
        rows = []
        csv_path = pre_out / "results.csv"
        if csv_path.is_file():
            import csv
            rows = list(csv.DictReader(csv_path.read_text(encoding="utf-8-sig").splitlines()))
        if not rows:
            problems.append(f"[precheck_subjects] 結果が読めない exit={code} {out[-300:]}")
        pre_accept = {x.split(":", 2)[0]: x.split(":", 2)[2] for x in a.accept if x.split(":")[1:2] == ["precheck"]}
        for r in rows:
            if r.get("verdict") == "PASS":
                continue
            if r.get("verdict") == "FAIL" and r["id"] in pre_accept:
                accepted.append(f"{r['id']} precheck（missing: {r.get('missing','')}）: {pre_accept[r['id']]}")
                continue
            problems.append(f"[precheck_subjects] {r['id']} {r.get('verdict')}: missing={r.get('missing','')}")

    todo = [f"L{i}: {l.strip()}" for i, l in enumerate(text.splitlines(), 1) if TODO.search(l)]
    results["todo_grep"] = len(todo)
    problems += [f"[TODO] {t}" for t in todo]

    ids = asset_ids(text)
    status = "PASS" if not problems else "FAIL"
    STAMPS.mkdir(parents=True, exist_ok=True)
    record = {"file": generation_gate.portable(path), "sha256": sha, "status": status, "asset_ids": ids,
              "excerpt_mode": a.excerpt, "accepted_warnings": accepted,
              "checked_at": datetime.now().isoformat(timespec="seconds"), "results": results,
              "problems": problems}
    if status == "PASS":
        (STAMPS / f"{sha}.json").write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    (STAMPS / "last_run.json").write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    if status == "PASS":
        generation_gate.share("関所: 合格票")

    for p in problems:
        print(p)
    for x in accepted:
        print(f"[受け入れた警告] {x}")
    mode = "・抜粋モード（並び検査は本編で）" if a.excerpt else ""
    print(f"総合判定: {status}（対象 {len(ids)}件・問題 {len(problems)}件・受け入れた警告 {len(accepted)}件{mode}）{path.name} sha256={sha[:12]}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
