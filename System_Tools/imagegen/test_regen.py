"""python3 test_regen.py（Pillow が必要）。実作品には書き込まない。"""
from datetime import datetime
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, Mock
from PIL import Image, ImageDraw
import extract_prompts
import regen

PROJECT = regen.REPO / "Scripts/1988年戸沢村ツキノワグマ食害事件"
LOG = regen.REPO.parent / ".codex/handoff/delegations/logs/2026-09-16-image-check-transparency"
EXPECTED = [
    "CHAR-15", "CHAR-16", "CHAR-17", "ASSET-020_char", "ASSET-022_char",
    "ASSET-024_char", "ASSET-045_char", "ASSET-045_bg", "ASSET-047_char",
    "ASSET-050_char", "ASSET-052_char", "ASSET-052_bg", "ASSET-053_char",
    "ASSET-053_overlay", "ASSET-055_char", "ASSET-069_still",
]


def item(key, slot):
    return {"id": key, "slot": slot, "prompt": "test prompt"}


class RegenTest(unittest.TestCase):
    def setUp(self):
        LOG.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix="fixture-", dir=LOG))

    def transparent(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        im = Image.new("RGBA", (256, 256), (255, 255, 255, 0))
        ImageDraw.Draw(im).rectangle((80, 70, 176, 190), fill=(20, 80, 160, 255))
        im.save(path)
        return im

    def fixture(self):
        project, work = self.root / "project", self.root / "work"
        (project / "画像").mkdir(parents=True)
        (work / "images").mkdir(parents=True)
        queue = [item("ASSET-020_char", "char"), item("CHAR-15", "char_ref")]
        for entry in queue:
            self.transparent(work / "images" / (entry["id"] + ".png"))
        return project, work, queue

    def test_tozawa_exact_16(self):
        actual = [x["id"] for x in regen.detect_targets(PROJECT, "79873b3c^")]
        difference = {"expected": EXPECTED, "actual": actual,
                      "missing": sorted(set(EXPECTED)-set(actual)),
                      "unexpected": sorted(set(actual)-set(EXPECTED))}
        regen.write_json(LOG / "target_detection.json", difference)
        self.assertEqual(actual, EXPECTED, json.dumps(difference, ensure_ascii=False))

    def test_standard_names(self):
        examples = [("CHAR-15", "char_ref", "キャライラスト/CHAR-15.png"),
                    ("ASSET-020_char", "char", "ASSET-020.png"),
                    ("ASSET-020_bg", "bg", "ASSET-020-1.png"),
                    ("ASSET-069_still", "still", "ASSET-069.png"),
                    ("ASSET-053_overlay", "overlay", "ASSET-053_overlay.png")]
        for key, slot, expected in examples:
            with self.subTest(key=key):
                self.assertEqual(regen.standard_name(item(key, slot)).as_posix(), expected)
        for key in ("ASSET-020_char-2", "../ASSET-020_char"):
            with self.assertRaises(ValueError):
                regen.standard_name(item(key, "char"))

    def test_assets_override_and_invalid_id(self):
        actual = regen.detect_targets(PROJECT, "not-used", "ASSET-053_overlay,CHAR-15")
        self.assertEqual([x["id"] for x in actual], ["CHAR-15", "ASSET-053_overlay"])
        for ids in ("ASSET-999_char", "CHAR-15,CHAR-15"):
            with self.assertRaises(ValueError):
                regen.detect_targets(PROJECT, None, ids)

    def test_overlay_uses_character_style(self):
        overlay = next(x for x in extract_prompts.parse(PROJECT / "Asset_Prompts_Full.md")
                       if x["id"] == "ASSET-053_overlay")
        self.assertEqual(overlay["aspect"], "1:1")
        self.assertTrue(overlay["prompt"].startswith(extract_prompts.CHAR_STYLE))
        self.assertTrue(overlay["prompt"].endswith(extract_prompts.CHAR_TAIL))

    def test_mapping_is_reference_only(self):
        report = regen.mapping_notes(PROJECT, extract_prompts.parse(PROJECT / "Asset_Prompts_Full.md"))
        regen.write_json(LOG / "mapping_notes.json", report)
        self.assertEqual(report["shots"], 298)
        self.assertEqual(report["png_differences"], 7)
        self.assertEqual(report["existing_references"], report["references"])
        self.assertEqual(regen.standard_name(item("ASSET-022_char", "char")).name, "ASSET-022.png")

    def test_checkerboard_fails_even_with_25_percent_alpha(self):
        for step in (4, 8, 16, 24, 32):
            with self.subTest(step=step):
                im = Image.new("RGBA", (256, 256))
                im.putdata([(255,255,255,255) if (x//step+y//step)%2 else (210,210,210,255)
                            for y in range(256) for x in range(256)])
                ImageDraw.Draw(im).rectangle((64,64,191,191), fill=(0,0,0,0))
                path = self.root / f"checker-{step}.png"
                im.save(path)
                result = regen.inspect_image(path, "overlay")
                self.assertEqual(result["alpha_zero_fraction"], .25)
                self.assertTrue(any(result["checker_corners"]))
                self.assertFalse(result["pass"])

    def test_real_transparency_passes_all_character_slots(self):
        path = self.root / "transparent.png"
        self.transparent(path)
        for slot in ("char", "char_ref", "overlay"):
            self.assertTrue(regen.inspect_image(path, slot)["pass"])

    def test_hidden_checker_and_uniform_gray_are_not_checkerboards(self):
        im = Image.new("RGBA", (64,64))
        im.putdata([(255,255,255,0) if (x//8+y//8)%2 else (210,210,210,0)
                    for y in range(64) for x in range(64)])
        self.assertFalse(regen.checker_corner(im))
        self.assertFalse(regen.checker_corner(Image.new("RGBA", (64,64), (210,210,210,255))))

    def test_alpha_threshold_and_background_resolution(self):
        path = self.root / "opaque.png"
        Image.new("RGB", (160,90), "white").save(path)
        self.assertFalse(regen.inspect_image(path, "char")["pass"])
        for slot in ("bg", "still"):
            result = regen.inspect_image(path, slot)
            self.assertTrue(result["pass"])
            self.assertEqual((result["width"], result["height"]), (160,90))
        im = Image.new("RGBA", (100,100), (255,0,0,255))
        ImageDraw.Draw(im).rectangle((0,0,99,18), fill=(0,0,0,0))
        im.save(path)
        self.assertFalse(regen.inspect_image(path, "char")["pass"])
        ImageDraw.Draw(im).rectangle((0,0,99,19), fill=(0,0,0,0))
        im.save(path)
        self.assertTrue(regen.inspect_image(path, "char")["pass"])

    def test_verify_auto_fixes_white_background_and_records_it(self):
        work = self.root / "work"
        (work / "images").mkdir(parents=True)
        path = work / "images/ASSET-020_char.png"
        Image.new("RGB", (100, 100), "white").save(path)
        queue = [item("ASSET-020_char", "char")]
        fixed = regen.auto_fix_transparency(work, queue)
        report = regen.verify(work, queue, fixed)
        self.assertEqual(fixed, {"ASSET-020_char"})
        self.assertTrue(report["all_pass"])
        self.assertTrue(report["items"][0]["auto_transparent"])
        self.assertTrue((work / "transparency_backup/ASSET-020_char.png").is_file())

    def test_checkerboard_is_not_auto_fixed(self):
        work = self.root / "work"
        (work / "images").mkdir(parents=True)
        path = work / "images/ASSET-020_char.png"
        image = Image.new("RGB", (128, 128))
        image.putdata([(255, 255, 255) if (x // 8 + y // 8) % 2 else (210, 210, 210)
                       for y in range(128) for x in range(128)])
        image.save(path)
        before = path.read_bytes()
        fixed = regen.auto_fix_transparency(work, [item("ASSET-020_char", "char")])
        self.assertEqual(fixed, set())
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse((work / "transparency_backup").exists())

    def test_missing_and_corrupt_images_are_in_sheet_and_report(self):
        (self.root / "images").mkdir()
        (self.root / "images/ASSET-001_bg.png").write_bytes(b"not png")
        report = regen.verify(self.root, [item("ASSET-001_bg", "bg"), item("CHAR-15", "char_ref")])
        self.assertEqual((report["total"], report["passed"]), (2,0))
        self.assertFalse(report["all_pass"])
        self.assertEqual([r["exists"] for r in report["items"]], [True,False])
        with Image.open(self.root / "sheet.jpg") as sheet:
            self.assertLessEqual(max(sheet.size), 2048)
        self.assertTrue((self.root / "verify.json").is_file())

    def test_apply_standard_names_backup_new_file_and_drive(self):
        project, work, queue = self.fixture()
        original = project / "画像/ASSET-020.png"
        original.write_bytes(b"old standard")
        derived = project / "画像/ASSET-020_実写.png"
        derived.write_bytes(b"leave derived alone")
        regen.verify(work, queue)
        drive = self.root / "drive"
        self.assertEqual(regen.apply(project, work, queue, drive), 2)
        backup = project / ("画像/_旧_"+datetime.now().strftime("%Y%m%d")) / original.name
        self.assertEqual(backup.read_bytes(), b"old standard")
        self.assertEqual(derived.read_bytes(), b"leave derived alone")
        for entry in queue:
            relative = regen.standard_name(entry)
            self.assertEqual((project / "画像" / relative).read_bytes(), (drive / relative).read_bytes())
        with self.assertRaises(ValueError):
            regen.apply(project, work, queue)
        self.assertEqual(backup.read_bytes(), b"old standard")

    def test_apply_requires_pass_and_rechecks_stale_images(self):
        project, work, queue = self.fixture()
        original = project / "画像/ASSET-020.png"
        original.write_bytes(b"do not modify")
        with self.assertRaises(ValueError):
            regen.apply(project, work, queue)
        regen.verify(work, queue)
        Image.new("RGB", (256,256), "white").save(work / "images/CHAR-15.png")
        with self.assertRaises(ValueError):
            regen.apply(project, work, queue)
        self.assertEqual(original.read_bytes(), b"do not modify")

    def test_apply_rejects_standard_name_collision_before_copy(self):
        project, work, queue = self.fixture()
        queue.append(item("ASSET-020_still", "still"))
        self.transparent(work / "images/ASSET-020_still.png")
        regen.verify(work, queue)
        with self.assertRaises(ValueError):
            regen.apply(project, work, queue)
        self.assertFalse((project / "画像/ASSET-020.png").exists())

    def test_run_delegates_without_waiting(self):
        project = self.root / "project"
        project.mkdir()
        (project / "Asset_Prompts_Full.md").write_text("### CHAR-15: test\n```a person```\n")
        with patch.object(regen.subprocess, "Popen", return_value=Mock(pid=12345)) as start:
            self.assertEqual(regen.main([str(project), "--assets", "CHAR-15", "--run"]), 0)
        self.assertEqual(start.call_args.args[0][0], "nohup")
        self.assertIn(str(regen.HERE / "run.py"), start.call_args.args[0])
        self.assertTrue(start.call_args.kwargs["start_new_session"])
        work = project / ".imagegen" / ("regen_"+datetime.now().strftime("%Y%m%d"))
        self.assertEqual((work / "run.pid").read_text().strip(), "12345")
        with patch.object(regen.subprocess, "Popen") as start:
            self.assertEqual(regen.main([str(project), "--verify"]), 1)
            start.assert_not_called()

    def test_run_passes_parallel_to_runner(self):
        project = self.root / "project"
        project.mkdir()
        (project / "Asset_Prompts_Full.md").write_text("### CHAR-15: test\n```a person```\n")
        work = project / ".imagegen/regen_20260913_review"
        with patch.object(regen.subprocess, "Popen", return_value=Mock(pid=12345)) as start:
            self.assertEqual(regen.main([str(project), "--assets", "CHAR-15",
                                        "--work-name", work.name, "--run", "--parallel", "1"]), 0)
        self.assertEqual(start.call_args.args[0],
                         ["nohup", regen.sys.executable, "-B", "-u", str(regen.HERE / "run.py"),
                          str(work), "--parallel", "1"])
        self.assertEqual((work / "run.pid").read_text().strip(), "12345")

    def test_run_passes_global_min_interval_and_work_name(self):
        project = self.root / "project"
        project.mkdir()
        (project / "Asset_Prompts_Full.md").write_text("### CHAR-15: test\n```a person```\n")
        work = project / ".imagegen/regen_20260913_review"
        with patch.object(regen.subprocess, "Popen", return_value=Mock(pid=12345)) as start:
            self.assertEqual(regen.main([str(project), "--assets", "CHAR-15", "--work-name", work.name,
                                        "--run", "--parallel", "2", "--min-interval", "60"]), 0)
        self.assertEqual(start.call_args.args[0][-4:], ["--parallel", "2", "--min-interval", "60.0"])
        self.assertIn(str(work), start.call_args.args[0])
        self.assertTrue(start.call_args.kwargs["start_new_session"])

    def test_run_forwards_exclusions_without_changing_existing_queue(self):
        project = self.root / "project"
        project.mkdir()
        (project / "Asset_Prompts_Full.md").write_text("### CHAR-15: test\n```a person```\n")
        work = project / ".imagegen/regen_20260913_review"
        common = [str(project), "--assets", "CHAR-15", "--work-name", work.name]
        self.assertEqual(regen.main(common), 0)
        before = (work / "image_queue.json").read_bytes()
        with patch.object(regen.subprocess, "Popen", return_value=Mock(pid=12345)) as start:
            self.assertEqual(regen.main(common + ["--run", "--exclude", "CHAR-15",
                                                 "--exclude-slots", "bg,still"]), 0)
        self.assertEqual(start.call_args.args[0][-4:],
                         ["--exclude", "CHAR-15", "--exclude-slots", "bg,still"])
        self.assertEqual((work / "image_queue.json").read_bytes(), before)

    def test_work_name_isolates_run_and_verify(self):
        project = self.root / "project"
        old = project / ".imagegen/regen_20260913"
        old.mkdir(parents=True)
        regen.write_json(old / "image_queue.json", [])
        original = (old / "image_queue.json").read_bytes()
        (project / "Asset_Prompts_Full.md").write_text("### CHAR-15: test\n```a person```\n")
        work = project / ".imagegen/regen_20260913_review"
        with patch.object(regen.subprocess, "Popen", return_value=Mock(pid=12345)) as start:
            self.assertEqual(regen.main([str(project), "--assets", "CHAR-15",
                                        "--work-name", work.name, "--run"]), 0)
        self.assertEqual(start.call_args.args[0][-1], str(work))
        self.assertEqual((work / "run.pid").read_text().strip(), "12345")
        self.transparent(work / "images/CHAR-15.png")
        self.assertEqual(regen.main([str(project), "--verify", "--work-name", work.name]), 0)
        self.assertTrue((work / "verify.json").is_file())
        self.assertEqual((old / "image_queue.json").read_bytes(), original)
        self.assertEqual(list(old.iterdir()), [old / "image_queue.json"])

    def test_verify_uses_existing_queue_across_midnight(self):
        project = self.root / "project"
        work = project / ".imagegen/regen_20260912"
        work.mkdir(parents=True)
        (project / "Asset_Prompts_Full.md").write_text("### CHAR-15: test\n```a person```\n")
        queue = extract_prompts.parse(project / "Asset_Prompts_Full.md")
        regen.write_json(work / "image_queue.json", queue)
        self.transparent(work / "images/CHAR-15.png")
        with patch.object(regen, "datetime") as clock:
            clock.now.return_value = datetime(2026, 9, 13)
            self.assertEqual(regen.main([str(project), "--verify"]), 0)
        self.assertTrue((work / "verify.json").is_file())
        self.assertFalse((project / ".imagegen/regen_20260913").exists())

    def test_short_project_name_rules_and_fallback(self):
        cases = {
            "1988年戸沢村ツキノワグマ食害事件": "戸沢村",
            "1915年三毛別羆事件": "1915年三毛別羆事件",
            "1902年八甲田山雪中行軍遭難事件": "八甲田山",
            "2009年トムラウシ山遭難事故": "トムラウシ山",
            "羅臼岳遭難事件": "羅臼岳",
            "戸沢村": "戸沢村",
            "2026年名前を判別できない事件": "2026年名前を判別できない事件",
        }
        for name, expected in cases.items():
            with self.subTest(name=name):
                self.assertEqual(regen.short_project_name(Path(name)), expected)

    def test_export_directory_uses_desktop_short_name_and_current_date(self):
        with patch.object(Path, "home", return_value=self.root), patch.object(regen, "datetime") as clock:
            clock.now.return_value = datetime(2026, 9, 13)
            self.assertEqual(regen.export_directory(PROJECT),
                             self.root / "Desktop/戸沢村_差し替え画像_20260913")
            self.assertEqual(regen.export_directory(Path("判別不能")),
                             self.root / "Desktop/判別不能_差し替え画像_20260913")

    def test_export_standard_names_and_leaves_project_images_untouched(self):
        project, work, queue = self.fixture()
        queue.extend([item("ASSET-045_bg", "bg"), item("ASSET-053_overlay", "overlay"),
                      item("ASSET-069_still", "still")])
        for entry in queue:
            self.transparent(work / "images" / (entry["id"] + ".png"))
        original = project / "画像/ASSET-020.png"
        original.write_bytes(b"keep original")
        regen.verify(work, queue)
        with patch.object(Path, "home", return_value=self.root):
            dest = regen.export(project, work, queue)
        self.assertTrue(dest.is_absolute())
        self.assertEqual({p.relative_to(dest).as_posix() for p in dest.rglob("*.png")},
                         {"ASSET-020.png", "キャライラスト/CHAR-15.png", "ASSET-045-1.png",
                          "ASSET-053_overlay.png", "ASSET-069.png"})
        for entry in queue:
            self.assertEqual(regen.sha(dest / regen.standard_name(entry)),
                             regen.sha(work / "images" / (entry["id"] + ".png")))
        self.assertEqual(original.read_bytes(), b"keep original")
        self.assertEqual(list((project / "画像").iterdir()), [original])

    def test_export_requires_verify_and_rechecks_stale_images(self):
        project, work, queue = self.fixture()
        with patch.object(Path, "home", return_value=self.root):
            with self.assertRaises(ValueError):
                regen.export(project, work, queue)
            regen.write_json(work / "verify.json", {"all_pass": False})
            with self.assertRaises(ValueError):
                regen.export(project, work, queue)
            regen.verify(work, queue)
            Image.new("RGB", (256,256), "white").save(work / "images/CHAR-15.png")
            with self.assertRaises(ValueError):
                regen.export(project, work, queue)
        self.assertFalse((self.root / "Desktop").exists())

    def test_export_rejects_collision_before_copy(self):
        project, work, queue = self.fixture()
        queue.append(item("ASSET-020_still", "still"))
        self.transparent(work / "images/ASSET-020_still.png")
        regen.verify(work, queue)
        with patch.object(Path, "home", return_value=self.root):
            with self.assertRaises(ValueError):
                regen.export(project, work, queue)
        self.assertFalse((self.root / "Desktop").exists())

    def test_export_cli_uses_latest_queue_and_prints_absolute_path_last(self):
        from contextlib import redirect_stdout
        from io import StringIO
        project = self.root / PROJECT.name
        work = project / ".imagegen/regen_20260912"
        work.mkdir(parents=True)
        (project / "Asset_Prompts_Full.md").write_text("### CHAR-15: test\n```a person```\n")
        queue = extract_prompts.parse(project / "Asset_Prompts_Full.md")
        regen.write_json(work / "image_queue.json", queue)
        self.transparent(work / "images/CHAR-15.png")
        regen.verify(work, queue)
        output = StringIO()
        with patch.object(Path, "home", return_value=self.root), patch.object(regen, "datetime") as clock:
            clock.now.return_value = datetime(2026, 9, 13)
            with redirect_stdout(output), patch.object(regen.subprocess, "Popen") as start:
                self.assertEqual(regen.main([str(project), "--export"]), 0)
                start.assert_not_called()
        dest = self.root / "Desktop/戸沢村_差し替え画像_20260913"
        self.assertEqual(output.getvalue().splitlines()[-1], str(dest.resolve()))
        self.assertTrue((dest / "キャライラスト/CHAR-15.png").is_file())
        self.assertFalse((project / "画像").exists())
        self.assertFalse((project / ".imagegen/regen_20260913").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
