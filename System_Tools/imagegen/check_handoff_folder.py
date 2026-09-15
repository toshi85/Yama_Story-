#!/usr/bin/env python3
"""デスクトップへ渡す山岳素材フォルダを機械検査する。"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ASSET_RE = re.compile(r"ASSET-[^|／`\n]*?\.(?:png|mp4)", re.IGNORECASE)
MEDIA_SUFFIXES = {".png", ".mp4"}


def normalized(name: str) -> str:
    return unicodedata.normalize("NFC", name)


def direct_files(folder: Path) -> list[Path]:
    return sorted(
        (path for path in folder.iterdir() if path.is_file()),
        key=lambda path: normalized(path.name),
    )


def t1_targets(files: list[Path]) -> list[Path]:
    return [
        path
        for path in files
        if path.suffix.lower() == ".png"
        and ("キャラ" in normalized(path.name) or "図解" in normalized(path.name))
    ]


def transparency_result(path: Path) -> tuple[bool, str, list[int] | None, float]:
    try:
        with Image.open(path) as image:
            mode = image.mode
            if "A" in image.getbands():
                alpha = image.getchannel("A")
                width, height = image.size
                corners = [
                    alpha.getpixel((0, 0)),
                    alpha.getpixel((width - 1, 0)),
                    alpha.getpixel((0, height - 1)),
                    alpha.getpixel((width - 1, height - 1)),
                ]
                histogram = alpha.histogram()
                transparent_pixels = sum(histogram[:10])
                transparent_percent = transparent_pixels * 100.0 / (width * height)
            else:
                corners = None
                transparent_percent = 0.0
    except (OSError, ValueError) as error:
        return False, f"読込不可({error})", None, 0.0

    valid = (
        mode == "RGBA"
        and corners is not None
        and all(value < 10 for value in corners)
        and transparent_percent >= 10.0
    )
    return valid, mode, corners, transparent_percent


def checklist_assets(checklists: list[Path]) -> dict[str, str]:
    assets: dict[str, str] = {}
    for checklist in checklists:
        text = checklist.read_text(encoding="utf-8")
        for line in text.splitlines():
            if not line.lstrip().startswith("|"):
                continue
            for match in ASSET_RE.finditer(line):
                name = match.group(0).strip().strip("*_ ")
                assets.setdefault(normalized(name), name)
    return assets


def find_font(size: int) -> ImageFont.ImageFont:
    candidates = (
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def checkerboard(size: tuple[int, int], square: int = 20) -> Image.Image:
    board = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(board)
    for y in range(0, size[1], square):
        for x in range(0, size[0], square):
            if (x // square + y // square) % 2 == 0:
                draw.rectangle((x, y, x + square - 1, y + square - 1), fill="#b8b8b8")
    return board


def write_sheet(targets: list[Path], output: Path) -> None:
    thumb_box = (300, 300)
    label_height = 56
    margin = 20
    columns = min(4, max(1, len(targets)))
    rows = max(1, (len(targets) + columns - 1) // columns)
    cell_width = thumb_box[0] + margin * 2
    cell_height = thumb_box[1] + label_height + margin * 2
    sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    font = find_font(16)

    for index, path in enumerate(targets):
        column = index % columns
        row = index // columns
        origin_x = column * cell_width + margin
        origin_y = row * cell_height + margin
        board = checkerboard(thumb_box)
        with Image.open(path) as source:
            image = source.convert("RGBA")
            image.thumbnail(thumb_box, Image.Resampling.LANCZOS)
            paste_x = (thumb_box[0] - image.width) // 2
            paste_y = (thumb_box[1] - image.height) // 2
            board.paste(image, (paste_x, paste_y), image)
        sheet.paste(board, (origin_x, origin_y))
        draw.text(
            (origin_x, origin_y + thumb_box[1] + 8),
            path.name,
            fill="black",
            font=font,
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, "JPEG", quality=90)


def is_within(path: Path, folder: Path) -> bool:
    try:
        path.resolve().relative_to(folder.resolve())
        return True
    except ValueError:
        return False


def inspect(folder: Path, sheet: Path | None) -> int:
    if not folder.is_dir():
        print(f"ERROR 検査フォルダがない: {folder}")
        print("T1 ERROR 0件 / T2 ERROR 0件")
        return 1

    files = direct_files(folder)
    targets = t1_targets(files)
    t1_errors: list[str] = []
    for path in targets:
        valid, mode, corners, transparent_percent = transparency_result(path)
        if not valid:
            corner_text = "なし" if corners is None else str(corners)
            t1_errors.append(
                f"ERROR T1 {path.name}: 背景が透過されていない"
                f"（mode={mode}, 四隅α={corner_text}, 透明={transparent_percent:.1f}%）"
            )

    checklists = [
        path
        for path in files
        if normalized(path.name).startswith("チェックリスト") and path.suffix.lower() == ".md"
    ]
    t2_errors: list[str] = []
    if not checklists:
        t2_errors.append("ERROR T2 チェックリストがない")
    else:
        listed = checklist_assets(checklists)
        present = {
            normalized(path.name): path.name
            for path in files
            if path.suffix.lower() in MEDIA_SUFFIXES and not path.name.startswith("_")
        }
        for key in sorted(present.keys() - listed.keys()):
            t2_errors.append(f"ERROR T2 未掲載 {present[key]}")
        for key in sorted(listed.keys() - present.keys()):
            t2_errors.append(f"ERROR T2 ファイルなし {listed[key]}")

    sheet_error = False
    if sheet is not None:
        if is_within(sheet, folder):
            print(f"ERROR T3 出力先が検査フォルダ内: {sheet}")
            sheet_error = True
        else:
            write_sheet(targets, sheet)

    for message in t1_errors + t2_errors:
        print(message)
    print(f"T1 ERROR {len(t1_errors)}件 / T2 ERROR {len(t2_errors)}件")
    return 1 if t1_errors or t2_errors or sheet_error else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--sheet", type=Path)
    args = parser.parse_args()
    return inspect(args.folder, args.sheet)


if __name__ == "__main__":
    sys.exit(main())
