import unittest

from validate_phase2_assets import prompt_lint


def segment(no, nar='説明です。', asset_type='キャラアニメーション', body='', note=''):
    return (
        f'ナレーター: {nar}\n'
        f'【制作メモ】ASSET-{no:03d} [{asset_type}]\n'
        f'{body}\n{note}\n\n'
    )


def warnings_for(text, prefix):
    errors, warns, info = [], [], []
    prompt_lint(text, errors, warns, info)
    return [warning for warning in warns if warning.startswith(prefix)]


def errors_for(text, prefix):
    errors, warns, info = [], [], []
    prompt_lint(text, errors, warns, info)
    return [error for error in errors if error.startswith(prefix)]


class Phase2LintCalibrationTest(unittest.TestCase):
    person_prompt = '''キャラプロンプト（1:1）:
```
Cute cartoon character design. A Japanese man standing. Full body. White background.
```'''
    object_prompt = '''キャラプロンプト（1:1）:
```
Cute cartoon character design. A paper tag and a clock. White background.
```'''

    def test_lint40_dialect_still_warns(self):
        text = segment(1, body=self.person_prompt, note='→男性セリフ「行くべ」')
        warns = warnings_for(text, 'セリフに方言語尾')
        self.assertEqual(1, len(warns))
        self.assertIn('ASSET-001', warns[0])

    def test_lint41_requires_dialogue_for_every_character_prompt(self):
        notes = [
            '→セリフ「行こう」',
            '→ セリフ：行こう',
            '→左の男性セリフ「行こう」',
            '→心の声の吹き出しで「行こう」',
            '→ 編集者指示: 心の声：行こう',
            '→ギザギザの吹き出しを出し「行こう」と入れる',
        ]
        text = ''.join(segment(i + 1, body=self.person_prompt, note=note)
                       for i, note in enumerate(notes))
        text += segment(7, body=self.person_prompt)
        text += segment(8, asset_type='Lovart動画', body=self.object_prompt)
        text += segment(9, body='', note='→素材の再利用。')
        errors = errors_for(text, 'キャラプロンプトがあるのにセリフ行なし')
        self.assertEqual(1, len(errors))
        self.assertIn('2件: ASSET-007, ASSET-008', errors[0])
        self.assertNotIn('ASSET-009', errors[0])

    def test_lint42_counts_display_units_and_ignores_other_quotes(self):
        text = segment(
            1,
            asset_type='Lovart動画',
            note=('→ 編集者指示: 「2023年・秋田大学病院・20人の記録」の資料を使い、'
                  '「傷の重さ → 運ぶ順番」を2段テロップで表示。'))
        text += segment(
            2,
            asset_type='Lovart動画',
            note='→ 編集者指示: テロップに「これは十四字を明確に超える長い表示文です」を使う。')
        warns = warnings_for(text, '編集者指示の14字超テロップ')
        self.assertEqual(1, len(warns))
        self.assertIn('ASSET-002', warns[0])
        self.assertNotIn('ASSET-001', warns[0])

    def test_lint43_requires_adjacent_narration_rows(self):
        text = segment(1, nar='前半ですが、', asset_type='Lovart動画')
        text += 'ナレーター: 制作メモのない中間行です。\n\n'
        text += segment(3, nar='後半です。', asset_type='Lovart動画')
        text += segment(4, nar='隣接する前半で、', asset_type='Lovart動画')
        text += segment(5, nar='隣接する後半です。', asset_type='Lovart動画')
        warns = warnings_for(text, '読点で分割された連続ナレーション')
        self.assertEqual(1, len(warns))
        self.assertIn('1件: ASSET-004→ASSET-005', warns[0])
        self.assertNotIn('ASSET-001→ASSET-003', warns[0])

    def test_lint44_only_warns_for_blanket_suppression(self):
        text = segment(
            1,
            asset_type='Lovart動画',
            note='→ 編集者指示: 「数百キロ」のテロップは出さない。別の要点は表示する。')
        text += segment(
            2,
            asset_type='Lovart動画',
            note='→ 編集者指示: 音だけにする。テロップは一切出さない。')
        warns = warnings_for(text, 'テロップ抑制指示')
        self.assertEqual(1, len(warns))
        self.assertIn('1件: ASSET-002', warns[0])
        self.assertNotIn('ASSET-001', warns[0])


if __name__ == '__main__':
    unittest.main()
