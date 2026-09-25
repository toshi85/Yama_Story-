#!/usr/bin/env python3
"""ai_image_review.py の外部呼び出しを伴わないテスト。"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ai_image_review as review


SAMPLE_MD = """# sample

ナレーター: ひとつ前の語り。

【制作メモ】ASSET-001 [キャラアニメーション]
シーン: 前の人物が立つ
キャラプロンプト（1:1）:
```
First prompt.
```
→ 背景再使用: 900
→ 編集者指示: 左に置く。

---

ナレーター: 二つ目の語り。

【制作メモ】ASSET-002 [Lovart静止画]
シーン: 山道の場面
静止画プロンプト（16:9）:
```
Second prompt.
```
→ 編集者指示: 余白を残す。

---

ナレーター: 三つ目の語り。

【制作メモ】ASSET-003 [キャラアニメーション]
シーン: クマが歩く
キャラプロンプト（1:1）:
```
Third prompt.
```
→ 編集者指示: 四足歩行。
"""

REAL_NAME_MD = SAMPLE_MD.replace("ASSET-001", "ASSET-115").replace(
    "ASSET-002", "ASSET-116"
).replace("ASSET-003", "ASSET-117")


def make_args(md: Path, images: Path, out: Path, **overrides: object) -> argparse.Namespace:
    values = {
        "prompts": md,
        "images": images,
        "out": out,
        "assets": None,
        "batch": 2,
        "dry_run": False,
        "stage": "all",
        "allow_stale": True,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class ReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.md = self.root / "Asset_Prompts_Full.md"
        self.md.write_text(SAMPLE_MD, encoding="utf-8")
        self.images = self.root / "images"
        self.images.mkdir()
        self.out = self.root / "out"
        # 検品記録は本物の .claude/.state ではなく一時フォルダへ（本人に渡す前の関所が読む記録を汚さない）
        sys.path.insert(0, str(Path(review.__file__).resolve().parents[1]))
        import generation_gate
        self.gate = generation_gate
        self._reviews = mock.patch.object(generation_gate, "REVIEWS", self.root / "image_reviews")
        self._reviews.start()

    def tearDown(self) -> None:
        self._reviews.stop()
        self.temp.cleanup()

    def test_parse_and_production_notes(self) -> None:
        cuts = review.parse_cuts(self.md)
        self.assertEqual([cut.asset for cut in cuts], [1, 2, 3])
        self.assertEqual(cuts[0].narration, "ひとつ前の語り。")
        self.assertEqual(cuts[0].scene, "前の人物が立つ")
        self.assertEqual(cuts[0].editor, "左に置く。")
        self.assertEqual(cuts[0].background_reuse, "900")
        self.assertEqual(cuts[1].prompts, ("Second prompt.",))

    def test_image_name_matching_both_forms(self) -> None:
        for name in ("ASSET-001_char.png", "ASSET-001_キャラ_女性.png", "ASSET-010_char.png"):
            (self.images / name).touch()
        self.assertEqual(
            [path.name for path in review.find_images(self.images, 1)],
            ["ASSET-001_char.png", "ASSET-001_キャラ_女性.png"],
        )

    def test_real_asset_argument_and_desktop_filenames_are_selected(self) -> None:
        real_md = self.root / "Real_Asset_Prompts_Full.md"
        real_md.write_text(REAL_NAME_MD, encoding="utf-8")
        for name in ("ASSET-115_キャラ_女性.png", "ASSET-116_キャラ.png"):
            (self.images / name).touch()
        parsed = review.build_parser().parse_args([
            str(real_md), "--images", str(self.images), "--out", str(self.out),
            "--assets", "115,116", "--dry-run", "--stage", "sol", "--allow-stale",
        ])
        self.assertEqual(parsed.assets, [115, 116])
        review.run_review(parsed)
        prompt = (self.out / "dry_run" / "sol_001.prompt.txt").read_text(encoding="utf-8")
        self.assertEqual(prompt.count("対象: ASSET-"), 2)
        self.assertIn("ASSET-115_キャラ_女性.png", prompt)
        self.assertIn("ASSET-116_キャラ.png", prompt)

    def test_batches(self) -> None:
        cuts = review.parse_cuts(self.md)
        self.assertEqual([[cut.asset for cut in group] for group in review.batches(cuts, 2)], [[1, 2], [3]])

    def test_resume_skips_existing_sol_and_astra_json(self) -> None:
        for number in (1, 2):
            (self.images / f"ASSET-{number:03d}_char.png").touch()
        (self.out / "sol").mkdir(parents=True)
        (self.out / "astra").mkdir(parents=True)
        (self.out / "sol" / "001.json").write_text(json.dumps({
            "cuts": [
                {"asset": "1", "flag": True, "items": ["A1"], "reason": "候補"},
                {"asset": "2", "flag": False, "items": [], "reason": "問題なし"},
            ]
        }), encoding="utf-8")
        (self.out / "astra" / "001.json").write_text(json.dumps({
            "asset": "1", "verdict": "直す", "items": ["A1"], "why": "違う", "prompt_fix": "Replace it."
        }), encoding="utf-8")

        # 前回の実行で、今の画像・今のカットの検品記録が残っている状態
        cuts = {c.asset: c for c in review.parse_cuts(self.md)}
        for number, verdict in ((1, "直す"), (2, None)):
            path = self.images / f"ASSET-{number:03d}_char.png"
            review._record_review(self.md, cuts[number], path, review._sha256(path),
                                  sol_flag=number == 1, astra_verdict=verdict)

        def must_not_run(command: object, prompt: str) -> object:
            raise AssertionError(f"既存結果を飛ばしていない: {command}")

        calls = review.run_review(make_args(self.md, self.images, self.out, assets=[1, 2]), must_not_run)
        self.assertEqual(calls, {"sol": 0, "astra": 0, "failures": 0})

    def test_resume_rereviews_image_replaced_after_review(self) -> None:
        # 2026-09-25: 結果ファイルが残っていると、差し替えた画像を見ないまま「検品済み」になった
        for number in (1, 2):
            (self.images / f"ASSET-{number:03d}_char.png").write_bytes(b"old")
        (self.out / "sol").mkdir(parents=True)
        (self.out / "sol" / "001.json").write_text(json.dumps({"cuts": [
            {"asset": "1", "flag": False, "items": [], "reason": "問題なし"},
            {"asset": "2", "flag": False, "items": [], "reason": "問題なし"}]}), encoding="utf-8")
        cuts = {c.asset: c for c in review.parse_cuts(self.md)}
        for number in (1, 2):
            path = self.images / f"ASSET-{number:03d}_char.png"
            review._record_review(self.md, cuts[number], path, review._sha256(path), sol_flag=False)
        (self.images / "ASSET-002_char.png").write_bytes(b"new")     # 検品のあとで差し替え
        ran = []

        def runner(command: object, prompt: str) -> object:
            ran.append(prompt)
            out = json.dumps({"cuts": [{"asset": "1", "flag": False, "items": [], "reason": "問題なし"},
                                       {"asset": "2", "flag": False, "items": [], "reason": "問題なし"}]})
            return mock.Mock(returncode=0, stdout=out, stderr="")

        review.run_review(make_args(self.md, self.images, self.out, assets=[1, 2]), runner)
        self.assertEqual(1, len(ran))
        self.assertEqual([], self.gate.check_reviewed([self.images / "ASSET-002_char.png"]))

    def test_handoff_gate_blocks_unreviewed_fix_and_changed_cut(self) -> None:
        path = self.images / "ASSET-001_char.png"
        path.write_bytes(b"img")
        self.assertIn("まだ通っていない", self.gate.check_reviewed([path])[0])
        cut = {c.asset: c for c in review.parse_cuts(self.md)}[1]
        review._record_review(self.md, cut, path, review._sha256(path), sol_flag=True, astra_verdict="直す")
        self.assertIn("直す", self.gate.check_reviewed([path])[0])
        review._record_review(self.md, cut, path, review._sha256(path), sol_flag=True, astra_verdict=None)
        self.assertIn("Astra", self.gate.check_reviewed([path])[0])
        review._record_review(self.md, cut, path, review._sha256(path), sol_flag=True, astra_verdict="本人判断")
        self.assertEqual([], self.gate.check_reviewed([path]))
        self.md.write_text(self.md.read_text(encoding="utf-8").replace("ナレーター:", "ナレーター: 変更", 1), encoding="utf-8")
        self.assertIn("変わった", self.gate.check_reviewed([path])[0])

    def test_markdown_has_three_sections(self) -> None:
        (self.out / "sol").mkdir(parents=True)
        (self.out / "astra").mkdir(parents=True)
        sol = {"cuts": [
            {"asset": "1", "flag": True, "items": ["A1"], "reason": "候補1"},
            {"asset": "2", "flag": True, "items": ["B1"], "reason": "候補2"},
            {"asset": "3", "flag": True, "items": ["C1"], "reason": "候補3"},
            {"asset": "4", "flag": False, "items": [], "reason": "問題なし"},
        ]}
        (self.out / "sol" / "001.json").write_text(json.dumps(sol), encoding="utf-8")
        for asset, verdict in ((1, "直す"), (2, "本人判断"), (3, "直さない")):
            value = {"asset": str(asset), "verdict": verdict, "items": ["A1"], "why": "理由", "prompt_fix": "Fix" if asset != 3 else ""}
            (self.out / "astra" / f"{asset:03d}.json").write_text(json.dumps(value), encoding="utf-8")
        review.render_outputs(
            self.out, [1, 2, 3, 4], [5], {"sol": 2, "astra": 3, "failures": 0}, [], []
        )
        text = (self.out / "一覧.md").read_text(encoding="utf-8")
        for heading in ("## 直す", "## 本人判断", "## 直さない"):
            self.assertIn(heading, text)
        self.assertIn("Sol が挙げなかったカット（1件）", text)
        self.assertIn("ASSET-005", text)

    def test_dry_run_writes_prompt_and_command_for_each_batch(self) -> None:
        for number in (1, 2, 3):
            (self.images / f"ASSET-{number:03d}_char.png").touch()
        calls = review.run_review(make_args(self.md, self.images, self.out, dry_run=True, stage="sol"))
        files = sorted(path.name for path in (self.out / "dry_run").iterdir())
        self.assertEqual(files, [
            "sol_001.command.txt", "sol_001.prompt.txt",
            "sol_002.command.txt", "sol_002.prompt.txt",
        ])
        prompt = (self.out / "dry_run" / "sol_001.prompt.txt").read_text(encoding="utf-8")
        command = (self.out / "dry_run" / "sol_001.command.txt").read_text(encoding="utf-8")
        self.assertIn("迷ったら flag=true", prompt)
        self.assertIn("ASSET-001", prompt)
        self.assertIn("ASSET-002", prompt)
        self.assertIn("gpt-5.6-sol", command)
        self.assertFalse((self.out / "一覧.md").exists())
        self.assertFalse((self.out / "results.json").exists())

    def test_command_uses_stdin_after_terminating_image_arguments(self) -> None:
        images = [Path("ASSET-115_キャラ_女性.png"), Path("ASSET-116_キャラ.png")]
        command = review.command_for("model", Path("schema.json"), images)
        self.assertEqual(command[-2:], ["--", "-"])
        self.assertEqual(command.count("-i"), 2)
        for image in images:
            index = command.index(str(image))
            self.assertEqual(command[index - 1], "-i")
        self.assertNotIn("PROMPT TEXT", command)

    def test_failed_call_is_logged_and_next_batch_runs(self) -> None:
        for number in (1, 2, 3):
            (self.images / f"ASSET-{number:03d}_char.png").touch()
        count = 0

        def runner(command: object, prompt: str) -> object:
            nonlocal count
            count += 1
            if count == 1:
                return review.subprocess.CompletedProcess(command, 2, stdout="", stderr="failure")
            return review.subprocess.CompletedProcess(command, 0, stdout=json.dumps({
                "cuts": [{"asset": "ASSET-003", "flag": False, "items": [], "reason": "問題なし"}]
            }), stderr="")

        calls = review.run_review(make_args(self.md, self.images, self.out, stage="sol"), runner)
        self.assertEqual(calls["sol"], 2)
        self.assertEqual(calls["failures"], 1)
        self.assertIn("sol batch 001", (self.out / "errors.log").read_text(encoding="utf-8"))
        listing = (self.out / "一覧.md").read_text(encoding="utf-8")
        self.assertIn("## ⚠️ 失敗した呼び出し（1件）", listing)
        self.assertIn("ASSET-001, ASSET-002／exit=2 failure", listing)
        self.assertEqual(listing.count("（失敗したカットは含まない）"), 3)
        self.assertFalse((self.out / "sol" / "001.json").exists())
        self.assertTrue((self.out / "sol" / "002.json").exists())
        saved = json.loads((self.out / "sol" / "002.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["cuts"][0]["asset"], "3")

    def test_failed_call_makes_main_return_one(self) -> None:
        (self.images / "ASSET-001_char.png").touch()
        failure = review.subprocess.CompletedProcess(
            ["codex"], 1, stdout="", stderr="first error line\nmore detail"
        )
        with mock.patch.object(review, "default_runner", return_value=failure):
            code = review.main([
                str(self.md), "--images", str(self.images), "--out", str(self.out),
                "--assets", "1", "--batch", "1", "--stage", "sol", "--allow-stale",
            ])
        self.assertEqual(code, 1)
        listing = (self.out / "一覧.md").read_text(encoding="utf-8")
        self.assertIn("## ⚠️ 失敗した呼び出し（1件）", listing)
        self.assertIn("first error line", listing)

    def test_zero_targets_returns_exit_code_one_with_reason(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = review.main([
                str(self.md), "--images", str(self.images), "--out", str(self.out),
                "--assets", "1,2", "--dry-run",
            ])
        self.assertEqual(code, 1)
        self.assertIn("対象0件", stderr.getvalue())
        self.assertIn("画像名", stderr.getvalue())

    def _write_cached_sol(self, asset: int = 1) -> None:
        (self.out / "sol").mkdir(parents=True, exist_ok=True)
        value = {"cuts": [{
            "asset": str(asset), "flag": False, "items": [], "reason": "問題なし"
        }]}
        (self.out / "sol" / "001.json").write_text(json.dumps(value), encoding="utf-8")

    def test_newer_image_stops_with_exit_code_two(self) -> None:
        image = self.images / "ASSET-001_char.png"
        image.touch()
        os.utime(self.md, (100, 100))
        os.utime(image, (200, 200))
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = review.main([
                str(self.md), "--images", str(self.images), "--out", str(self.out),
                "--assets", "1", "--stage", "sol",
            ])
        self.assertEqual(code, 2)
        self.assertIn("プロンプトより新しい画像が 1 枚あります（例: ASSET-001）", stderr.getvalue())
        self.assertIn("--allow-stale", stderr.getvalue())

    def test_allow_stale_continues_and_writes_warning(self) -> None:
        image = self.images / "ASSET-001_char.png"
        image.touch()
        os.utime(self.md, (100, 100))
        os.utime(image, (200, 200))
        self._write_cached_sol()
        code = review.main([
            str(self.md), "--images", str(self.images), "--out", str(self.out),
            "--assets", "1", "--stage", "sol", "--allow-stale",
        ])
        self.assertEqual(code, 0)
        listing = (self.out / "一覧.md").read_text(encoding="utf-8")
        self.assertIn("## ⚠️ プロンプトより新しい画像（1枚）", listing)
        self.assertIn("ASSET-001", listing)

    def test_older_image_does_not_stop(self) -> None:
        image = self.images / "ASSET-001_char.png"
        image.touch()
        os.utime(image, (100, 100))
        os.utime(self.md, (200, 200))
        self._write_cached_sol()
        code = review.main([
            str(self.md), "--images", str(self.images), "--out", str(self.out),
            "--assets", "1", "--stage", "sol",
        ])
        self.assertEqual(code, 0)
        listing = (self.out / "一覧.md").read_text(encoding="utf-8")
        self.assertNotIn("プロンプトより新しい画像", listing)


if __name__ == "__main__":
    unittest.main()
