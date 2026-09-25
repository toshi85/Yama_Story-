import unittest

from validate_phase2_assets import prompt_lint


def segment(no, nar='説明です。', asset_type='キャラアニメーション', body='', note='', scene=''):
    return (
        f'ナレーター: {nar}\n'
        f'【制作メモ】ASSET-{no:03d} [{asset_type}]\n'
        f'{f"シーン: {scene}\\n" if scene else ""}'
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

    def test_lint45_warns_when_singular_narration_draws_multiple_bears(self):
        body = '''キャラプロンプト（1:1）:\n```\nTwo bears side by side. White background.\n```'''
        text = segment(45, nar='そのクマは、撃たれた個体よりも大きかった。', body=body)
        warns = warnings_for(text, 'ナレーションは単数なのに複数を描かせている')
        self.assertEqual(1, len(warns))
        self.assertIn('ASSET-045', warns[0])

    def test_lint45_accepts_plural_narration_and_multiple_bears(self):
        body = '''キャラプロンプト（1:1）:\n```\nA mother bear and two cubs. White background.\n```'''
        text = segment(45, nar='親子のクマが歩いていた。', body=body)
        self.assertEqual([], warnings_for(text, 'ナレーションは単数なのに複数を描かせている'))

    def test_lint45_accepts_singular_prompt(self):
        self.assertEqual([], warnings_for(
            segment(45, nar='男性が立っていた。', body=self.person_prompt),
            'ナレーションは単数なのに複数を描かせている'))

    def test_lint45_ignores_plural_word_inside_single_reused_character_description(self):
        body = '''キャラプロンプト（1:1）:\n```\n(CHAR-01 再利用) CHAR-01 raises both arms. White background.\n```'''
        text = segment(45, nar='男性が驚いた。', body=body)
        self.assertEqual([], warnings_for(
            text, 'ナレーションは単数なのに複数を描かせている'))

    def test_lint46_warns_when_scene_direction_is_missing_from_prompts(self):
        text = segment(46, asset_type='静止画', scene='男性が山の方へ向く', body='''静止画プロンプト（16:9）:\n```\nA Japanese man on a mountain trail.\n```''')
        self.assertEqual(1, len(warnings_for(text, '向きの指定なし')))

    def test_lint46_accepts_direction_in_any_prompt(self):
        text = segment(46, asset_type='静止画', scene='男性が山の方へ向く', body='''静止画プロンプト（16:9）:\n```\nA Japanese man facing to the right.\n```''')
        self.assertEqual([], warnings_for(text, '向きの指定なし'))

    def test_lint47_warns_when_environment_prompt_has_no_time(self):
        text = segment(47, nar='深夜に小屋を出た。', asset_type='静止画', body='''背景プロンプト（16:9）:\n```\nA remote mountain hut under a dark sky.\n```''')
        self.assertEqual(1, len(warnings_for(text, '時間帯の指定なし')))

    def test_lint47_ignores_character_only_cut(self):
        text = segment(47, nar='深夜に立ち尽くした。', body=self.person_prompt)
        self.assertEqual([], warnings_for(text, '時間帯の指定なし'))

    def test_lint48_warns_for_historical_scene_without_period(self):
        body = '''静止画プロンプト（16:9）:\n```\nA Japanese man beside a telephone in an office.\n```'''
        text = '# 1988年の事件\n' + segment(48, asset_type='静止画', body=body)
        self.assertEqual(1, len(warnings_for(text, '時代の指定なし')))

    def test_lint48_accepts_explicit_historical_period(self):
        body = '''静止画プロンプト（16:9）:\n```\nLate 1980s Japan, a Japanese man beside a telephone in a Showa-era office.\n```'''
        text = '# 1988年の事件\n' + segment(48, asset_type='静止画', body=body)
        self.assertEqual([], warnings_for(text, '時代の指定なし'))

    def test_lint49_warns_when_positioned_telop_has_no_space(self):
        body = '''静止画プロンプト（16:9）:\n```\nA wide mountain landscape.\n```'''
        text = segment(49, asset_type='静止画', body=body, note='→ 編集者指示: 上部にテロップを入れる。')
        self.assertEqual(1, len(warnings_for(text, 'テロップ余白の指定なし')))

    def test_lint49_accepts_prompt_with_copy_space(self):
        body = '''静止画プロンプト（16:9）:\n```\nA wide mountain landscape, leave empty space in the upper third for a caption.\n```'''
        text = segment(49, asset_type='静止画', body=body, note='→ 編集者指示: 上部にテロップを入れる。')
        self.assertEqual([], warnings_for(text, 'テロップ余白の指定なし'))

    def test_lint50_warns_when_diagram_text_is_deferred(self):
        text = segment(50, asset_type='テキスト図解', note='→ 編集者指示: 数字は編集で入れる。')
        self.assertEqual(1, len(warnings_for(text, '図解・グラフを編集任せにしている')))

    def test_lint50_ignores_completed_diagram(self):
        text = segment(50, asset_type='テキスト図解', note='→ 編集者指示: 数字と文字は画像内に完成済み。')
        self.assertEqual([], warnings_for(text, '図解・グラフを編集任せにしている'))


class CharacterFacingHeadsBackgroundTest(unittest.TestCase):
    """rules 51-53: 2026-09-24 せたな町で有料生成後に差し戻された3件を、実際の文面で注入する。"""
    # せたな町 Asset_Prompts_Full.md ASSET-019 の実物（後ろ向き・chibiと4〜5頭身の混在）
    FAILED_CHAR = ("Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, "
                   "slightly chibi proportions, children's animation style. A full-body Japanese husband in his 50s wearing "
                   "a dark blue field jacket, seen from behind to avoid a real-person likeness, stepping out of a house "
                   "toward the mountain with one arm forward, four-to-five-head proportions, compact torso and short limbs. "
                   "Real alpha transparency, only this figure and one necessary hand-held prop, no setting, no lettering.")
    GOOD_CHAR = ("Cute cartoon character design, thick black outlines, flat cel-shaded colors. A full-body Japanese husband "
                 "in his 50s, three-quarter front view facing to the right, face clearly visible, large expressive eyes, "
                 "a very large head about one third of the total height, a short compact torso and short stubby arms and "
                 "legs, roughly three heads tall. Do NOT draw them with realistic adult proportions — not four, five, six "
                 "or seven heads tall. Transparent background.")
    STILL_BG = "A rural house doorway toward a wooded mountain road in early spring, Japan. No people. 16:9."
    VIDEO_BG = "Animate the frozen frame for 8 seconds. The camera advances along the mountain road. No people."

    def cut(self, no, char, bg=STILL_BG, memo='', extra=''):
        body = f'キャラプロンプト（1:1）:\n```\n{char}\n```\n背景プロンプト（16:9）:\n```\n{bg}\n```\n{extra}'
        return segment(no, body=body, note=memo)

    def test_yesterdays_back_view_is_blocked(self):
        self.assertEqual(1, len(errors_for(self.cut(19, self.FAILED_CHAR), 'キャラが後ろ向きなのに向き理由なし')))

    def test_yesterdays_chibi_mix_is_blocked(self):
        self.assertEqual(1, len(errors_for(self.cut(19, self.FAILED_CHAR), 'キャラの頭身指定が欠落・矛盾')))

    def test_four_to_five_heads_is_blocked_after_three_heads_ruling(self):
        # 本人裁定 2026-09-25: 3頭身。旧定型句の4〜5頭身は矛盾として止める
        old = self.GOOD_CHAR.replace('roughly three heads tall', 'roughly four to five heads tall')
        self.assertEqual(1, len(errors_for(self.cut(19, old), 'キャラの頭身指定が欠落・矛盾')))

    def test_video_background_is_blocked(self):
        self.assertEqual(1, len(errors_for(self.cut(19, self.GOOD_CHAR, bg=self.VIDEO_BG), 'キャラカットの背景が静止画になっていない')))

    def test_video_alongside_without_editor_rule_is_blocked(self):
        extra = 'Google Flow動画プロンプト:\n```\nAnimate the frozen frame for 8 seconds.\n```'
        self.assertEqual(1, len(errors_for(self.cut(19, self.GOOD_CHAR, extra=extra), 'キャラカットの背景が静止画になっていない')))
        ok = self.cut(19, self.GOOD_CHAR, extra=extra, memo='→ 編集者指示: キャラ画の区間は開始画像を背景にする。')
        self.assertEqual([], errors_for(ok, 'キャラカットの背景が静止画になっていない'))

    def test_good_character_cut_passes_all_three(self):
        text = self.cut(19, self.GOOD_CHAR)
        for prefix in ('キャラが後ろ向き', '後ろ向きのキャラカットが多すぎる', 'キャラの頭身', 'キャラカットの背景'):
            self.assertEqual([], errors_for(text, prefix), prefix)

    def test_needed_back_view_with_reason_passes(self):
        back = self.GOOD_CHAR.replace('three-quarter front view facing to the right, face clearly visible',
                                      'seen from behind walking away up the trail')
        text = ''.join(self.cut(i, self.GOOD_CHAR) for i in range(1, 6)) + \
            self.cut(6, back, memo='向き理由=走り去る後ろ姿をナレーションが語る')
        self.assertEqual([], errors_for(text, 'キャラが後ろ向きなのに向き理由なし'))
        self.assertEqual([], errors_for(text, '後ろ向きのキャラカットが多すぎる'))

    def test_all_back_view_with_reasons_still_blocked_by_ratio(self):
        back = self.GOOD_CHAR.replace('three-quarter front view facing to the right, face clearly visible', 'seen from behind')
        text = ''.join(self.cut(i, back, memo='向き理由=顔を伏せる') for i in range(1, 6))
        self.assertEqual(1, len(errors_for(text, '後ろ向きのキャラカットが多すぎる')))

    def test_cartoon_master_back_view_is_blocked(self):
        master = ('### CHAR-02｜夫\n\n```text\nOne full-body Japanese man. Rear or three-quarter back view only, '
                  'face not identifiable. Cute Japanese cartoon character design.\n```\n\n---\n\n')
        errs = errors_for(master + self.cut(19, self.GOOD_CHAR), 'キャラが後ろ向きなのに向き理由なし')
        self.assertEqual(1, len(errs))
        self.assertIn('CHAR-02(基準画像)', errs[0])

    def test_photoreal_master_back_view_is_allowed(self):
        master = ('### CHAR-01｜女性\n\n```text\nA Japanese woman. Show her only from behind; no identifiable face. '
                  'Photorealistic live-action style.\n```\n\n---\n\n')
        self.assertEqual([], errors_for(master + self.cut(19, self.GOOD_CHAR), 'キャラが後ろ向きなのに向き理由なし'))


if __name__ == '__main__':
    unittest.main()
