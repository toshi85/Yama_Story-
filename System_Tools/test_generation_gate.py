"""generation_gate.py: 2026-09-24 せたな町の失敗（見本なし全件発注・後付けの文・記録なし）を注入して止まるか確かめる。"""
import hashlib
import json
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "imagegen"))
import generation_gate as gg
import extract_prompts as ep

CHAR = ("Cute cartoon character design, thick black outlines, flat cel-shaded colors, children's animation style. "
        "A full-body Japanese husband in his 50s, three-quarter front view facing to the right, face clearly visible. "
        "Transparent background.")
BG = "A rural house doorway toward a wooded mountain road in early spring, Japan. No people. 16:9 aspect ratio."
MD = "# テスト\n\n## 1. 全素材リスト\n\n" + "".join(
    f"ナレーター: 説明{i}です。\n\n【制作メモ】ASSET-{i:03d} [キャラアニメーション]\n"
    f"キャラプロンプト（1:1）:\n```\n{CHAR.replace('husband', f'husband number {i}')}\n```\n"
    f"背景プロンプト（16:9）:\n```\n{BG}\n```\n\n---\n\n" for i in range(1, 6))


class GateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for name in ("STAMPS", "APPROVALS", "USAGE"):
            setattr(gg, name, self.tmp / name.lower())
        self.md = self.tmp / "作品" / "Asset_Prompts.md"
        self.md.parent.mkdir()
        self.md.write_text(MD, encoding="utf-8")
        self.stamp()
        self.items = [{"id": f"ASSET-{i:03d}_char", "prompt": CHAR.replace("husband", f"husband number {i}")}
                      for i in range(1, 6)]

    def stamp(self):
        gg.STAMPS.mkdir(parents=True, exist_ok=True)
        (gg.STAMPS / "x.json").write_text(json.dumps({
            "file": str(self.md), "status": "PASS",
            "sha256": hashlib.sha256(self.md.read_bytes()).hexdigest()}), encoding="utf-8")

    def approve(self, kind="image"):
        gg.APPROVALS.mkdir(parents=True, exist_ok=True)
        (gg.APPROVALS / f"{gg.header_key(self.md)}_{kind}.json").write_text("{}", encoding="utf-8")

    def test_no_stamp_is_blocked(self):
        (gg.STAMPS / "x.json").unlink()
        with self.assertRaises(gg.GateError):
            gg.require("image", self.items[:1], tool="t", paid=True)

    def test_sentence_appended_after_200_chars_is_blocked(self):
        # 旧フックは先頭200文字しか照合しなかった。末尾に後ろ向き指示を足したキューを流す
        bad = [{"id": "ASSET-001_char", "prompt": self.items[0]["prompt"] + " Seen from behind, face not identifiable."}]
        self.approve()
        with self.assertRaises(gg.GateError) as cm:
            gg.require("image", bad, tool="t", paid=True)
        self.assertIn("全文一致しない", str(cm.exception))

    def test_single_word_prompt_is_blocked(self):
        # 部分一致だと .md のどこかに含まれる1語（woodland 等）が通ってしまった（2026-09-25 実測）
        self.approve()
        with self.assertRaises(gg.GateError):
            gg.require("image", [{"id": "S001", "prompt": "rural"}], tool="t", paid=True)

    def test_edited_md_invalidates_stamp(self):
        self.md.write_text(MD + "\n追記", encoding="utf-8")
        with self.assertRaises(gg.GateError):
            gg.require("image", self.items[:1], tool="t", paid=True)

    def test_paid_bulk_before_sample_approval_is_blocked(self):
        # 2026-09-24: 見本を見ずに全件を有料発注した
        with self.assertRaises(gg.GateError) as cm:
            gg.require("image", self.items, tool="fal_queue.py", paid=True)
        self.assertIn("approve", str(cm.exception))

    def test_paid_one_sample_per_kind_then_block(self):
        self.assertEqual(1, len(gg.require("image", self.items[:1], tool="t", paid=True)))
        with self.assertRaises(gg.GateError):
            gg.require("image", self.items[1:2], tool="t", paid=True)   # 同じ種類（キャラ）の2件目

    def test_unpaid_bulk_is_trimmed_to_one_per_kind(self):
        self.assertEqual(1, len(gg.require("image", self.items, tool="run.py", paid=False)))

    def test_samples_cover_every_kind_even_if_queue_starts_with_backgrounds(self):
        # 2026-09-25: 先頭3件（背景だけ）を見本にすると、キャラを見ずに承認できた
        queue = [{"id": q["id"], "prompt": q["prompt"]} for q in ep.parse(self.md)]
        queue.sort(key=lambda q: q["id"].endswith("_char"))          # 背景を先頭に並べる
        got = {gg.slot_of(i["id"], "image") for i in gg.require("image", queue, tool="run.py", paid=False)}
        self.assertEqual({"bg", "char"}, got)

    def test_approval_needs_samples_of_every_kind(self):
        bg_only = [{"id": q["id"], "prompt": q["prompt"]} for q in ep.parse(self.md) if q["id"].endswith("_bg")][:1]
        gg.require("image", bg_only, tool="run.py", paid=False)
        used = json.loads(gg._usage_file(self.md, "image").read_text(encoding="utf-8"))
        missing = gg.slots_in_md(self.md, "image") - {gg.slot_of(u, "image") for u in used}
        self.assertEqual({"char"}, missing)

    def test_after_approval_all_pass_and_record_written(self):
        self.approve()
        self.assertEqual(5, len(gg.require("image", self.items, tool="fal_queue.py", paid=True)))
        recs = list((self.md.parent / "発注記録").glob("*.json"))
        self.assertEqual(1, len(recs))
        rec = json.loads(recs[0].read_text(encoding="utf-8"))
        self.assertEqual(5, len(rec["items"]))
        self.assertTrue(rec["paid"])

    def test_video_needs_its_own_approval(self):
        self.approve("image")
        with self.assertRaises(gg.GateError):
            gg.require("video", self.items, tool="fal_video_queue.py", paid=True)

    def test_body_cut_edit_keeps_approval_but_header_edit_drops_it(self):
        self.approve()
        self.md.write_text(MD.replace("説明1です", "説明1を直しました"), encoding="utf-8")
        self.assertTrue(gg.approved(self.md, "image"))
        self.md.write_text("### CHAR-01: 夫\n```\nnew\n```\n" + MD, encoding="utf-8")
        self.assertFalse(gg.approved(self.md, "image"))

    def test_chatgpt_route_queue_passes(self):
        # extract_prompts.py が画風文を差し替えたキュー（ChatGPT経路）も、本文が .md の文なら通る
        self.approve()
        queue = [{"id": q["id"], "prompt": q["prompt"]} for q in ep.parse(self.md)]
        self.assertEqual(len(queue), len(gg.require("image", queue, tool="run.py", paid=False)))

    def test_chatgpt_route_with_injected_sentence_is_blocked(self):
        self.approve()
        queue = [{"id": q["id"], "prompt": q["prompt"]} for q in ep.parse(self.md)]
        queue[0]["prompt"] += " Rear view only."
        with self.assertRaises(gg.GateError):
            gg.require("image", queue, tool="run.py", paid=False)

    def test_portable_name_is_same_on_every_pc(self):
        # Windows は D:\0\Yama_Story-、Mac は …/Antigravity/Yama_Story。記録の名前はどちらでも同じにする
        md = gg.YAMA_REPO / "Scripts" / "作品" / "Asset_Prompts.md"
        self.assertEqual("yama:Scripts/作品/Asset_Prompts.md", gg.portable(md))
        self.assertEqual(md, gg.from_portable("yama:Scripts/作品/Asset_Prompts.md"))

    def test_approval_made_on_other_pc_is_used(self):
        # 別のPCで本人が承認し push した記録（origin/main にだけある）を、このPCでも使う
        name = f"{gg.header_key(self.md)}_image.json"
        with unittest.mock.patch.object(gg, "_shared", lambda d: True), \
             unittest.mock.patch.object(gg, "_remote", lambda d: {name: "{}"} if d == gg.APPROVALS else {}):
            self.assertTrue(gg.approved(self.md, "image"))
            self.assertEqual(5, len(gg.require("image", self.items, tool="t", paid=True, record=False)))

    def test_samples_made_on_other_pc_count(self):
        name = gg._usage_file(self.md, "image").name
        with unittest.mock.patch.object(gg, "_shared", lambda d: True), \
             unittest.mock.patch.object(gg, "_remote", lambda d: {name: '["ASSET-001_char"]'} if d == gg.USAGE else {}), \
             unittest.mock.patch.object(gg, "share", lambda *a, **k: None):
            with self.assertRaises(gg.GateError):   # キャラの見本は別のPCで作成済み→2件目は止まる
                gg.require("image", self.items[1:2], tool="t", paid=True, record=False)

    def test_is_yama(self):
        self.assertTrue(gg.is_yama(r"D:\0\Yama_Story-\Scripts\x\plan.json"))
        self.assertTrue(gg.is_yama("/Users/me/Antigravity/Yama_Story/Scripts/x/plan.json"))
        self.assertFalse(gg.is_yama(r"D:\0\Business\Jinruishi\video\犬\plan.json"))


if __name__ == "__main__":
    unittest.main()
