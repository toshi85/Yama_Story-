from __future__ import annotations

import subprocess
import sys
import unicodedata
from pathlib import Path
import importlib.util

from PIL import Image


SCRIPT = Path(__file__).with_name("check_handoff_folder.py")


def make_rgba(path: Path) -> None:
    image = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    for x in range(10, 30):
        for y in range(10, 30):
            image.putpixel((x, y), (200, 30, 30, 255))
    image.save(path)


def make_white(path: Path) -> None:
    Image.new("RGB", (40, 40), "white").save(path)


def checklist(folder: Path, *names: str) -> None:
    rows = ["| 素材 | 見てほしい所 |", "|:--|:--|"]
    rows.extend(f"| {name} | 確認 |" for name in names)
    (folder / "チェックリスト.md").write_text("\n".join(rows), encoding="utf-8")


def run(folder: Path, *args: str, owner: bool = False) -> subprocess.CompletedProcess[str]:
    """T1〜T3 の検査はAI検品の関所（T4）と切り離して見る。owner=True で本人のPCとして T4 も走らせる。"""
    shim = (
        "import runpy, sys; sys.path.insert(0, sys.argv[1]); import generation_gate as g; "
        + ("" if owner else "g.owner_machine = lambda: False; ")
        + "script = sys.argv[2]; sys.argv = [script] + sys.argv[3:]; runpy.run_path(script, run_name='__main__')"
    )
    return subprocess.run(
        [sys.executable, "-X", "utf8", "-c", shim, str(SCRIPT.parents[1]), str(SCRIPT), str(folder), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",   # Windows でも日本語の出力を読めるように
        check=False,
    )


def test_unreviewed_image_is_t4_on_owner_machine(tmp_path: Path) -> None:
    # 2026-09-25: AI検品（ai_image_review.py）を飛ばしても本人に渡せた
    sys.path.insert(0, str(SCRIPT.parents[1]))
    import generation_gate
    if not generation_gate.owner_machine():
        return
    folder = tmp_path / "handoff"
    folder.mkdir()
    make_rgba(folder / "ASSET-001_char_t4probe.png")
    checklist(folder, "ASSET-001_char_t4probe.png")
    result = run(folder, owner=True)
    assert result.returncode == 1
    assert "ERROR T4 ASSET-001_char_t4probe.png" in result.stdout


def test_transparent_character_is_ok(tmp_path: Path) -> None:
    name = "ASSET-001_キャラ.png"
    make_rgba(tmp_path / name)
    checklist(tmp_path, name)
    result = run(tmp_path)
    assert result.returncode == 0
    assert "T1 ERROR 0件 / T2 ERROR 0件" in result.stdout


def test_white_character_and_diagram_are_t1_but_photo_is_not(tmp_path: Path) -> None:
    names = ["ASSET-001_キャラ.png", "ASSET-002_図解.png", "ASSET-003_写真.png"]
    for name in names:
        make_white(tmp_path / name)
    checklist(tmp_path, *names)
    result = run(tmp_path)
    assert result.returncode == 1
    assert "ERROR T1 ASSET-001_キャラ.png" in result.stdout
    assert "ERROR T1 ASSET-002_図解.png" in result.stdout
    assert "ERROR T1 ASSET-003_写真.png" not in result.stdout
    assert "T1 ERROR 2件 / T2 ERROR 0件" in result.stdout


def test_unlisted_and_missing_are_t2(tmp_path: Path) -> None:
    make_white(tmp_path / "ASSET-001_写真.png")
    checklist(tmp_path, "ASSET-002.mp4")
    result = run(tmp_path)
    assert result.returncode == 1
    assert "ERROR T2 未掲載 ASSET-001_写真.png" in result.stdout
    assert "ERROR T2 ファイルなし ASSET-002.mp4" in result.stdout


def test_fullwidth_slash_and_parentheses_are_parsed(tmp_path: Path) -> None:
    names = ["ASSET-099_背景.png", "ASSET-232_背景（099と同じ）.png"]
    for name in names:
        make_white(tmp_path / name)
    checklist(tmp_path, "ASSET-099_背景.png／ASSET-232_背景（099と同じ）.png")
    result = run(tmp_path)
    assert result.returncode == 0
    assert "T2 ERROR 0件" in result.stdout


def test_all_checklists_are_combined(tmp_path: Path) -> None:
    names = ["ASSET-001_写真.png", "ASSET-002.mp4"]
    make_white(tmp_path / names[0])
    (tmp_path / names[1]).write_bytes(b"video")
    checklist(tmp_path, names[0])
    (tmp_path / "チェックリスト_動画.md").write_text(
        f"| 素材 |\n|:--|\n| {names[1]} |", encoding="utf-8"
    )
    result = run(tmp_path)
    assert result.returncode == 0
    assert "T2 ERROR 0件" in result.stdout


def test_nfd_filename_matches_nfc_checklist(tmp_path: Path) -> None:
    nfc_name = "ASSET-010_キャラガ.png"
    nfd_name = unicodedata.normalize("NFD", nfc_name)
    make_rgba(tmp_path / nfd_name)
    checklist(tmp_path, nfc_name)
    result = run(tmp_path)
    assert result.returncode == 0


def test_missing_checklist(tmp_path: Path) -> None:
    result = run(tmp_path)
    assert result.returncode == 1
    assert "ERROR T2 チェックリストがない" in result.stdout


def test_underscore_media_is_ignored(tmp_path: Path) -> None:
    make_white(tmp_path / "_確認用_一覧.png")
    checklist(tmp_path)
    result = run(tmp_path)
    assert result.returncode == 0


def test_sheet_is_created_outside_folder(tmp_path: Path) -> None:
    folder = tmp_path / "handoff"
    folder.mkdir()
    name = "ASSET-001_キャラ.png"
    make_rgba(folder / name)
    checklist(folder, name)
    sheet = tmp_path / "check" / "sheet.jpg"
    result = run(folder, "--sheet", str(sheet))
    assert result.returncode == 0
    assert sheet.is_file()
    with Image.open(sheet) as image:
        assert image.format == "JPEG"


def test_sheet_inside_folder_is_error_and_not_written(tmp_path: Path) -> None:
    checklist(tmp_path)
    sheet = tmp_path / "sheet.jpg"
    result = run(tmp_path, "--sheet", str(sheet))
    assert result.returncode == 1
    assert "ERROR T3 出力先が検査フォルダ内" in result.stdout
    assert not sheet.exists()


def test_fix_transparency_changes_t1_result_and_creates_external_backup(
    tmp_path: Path, capsys
) -> None:
    folder = tmp_path / "handoff"
    folder.mkdir()
    name = "ASSET-001_キャラ.png"
    make_white(folder / name)
    checklist(folder, name)
    spec = importlib.util.spec_from_file_location("handoff_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    module.REPO = tmp_path
    sys.path.insert(0, str(SCRIPT.parents[1]))
    import generation_gate
    real_owner = generation_gate.owner_machine
    generation_gate.owner_machine = lambda: False   # T1 の検査だけを見る（T4 は別テスト）
    try:
        _check_fix_transparency(module, folder, name, tmp_path, capsys)
    finally:
        generation_gate.owner_machine = real_owner


def _check_fix_transparency(module, folder, name, tmp_path, capsys) -> None:
    assert module.inspect(folder, None) == 1
    assert "T1 ERROR 1件 / T2 ERROR 0件" in capsys.readouterr().out
    assert module.inspect(folder, None, True) == 0
    output = capsys.readouterr().out
    assert "透過修正 1枚" in output
    assert "T1 ERROR 0件 / T2 ERROR 0件" in output
    backups = list((tmp_path / "check/transparency_backup").iterdir())
    assert len(backups) == 1
    backup_dir = backups[0]
    assert str(backup_dir) in output
    assert (backup_dir / name).is_file()
