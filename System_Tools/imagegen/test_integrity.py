import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import collect
from integrity import verified_ids
from integrity import image_valid
from recover import normalize


class IntegrityTest(unittest.TestCase):
    def test_character_requires_valid_png_aspect_and_alpha(self):
        from PIL import Image
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / 'image.png'
            def check():
                stat = path.stat()
                return image_valid(str(path), stat.st_size, stat.st_mtime_ns, '1:1', 'char')
            Image.new('RGB', (64, 64), 'white').save(path)
            self.assertFalse(check())
            Image.new('RGBA', (64, 64), (0, 0, 0, 0)).save(path)
            self.assertFalse(check())
            im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
            im.putpixel((32, 32), (255, 0, 0, 255))
            im.save(path)
            self.assertTrue(check())
            Image.new('RGBA', (128, 64), (0, 0, 0, 0)).save(path)
            self.assertFalse(check())
            path.write_bytes(b'broken png')
            self.assertFalse(check())

    def test_filename_alone_does_not_prove_completion(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'images').mkdir()
            (root / '.imagegen').mkdir()
            (root / '.imagegen' / 'require_receipts').touch()
            (root / 'images' / 'ASSET-001.png').write_bytes(b'wrong previous image')
            queue = [{'id': 'ASSET-001', 'prompt': 'new scene'}]
            self.assertEqual(verified_ids(root, queue), set())

    def test_changed_image_or_prompt_invalidates_receipt(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'images').mkdir()
            receipts = root / '.imagegen' / 'receipts'
            receipts.mkdir(parents=True)
            (root / '.imagegen' / 'require_receipts').touch()
            image = root / 'images' / 'ASSET-001.png'
            image.write_bytes(b'new image')
            receipt = {'id': 'ASSET-001', 'sha256': hashlib.sha256(image.read_bytes()).hexdigest(), 'prompt_sha256': hashlib.sha256(b'new scene').hexdigest()}
            (receipts / 'ASSET-001.json').write_text(json.dumps(receipt))
            self.assertEqual(verified_ids(root, [{'id': 'ASSET-001', 'prompt': 'new scene'}]), {'ASSET-001'})
            self.assertEqual(verified_ids(root, [{'id': 'ASSET-001', 'prompt': 'other scene'}]), set())
            image.write_bytes(b'previous stale image')
            self.assertEqual(verified_ids(root, [{'id': 'ASSET-001', 'prompt': 'new scene'}]), set())

    def test_stale_download_cannot_overwrite_recovered_image(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / 'work'
            (root / 'images').mkdir(parents=True)
            (root / '.imagegen').mkdir()
            (root / '.imagegen' / 'require_receipts').touch()
            (root / 'image_queue.json').write_text(json.dumps([{'id': 'ASSET-001', 'prompt': 'scene'}]))
            (root / 'images' / 'ASSET-001.png').write_bytes(b'recovered')
            downloads = Path(tmp) / 'downloads'
            downloads.mkdir()
            (downloads / 'ASSET-001.png').write_bytes(b'stale')
            previous = collect.DOWNLOADS
            try:
                collect.DOWNLOADS = downloads
                self.assertEqual(collect.collect(root), 0)
                self.assertEqual((root / 'images' / 'ASSET-001.png').read_bytes(), b'recovered')
            finally:
                collect.DOWNLOADS = previous

    def test_ui_expand_label_is_not_part_of_request(self):
        self.assertEqual(normalize('Generate a bear.\n表示を増やす'), 'Generate a bear.')
        self.assertNotEqual(normalize('Generate a bear.'), normalize('Generate a house.'))


if __name__ == '__main__':
    unittest.main()
