#!/usr/bin/env python3
"""変更したプロンプトだけを既存の run.py で生成し、検査後に標準名へコピーする。"""
import argparse
from contextlib import contextmanager
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

import extract_prompts
from transparency import make_transparent

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TRANSPARENT_SLOTS = {"char", "char_ref", "overlay"}
# 納品先の「画像/」を基準とする固定規則。派生ファイルは対象にしない。
NAME_RULES = {
    "char_ref": "キャライラスト/{base}.png",
    "char": "{base}.png",
    "bg": "{base}-1.png",
    "still": "{base}.png",
    "overlay": "{base}_overlay.png",
}


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TextDocument:
    """parse の read_text インターフェースで git show の版も同じ解析へ渡す。"""
    def __init__(self, text):
        self.text = text

    def read_text(self, encoding="utf-8"):
        return self.text


def indexed(items):
    result = {item["id"]: item for item in items}
    if len(result) != len(items):
        raise ValueError("プロンプトのIDが重複しています")
    return result


def sort_key(item):
    base, _, slot = item["id"].partition("_")
    return (0 if base.startswith("CHAR-") else 1, int(base.split("-")[1]),
            {"char": 0, "bg": 1, "still": 2, "overlay": 3}.get(slot, 0))


def detect_targets(project, since, assets=None):
    source = project / "Asset_Prompts_Full.md"
    current = indexed(extract_prompts.parse(source))
    if assets is not None:
        requested = assets.split(",")
        if not all(requested) or len(requested) != len(set(requested)):
            raise ValueError("--assets は空欄・重複のないID一覧を指定してください")
        unknown = sorted(set(requested) - current.keys())
        if unknown:
            raise ValueError(f"生成対象にないID: {unknown}")
        selected = [current[key] for key in requested]
    else:
        if not since:
            raise ValueError("キュー作成には --since が必要です")
        relative = source.resolve().relative_to(REPO).as_posix()
        old_text = subprocess.run(
            ["git", "-C", str(REPO), "show", f"{since}:{relative}"],
            check=True, capture_output=True, text=True, encoding="utf-8",
        ).stdout
        old = indexed(extract_prompts.parse(TextDocument(old_text)))
        selected = [item for key, item in current.items()
                    if key not in old or item["prompt"] != old[key]["prompt"]]
    return sorted(selected, key=sort_key)


def standard_name(item):
    key, slot = item["id"], item["slot"]
    pattern = r"CHAR-\d{2,}" if slot == "char_ref" else rf"ASSET-\d{{3,}}_{slot}"
    if slot not in NAME_RULES or not re.fullmatch(pattern, key):
        raise ValueError(f"標準名の規則にないID/slot: {key}/{slot}")
    return Path(NAME_RULES[slot].format(base=key.split("_")[0]))


def short_project_name(project):
    """年を除き、市町村・山岳・峠で終わる地名を抽出。判別不能なら原名。"""
    name = re.sub(r"^\d{4}年", "", project.name)
    match = re.fullmatch(
        r"(.+?(?:市|町|村|山|岳|峠))"
        r"(?:(?:ツキノワグマ|ヒグマ|クマ|熊)?"
        r"(?:食害|獣害|襲撃|雪中行軍|集団|雪崩|滑落|遭難)*(?:事件|事故)?)?", name)
    return match.group(1) if match else project.name


def export_directory(project):
    date = datetime.now().strftime("%Y%m%d")
    return Path.home() / "Desktop" / f"{short_project_name(project)}_差し替え画像_{date}"


def require_ai_review(work, queue):
    """本人に渡す前のAI検品（generation_gate.check_reviewed）。受講生の環境では対象外。"""
    sys.path.insert(0, str(HERE.parent))
    import generation_gate
    if not generation_gate.owner_machine():
        return
    problems = generation_gate.check_reviewed([work / "images" / (item["id"] + ".png") for item in queue
                                               if (work / "images" / (item["id"] + ".png")).exists()])
    if problems:
        raise ValueError("AI検品（ai_image_review.py）を通っていない画像があるため止めました:\n  "
                         + "\n  ".join(problems[:10]))


def export(project, work, queue):
    report_path = work / "verify.json"
    if not report_path.exists() or not json.loads(report_path.read_text())["all_pass"]:
        raise ValueError("先に --verify を全件合格させ、sheet.jpg を目視確認してください")
    if not verify(work, queue)["all_pass"]:
        raise ValueError("現在の画像が検査不合格のため書き出しません")
    require_ai_review(work, queue)
    root = export_directory(project)
    if root.is_symlink():
        raise ValueError(f"リンク先には書き出しません: {root}")
    plans, destinations = [], set()
    for item in queue:
        relative = standard_name(item)
        dest = root / relative
        if dest in destinations:
            raise ValueError(f"標準名が衝突しています: {relative}")
        destinations.add(dest)
        if (dest.is_symlink() or dest.parent.is_symlink()
                or not dest.resolve().is_relative_to(root.resolve())
                or (dest.exists() and not dest.is_file())):
            raise ValueError(f"書き出し先が不正です: {dest}")
        plans.append((work / "images" / (item["id"] + ".png"), dest))
    for source, dest in plans:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
    return root.resolve()


def mapping_notes(project, items):
    """shots の参照は納品名を変更する根拠にせず、相違を参考情報として残す。"""
    source = project / "shots.json"
    if not source.exists():
        return {"shots": 0, "notes": [], "info": "shots.json なし（標準名は固定）"}
    data = json.loads(source.read_text(encoding="utf-8"))
    shots = data["shots"] if isinstance(data, dict) else data
    by_asset = {}
    for item in items:
        if item["slot"] in ("char", "still", "bg"):
            by_asset.setdefault(item["id"].split("_")[0], []).append(item)
    notes, matched_rows, references, existing = [], 0, 0, 0
    for row in shots:
        row_notes = []
        for field in ("asset_file", "background_file"):
            value = row.get(field, "")
            if value:
                references += 1
                existing += int((project / value).is_file())
        for item in by_asset.get(row.get("asset_id"), []):
            field = "background_file" if item["slot"] == "bg" else "asset_file"
            value = row.get(field, "")
            expected = (Path("画像") / standard_name(item)).as_posix()
            if value != expected:
                row_notes.append({"shot_id": row.get("id"), "id": item["id"],
                                  "field": field, "standard": expected, "actual": value,
                                  "actual_exists": bool(value) and (project / value).is_file(),
                                  "standard_exists": (project / expected).is_file()})
        notes.extend(row_notes)
        matched_rows += int(not row_notes)
    png_differences = sum(n["actual"].lower().endswith(".png") for n in notes)
    return {"shots": len(shots), "rows_without_difference": matched_rows,
            "references": references, "existing_references": existing,
            "png_differences": png_differences, "notes": notes}


def checker_corner(crop):
    """白/明灰の二色が縦横とも周期的に反転する、描き込まれた格子を検出。"""
    crop = crop.convert("RGBA")
    w, h = crop.size
    labels = []
    pixels = crop.load()
    for r, g, b, a in (pixels[x, y] for y in range(h) for x in range(w)):
        neutral = a >= 250 and max(r, g, b) - min(r, g, b) <= 12
        labels.append(1 if neutral and min(r, g, b) >= 245 else
                      0 if neutral and 180 <= min(r, g, b) and max(r, g, b) <= 240 else -1)
    total = w * h
    if not total or min(labels.count(0), labels.count(1)) < total * .1:
        return False
    if sum(x >= 0 for x in labels) < total * .9:
        return False
    for step in range(2, min(w, h) // 2 + 1):
        scores = []
        for dx, dy in ((step, 0), (0, step)):
            pairs = [(labels[y*w+x], labels[(y+dy)*w+x+dx])
                     for y in range(h-dy) for x in range(w-dx)]
            valid = [(a, b) for a, b in pairs if a >= 0 and b >= 0]
            scores.append(sum(a != b for a, b in valid) / max(1, len(valid)))
        if min(scores) >= .88:
            return True
    return False


def inspect_image(path, slot):
    from PIL import Image
    result = {"exists": path.is_file(), "pass": False}
    if not result["exists"]:
        return dict(result, reason="未生成")
    try:
        with Image.open(path) as im:
            im.load()
            result.update(width=im.width, height=im.height, sha256=sha(path))
            if im.format != "PNG":
                return dict(result, reason="PNGではありません")
            if slot in TRANSPARENT_SLOTS:
                alpha = "A" in im.getbands() or "transparency" in im.info
                rgba = im.convert("RGBA")
                fraction = rgba.getchannel("A").histogram()[0] / (im.width * im.height)
                size = min(64, im.width, im.height)
                corners = [(0, 0), (im.width-size, 0),
                           (0, im.height-size), (im.width-size, im.height-size)]
                checker = [checker_corner(rgba.crop((x, y, x+size, y+size)))
                           for x, y in corners]
                result.update(alpha=alpha, alpha_zero_fraction=fraction,
                              checker_corners=checker)
                result["pass"] = alpha and fraction >= .2 and not any(checker)
                result["reason"] = "合格" if result["pass"] else "透過/市松模様の検査不合格"
            else:
                result.update({"pass": True, "reason": "解像度記録"})
    except (OSError, ValueError) as exc:
        result.update(reason=f"画像を読めません: {exc}")
    return result


def auto_fix_transparency(work, queue):
    """市松模様以外の、アルファ不足の透過対象だけを補正する。"""
    fixed = set()
    backup_dir = work / "transparency_backup"
    for item in queue:
        if item["slot"] not in TRANSPARENT_SLOTS:
            continue
        path = work / "images" / (item["id"] + ".png")
        result = inspect_image(path, item["slot"])
        if (not result.get("exists") or any(result.get("checker_corners", []))
                or result.get("pass")):
            continue
        if not result.get("alpha", False) or result.get("alpha_zero_fraction", 0) < .2:
            outcome = make_transparent(path, backup_dir)
            if outcome["processed"]:
                fixed.add(item["id"])
    return fixed


def verify(work, queue, auto_transparent_ids=None):
    from PIL import Image, ImageDraw
    auto_transparent_ids = set(auto_transparent_ids or ())
    results = [dict(id=item["id"], slot=item["slot"],
                    **({"auto_transparent": True} if item["id"] in auto_transparent_ids else {}),
                    **inspect_image(work / "images" / (item["id"] + ".png"), item["slot"]))
               for item in queue]
    report = {"total": len(results), "passed": sum(r["pass"] for r in results),
              "all_pass": bool(results) and all(r["pass"] for r in results), "items": results}
    columns = max(1, math.ceil(math.sqrt(len(results))))
    rows = max(1, math.ceil(len(results) / columns))
    cell = min(320, 2048 // max(columns, rows))
    sheet = Image.new("RGB", (columns * cell, rows * cell), "#dddddd")
    draw = ImageDraw.Draw(sheet)
    for index, result in enumerate(results):
        x, y = index % columns * cell, index // columns * cell
        if result.get("width"):
            try:
                with Image.open(work / "images" / (result["id"] + ".png")) as im:
                    thumb = im.convert("RGBA")
                    thumb.thumbnail((cell-12, cell-42))
                    sheet.paste(thumb, (x+(cell-thumb.width)//2, y+32), thumb)
            except (OSError, ValueError):
                pass
        label = f'{result["id"]}  {"PASS" if result["pass"] else "FAIL" if result["exists"] else "MISSING"}'
        draw.text((x+6, y+8), label, fill="#166534" if result["pass"] else "#b91c1c")
    sheet.save(work / "sheet.jpg", quality=90)
    write_json(work / "verify.json", report)
    return report


def apply(project, work, queue, drive_dir=None):
    report_path = work / "verify.json"
    if not report_path.exists() or not json.loads(report_path.read_text())["all_pass"]:
        raise ValueError("先に --verify を全件合格させ、sheet.jpg を目視確認してください")
    # 古い verify.json だけを根拠にしない。コピー直前の画像を再検査する。
    if not verify(work, queue)["all_pass"]:
        raise ValueError("現在の画像が検査不合格のため適用しません")
    require_ai_review(work, queue)
    root = project / "画像"
    date = datetime.now().strftime("%Y%m%d")
    plans, destinations = [], set()
    for item in queue:
        relative = standard_name(item)
        dest = root / relative
        backup = root / f"_旧_{date}" / relative
        if dest in destinations:
            raise ValueError(f"標準名が衝突しています: {relative}")
        destinations.add(dest)
        if dest.is_symlink() or backup.is_symlink():
            raise ValueError(f"リンク先には適用しません: {relative}")
        if backup.exists():
            raise ValueError(f"退避先が既に存在します（上書きしません）: {backup}")
        if dest.exists() and not dest.is_file():
            raise ValueError(f"コピー先がファイルではありません: {dest}")
        for target, base in [(dest, root), (backup, root)]:
            if not target.resolve().is_relative_to(base.resolve()):
                raise ValueError(f"画像フォルダ外のパスです: {target}")
        if drive_dir:
            target = drive_dir / relative
            if (target.is_symlink() or not target.resolve().is_relative_to(drive_dir.resolve())
                    or (target.exists() and not target.is_file())):
                raise ValueError(f"同期先が不正です: {target}")
            if drive_dir.resolve() == root.resolve() or drive_dir.resolve().is_relative_to(root.resolve()):
                raise ValueError("--drive-dir はローカルの画像フォルダと別にしてください")
        plans.append((work / "images" / (item["id"] + ".png"), dest, backup, relative))
    for source, dest, backup, relative in plans:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(dest), str(backup))
        shutil.copy2(source, dest)
        if drive_dir:
            target = drive_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return len(plans)


@contextmanager
def idle_work(work):
    """run.py と同じロックを検査し、稼働中のキュー/画像には書き込まない。"""
    import fcntl
    with (work / ".imagegen.lock").open("a+") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError("この作業フォルダは生成中です。終了後に実行してください") from exc
        yield


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--since")
    parser.add_argument("--assets")
    parser.add_argument("--work-name", help="作業フォルダ名（既定: regen_<YYYYMMDD>）")
    parser.add_argument("--parallel", type=int, help="run.py に渡す並列数")
    parser.add_argument("--min-interval", type=float, help="run.py に渡す全ウィンドウ共通の最小送信間隔（秒）")
    parser.add_argument("--exclude", help="run.py に渡す除外ID（カンマ区切り）")
    parser.add_argument("--exclude-slots", help="run.py に渡す除外slot（例: bg,still）")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--run", action="store_true")
    modes.add_argument("--verify", action="store_true")
    modes.add_argument("--apply", action="store_true")
    modes.add_argument("--export", action="store_true")
    parser.add_argument("--drive-dir", type=Path)
    args = parser.parse_args(argv)
    if args.drive_dir and not args.apply:
        parser.error("--drive-dir は --apply と併用してください")
    if args.work_name is not None and (not args.work_name or args.work_name in (".", "..")
                                      or Path(args.work_name).name != args.work_name):
        parser.error("--work-name は単一のフォルダ名を指定してください")
    if args.parallel is not None and args.parallel < 1:
        parser.error("--parallel は1以上を指定してください")
    if args.min_interval is not None and (not math.isfinite(args.min_interval) or args.min_interval < 0):
        parser.error("--min-interval は0以上の有限の秒数を指定してください")
    project = args.project.resolve()
    work = project / ".imagegen" / (args.work_name or "regen_" + datetime.now().strftime("%Y%m%d"))
    try:
        current = extract_prompts.parse(project / "Asset_Prompts_Full.md")
        indexed(current)
        if not args.since and not args.assets and (args.verify or args.apply or args.export):
            candidates = sorted(path.parent for path in (project / ".imagegen").glob(
                "regen_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/image_queue.json"))
            if candidates and args.work_name is None:
                work = candidates[-1]
            queue = json.loads((work / "image_queue.json").read_text(encoding="utf-8"))
        else:
            queue = detect_targets(project, args.since, args.assets)
        indexed(queue)
        if not queue:
            print("変更対象は0枚です")
            return 0
        current_by_id = indexed(current)
        for item in queue:
            standard_name(item)
            if (item["id"] not in current_by_id
                    or item["prompt"] != current_by_id[item["id"]]["prompt"]
                    or item["slot"] != current_by_id[item["id"]]["slot"]):
                raise ValueError(f'キュー作成後にプロンプトが変わっています: {item["id"]}')
        work.mkdir(parents=True, exist_ok=True)
        with idle_work(work):
            queue_path = work / "image_queue.json"
            if queue_path.exists():
                old = json.loads(queue_path.read_text(encoding="utf-8"))
                if old != queue:
                    raise ValueError("同日の作業キューが異なります。既存の生成物は上書きしません")
            else:
                write_json(queue_path, queue)
            write_json(work / "mapping_notes.json", mapping_notes(project, current))
            (work / ".imagegen").mkdir(exist_ok=True)
            (work / "images").mkdir(exist_ok=True)
            # 既存の回収処理が要求文と画像ハッシュを照合する仕組みを使用。
            (work / ".imagegen" / "require_receipts").touch()
            if args.verify:
                fixed = auto_fix_transparency(work, queue)
                report = verify(work, queue, fixed)
                print(f'検査 {report["passed"]}/{report["total"]} PASS: {work / "verify.json"}')
                return 0 if report["all_pass"] else 1
            if args.apply:
                print(f"適用 {apply(project, work, queue, args.drive_dir)}枚")
                return 0
            if args.export:
                print(export(project, work, queue))
                return 0
        print(f"対象 {len(queue)}枚: {queue_path}")
        if args.run:
            with (work / "run.log").open("a", encoding="utf-8") as log:
                proc = subprocess.Popen(
                    ["nohup", sys.executable, "-B", "-u", str(HERE / "run.py"), str(work)]
                    + (["--parallel", str(args.parallel)] if args.parallel is not None else [])
                    + (["--min-interval", str(args.min_interval)] if args.min_interval is not None else [])
                    + (["--exclude", args.exclude] if args.exclude is not None else [])
                    + (["--exclude-slots", args.exclude_slots] if args.exclude_slots is not None else []),
                    stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                    start_new_session=True,
                )
            (work / "run.pid").write_text(str(proc.pid) + "\n")
            print(f"PID={proc.pid} log={work / 'run.log'}")
        return 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"停止: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
