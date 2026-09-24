#!/usr/bin/env python3
"""検査済みの修正画像だけを、元と同じ名前でデスクトップ納品へ反映する。停止ゲート check_scene_fitness を通らなければ反映0件で止まる。
手順: 納品フォルダを staging へ複製 → fixed/画像 を上書き → review JSON を staging から作る → ゲート（delivery）→ PASS なら納品を差し替え（旧版は previous_desktop_delivery_claude/ に退避）
使い方: python finalize_claude.py [--dry-run] [--review <json>] [--allow-fail]  （--allow-fail は残FAILがあってもキャラ比率60%以上なら反映する運用。ゲートの他の検査は必須）
"""
import sys, json, shutil, subprocess, hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
WORKSPACE = ROOT.parents[3]
sys.path.insert(0, str(WORKSPACE / ".codex/skills/yama-asset-checker/scripts"))
from check_scene_fitness import check as check_scene_fitness
DEST = Path.home() / "Desktop/せたな町_素材_20260924"
STAGE = HERE / "delivery_staging_claude"; BACKUP = HERE / "previous_desktop_delivery_claude"
FIXED = HERE / "fixed" / "画像"
dry = "--dry-run" in sys.argv
review_path = Path(sys.argv[sys.argv.index("--review") + 1]) if "--review" in sys.argv else None
allow_fail = "--allow-fail" in sys.argv

def main():
    if STAGE.exists(): shutil.rmtree(STAGE)
    shutil.copytree(DEST, STAGE, ignore=shutil.ignore_patterns("*.md", "*.json", "試作_*"))
    names = sorted(p.name for p in FIXED.glob("ASSET-*.png"))
    for n in names:
        assert (STAGE / "画像" / n).exists(), f"納品に無い名前: {n}"
        shutil.copy2(FIXED / n, STAGE / "画像" / n)
    print(f"staging: {len(names)} files replaced")
    if review_path is None:
        subprocess.run([sys.executable, str(HERE / "update_review_json.py"), str(STAGE)], check=True)
        rp = HERE / "scene_fitness_review_claude.json"
    else:
        rp = review_path
    review = json.loads(rp.read_text())
    source = (ROOT.parent / "Asset_Prompts_Full.md").read_text()
    baseline = json.loads((ROOT / "scene_fitness_review/replacement_baseline_names.json").read_text())
    errors = check_scene_fitness(source, review, "delivery", STAGE, baseline=baseline, composite_root=HERE / "composites_final")
    ratio_err = [e for e in errors if e.startswith("シーン適合済みキャラ比率不足")]
    fail_err = [e for e in errors if "実素材のシーン適合確認が未完了" in e or "静止背景の人物なし目視確認が未完了" in e or "完成画の確認が未完了" in e or "全件確認していない" in e]
    other = [e for e in errors if e not in ratio_err and e not in fail_err]
    print(f"gate: {len(errors)} issues (ratio={len(ratio_err)}, remaining-fail={len(fail_err)}, other={len(other)})")
    for e in other[:20]: print("  OTHER:", e)
    if other or ratio_err or (fail_err and not allow_fail):
        print("STOP: gate FAIL → 納品先への反映 0件"); (HERE / "gate_result.json").write_text(json.dumps({"status": "FAIL", "errors": errors}, ensure_ascii=False, indent=1)); return 1
    (HERE / "gate_result.json").write_text(json.dumps({"status": "PASS_WITH_REMAINING_FAIL" if fail_err else "PASS", "errors": errors}, ensure_ascii=False, indent=1))
    if dry: print("dry-run: 反映しない"); return 0
    # 反映: 旧版を退避し、staging の画像だけを納品へコピー（動画・文書は触らない）
    BACKUP.mkdir(exist_ok=True)
    for n in names:
        shutil.copy2(DEST / "画像" / n, BACKUP / n); shutil.copy2(STAGE / "画像" / n, DEST / "画像" / n)
    shutil.copy2(rp, DEST / "検査結果_Claude_20260925.json")
    print(f"APPLIED: {len(names)} images replaced in {DEST}; backup at {BACKUP}"); return 0

if __name__ == "__main__":
    raise SystemExit(main())
