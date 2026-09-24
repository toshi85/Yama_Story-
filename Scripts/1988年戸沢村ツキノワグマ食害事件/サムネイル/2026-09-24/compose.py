from pathlib import Path
from urllib.request import urlretrieve
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
SOURCES = {
    "A_表情": HERE / "背景_A_表情.png",
    "B_日常": HERE / "背景_B_日常.png",
    "C_背後": HERE / "背景_C_背後.png",
}
FONT_TOP = "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"
FONT_BOTTOM = HERE / ".font_cache" / "SourceHanSansJP-Heavy.otf"
FONT_BOTTOM_URL = (
    "https://raw.githubusercontent.com/adobe-fonts/source-han-sans/"
    "release/SubsetOTF/JP/SourceHanSansJP-Heavy.otf"
)
TOP = "クルミを拾いに…"
BOTTOM = "200m先で発見"

if not FONT_BOTTOM.exists():
    FONT_BOTTOM.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(FONT_BOTTOM_URL, FONT_BOTTOM)


def fit_font(draw, text, path, size, max_width, index=0):
    while size > 30:
        font = ImageFont.truetype(path, size, index=index)
        if draw.textbbox((0, 0), text, font=font, stroke_width=7)[2] <= max_width:
            return font
        size -= 1
    raise RuntimeError(f"text does not fit: {text}")


for name, source in SOURCES.items():
    image = Image.open(source).convert("RGB")
    w, h = image.size
    target_ratio = 1280 / 720
    current_ratio = w / h
    if current_ratio > target_ratio:
        crop_w = round(h * target_ratio)
        image = image.crop(((w - crop_w) // 2, 0, (w + crop_w) // 2, h))
    else:
        crop_h = round(w / target_ratio)
        image = image.crop((0, (h - crop_h) // 2, w, (h + crop_h) // 2))
    image = image.resize((1280, 720), Image.Resampling.LANCZOS)

    # Keep a readable area for the two text lines without changing the scene.
    shade = Image.new("RGBA", image.size, (0, 0, 0, 0))
    pixels = shade.load()
    for y in range(720):
        for x in range(1280):
            left = max(0, 1 - x / 900)
            lower = max(0, (y - 415) / 305)
            alpha = int(62 * left + 40 * lower * left)
            pixels[x, y] = (0, 0, 0, min(alpha, 100))
    image = Image.alpha_composite(image.convert("RGBA"), shade)
    draw = ImageDraw.Draw(image)

    top_font = fit_font(draw, TOP, FONT_TOP, 82, 815, index=1)
    bottom_font = fit_font(draw, BOTTOM, FONT_BOTTOM, 122, 825)
    draw.text((52, 56), TOP, font=top_font, fill=(255, 255, 255),
              stroke_width=4, stroke_fill=(5, 5, 5))
    draw.text((48, 555), BOTTOM, font=bottom_font, fill=(236, 30, 32),
              stroke_width=7, stroke_fill=(5, 5, 5))
    output = HERE / f"サムネ_{name}.png"
    image.convert("RGB").save(output, "PNG", optimize=True)
    print(output)
