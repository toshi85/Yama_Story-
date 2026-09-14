#!/usr/bin/env python3
"""Judge whether each ASSET prompt visibly depicts its narration subject."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path


JUDGE_TEMPLATE = """あなたは山岳ドキュメンタリーの素材プロンプトを、画像生成前にテキストだけで審査します。

## 審査対象
{packet}

## 判定ルール
1. 物差しは1本だけです。ナレーションで言っている主語・主題（人物・物・出来事）が、プロンプトの絵に見えるかを判定してください。「反応」「痕跡」「書類」「風景」で主題を代替していたら FAIL です。
   ナレーションに複数の主語（例: 夫・クマ・妻）があるとき、そのうち1つでも絵に無ければ FAIL とし、missing にその主語を書いてください。
2. ただし次は PASS です。
   ① 抽象文（結論・心情・時間の経過・問いかけ）を象徴で受けるもの
   ② 痕跡・足跡・資料・数字が主題そのもの
   ③ `→ 画像再使用 / 背景再使用` で別カットの絵を指定している場合は、その参照先が主題を描いていると仮定する
   ④ テロップで補う数字・地名・人数（ただし人物の人数はプロンプト側にも同数が要る）
   ⑤ 実在の被害者・公人の顔を避ける構図
   ⑥ 主題が「描くとポリシー拒否になる物」（人体の一部・胃の内容物・臓器）の場合は、それを持つ／見つけた人物や動物（駆除したクマ・検査員）が描かれていれば PASS。中身はテロップで受ける
   ⑦ 主題が「行為の結果・傾向・比較」（許可を取る／頭を狙う傾向／体格差）の場合は、主語（人物・クマ）が主題に関わる姿（書類を持つ／2頭を並べる）で描かれていれば PASS。図解・矢印・数値は編集者指示に任せる
3. 遺体・負傷・捕獲したクマ・襲撃の瞬間は、カートゥンで描くのが方針です。描かずに逃げていたら FAIL にしてください。
4. 評価語や提案は書かないでください。JSON 以外を出力しないでください。

次の形の JSON 1個だけを出力してください。id は審査対象のものをそのまま使います。
{{"id":"ASSET-NNN","verdict":"PASS|FAIL","subject":"ナレーションの主語・主題（名詞1〜3語）","evidence":"主題を描いているプロンプト内の文（原文引用）または該当なし","missing":"FAILのとき、何が描かれていないか1行","reason":"1文"}}
"""

RESULT_KEYS = {"id", "verdict", "subject", "evidence", "missing", "reason"}
CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ナレーションの主題が素材プロンプトの画面に見えるかを Codex で事前検査する。"
    )
    parser.add_argument("prompts", metavar="Asset_Prompts.md", type=Path)
    parser.add_argument("--ids", help="ASSET-022,ASSET-074 のようなカンマ区切り")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--source-text", type=Path, help="較正用に解析本文だけを差し替える")
    parser.add_argument("--jobs", type=int, default=2, help="並列 codex exec 数（既定: 2）")
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def normalize_ids(value: str | None) -> list[str] | None:
    if value is None:
        return None
    ids = []
    for item in value.split(","):
        match = re.fullmatch(r"(?:ASSET-)?(\d{3})", item.strip(), re.I)
        if not match:
            raise ValueError("--ids must be comma-separated ASSET-NNN or NNN values")
        ids.append(match.group(1))
    return list(dict.fromkeys(ids))


def raw_asset_bodies(text: str) -> dict[str, str]:
    pattern = re.compile(
        r"(?ms)^ナレーター:\s*(.*?)\r?\n\s*\r?\n"
        r"【制作メモ】ASSET-(\d{3})\s+\[[^\]]+\][^\r\n]*\r?\n"
        r"(.*?)(?=^\s*---\s*$|\Z)"
    )
    return {m.group(2): m.group(3) for m in pattern.finditer(text)}


def labelled_fences(body: str) -> list[dict[str, str]]:
    fences = []
    pattern = re.compile(r"(?ms)^([^\r\n`]*)\r?\n```([^\r\n]*)\r?\n(.*?)\r?\n```")
    for match in pattern.finditer(body):
        label = match.group(1).strip()
        fences.append({"label": label, "language": match.group(2).strip(), "text": match.group(3).strip()})
    if not fences:
        for match in re.finditer(r"(?ms)^```([^\r\n]*)\r?\n(.*?)\r?\n```", body):
            fences.append({"label": "", "language": match.group(1).strip(), "text": match.group(2).strip()})
    return fences


def build_blocks(text: str) -> dict[str, dict]:
    # Import the established parser lazily so `--help` stays independent of its image dependencies.
    from verify_assets import fenced_after, parse_master

    parsed, _ = parse_master(text)
    bodies = raw_asset_bodies(text)
    blocks = {}
    for aid, block in parsed.items():
        body = bodies.get(aid, "")
        reuse_lines = re.findall(
            r"(?m)^→\s*(?:画像再使用|背景再使用|編集者指示)[^\r\n]*$", body
        )
        fences = labelled_fences(body)
        # Keep using the shared fence helper as the canonical fallback for unusual labels.
        if not fences:
            fallback = fenced_after(body, r"(?:キャラ|背景|静止画|Google Flow動画)プロンプト[^\n]*")
            if fallback:
                fences = [{"label": "プロンプト", "language": "", "text": fallback}]
        blocks[aid] = {
            "id": f"ASSET-{aid}",
            "narration": block["narration"],
            "asset_type": block["type"],
            "scene": block["scene"],
            "fences": fences,
            "directions": reuse_lines,
        }
    return blocks


def validate_result(path: Path, expected_id: str) -> dict:
    raw = path.read_text(encoding="utf-8-sig").strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.I)
    data = json.loads(raw)
    if not isinstance(data, dict) or set(data) != RESULT_KEYS:
        raise ValueError("judge result has invalid keys")
    if data["id"] != expected_id or data["verdict"] not in {"PASS", "FAIL"}:
        raise ValueError("judge result has invalid id or verdict")
    if not all(isinstance(data[key], str) for key in RESULT_KEYS):
        raise ValueError("judge result values must all be strings")
    if not data["subject"].strip() or not data["evidence"].strip() or not data["reason"].strip():
        raise ValueError("judge result has an empty required value")
    if data["verdict"] == "FAIL" and not data["missing"].strip():
        raise ValueError("FAIL result must include missing")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def log_line(path: Path, message: str, lock: threading.Lock) -> None:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with lock, path.open("a", encoding="utf-8") as handle:
        handle.write(f"{stamp}\t{message}\n")
        handle.flush()


def judge_one(block: dict, out: Path, progress: Path, lock: threading.Lock) -> dict:
    aid = block["id"]
    folder = out / aid
    folder.mkdir(parents=True, exist_ok=True)
    packet_path = folder / "packet.json"
    packet_path.write_text(json.dumps(block, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result_path = folder / "result.json"
    if result_path.is_file():
        try:
            data = json.loads(result_path.read_text(encoding="utf-8-sig"))
            verdict = data.get("verdict", "UNVERIFIED")
        except Exception:
            verdict = "UNVERIFIED"
        log_line(progress, f"{aid}\tSKIP result.json exists verdict={verdict}", lock)
        return {"id": aid, "verdict": verdict, "data": data if 'data' in locals() else {}}
    if not block["fences"]:
        data = {
            "id": aid, "verdict": "SKIP", "subject": "", "evidence": "フェンスなし",
            "missing": "", "reason": "テキストのみ・Google Earth・再利用のみのブロック",
        }
        result_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (folder / "exec.log").write_text("SKIP: no fenced prompt\n", encoding="utf-8")
        log_line(progress, f"{aid}\tSKIP no fenced prompt", lock)
        return {"id": aid, "verdict": "SKIP", "data": data}

    exe = shutil.which("codex")
    if not exe:
        error = "Codex CLI was not found"
        (folder / "exec.log").write_text(error + "\n", encoding="utf-8")
        log_line(progress, f"{aid}\tUNVERIFIED {error}", lock)
        return {"id": aid, "verdict": "UNVERIFIED", "data": {"reason": error}}
    prompt = JUDGE_TEMPLATE.format(packet=json.dumps(block, ensure_ascii=False, indent=2))
    cmd = [
        exe, "exec", "--sandbox", "read-only", "--skip-git-repo-check",
        "-o", str(result_path), "--color", "never", "-",
    ]
    try:
        run = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=900, creationflags=CREATE_NO_WINDOW,
        )
        (folder / "exec.log").write_text(
            run.stdout + ("\n[stderr]\n" + run.stderr if run.stderr else ""), encoding="utf-8"
        )
        if run.returncode != 0:
            raise RuntimeError(f"codex exec failed with exit code {run.returncode}")
        data = validate_result(result_path, aid)
        log_line(progress, f"{aid}\t{data['verdict']}", lock)
        return {"id": aid, "verdict": data["verdict"], "data": data}
    except Exception as exc:
        message = " ".join(str(exc).split())
        with (folder / "exec.log").open("a", encoding="utf-8") as handle:
            handle.write(f"\n[precheck error]\n{type(exc).__name__}: {message}\n")
        log_line(progress, f"{aid}\tUNVERIFIED {type(exc).__name__}: {message}", lock)
        return {"id": aid, "verdict": "UNVERIFIED", "data": {"reason": message}}


def clean_cell(value: object) -> str:
    return " ".join(str(value or "").split()).replace("|", "\\|")


def write_outputs(selected: list[str], blocks: dict[str, dict], results: list[dict], out: Path) -> None:
    by_id = {item["id"].removeprefix("ASSET-"): item for item in results}
    counts = {name: 0 for name in ("PASS", "FAIL", "SKIP", "UNVERIFIED")}
    rows = []
    for aid in selected:
        item = by_id[aid]
        counts[item["verdict"]] = counts.get(item["verdict"], 0) + 1
        data = item["data"]
        rows.append([
            f"ASSET-{aid}", item["verdict"], blocks[aid]["narration"],
            data.get("subject", ""), data.get("evidence", ""), data.get("missing", ""), data.get("reason", ""),
        ])
    with (out / "results.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "verdict", "narration", "subject", "evidence", "missing", "reason"])
        writer.writerows(rows)
    report = [
        "# Subject precheck report", "",
        f"- PASS: {counts['PASS']}", f"- FAIL: {counts['FAIL']}", f"- SKIP: {counts['SKIP']}",
        f"- UNVERIFIED: {counts['UNVERIFIED']}", "", "## FAIL", "",
        "| id | narration | subject | missing |", "|---|---|---|---|",
    ]
    for row in rows:
        if row[1] == "FAIL":
            report.append(f"| {row[0]} | {clean_cell(row[2])} | {clean_cell(row[3])} | {clean_cell(row[5])} |")
    (out / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    if args.jobs < 1:
        raise SystemExit("--jobs must be at least 1")
    try:
        requested = normalize_ids(args.ids)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    source = args.source_text or args.prompts
    text = read_text(source)
    blocks = build_blocks(text)
    selected = requested if requested is not None else [aid for aid, block in blocks.items() if block["fences"]]
    missing = [aid for aid in selected if aid not in blocks]
    if missing:
        raise SystemExit("ASSET IDs not found: " + ", ".join(f"ASSET-{aid}" for aid in missing))
    default_out = args.prompts.parent / ".imagegen" / f"precheck_{datetime.now():%Y%m%d}"
    out = (args.out or default_out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    progress = out / "progress.log"
    lock = threading.Lock()
    log_line(progress, f"START results=0/{len(selected)} jobs={args.jobs} source={source}", lock)
    results = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(judge_one, blocks[aid], out, progress, lock): aid for aid in selected}
        for future in as_completed(futures):
            results.append(future.result())
    write_outputs(selected, blocks, results, out)
    log_line(progress, f"DONE results={len(results)}/{len(selected)}", lock)
    verdicts = {item["verdict"] for item in results}
    if "UNVERIFIED" in verdicts:
        return 2
    return 1 if "FAIL" in verdicts else 0


if __name__ == "__main__":
    raise SystemExit(main())
