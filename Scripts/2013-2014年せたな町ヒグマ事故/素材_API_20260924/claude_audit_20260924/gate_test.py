#!/usr/bin/env python3
"""停止ゲートの実検証（追加課金なし・一時フォルダ）。
(1) 生成入口: build_bg_queue と同じ経路で「不適合な入力」（レビュー未完了）を与え、check_scene_fitness の preflight が FAIL＝発注0件で止まることを実証
(2) 納品入口: finalize_claude と同じ経路で、意図的に post_status=fail を混ぜた review を与え、納品先への反映0件で止まることを実証
実行ログは gate_test_result.json に残す。
"""
import json, sys, shutil, hashlib, tempfile, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent; WORKSPACE = ROOT.parents[3]
sys.path.insert(0, str(WORKSPACE / ".codex/skills/yama-asset-checker/scripts"))
from check_scene_fitness import check
source = (ROOT.parent / "Asset_Prompts_Full.md").read_text()
baseline = json.loads((ROOT / "scene_fitness_review/replacement_baseline_names.json").read_text())
result = {}
# (1) preflight: 原票（pre_status=pending）をそのまま渡す → FAIL 必須
orig = json.loads((ROOT / "scene_fitness_review/scene_fitness_review.json").read_text())
e1 = check(source, orig, "preflight")
result["preflight_with_pending_review"] = {"errors": len(e1), "blocked": bool(e1), "sample": e1[:3]}
# (2) delivery: 一時フォルダに納品を複製し、Claude版 review の1件を故意に fail にして渡す → FAIL 必須、反映0件
tmp = Path(tempfile.mkdtemp(prefix="gate_test_"))
DEST = Path.home() / "Desktop/せたな町_素材_20260924"
stage = tmp / "stage"; shutil.copytree(DEST, stage, ignore=shutil.ignore_patterns("*.md", "*.json", "試作_*"))
before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEST / "画像").glob("*.png")}
subprocess.run([sys.executable, str(HERE / "update_review_json.py"), str(stage)], check=True, capture_output=True)
rv = json.loads((HERE / "scene_fitness_review_claude.json").read_text())
victim = next(c for c in rv["cuts"] if c["category"] == "キャラアニメーション" and c["post_status"] == "pass")
victim["post_status"] = "fail"; victim["composite_verdict"] = "fail"; victim["human_free_background"] = False
bad = tmp / "review_bad.json"; bad.write_text(json.dumps(rv, ensure_ascii=False))
e2 = check(source, rv, "delivery", stage, baseline=baseline, composite_root=HERE / "composites_final")
hit = [e for e in e2 if f"ASSET-{victim['asset_no']:03d}" in e]
result["delivery_with_injected_fail"] = {"errors": len(e2), "blocked": bool(e2), "victim": f"ASSET-{victim['asset_no']:03d}", "victim_errors": hit[:4]}
# finalize_claude を --review で不適合 review 指定・dry-run 無しで走らせ、納品が1バイトも変わらないことを確認
r = subprocess.run([sys.executable, str(HERE / "finalize_claude.py"), "--review", str(bad)], capture_output=True, text=True)
after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEST / "画像").glob("*.png")}
changed = [n for n in before if before[n] != after.get(n)] + [n for n in after if n not in before]
result["finalize_with_bad_review"] = {"exit": r.returncode, "stdout_tail": r.stdout.strip().splitlines()[-2:], "delivery_files_changed": changed}
# (3) 別経路の封じ: finalize_cartoon_delivery.py（Codex版）も同じゲートを呼ぶかをコードで確認
code = (ROOT / "finalize_cartoon_delivery.py").read_text()
result["codex_finalize_calls_gate"] = "check_scene_fitness(" in code and "scene_errors" in code
# (4) 生成入口: このセッションの生成キューは repair_plan（Claude検収FAIL）だけから作られ、検収PASSのカットは含まないことを確認
plan = json.loads((HERE / "repair_plan.json").read_text()); q = json.loads((HERE / "regen_bg/image_queue.json").read_text())
rev = {c["asset"]: c["verdict"] for c in json.loads((HERE / "claude_review_full.json").read_text())["cuts"]}
leak = [x["id"] for x in q if rev.get(x["id"].rsplit("_", 1)[0]) == "PASS"]
result["generation_queue_only_from_failed_review"] = {"queue": len(q), "pass_leak": leak}
ok = result["preflight_with_pending_review"]["blocked"] and result["delivery_with_injected_fail"]["blocked"] and result["finalize_with_bad_review"]["exit"] != 0 and not changed and not leak
result["overall"] = "PASS" if ok else "FAIL"
(HERE / "gate_test_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=1))
shutil.rmtree(tmp, ignore_errors=True)
print(json.dumps(result, ensure_ascii=False, indent=1))
