#!/usr/bin/env python3
"""
検査の較正チェック（2026-09-01 新設）

**出荷済み（＝本人が承認して公開した）台本が、いまの検査を通るか**を一括で確認する。
通らないなら検査側が間違い。→ feedback_calibrate_audits_to_shipped_content.md

2026-09-01 に、この考え方で3つの誤った基準が見つかった:
  - `遺体` を本文で禁止 → 出荷済み12本が使用（朱鞠内湖4件・十和利山30件）。タイトル/サムネ専用へ
  - イントロ 200-270字 → 出荷済み7本のうち4本が違反（羅臼岳128・大千軒岳151・風不死岳162）。120-380へ
  - セットアップ 150字以内 → 7本のうち6本が違反（実測112-778・中央値444）。150-500へ

**検査のしきい値を変えたら、必ずこれを走らせる。**
  python3 check_calibration.py
"""
import subprocess, glob, sys, os, json

VALIDATORS = [
    ("safety",      "validate_yama_safety.py"),
    ("narrative",   "validate_yama_narrative.py"),
    ("facts",       "validate_yama_facts.py"),
    ("intro",       "validate_yama_intro.py"),
    ("numeric",     "audit_numeric_facts.py"),
    ("consistency", "validate_yama_consistency.py"),
]

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    scripts = sorted(glob.glob(os.path.join(here, "..", "Scripts", "*", "Master.md")))
    if not scripts:
        print("出荷済み台本が見つかりません"); return 2

    print("=" * 78)
    print("検査の較正チェック — 出荷済み台本が、いまの検査を通るか")
    print("=" * 78)
    print(f"{'台本':<26}" + "".join(f"{n:>13}" for n, _ in VALIDATORS))

    bl_path = os.path.join(here, "calibration_baseline.json")
    baseline = {}
    if os.path.exists(bl_path):
        baseline = {k: v for k, v in json.load(open(bl_path, encoding="utf-8")).items()
                    if not k.startswith("_")}

    ng, known = [], []
    for sp in scripts:
        name = os.path.basename(os.path.dirname(sp))[:24]
        row = f"{name:<26}"
        for label, v in VALIDATORS:
            r = subprocess.run([sys.executable, os.path.join(here, v), sp],
                               capture_output=True, text=True)
            ok = r.returncode == 0
            full = os.path.basename(os.path.dirname(sp))
            is_known = label in baseline.get(full, {})
            if ok:
                row += f"{'  OK':>13}"
            elif is_known:
                row += f"{'  (既知)':>13}"; known.append((full, label))
            else:
                row += f"{'  NG':>13}"; ng.append((full, label))
        print(row)

    print()
    print(f"既知の失敗（台帳に理由あり）: {len(known)}件")
    if not ng:
        print("[PASS] 台帳に無い新しい失敗はありません。基準は実績と整合しています")
        return 0
    print(f"--- 🔴 REGRESSION: 台帳に無い新しい失敗 {len(ng)}件 ---")
    for n, l in ng:
        print(f"  x {n}  ←  {l}")
    print("\n⚠️ 出荷済み（本人が承認して公開した）内容が新たに落ちたなら、まず検査側を疑う。")
    print("   直した結果それが正しい失敗なら、calibration_baseline.json に理由つきで登録する。")
    print("   台本を基準に合わせるのではなく、基準を実績に合わせること。")
    print("   → feedback_calibrate_audits_to_shipped_content.md")
    return 1

if __name__ == "__main__":
    sys.exit(main())
