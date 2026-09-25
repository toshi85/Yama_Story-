#!/usr/bin/env python3
"""山岳素材画像を Sol で全件確認し、指摘候補だけ Astra で詳しく確認する。"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from extract_prompts import parse as parse_prompts


SOL_MODEL = "gpt-5.6-sol"
ASTRA_MODEL = "gpt-6-astra"
EFFORT = "medium"
ITEM_CODES = [
    "A1", "A2", "A3", "A4", "A5", "A6",
    "B1", "B2", "B3", "B4",
    "C1", "C2", "C3", "C4", "C5",
    "D1", "D2", "D3",
    "E1", "E2", "E3", "E4", "E5",
    "F1", "F2",
]


SOL_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "cuts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "asset": {"type": "string"},
                    "flag": {"type": "boolean"},
                    "items": {"type": "array", "items": {"type": "string", "enum": ITEM_CODES}},
                    "reason": {"type": "string"},
                },
                "required": ["asset", "flag", "items", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["cuts"],
    "additionalProperties": False,
}


ASTRA_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "asset": {"type": "string"},
        "verdict": {"type": "string", "enum": ["直す", "直さない", "本人判断"]},
        "items": {"type": "array", "items": {"type": "string", "enum": ITEM_CODES}},
        "why": {"type": "string"},
        "prompt_fix": {"type": "string"},
    },
    "required": ["asset", "verdict", "items", "why", "prompt_fix"],
    "additionalProperties": False,
}


@dataclass(frozen=True)
class Cut:
    asset: int
    narration: str
    kind: str
    prompts: tuple[str, ...]
    scene: str
    editor: str
    background_reuse: str


Runner = Callable[[Sequence[str], str], subprocess.CompletedProcess[str]]


class ReviewInputError(Exception):
    """レビュー対象を1件も組み立てられない入力。"""


class StalePromptError(Exception):
    """対象画像よりプロンプトMDが古い。"""


def extract_review_rules(check_path: Path) -> str:
    text = check_path.read_text(encoding="utf-8")
    match = re.search(
        r"^## チェック項目\s*$.*?^## 指摘しない項目[^\n]*\s*$.*?(?=^## )",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(f"チェック項目を取り出せません: {check_path}")
    return match.group(0).strip()


def _line(block: str, label: str) -> str:
    match = re.search(rf"^{re.escape(label)}\s*(.+?)\s*$", block, re.MULTILINE)
    return match.group(1).strip() if match else ""


def parse_cuts(md_path: Path) -> list[Cut]:
    """extract_prompts.parse() と同じMDから、レビュー用のカット情報を組み立てる。"""
    parsed = parse_prompts(md_path)
    by_asset: dict[int, list[dict[str, Any]]] = {}
    for item in parsed:
        if item["asset_no"] is not None:
            by_asset.setdefault(int(item["asset_no"]), []).append(item)

    text = md_path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^【制作メモ】ASSET-(\d+)\s*\[([^\]]+)\]", text, re.MULTILINE))
    cuts: list[Cut] = []
    for index, match in enumerate(matches):
        asset = int(match.group(1))
        if asset not in by_asset:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start():end]
        items = by_asset[asset]
        cuts.append(Cut(
            asset=asset,
            narration=str(items[0].get("narration", "")),
            kind=match.group(2).strip(),
            prompts=tuple(str(item.get("body") or item.get("prompt") or "") for item in items),
            scene=_line(block, "シーン:"),
            editor=_line(block, "→ 編集者指示:"),
            background_reuse=_line(block, "→ 背景再使用:"),
        ))
    return cuts


def _sha256(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cut_digest(cut: "Cut") -> str:
    """そのカットのナレーション・シーン・プロンプト等の指紋。変われば検品はやり直し。"""
    import dataclasses
    import hashlib
    return hashlib.sha256(json.dumps(dataclasses.asdict(cut), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _record_review(md_path: Path, cut: "Cut", image: Path, digest: str, *, sol_flag, astra_verdict=None) -> None:
    """本人に渡す前の関所（generation_gate.check_reviewed）が読む検品記録。画像の中身ごとに1件。"""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import generation_gate
    generation_gate.record_image_review(digest, {
        "asset": cut.asset, "image": str(image), "md": str(md_path), "cut_digest": cut_digest(cut),
        "sol_flag": sol_flag, "astra_verdict": astra_verdict,
    })


def _already_reviewed(cuts, image_map, need_astra=False) -> bool:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import generation_gate
    for cut in cuts:
        for path in image_map[cut.asset]:
            rec = generation_gate.image_review(_sha256(path), cut.asset)
            if not rec or rec.get("cut_digest") != cut_digest(cut):
                return False
            if need_astra and rec.get("astra_verdict") is None:
                return False
    return True


def find_images(images_dir: Path, asset: int) -> list[Path]:
    """regen形式と渡し形式をともに含む ASSET-NNN_*.png を返す。"""
    prefix = f"ASSET-{asset:03d}_"
    return sorted(
        path for path in images_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".png" and path.name.startswith(prefix)
    )


def batches(values: Sequence[Cut], size: int) -> list[list[Cut]]:
    if size < 1:
        raise ValueError("--batch は1以上にしてください")
    return [list(values[index:index + size]) for index in range(0, len(values), size)]


def _context(cut: Cut | None, heading: str) -> str:
    if cut is None:
        return f"{heading}: なし"
    return (
        f"{heading}: ASSET-{cut.asset:03d}\n"
        f"  ナレーション: {cut.narration or 'なし'}\n"
        f"  シーン: {cut.scene or 'なし'}"
    )


def _cut_text(cut: Cut, image_paths: Sequence[Path], previous: Cut | None, following: Cut | None) -> str:
    prompt_lines = "\n".join(
        f"  プロンプト{index}: {prompt}" for index, prompt in enumerate(cut.prompts, start=1)
    )
    image_lines = "\n".join(f"  画像{index}: {path.name}" for index, path in enumerate(image_paths, start=1))
    return (
        f"対象: ASSET-{cut.asset:03d}\n"
        f"素材タイプ: {cut.kind}\n"
        f"ナレーション: {cut.narration or 'なし'}\n"
        f"シーン: {cut.scene or 'なし'}\n"
        f"編集者指示: {cut.editor or 'なし'}\n"
        f"背景再使用: {cut.background_reuse or 'なし'}\n"
        f"{prompt_lines}\n"
        f"添付画像（この順番）:\n{image_lines}\n"
        f"{_context(previous, '前のカット')}\n"
        f"{_context(following, '次のカット')}"
    )


def make_sol_prompt(rules: str, entries: Sequence[tuple[Cut, Sequence[Path], Cut | None, Cut | None]]) -> str:
    details = "\n\n---\n\n".join(_cut_text(*entry) for entry in entries)
    return f"""あなたは山岳ドキュメンタリー用の素材画像を事前確認します。
次の基準だけを使い、各対象カットを必ず1件ずつJSONに出してください。
- 少しでも迷ったら flag=true にする（見逃しより挙げすぎを選ぶ）。
- 「指摘しない項目」は挙げない。
- 画像に実際に写っている物だけで判断し、見えないことを推測で断定しない。
- flag=false のとき items は空配列にする。
- reason は日本語1行にする。
- 添付画像が同じカットに複数ある場合は全部を見る。

{rules}

## 対象カット

{details}
"""


def make_astra_prompt(
    rules: str,
    cut: Cut,
    images: Sequence[Path],
    previous: Cut | None,
    following: Cut | None,
    sol_result: dict[str, Any],
) -> str:
    return f"""あなたは山岳ドキュメンタリー用の素材画像を最終確認します。
Sol が挙げた次の1カットを詳しく見て、本当に修正が必要か判定してください。
- verdict は「直す」「直さない」「本人判断」のいずれか。
- why は日本語2行以内。
- 「直す」の場合、prompt_fix に英語プロンプトの差し替え文を書く。
- 「直さない」の場合、prompt_fix は空文字にする。「本人判断」は必要なら修正案を書いてよい。
- 「指摘しない項目」は挙げない。
- 画像に実際に写っている物だけで判断し、見えないことを推測で断定しない。
- 前後カットの添付画像は文脈・一貫性の確認だけに使う。

{rules}

## Sol の指摘

項目: {', '.join(sol_result.get('items', [])) or 'なし'}
理由: {sol_result.get('reason', '')}

## 対象カット

{_cut_text(cut, images, previous, following)}
"""


def command_for(model: str, schema: Path, images: Sequence[Path]) -> list[str]:
    command = [
        "codex", "exec", "-m", model,
        "-c", f"model_reasoning_effort={EFFORT}",
        "-c", "service_tier=default",
        "-s", "read-only",
        "--skip-git-repo-check",
        "--output-schema", str(schema),
    ]
    for image in images:
        command.extend(["-i", str(image)])
    # -- で可変長の -i を明示的に終え、位置引数 - により標準入力を読む。
    command.extend(["--", "-"])
    return command


def default_runner(command: Sequence[str], prompt: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, input=prompt, text=True, capture_output=True, check=False)


def _parse_json_output(stdout: str) -> Any:
    text = stdout.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        starts = [position for position in (text.rfind("\n{"), text.find("{")) if position >= 0]
        if not starts:
            raise
        start = max(starts)
        if text[start] == "\n":
            start += 1
        return json.JSONDecoder().raw_decode(text[start:])[0]


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_asset(value: Any) -> str:
    match = re.fullmatch(r"(?:ASSET-)?0*(\d+)", str(value).strip(), re.IGNORECASE)
    if not match:
        raise ValueError(f"不正なasset番号: {value!r}")
    return str(int(match.group(1)))


def _normalize_sol(value: dict[str, Any]) -> dict[str, Any]:
    for cut in value.get("cuts", []):
        cut["asset"] = _normalize_asset(cut["asset"])
    return value


def _normalize_astra(value: dict[str, Any]) -> dict[str, Any]:
    value["asset"] = _normalize_asset(value["asset"])
    return value


def _append_error(
    out_dir: Path,
    label: str,
    assets: Sequence[int],
    result: subprocess.CompletedProcess[str] | Exception,
) -> dict[str, Any]:
    if isinstance(result, Exception):
        detail = f"{type(result).__name__}: {result}"
        first_line = detail.splitlines()[0]
    else:
        detail = f"exit={result.returncode} stderr={result.stderr.strip()} stdout={result.stdout.strip()}"
        message = result.stderr.strip() or result.stdout.strip() or "エラー内容なし"
        first_line = f"exit={result.returncode} {message.splitlines()[0]}"
    with (out_dir / "errors.log").open("a", encoding="utf-8") as handle:
        handle.write(f"[{label}] {detail}\n")
    return {"label": label, "assets": list(assets), "error": first_line}


def _dry_files(out_dir: Path, stem: str, command: Sequence[str], prompt: str) -> None:
    dry_dir = out_dir / "dry_run"
    dry_dir.mkdir(parents=True, exist_ok=True)
    (dry_dir / f"{stem}.prompt.txt").write_text(prompt, encoding="utf-8")
    prompt_file = shlex.quote(str(dry_dir / f"{stem}.prompt.txt"))
    (dry_dir / f"{stem}.command.txt").write_text(
        f"{shlex.join(command)} < {prompt_file}\n", encoding="utf-8"
    )


def _neighbors(all_cuts: Sequence[Cut]) -> dict[int, tuple[Cut | None, Cut | None]]:
    return {
        cut.asset: (
            all_cuts[index - 1] if index else None,
            all_cuts[index + 1] if index + 1 < len(all_cuts) else None,
        )
        for index, cut in enumerate(all_cuts)
    }


def _collect_sol(out_dir: Path) -> list[dict[str, Any]]:
    cuts: list[dict[str, Any]] = []
    for path in sorted((out_dir / "sol").glob("*.json")) if (out_dir / "sol").exists() else []:
        value = _normalize_sol(_load_json(path))
        cuts.extend(value.get("cuts", []))
    return cuts


def _collect_astra(out_dir: Path) -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    for path in sorted((out_dir / "astra").glob("*.json")) if (out_dir / "astra").exists() else []:
        value = _normalize_astra(_load_json(path))
        values[str(value["asset"])] = value
    return values


def render_outputs(
    out_dir: Path,
    reviewed_assets: Sequence[int],
    missing_assets: Sequence[int],
    calls: dict[str, int],
    failures: Sequence[dict[str, Any]],
    newer_images: Sequence[tuple[int, Path]],
) -> None:
    sol = _collect_sol(out_dir)
    astra = _collect_astra(out_dir)
    flagged = {str(item["asset"]): item for item in sol if item.get("flag")}
    not_flagged = sorted(int(item["asset"]) for item in sol if not item.get("flag"))

    failed_assets = {str(asset) for failure in failures for asset in failure["assets"]}
    sections: dict[str, list[dict[str, Any]]] = {"直す": [], "本人判断": [], "直さない": []}
    for asset, sol_item in sorted(flagged.items(), key=lambda pair: int(pair[0])):
        if asset in failed_assets:
            continue
        result = astra.get(asset)
        if result is None:
            result = {
                "asset": asset,
                "verdict": "本人判断",
                "items": sol_item.get("items", []),
                "why": f"Astra未判定。Sol: {sol_item.get('reason', '')}",
                "prompt_fix": "",
            }
        sections[result["verdict"]].append(result)

    lines = ["# AI画像チェック一覧", ""]
    if newer_images:
        assets = sorted({asset for asset, _path in newer_images})
        lines.extend([
            f"## ⚠️ プロンプトより新しい画像（{len(newer_images)}枚）：古いプロンプトを基準に判定しています",
            "",
            ", ".join(f"ASSET-{asset:03d}" for asset in assets),
            "",
        ])
    if failures:
        lines.extend([f"## ⚠️ 失敗した呼び出し（{len(failures)}件）", ""])
        for failure in failures:
            assets = ", ".join(f"ASSET-{asset:03d}" for asset in failure["assets"])
            lines.append(f"- {assets}／{failure['error']}")
        lines.append("")
    for verdict in ("直す", "本人判断", "直さない"):
        lines.extend([f"## {verdict}", "", "（失敗したカットは含まない）", ""])
        if not sections[verdict]:
            lines.extend(["- なし", ""])
            continue
        for item in sections[verdict]:
            codes = ", ".join(item.get("items", [])) or "なし"
            why = re.sub(r"\s*\n\s*", " / ", str(item.get("why", ""))).strip()
            fix = re.sub(r"\s*\n\s*", " ", str(item.get("prompt_fix", ""))).strip() or "なし"
            lines.append(f"- ASSET-{int(item['asset']):03d}／{codes}／{why}／{fix}")
        lines.append("")

    not_flagged_text = ", ".join(f"ASSET-{asset:03d}" for asset in not_flagged) or "なし"
    missing_text = ", ".join(f"ASSET-{asset:03d}" for asset in sorted(missing_assets)) or "なし"
    lines.extend([
        f"## Sol が挙げなかったカット（{len(not_flagged)}件）",
        "",
        not_flagged_text,
        "",
        "## 画像が無く飛ばしたカット",
        "",
        missing_text,
        "",
        "## 実行情報",
        "",
        f"- Sol: model={SOL_MODEL}, effort={EFFORT}, 呼び出し回数={calls['sol']}",
        f"- Astra: model={ASTRA_MODEL}, effort={EFFORT}, 呼び出し回数={calls['astra']}",
    ])
    (out_dir / "一覧.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    results = {
        "models": {
            "sol": {"model": SOL_MODEL, "effort": EFFORT, "calls": calls["sol"]},
            "astra": {"model": ASTRA_MODEL, "effort": EFFORT, "calls": calls["astra"]},
        },
        "reviewed_assets": [str(asset) for asset in reviewed_assets],
        "missing_images": [str(asset) for asset in sorted(missing_assets)],
        "newer_images": [str(path) for _asset, path in newer_images],
        "failures": list(failures),
        "sol": sol,
        "astra": [astra[key] for key in sorted(astra, key=int)],
    }
    _write_json(out_dir / "results.json", results)


def run_review(args: argparse.Namespace, runner: Runner | None = None) -> dict[str, int]:
    runner = runner or default_runner
    md_path = args.prompts.resolve()
    images_dir = args.images.resolve()
    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    if not md_path.is_file():
        raise FileNotFoundError(md_path)
    if not images_dir.is_dir():
        raise NotADirectoryError(images_dir)

    check_path = Path(__file__).with_name("IMAGE_CHECK.md")
    rules = extract_review_rules(check_path)
    all_cuts = parse_cuts(md_path)
    print(f"parse したカット数: {len(all_cuts)}", flush=True)
    neighbors = _neighbors(all_cuts)
    requested = set(args.assets) if args.assets else None
    selected = [cut for cut in all_cuts if requested is None or cut.asset in requested]
    print(f"--assets で絞った後のカット数: {len(selected)}", flush=True)
    found_numbers = {cut.asset for cut in selected}
    image_map = {cut.asset: find_images(images_dir, cut.asset) for cut in selected}
    available = [cut for cut in selected if image_map[cut.asset]]
    missing_images = [cut.asset for cut in selected if not image_map[cut.asset]]
    print(f"画像が見つかったカット数: {len(available)}", flush=True)
    if not selected:
        detail = "指定番号がMD内の生成対象と一致しない" if requested else "MDから生成対象をparseできない"
        raise ReviewInputError(detail)
    if requested is not None and requested - found_numbers:
        missing = ",".join(str(value) for value in sorted(requested - found_numbers))
        raise ValueError(f"MDに存在しない、または生成プロンプトがないアセット: {missing}")
    if not available:
        raise ReviewInputError("画像名が ASSET-NNN_ で始まるPNGに一致しない")
    prompt_mtime = md_path.stat().st_mtime
    newer_images = [
        (cut.asset, path)
        for cut in available
        for path in image_map[cut.asset]
        if path.stat().st_mtime > prompt_mtime
    ]
    if newer_images and not args.allow_stale:
        example = f"ASSET-{newer_images[0][0]:03d}"
        raise StalePromptError(
            f"プロンプトより新しい画像が {len(newer_images)} 枚あります（例: {example}）。"
            "本人の指示で変えた内容を Asset_Prompts_Full.md に反映してから実行してください。"
            "反映済みで続けるときは --allow-stale"
        )
    calls = {"sol": 0, "astra": 0, "failures": 0}
    failures: list[dict[str, Any]] = []
    prior_calls = {
        "sol": len(list((out_dir / "sol").glob("*.json"))) if (out_dir / "sol").exists() else 0,
        "astra": len(list((out_dir / "astra").glob("*.json"))) if (out_dir / "astra").exists() else 0,
    }

    schema_dir = out_dir / "schemas"
    _write_json(schema_dir / "sol.json", SOL_SCHEMA)
    _write_json(schema_dir / "astra.json", ASTRA_SCHEMA)

    if args.stage in ("sol", "all"):
        (out_dir / "sol").mkdir(parents=True, exist_ok=True)
        for batch_no, group in enumerate(batches(available, args.batch), start=1):
            destination = out_dir / "sol" / f"{batch_no:03d}.json"
            # 前回の結果は、画像とカットが検品時のままのときだけ使い回す（差し替え後は見直す）
            if destination.exists() and _already_reviewed(group, image_map):
                continue
            entries = [
                (cut, image_map[cut.asset], neighbors[cut.asset][0], neighbors[cut.asset][1])
                for cut in group
            ]
            prompt = make_sol_prompt(rules, entries)
            images = [path for cut in group for path in image_map[cut.asset]]
            command = command_for(SOL_MODEL, schema_dir / "sol.json", images)
            if args.dry_run:
                _dry_files(out_dir, f"sol_{batch_no:03d}", command, prompt)
                continue
            calls["sol"] += 1
            # 見せる前の画像の中身を控える（検品後に差し替えた画像を「検品済み」と数えないため）
            seen = {cut.asset: [(path, _sha256(path)) for path in image_map[cut.asset]] for cut in group}
            try:
                result = runner(command, prompt)
                if result.returncode:
                    failures.append(_append_error(
                        out_dir, f"sol batch {batch_no:03d}", [cut.asset for cut in group], result
                    ))
                    continue
                value = _normalize_sol(_parse_json_output(result.stdout))
                _write_json(destination, value)
                flags = {int(item["asset"]): bool(item.get("flag")) for item in value.get("cuts", [])}
                for cut in group:
                    for path, digest in seen[cut.asset]:
                        _record_review(md_path, cut, path, digest, sol_flag=flags.get(cut.asset))
            except Exception as exc:  # 1バッチの失敗で全体を止めない
                failures.append(_append_error(
                    out_dir, f"sol batch {batch_no:03d}", [cut.asset for cut in group], exc
                ))

    sol_results = _collect_sol(out_dir)
    selected_numbers = {cut.asset for cut in available}
    flagged = {
        int(item["asset"]): item
        for item in sol_results
        if item.get("flag") and int(item["asset"]) in selected_numbers
    }
    by_number = {cut.asset: cut for cut in all_cuts}

    if args.stage in ("astra", "all"):
        (out_dir / "astra").mkdir(parents=True, exist_ok=True)
        for asset in sorted(flagged):
            destination = out_dir / "astra" / f"{asset:03d}.json"
            if destination.exists() and _already_reviewed([by_number[asset]], image_map, need_astra=True):
                continue
            cut = by_number[asset]
            previous, following = neighbors[asset]
            context_images = list(image_map[asset])
            for neighbor in (previous, following):
                if neighbor is not None:
                    context_images.extend(find_images(images_dir, neighbor.asset))
            prompt = make_astra_prompt(rules, cut, image_map[asset], previous, following, flagged[asset])
            command = command_for(ASTRA_MODEL, schema_dir / "astra.json", context_images)
            if args.dry_run:
                _dry_files(out_dir, f"astra_{asset:03d}", command, prompt)
                continue
            calls["astra"] += 1
            seen = [(path, _sha256(path)) for path in image_map[asset]]
            try:
                result = runner(command, prompt)
                if result.returncode:
                    failures.append(_append_error(out_dir, f"astra asset {asset:03d}", [asset], result))
                    continue
                value = _normalize_astra(_parse_json_output(result.stdout))
                _write_json(destination, value)
                for path, digest in seen:
                    _record_review(md_path, cut, path, digest, sol_flag=True, astra_verdict=value["verdict"])
            except Exception as exc:  # 1カットの失敗で全体を止めない
                failures.append(_append_error(out_dir, f"astra asset {asset:03d}", [asset], exc))

    calls["failures"] = len(failures)
    if not args.dry_run:
        reported_calls = {
            "sol": prior_calls["sol"] + calls["sol"],
            "astra": prior_calls["astra"] + calls["astra"],
            "failures": calls["failures"],
        }
        render_outputs(
            out_dir,
            [cut.asset for cut in available],
            missing_images,
            reported_calls,
            failures,
            newer_images if args.allow_stale else [],
        )
    return calls


def _asset_numbers(value: str) -> list[int]:
    try:
        numbers = [int(part.strip()) for part in value.split(",") if part.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--assets は 115,151,199 の形式です") from exc
    if not numbers:
        raise argparse.ArgumentTypeError("--assets を空にはできません")
    return numbers


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompts", type=Path, help="Asset_Prompts_Full.md")
    parser.add_argument("--images", type=Path, required=True, help="画像フォルダ")
    parser.add_argument("--out", type=Path, required=True, help="出力フォルダ")
    parser.add_argument("--assets", type=_asset_numbers, help="対象番号（例: 115,151,199）")
    parser.add_argument("--batch", type=int, default=4, help="Solの1回あたりのカット数（既定: 4）")
    parser.add_argument("--dry-run", action="store_true", help="Codexを呼ばずプロンプトとコマンドを書く")
    parser.add_argument("--stage", choices=("sol", "astra", "all"), default="all")
    parser.add_argument(
        "--allow-stale",
        action="store_true",
        help="プロンプトより新しい画像があっても、古いプロンプト基準で続ける",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.batch < 1:
        parser.error("--batch は1以上にしてください")
    try:
        outcome = run_review(args)
    except StalePromptError as exc:
        print(str(exc), file=sys.stderr, flush=True)
        return 2
    except ReviewInputError as exc:
        print(f"対象0件: {exc}", file=sys.stderr, flush=True)
        return 1
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        parser.error(str(exc))
    return 1 if outcome["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
