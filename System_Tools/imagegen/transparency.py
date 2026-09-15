#!/usr/bin/env python3
"""画像の外周につながった単色背景を安全に透過する共通処理。"""

from __future__ import annotations

from collections import deque
from pathlib import Path
import shutil
import statistics

from PIL import Image, ImageFilter


TOLERANCE = 25


def _transparent_ratio(image: Image.Image) -> float:
    if image.mode != "RGBA":
        return 0.0
    histogram = image.getchannel("A").histogram()
    return sum(histogram[:10]) / (image.width * image.height)


def _is_transparent_image(image: Image.Image) -> bool:
    if image.mode != "RGBA" or not image.width or not image.height:
        return False
    alpha = image.getchannel("A")
    corners = (
        alpha.getpixel((0, 0)),
        alpha.getpixel((image.width - 1, 0)),
        alpha.getpixel((0, image.height - 1)),
        alpha.getpixel((image.width - 1, image.height - 1)),
    )
    return all(value < 10 for value in corners) and _transparent_ratio(image) >= 0.10


def is_transparent(path: str | Path) -> bool:
    """RGBA・四隅α<10・透明画素10%以上なら透過済みと判定する。"""
    try:
        with Image.open(path) as image:
            image.load()
            return _is_transparent_image(image)
    except (OSError, ValueError):
        return False


def _backup_path(path: Path, backup_dir: Path) -> Path:
    candidate = backup_dir / path.name
    counter = 1
    while candidate.exists():
        candidate = backup_dir / f"{path.stem}_{counter}{path.suffix}"
        counter += 1
    return candidate


def _connected_background(image: Image.Image) -> Image.Image:
    """四隅の中央値に近く、外周から4近傍でつながる画素のマスクを返す。"""
    rgb = image.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    corner_colors = (
        pixels[0, 0], pixels[width - 1, 0],
        pixels[0, height - 1], pixels[width - 1, height - 1],
    )
    background = tuple(int(statistics.median(channel)) for channel in zip(*corner_colors))
    seen = bytearray(width * height)
    mask_data = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def add(x: int, y: int) -> None:
        index = y * width + x
        if seen[index]:
            return
        seen[index] = 1
        color = pixels[x, y]
        if all(abs(color[channel] - background[channel]) <= TOLERANCE for channel in range(3)):
            mask_data[index] = 255
            queue.append((x, y))

    for x in range(width):
        add(x, 0)
        if height > 1:
            add(x, height - 1)
    for y in range(1, height - 1):
        add(0, y)
        if width > 1:
            add(width - 1, y)

    while queue:
        x, y = queue.popleft()
        if x:
            add(x - 1, y)
        if x + 1 < width:
            add(x + 1, y)
        if y:
            add(x, y - 1)
        if y + 1 < height:
            add(x, y + 1)

    return Image.frombytes("L", (width, height), bytes(mask_data))


def make_transparent(path: str | Path, backup_dir: str | Path) -> dict:
    """外周連結背景を透過し、変更前の画像を重複しない名前で控える。"""
    path = Path(path)
    backup_dir = Path(backup_dir)
    with Image.open(path) as source:
        source.load()
        before = _transparent_ratio(source)
        if _is_transparent_image(source):
            return {
                "processed": False,
                "before_transparent_ratio": before,
                "after_transparent_ratio": before,
                "backup": None,
            }
        rgba = source.convert("RGBA")

    background = _connected_background(rgba)
    # 背景マスクを1pxだけ内側へ広げてから軽くぼかし、白い縁を残さない。
    softened = background.filter(ImageFilter.MaxFilter(3)).filter(
        ImageFilter.GaussianBlur(radius=0.7)
    )
    old_alpha = rgba.getchannel("A")
    new_alpha = Image.eval(softened, lambda value: 255 - value)
    new_alpha = Image.frombytes(
        "L", rgba.size,
        bytes(min(old, new) for old, new in zip(old_alpha.tobytes(), new_alpha.tobytes())),
    )
    rgba.putalpha(new_alpha)

    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = _backup_path(path, backup_dir)
    shutil.copy2(path, backup)
    rgba.save(path, "PNG")
    return {
        "processed": True,
        "before_transparent_ratio": before,
        "after_transparent_ratio": _transparent_ratio(rgba),
        "backup": str(backup),
    }
