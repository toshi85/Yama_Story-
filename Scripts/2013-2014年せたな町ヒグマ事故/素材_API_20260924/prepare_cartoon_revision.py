#!/usr/bin/env python3
"""Prepare the approved compact cartoon style without placing paid requests."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "Asset_Prompts_Full_ratio60.md"
OUT = ROOT.parent / "Asset_Prompts_Full_cartoon.md"
STYLE = (
    "Cute 2D children's animation cartoon. A large head taking about one quarter of total height; "
    "four to five heads tall, large head, short compact torso, short stubby arms and legs. "
    "Uniform thick black outlines around the silhouette and major shapes, flat colors with at most "
    "one flat shadow shade, large expressive eyes. No realistic adult proportions, no slender or "
    "elongated body, no detailed fabric texture, no gradients, no painterly rendering, no photo realism."
)
OLD_STYLE = "Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style."


def revise(prompt: str) -> str:
    if OLD_STYLE not in prompt:
        raise ValueError("Original character style was not found")
    return prompt.replace(OLD_STYLE, STYLE, 1)


def main() -> None:
    source = SOURCE.read_text()
    plan = json.loads((ROOT / "ratio60_character_plan.json").read_text())
    masters = json.loads((ROOT / "ratio60_masters.json").read_text())
    if len(plan) != 132 or len(masters) != 3:
        raise SystemExit("FAIL: expected 132 character cuts and 3 masters")
    for item in plan:
        old = item["prompt"]
        if source.count(old) != 1:
            raise SystemExit(f"FAIL: exact source prompt missing or repeated: {item['id']}")
        item["prompt"] = revise(old)
        source = source.replace(old, item["prompt"], 1)
        item["references"] = [x.replace("-v2.png", "-v3.png") for x in item.get("references", [])]
    for item in masters:
        item["prompt"] = revise(item["prompt"])
        item["id"] = item["id"].replace("-v2", "-v3")
        match = re.search(rf"(### {item['id'][:7]}[^\n]*\n\n```text\n)(.*?)(\n```)", source, re.S)
        if not match:
            raise SystemExit(f"FAIL: master block missing: {item['id']}")
        source = source[:match.start(2)] + item["prompt"] + source[match.end(2):]
    source = source.replace("CHAR-02-front-v2.png", "CHAR-02-front-v3.png").replace("CHAR-03-front-v2.png", "CHAR-03-front-v3.png").replace("CHAR-04-front-v2.png", "CHAR-04-front-v3.png")
    old_blocks = re.findall(r"キャラプロンプト（1:1）:\n```\n" + re.escape(OLD_STYLE) + r"[^\n]*\n```\n", source)
    if len(old_blocks) != 36:
        raise SystemExit(f"FAIL: expected 36 superseded prompts, found {len(old_blocks)}")
    source = re.sub(r"キャラプロンプト（1:1）:\n```\n" + re.escape(OLD_STYLE) + r"[^\n]*\n```\n", "", source)
    source = source.replace("改訂キャラプロンプト（背景透過・1:1）:", "キャラプロンプト（1:1）:")
    if OLD_STYLE in source or source.count("four to five heads tall") != 135:
        raise SystemExit("FAIL: active cartoon style is incomplete")
    OUT.write_text(source)
    (ROOT / "cartoon_character_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "cartoon_masters.json").write_text(json.dumps(masters, ensure_ascii=False, indent=2) + "\n")
    print("Prepared 132 character prompts and 3 masters; paid requests: 0")


if __name__ == "__main__":
    main()
