#!/usr/bin/env python3
"""Build the approved 60% character cut revision before any paid request."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT.parent / "Asset_Prompts_Full_before_ratio60.md"
REVISED = ROOT.parent / "Asset_Prompts_Full_ratio60.md"
MARKER = re.compile(r"【制作メモ】ASSET-(\d+) \[([^\]]+)\]")
ORIGINAL_CHARACTER = {19, 22, 34, 40, 43, 50, 57, 63, 75, 76, 77, 80, 85, 86, 93, 104, 105, 107, 109, 114, 124, 130, 135, 138, 143, 153, 155, 156, 159, 164, 176, 182, 185, 198, 208, 212}
# Evidence, terrain and closing images that need to remain the primary shot.
EVIDENCE = {14, 16, 21, 27, 30, 32, 35, 44, 48, 49, 52, 60, 61, 64, 70, 73, 81, 82, 87, 88, 94, 95, 119, 121, 126, 132, 133, 161, 217, 220}
MASTER_ROLE = {
    2: "Japanese husband in his 50s, short black hair with some gray, dark blue field jacket, gray trousers",
    3: "Japanese woman in her mid 40s, dark hair tied low, maroon field jacket, charcoal trousers",
    4: "Japanese man in his early 60s, short graying hair, gray field jacket, dark trousers",
}
MASTER_ASSETS = {2: {19, 22}, 3: {63, 75, 76}, 4: {77, 80, 85}}
STYLE = "Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style."


def role_for(number, scene):
    for cid, assets in MASTER_ASSETS.items():
        if number in assets:
            return MASTER_ROLE[cid], f"CHAR-0{cid}-front-v2.png"
    if any(x in scene for x in ("夫",)):
        return MASTER_ROLE[2], "CHAR-02-front-v2.png"
    if any(x in scene for x in ("女性", "山菜採り", "山菜を")):
        return "Japanese adult woman in a muted outdoor jacket, clearly fictional cartoon design", None
    if any(x in scene for x in ("男性", "ナタ")):
        return MASTER_ROLE[4], "CHAR-04-front-v2.png"
    if any(x in scene for x in ("研究", "専門家", "DNA", "試料", "遺伝子")):
        return "Japanese adult research worker in a pale gray laboratory coat, fictional cartoon design", None
    if any(x in scene for x in ("ハンター", "捜索", "クマ", "箱わな", "足跡", "山道", "山林", "森")):
        return "Japanese adult hunter or search volunteer in a dark green outdoor jacket, fictional cartoon design", None
    if any(x in scene for x in ("町長", "職員", "対策", "記録", "会議", "文書")):
        return "Japanese adult municipal worker in a navy jacket, fictional cartoon design", None
    return "Japanese adult local resident in a plain outdoor jacket, fictional cartoon design", None


def prompt_for(number, scene, role):
    # The existing live-action direction often says "back view". That direction
    # must never leak into the cartoon overlay request.
    scene = scene.replace("後ろ姿", "斜め前から顔が見える姿").replace("背中", "顔が見える姿").replace("顔を映さず", "架空の顔を見せ")
    return (f"{STYLE} One full-body {role}. Three-quarter front view, face clearly visible with distinct eyes, "
            "nose and mouth; serious or concerned expression appropriate to the situation, no cheerful smile. This is a fictional illustration, "
            "with no resemblance claim to a real person. The person reacts to or performs the action in this "
            f"Japanese scene description: {scene} Show only the person and at most one necessary hand-held prop; "
            "do not draw the scenery, another person, a bear, a vehicle, a building, a map, or printed material. "
            "Head and feet fully inside the square frame, one figure only, no duplicate poses, no panel grid. "
            "Clean transparent alpha background. No written words, numbers, logos, blood, wounds, or gore. 1:1 square image.")


def main():
    original = SCRIPT.read_text()
    markers = list(MARKER.finditer(original))
    if len(markers) != 220 or {int(m.group(1)) for m in markers} != set(range(1, 221)):
        raise SystemExit("FAIL: source must contain ASSET-001..220 exactly once")
    skip = {n for n, k in ((int(m.group(1)), m.group(2)) for m in markers) if k in {"Google Earth", "テキストのみ"}}
    char_set = set(range(13, 221)) - skip - EVIDENCE
    if len(char_set) != 132 or not ORIGINAL_CHARACTER <= char_set or char_set & set(range(1, 13)):
        raise SystemExit(f"FAIL: character plan invalid: {len(char_set)}")
    head = original[:markers[0].start()]
    head = head.replace("顔が特定できる正面描写は作らない。", "キャラ系は架空の顔を正面または斜め前から見せる。冒頭の実写動画だけは顔を特定させない。")
    head = head.replace("Rear or three-quarter back view only, face not identifiable.", "Three-quarter front view, visible expressive fictional face with clear eyes, nose and mouth; no resemblance to a real person.")
    parts = [head]
    image_items = []
    mapping = []
    for j, m in enumerate(markers):
        number, category = int(m.group(1)), m.group(2)
        block = original[m.start():markers[j+1].start() if j+1 < len(markers) else len(original)]
        scene_match = re.search(r"^シーン: (.+)$", block, re.M)
        if not scene_match:
            raise SystemExit(f"FAIL: ASSET-{number:03d} has no scene")
        scene = scene_match.group(1)
        if number in char_set:
            role, ref = role_for(number, scene)
            prompt = prompt_for(number, scene, role)
            revised_scene = scene.replace("後ろ姿", "顔が見える斜め前の姿").replace("背中", "顔が見える姿").replace("顔を映さず", "架空の顔を見せて")
            block = block.replace(f"シーン: {scene}", f"シーン: {revised_scene}", 1)
            if category != "キャラアニメーション":
                block = block.replace(f"ASSET-{number:03d} [{category}]", f"ASSET-{number:03d} [キャラアニメーション]", 1)
                block += "\n既存の写実素材は背景またはつなぎ用。実写人物の顔非表示指定はキャラPNGには適用しない。\n"
                block += f"\nキャラプロンプト（背景透過・1:1）:\n{prompt}\n"
                block += f"→ 編集者指示: 既存の背景または動画に、画像/ASSET-{number:03d}_char.pngを合成。文字は編集で付ける。\n"
            else:
                block = re.sub(r"seen from behind to avoid a real-person likeness", "three-quarter front view with a clearly visible fictional expressive face", block, flags=re.I)
                block = block.replace("顔は特定させない", "架空の顔を見せる")
                block += f"\n改訂キャラプロンプト（背景透過・1:1）:\n{prompt}\n"
            if number == 207:
                block += "→ 編集者指示: 採用画像はチェックマークを除去したASSET-207_char.png。DNAの判定記号をAI画像に描かず、確認済みの結果だけを編集文字で示す。\n"
            image_items.append({"id": f"ASSET-{number:03d}_char", "asset_no": number, "kind": "キャラアニメーション", "slot": "char", "prompt": prompt,
                                "quality": "medium", "image_size": {"width": 1024, "height": 1024}, "background": "transparent",
                                "references": [ref] if ref else []})
            mapping.append({"asset_no": number, "previous_kind": category, "revised_kind": "キャラアニメーション", "base_media": "video" if category == "Lovart動画" else "still" if category != "キャラアニメーション" else "existing_background", "face_visible": True})
        else:
            mapping.append({"asset_no": number, "previous_kind": category, "revised_kind": category})
        parts.append(block)
    REVISED.write_text("".join(parts))
    (ROOT / "ratio60_character_plan.json").write_text(json.dumps(image_items, ensure_ascii=False, indent=2))
    (ROOT / "ratio60_cut_mapping.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2))
    masters = []
    for cid, role in MASTER_ROLE.items():
        masters.append({"id": f"CHAR-0{cid}-front-v2", "prompt": f"{STYLE} One full-body {role}. Fictional Japanese cartoon person, three-quarter front view, visible serious and concerned expressive face with clearly drawn eyes, nose and mouth. Mouth closed, eyebrows slightly tense, alert eyes, absolutely no smile, no cheerful expression. Neutral standing pose, hands visible, head and feet fully in frame. Exactly one character and one pose, no character sheet, no turnaround panels. Transparent alpha background, no scenery, no text, no logo, no gore. 1:1 square image.", "quality": "medium", "image_size": {"width": 1024, "height": 1024}, "background": "transparent"})
    (ROOT / "ratio60_masters.json").write_text(json.dumps(masters, ensure_ascii=False, indent=2))
    if any(any(word in item["prompt"].lower() for word in ("from behind", "back view", "後ろ姿", "背中", "face not identifiable", "no face visible")) for item in image_items + masters):
        raise SystemExit("FAIL: character prompt contains back-view instruction")
    print(f"PASS: {len(char_set)}/220={len(char_set)/220:.1%} character cuts; {len(char_set)-len(ORIGINAL_CHARACTER)} newly converted; 3 front-facing masters")


if __name__ == "__main__":
    main()
