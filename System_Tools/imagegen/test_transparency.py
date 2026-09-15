from pathlib import Path

from PIL import Image, ImageDraw

from transparency import is_transparent, make_transparent


def character_on_background(path: Path, background=(255, 255, 255)) -> None:
    image = Image.new("RGB", (100, 100), background)
    draw = ImageDraw.Draw(image)
    draw.ellipse((20, 10, 80, 90), fill=(30, 80, 160))
    draw.ellipse((35, 30, 45, 40), fill="white")  # 外周と非連結の目の白
    draw.rectangle((35, 55, 65, 80), fill="white")  # 外周と非連結の白い服
    image.save(path)


def test_white_background_is_removed_but_internal_white_remains(tmp_path: Path) -> None:
    path = tmp_path / "character.png"
    character_on_background(path)
    result = make_transparent(path, tmp_path / "backup")
    assert result["processed"]
    assert result["before_transparent_ratio"] == 0
    assert result["after_transparent_ratio"] > 0.5
    with Image.open(path) as image:
        assert image.mode == "RGBA"
        assert image.getpixel((0, 0))[3] < 10
        assert image.getpixel((40, 35)) == (255, 255, 255, 255)
        assert image.getpixel((50, 65)) == (255, 255, 255, 255)


def test_uniform_gray_background_is_removed(tmp_path: Path) -> None:
    path = tmp_path / "gray.png"
    character_on_background(path, (190, 190, 190))
    make_transparent(path, tmp_path / "backup")
    assert is_transparent(path)


def test_already_transparent_is_unchanged_and_has_no_backup(tmp_path: Path) -> None:
    path = tmp_path / "done.png"
    image = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    ImageDraw.Draw(image).rectangle((12, 12, 27, 27), fill=(255, 255, 255, 255))
    image.save(path)
    before = path.read_bytes()
    result = make_transparent(path, tmp_path / "backup")
    assert not result["processed"]
    assert path.read_bytes() == before
    assert not (tmp_path / "backup").exists()


def test_backup_names_do_not_overwrite(tmp_path: Path) -> None:
    path = tmp_path / "character.png"
    backup = tmp_path / "backup"
    character_on_background(path)
    first = make_transparent(path, backup)
    character_on_background(path)
    second = make_transparent(path, backup)
    assert Path(first["backup"]).name == "character.png"
    assert Path(second["backup"]).name == "character_1.png"
    assert len(list(backup.iterdir())) == 2
