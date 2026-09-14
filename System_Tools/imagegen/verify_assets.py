#!/usr/bin/env python3
"""Build inspection previews and ask Codex to verify generated ASSET images."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


def _ensure_pillow() -> None:
    try:
        import PIL  # noqa: F401
        return
    except ImportError:
        pass
    repo = Path(__file__).resolve().parents[3]
    venv_python = repo / ".venv-edit" / "Scripts" / "python.exe"
    if venv_python.is_file() and Path(sys.executable).resolve() != venv_python.resolve():
        os.execv(str(venv_python), [str(venv_python), *sys.argv])
    raise SystemExit("Pillow is required (expected in D:\\0\\.venv-edit).")


_ensure_pillow()
from PIL import Image, ImageOps  # noqa: E402


REVIEW_TEMPLATE = """You are inspecting one generated visual asset using machine vision.

## Given material
Narration: {narration}
Scene: {scene}
Type: {asset_type}
Character prompt:
{character_prompt}
Background/still prompt:
{background_prompt}
Reference CHAR explanation:
{reference_explanation}

The first attached image is the inspection preview. Any later attached images are the named reference CHAR images, in the same order as the explanation above. Reference images define identity and clothing; do not mistake their white background or neutral pose for requirements of the scene preview.

## Instructions
(a) Derive 3 to 6 concrete conditions this image must satisfy from the narration and scene, using the prompt details where relevant. Consider whether the main subject is visible; character identity and clothing; direction and action; season and time of day; absence of burned-in text; and cartoon versus photorealistic style.
(b) Inspect the preview and judge every condition as PASS, FAIL, or UNVERIFIED. Give exactly one non-empty evidence sentence for each condition. Use UNVERIFIED when the pixels cannot establish the condition; do not guess.
(c) Set overall ok to true only when there are no FAIL verdicts. Put concise summaries of FAIL items in issues. Give one sentence in fix_hint explaining how the generation prompt should be changed; if no change is needed, say so in one sentence.
(d) Output JSON only, with exactly this top-level shape:
{{"requirements":[{{"text":"...","verdict":"PASS|FAIL|UNVERIFIED","evidence":"..."}}],"ok":true,"issues":[],"fix_hint":"..."}}
Do not use Markdown fences and do not add commentary outside the JSON.
"""


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--prompts", required=True, type=Path)
    p.add_argument("--images", required=True, type=Path)
    p.add_argument("--terrain", required=True, type=Path)
    p.add_argument("--ids", required=True)
    p.add_argument("--out", required=True, type=Path)
    return p.parse_args()


def read_source(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def fenced_after(body: str, heading_pattern: str) -> str:
    m = re.search(heading_pattern + r"[^\n]*:\s*\r?\n```[^\n]*\r?\n(.*?)\r?\n```", body, re.S | re.I)
    return m.group(1).strip() if m else ""


def parse_master(text: str) -> tuple[dict[str, dict], dict[str, dict]]:
    char_defs: dict[str, dict] = {}
    for m in re.finditer(r"(?ms)^###\s+CHAR-(\d{2}):\s*(.*?)\r?\n```[^\n]*\r?\n(.*?)\r?\n```", text):
        cid = f"CHAR-{m.group(1)}"
        char_defs[cid] = {"id": cid, "description": m.group(2).strip(), "prompt": m.group(3).strip()}

    blocks: dict[str, dict] = {}
    pattern = re.compile(
        r"(?ms)^ナレーター:\s*(.*?)\r?\n\s*\r?\n"
        r"【制作メモ】ASSET-(\d{3})\s+\[([^\]]+)\][^\r\n]*\r?\n"
        r"(.*?)(?=^\s*---\s*$|\Z)"
    )
    for m in pattern.finditer(text):
        body = m.group(4)
        scene_m = re.search(r"(?m)^シーン:\s*(.+)$", body)
        character_prompt = fenced_after(body, r"キャラプロンプト[^\n]*")
        background_prompt = fenced_after(body, r"背景プロンプト[^\n]*")
        if not background_prompt:
            background_prompt = fenced_after(body, r"静止画プロンプト[^\n]*")
        if not character_prompt and not background_prompt:
            fence_m = re.search(r"(?ms)^```[^\n]*\r?\n(.*?)\r?\n```", body)
            if fence_m:
                background_prompt = fence_m.group(1).strip()
        reuse_m = re.search(r"(?m)^→\s*背景再使用:\s*(\d{3})\s*$", body)
        refs = re.findall(r"\(CHAR-(\d{2})\s+再利用\)", character_prompt)
        blocks[m.group(2)] = {
            "id": m.group(2),
            "narration": m.group(1).strip(),
            "scene": scene_m.group(1).strip() if scene_m else "",
            "type": m.group(3).strip(),
            "character_prompt": character_prompt,
            "background_prompt": background_prompt,
            "background_reuse": reuse_m.group(1) if reuse_m else None,
            "reference_char_ids": list(dict.fromkeys(f"CHAR-{x}" for x in refs)),
        }
    return blocks, char_defs


def get_ffmpeg() -> str:
    env_path = os.environ.get("YAMA_FFMPEG")
    if env_path and Path(env_path).is_file():
        return env_path
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        found = shutil.which("ffmpeg")
        if found:
            return found
    raise RuntimeError("ffmpeg was not found")


def terrain_frame(video: Path, target: Path) -> None:
    ffmpeg = get_ffmpeg()
    probe = subprocess.run(
        [ffmpeg, "-hide_banner", "-nostdin", "-i", str(video)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", probe.stderr)
    if not match:
        raise RuntimeError(f"Could not read duration: {video}")
    duration = int(match.group(1)) * 3600 + int(match.group(2)) * 60 + float(match.group(3))
    cmd = [ffmpeg, "-hide_banner", "-nostdin", "-y", "-ss", f"{duration / 2:.3f}", "-i", str(video), "-frames:v", "1", str(target)]
    run = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    if run.returncode != 0 or not target.is_file():
        raise RuntimeError("ffmpeg frame extraction failed: " + "\n".join(run.stderr.splitlines()[-5:]))


def save_jpeg_under_limit(image: Image.Image, target: Path) -> None:
    image = image.convert("RGB")
    image.thumbnail((1280, 1280), Image.Resampling.LANCZOS)
    while True:
        image.save(target, "JPEG", quality=85, optimize=True, progressive=True)
        if target.stat().st_size <= 300_000:
            return
        if max(image.size) <= 480:
            raise RuntimeError(f"Could not make preview <=300KB at JPEG quality 85: {target}")
        image = image.resize(
            (max(1, round(image.width * 0.9)), max(1, round(image.height * 0.9))),
            Image.Resampling.LANCZOS,
        )


def build_preview(packet: dict, folder: Path) -> Path:
    preview = folder / "preview.jpg"
    sources = packet["image_paths"]
    if sources.get("terrain"):
        frame = folder / "terrain_middle.png"
        terrain_frame(Path(sources["terrain"]), frame)
        with Image.open(frame) as im:
            output = im.copy()
    elif sources.get("character") and sources.get("background"):
        with Image.open(sources["background"]) as bg, Image.open(sources["character"]) as char:
            output = ImageOps.fit(bg.convert("RGB"), (1280, 720), method=Image.Resampling.LANCZOS)
            fg = char.convert("RGBA")
            fg.thumbnail((1280, round(720 * 0.60)), Image.Resampling.LANCZOS)
            output = output.convert("RGBA")
            output.alpha_composite(fg, ((1280 - fg.width) // 2, 720 - fg.height))
    elif sources.get("still"):
        with Image.open(sources["still"]) as im:
            output = im.copy()
    else:
        raise RuntimeError(f"No usable image source for ASSET-{packet['id']}")
    save_jpeg_under_limit(output, preview)
    return preview


def make_packet(block: dict, char_defs: dict[str, dict], images: Path, terrain: Path) -> dict:
    aid = block["id"]
    terrain_path = terrain / f"ASSET-{aid}.mp4"
    main_path = images / f"ASSET-{aid}.png"
    own_bg = images / f"ASSET-{aid}-1.png"
    reuse = block["background_reuse"]
    reused_bg = images / f"ASSET-{reuse}-1.png" if reuse else None
    is_character = bool(block["character_prompt"])
    paths: dict[str, object] = {"character": None, "background": None, "still": None, "terrain": None, "reference_chars": []}
    if terrain_path.is_file():
        paths["terrain"] = str(terrain_path.resolve())
    elif is_character:
        if not main_path.is_file():
            raise FileNotFoundError(main_path)
        paths["character"] = str(main_path.resolve())
        bg = own_bg if own_bg.is_file() else reused_bg
        if not bg or not bg.is_file():
            raise FileNotFoundError(f"Background missing for ASSET-{aid}")
        paths["background"] = str(bg.resolve())
    else:
        if not main_path.is_file():
            raise FileNotFoundError(main_path)
        paths["still"] = str(main_path.resolve())

    refs = []
    for cid in block["reference_char_ids"]:
        ref_path = images / "キャライラスト" / f"{cid}.png"
        if not ref_path.is_file():
            raise FileNotFoundError(ref_path)
        definition = char_defs.get(cid, {"id": cid, "description": "", "prompt": ""})
        refs.append({**definition, "image_path": str(ref_path.resolve())})
        paths["reference_chars"].append(str(ref_path.resolve()))
    return {**block, "reference_characters": refs, "image_paths": paths}


def format_prompt(packet: dict) -> str:
    if packet["reference_characters"]:
        explanation = "\n\n".join(
            f"{x['id']}: {x['description']}\nCanonical character prompt: {x['prompt']}"
            for x in packet["reference_characters"]
        )
    else:
        explanation = "None. No reference CHAR image is attached."
    return REVIEW_TEMPLATE.format(
        narration=packet["narration"], scene=packet["scene"], asset_type=packet["type"],
        character_prompt=packet["character_prompt"] or "None.",
        background_prompt=packet["background_prompt"] or "None.",
        reference_explanation=explanation,
    )


def validate_result(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8-sig").strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.I)
    data = json.loads(raw)
    reqs = data.get("requirements")
    if not isinstance(reqs, list) or not 3 <= len(reqs) <= 6:
        raise ValueError("requirements must contain 3 to 6 items")
    for req in reqs:
        if not isinstance(req, dict) or not isinstance(req.get("text"), str) or not req["text"].strip():
            raise ValueError("invalid requirement text")
        if req.get("verdict") not in {"PASS", "FAIL", "UNVERIFIED"}:
            raise ValueError("invalid requirement verdict")
        if not isinstance(req.get("evidence"), str) or not req["evidence"].strip():
            raise ValueError("empty requirement evidence")
    if not isinstance(data.get("ok"), bool):
        raise ValueError("ok must be boolean")
    if data["ok"] != all(x["verdict"] != "FAIL" for x in reqs):
        raise ValueError("ok is inconsistent with FAIL verdicts")
    if not isinstance(data.get("issues"), list) or not all(isinstance(x, str) for x in data["issues"]):
        raise ValueError("issues must be an array of strings")
    if not isinstance(data.get("fix_hint"), str) or not data["fix_hint"].strip():
        raise ValueError("fix_hint must be a non-empty string")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def run_review(packet: dict, preview: Path, folder: Path) -> dict:
    exe = shutil.which("codex")
    if not exe:
        raise RuntimeError("Codex CLI was not found")
    prompt = format_prompt(packet)
    (folder / "review_prompt.txt").write_text(prompt, encoding="utf-8")
    result_path = folder / "result.json"
    cmd = [exe, "exec", "--sandbox", "read-only", "--skip-git-repo-check", "-o", str(result_path), "--color", "never", "--image", str(preview)]
    for ref in packet["image_paths"]["reference_chars"]:
        cmd.extend(["--image", ref])
    cmd.append("-")
    run = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    (folder / "exec.log").write_text(run.stdout + ("\n[stderr]\n" + run.stderr if run.stderr else ""), encoding="utf-8")
    if run.returncode != 0:
        raise RuntimeError(f"codex exec failed with exit code {run.returncode}")
    if not result_path.is_file():
        raise RuntimeError("codex exec did not create result.json")
    return validate_result(result_path)


def one_sentence(value: str) -> str:
    value = " ".join(value.split()).replace("|", "\\|")
    m = re.match(r".*?[。.!?！？](?:\s|$)", value)
    return (m.group(0) if m else value).strip()


def make_report(ids: list[str], blocks: dict[str, dict], out: Path, elapsed: float, exec_calls: int) -> None:
    rows = []
    ok_count = 0
    unverified = 0
    for aid in ids:
        result_path = out / aid / "result.json"
        try:
            data = validate_result(result_path)
            fails = sum(x["verdict"] == "FAIL" for x in data["requirements"])
            unverified += sum(x["verdict"] == "UNVERIFIED" for x in data["requirements"])
            if data["ok"]:
                ok_count += 1
            overall = "OK" if data["ok"] else "NG"
            issue = one_sentence(data["issues"][0]) if data["issues"] else "—"
            hint = one_sentence(data["fix_hint"])
        except Exception as exc:
            fails, overall, issue, hint = 0, "ERROR", one_sentence(str(exc)), "—"
        rows.append(f"| {aid} | {blocks.get(aid, {}).get('type', 'UNKNOWN')} | {overall} | {fails} | {issue} | {hint} |")
    ng_count = len(ids) - ok_count
    report = [
        "# ASSET machine-vision verification report", "",
        "| ID | 種別 | 総合 | FAIL項目数 | issues先頭1文 | fix_hint |",
        "|---:|---|---:|---:|---|---|", *rows, "",
        "## 集計", "",
        f"- ok件数: {ok_count}", f"- NG件数: {ng_count}",
        f"- UNVERIFIED総数: {unverified}", f"- 所要時間: {elapsed:.1f}秒",
        f"- exec呼び出し回数: {exec_calls}", "",
    ]
    (out / "verify_report.md").write_text("\n".join(report), encoding="utf-8")


def log_line(path: Path, message: str) -> None:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with path.open("a", encoding="utf-8") as f:
        f.write(f"{stamp}\t{message}\n")
        f.flush()


def main() -> int:
    args = parse_args()
    ids = [x.strip() for x in args.ids.split(",") if x.strip()]
    if not ids or any(not re.fullmatch(r"\d{3}", x) for x in ids):
        raise SystemExit("--ids must be a comma-separated list of three-digit IDs")
    args.out.mkdir(parents=True, exist_ok=True)
    progress = args.out / "progress.log"
    started = time.monotonic()
    log_line(progress, f"START ids={len(ids)}")
    text = read_source(args.prompts)
    blocks, char_defs = parse_master(text)
    (args.out / "review_prompt.txt").write_text(REVIEW_TEMPLATE, encoding="utf-8")
    exec_calls = 0
    for aid in ids:
        folder = args.out / aid
        folder.mkdir(parents=True, exist_ok=True)
        try:
            if aid not in blocks:
                raise KeyError(f"ASSET-{aid} was not found in prompts")
            packet = make_packet(blocks[aid], char_defs, args.images, args.terrain)
            (folder / "packet.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            preview = build_preview(packet, folder)
            result_path = folder / "result.json"
            if result_path.is_file():
                log_line(progress, f"{aid}\tSKIP result.json exists")
                continue
            exec_calls += 1
            result = run_review(packet, preview, folder)
            fail_count = sum(x["verdict"] == "FAIL" for x in result["requirements"])
            log_line(progress, f"{aid}\tOK overall={result['ok']} fail={fail_count}")
        except Exception as exc:
            log_line(progress, f"{aid}\tERROR {type(exc).__name__}: {' '.join(str(exc).split())}")
    elapsed = time.monotonic() - started
    make_report(ids, blocks, args.out, elapsed, exec_calls)
    result_count = sum((args.out / aid / "result.json").is_file() for aid in ids)
    log_line(progress, f"DONE results={result_count}/{len(ids)} exec_calls={exec_calls} elapsed_seconds={elapsed:.1f}")
    return 0 if result_count == len(ids) else 1


if __name__ == "__main__":
    raise SystemExit(main())
