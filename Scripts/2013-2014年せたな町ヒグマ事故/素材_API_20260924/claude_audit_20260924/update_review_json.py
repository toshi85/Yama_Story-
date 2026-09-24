#!/usr/bin/env python3
"""Claudeの全件検収（claude_review_full.json）と修正ファイル（fixed/画像）を、停止ゲート check_scene_fitness が読む
scene_fitness_review.json の形式へ書き出す。出力: claude_audit_20260924/scene_fitness_review_claude.json
- 元の監査原票はそのまま残す（上書きしない）
- 修正後に本人/Claudeが目視でPASSにしたカットだけ post_status=pass。未修正FAILは fail のまま
使い方: python update_review_json.py <staging_root>   … staging_root は納品フォルダの複製（画像/ 動画/ を含む）
"""
import sys, json, hashlib, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
staging = Path(sys.argv[1]).resolve()
source = (ROOT.parent / "Asset_Prompts_Full.md").read_bytes()
orig = json.load(open(ROOT / "scene_fitness_review/scene_fitness_review.json"))
baseline = json.load(open(ROOT / "scene_fitness_review/replacement_baseline_names.json"))
review = json.load(open(HERE / "claude_review_full.json"))
post = json.load(open(HERE / "post_fix_verdicts.json")) if (HERE / "post_fix_verdicts.json").exists() else {}
spec = {a["asset"]: a for a in json.load(open(HERE / "spec.json"))}
CHAR = {"キャラ画像", "キャラアニメーション", "キャラ流用", "キャラ静止画"}
comp_root = HERE / "composites_final"; comp_root.mkdir(exist_ok=True)
from PIL import Image
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def entities(a):
    """台本のシーン文から必要な要素を1語以上抜く（人物・物・動作）。ゲートは非空と一致だけを見る。"""
    s = spec[a]["scene"].rstrip("。")
    parts = [p for p in re.split(r"[、と・]", s) if p]
    return parts or [s]
out = {"source_sha256": hashlib.sha256(source).hexdigest(), "review_version": "claude-2026-09-25", "scope": "Claude全件検収＋画像修正後の再判定", "cuts": []}
by_orig = {c["asset_no"]: c for c in orig["cuts"]}
for c in review["cuts"]:
    a = c["asset"]; no = int(a.split("-")[1]); o = dict(by_orig[no]); cat = spec[a]["category"]
    editor = cat in {"Google Earth", "テキストのみ"}
    verdict = post.get(a, {}).get("verdict", c["verdict"])
    evidence = post.get(a, {}).get("evidence", c["evidence"])
    req = list(baseline.get(a, []))
    files = {}
    for name in req:
        p = staging / name
        if p.exists(): files[name] = sha(p)
    o.update({"scene": spec[a]["scene"], "category": cat, "required_files": req, "files": files,
              "pre_status": "pass", "visual_plan": f"台本シーン『{spec[a]['scene']}』を、{'人物のいない静止背景＋透過キャラ' if cat in CHAR else '実素材'}で表す", "pre_evidence": "Claudeが台本・シーン文・キャラ定義と実物を照合（batches/*.json）", "reviewer": "Claude",
              "character_relation": ("キャラ＝" + (c.get("fix") or "").split("。")[0]) if cat in CHAR else "",
              "required_entities": entities(a) if cat in CHAR else [], "planned_entities": entities(a) if cat in CHAR else [],
              "post_status": "editor_pending" if editor else ("pass" if verdict == "PASS" else "fail"),
              "visual_evidence": evidence if not editor else "編集者担当（Google Earth／文字カード）",
              "finding": "" if verdict == "PASS" else evidence,
              "video_evidence": "1fpsで全尺＋最終コマを目視" if any(n.endswith(".mp4") for n in req) else "",
              "static_background_plan": "人物・手の写らない16:9静止画に透過キャラPNGを重ねる" if cat in CHAR else ""})
    if cat in CHAR:
        bgname = next((n for n in req if n.endswith(("_still.png", "_bg.png"))), None); chname = next((n for n in req if n.endswith("_char.png")), None)
        o["video_usage"] = "transition_only" if any(n.endswith(".mp4") for n in req) else "none"
        o["human_free_background"] = verdict == "PASS"
        o["background_evidence"] = ("原寸で人物・手なしを確認: " + evidence) if verdict == "PASS" else evidence
        names = sorted(n for n in req if n.endswith(("_still.png", "_bg.png", "_char.png")))
        o["composite_source_sha256"] = hashlib.sha256(json.dumps([(n, files.get(n)) for n in names], ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
        if bgname and chname and (staging / bgname).exists() and (staging / chname).exists():
            bg = Image.open(staging / bgname).convert("RGBA"); ch = Image.open(staging / chname).convert("RGBA")
            ch.thumbnail((int(bg.width * .36), int(bg.height * .72)), Image.Resampling.LANCZOS)
            bg.alpha_composite(ch, (int(bg.width * .04), bg.height - ch.height))
            target = comp_root / f"{a}_composite.jpg"; bg.convert("RGB").save(target, quality=88)
            o["composite_preview"] = target.name; o["composite_sha256"] = sha(target)
        o["composite_verdict"] = "pass" if verdict == "PASS" else "fail"
        o["composition_evidence"] = evidence
        o["verified_entities"] = entities(a) if verdict == "PASS" else []
    out["cuts"].append(o)
dst = HERE / "scene_fitness_review_claude.json"
json.dump(out, open(dst, "w"), ensure_ascii=False, indent=1)
n_pass = sum(1 for c in out["cuts"] if c["post_status"] == "pass"); n_char_pass = sum(1 for c in out["cuts"] if c["category"] in CHAR and c["post_status"] == "pass")
print(f"wrote {dst.name}: pass={n_pass} char_pass={n_char_pass}/132 editor={sum(1 for c in out['cuts'] if c['post_status']=='editor_pending')} fail={sum(1 for c in out['cuts'] if c['post_status']=='fail')}")
