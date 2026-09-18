# 台本修正ログ（本人の人間チェック → 次作で同じ修正を出さないための台帳）

本人が台本を修正したら、その都度このファイルの「記録」に追記する。本人の修正は原文のまま残し、同じ作業で一般化した型IDと昇格先を記録する。次の台本では、執筆前と人間に渡す前に全記録の型を全章へ当てる。

## 記録

| 日付 | 台本 | 章 | Before | After | 型ID | 昇格先 |
|:--|:--|:--|:--|:--|:--|:--|
| 2026-09-18 | せたな町 | §1（フック） | 「山菜を採りに山へ入った52歳の女性が、戻りませんでした。」 | 「…52歳の女性が、消息不明。」 | YCP-045 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §1（フック） | 「不在に気づいた夫が、山へ向かいます。」 | 「異変に気づいた夫が、山へ向かいます。」 | YCP-046 | `Correction_Patterns.md`／`correction_word_map.txt` WARN |
| 2026-09-18 | せたな町 | §1（フック） | 「落ちていたのは、女性の衣服でした。」 | 「落ちていたのは、女性の衣服のみ。」 | YCP-045 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §1（フック） | 「捜索に出た人たちが見つけたのは、帰らぬ人となった女性の姿。」 | 「…見つけたのは、無残な姿となった女性でした。」（この行の後に空行を追加） | YCP-047／YCP-019 | `Correction_Patterns.md`／`correction_word_map.txt` WARN |
| 2026-09-18 | せたな町 | §1（フック） | 「一年後。約8キロ離れた山で、また女性が襲われました。」 | 「一年後、また女性が襲われました。」 | YCP-048 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §1（フック） | 「襲ったのは、同じ一頭です。」 | 「襲ったのは、あの時のクマです。」 | YCP-049 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §1（フック） | 「なぜ、その一頭は捕まらなかったのか。」 | 「なぜ、クマは捕まらなかったのか。」 | YCP-049 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §1（フック） | 「そして、町が探し続けたクマは、どこにいたのか。」 | 「そして、探し続けたクマは、どこにいたのか。」 | YCP-016 | `Correction_Patterns.md`（既存型へ実例追記） |
| 2026-09-18 | せたな町 | §2（場面導入） | 「女性が入ったのは、北檜山区の新成地区です。」 | 「北海道の南西部、日本海に面したせたな町。」 | YCP-050 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §2（場面導入） | 「地図には、丸山という標高334メートルの山が記されています。」 | （削除） | YCP-051 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §2（場面導入） | 「山あいには、谷に沿って流れる川があります。」 | （削除） | YCP-051 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §2（場面導入） | 「52歳の女性が山に入った目的は、山菜採りでした。」 | 「町の北檜山区、新成地区の山へと52歳の女性が足を踏み入れます。」＋空行＋「目的は春の山菜採り。」 | YCP-052 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §3 | 「夫が出発する女性を見送ったのかは、分かっていません。」 | （削除） | YCP-053 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §2 | 「ただし、採っていた山菜の種類までは分かっていません。」 | （削除） | YCP-053 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §7 | 「当時の放送の文面や回数までは、記事に載っていません。」 | （削除） | YCP-053 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §17 | 「ただし、けがをした部位や入院の期間までは、公表された一覧に示されていません。」 | （削除） | YCP-053 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §24 | 「2014年の2人が事前にどんな情報を見ていたかまでは、確認できていません。」 | （削除） | YCP-053 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §22 | 「どちらの事故の直後に設けたか、日付まではこの答弁にありません。」 | （削除） | YCP-053 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §2〜§5冒頭 | （場面の時刻を独立行で置かずに開始） | 「4月16日午前」／「午前12時」／「翌日の4月17日」を1行で置いてから場面に入る | YCP-054 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §3〜§4 | 「山菜を採りに入った女性と、不在に気づいた夫。」→「このあと、夫は女性の衣服などを見つけることになります。」→「夫が見つけたのは、女性の衣服などでした。」→「女性のものを発見した夫は、警察に通報します。」→「そのあと、猟友会や役場の職員らが女性を捜しました。」 | 「昼食の時間になっても帰らない妻を心配した夫は、」→「山のほうへと探しにいくことに。」→「すると、妻のワゴン車と衣服の一部が山で見つかります。」→「何か事件に巻き込まれたと判断した夫は、警察に通報。」→「到着した警察と消防は辺りを捜索。」→「すると、およそ車から200メートルほど離れた地点で妻を発見。」 | YCP-055 | `Correction_Patterns.md`／`SCRIPT_CHECKLIST.md` |
| 2026-09-18 | せたな町 | §3〜§4 | 「52歳の女性がいない」「女性の行方」「女性のもの」「女性本人」 | 「帰らない妻」「妻のワゴン車」「妻を発見」 | YCP-056 | `Correction_Patterns.md`／`SCRIPT_CHECKLIST.md` |
| 2026-09-18 | せたな町 | §4 | 「見つかった52歳の女性は、すでに帰らぬ人となっていたのです。」 | 「しかし、すでに息を引き取っていました。」＋「遺体は両手両足の筋肉を食い取られており、見るに堪えない状況でした。」 | YCP-057 | `Correction_Patterns.md`／`correction_word_map.txt` WARN（全章） |
| 2026-09-18 | せたな町 | §4 | 「道の人身事故の一覧にも、この女性が命を落としたことが記されています。」／「のちの函館新聞社の記事は、地元のハンターによる山林一帯の捜索も伝えました。」／「記事は両年の事故を紹介したあとに、この経緯を記しています。」 | （削除） | YCP-058 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §3〜§4 | 「このあと、夫は女性の衣服などを見つけることになります。」／「妻がいないと感じた夫の捜索は、衣服の発見と通報につながりました。」 | （削除） | YCP-059 | `Correction_Patterns.md`／`validate_yama_narrative.py` WARN |
| 2026-09-18 | せたな町 | §5 | 「翌日の4月17日、道総研が現地の調査に入りました。」 | 「翌日の4月17日」＋「北海道の研究機関『道総研』が、現地の調査に入りました。」 | YCP-060 | `Correction_Patterns.md`／`abbreviations.txt`／`validate_yama_narrative.py` WARN |
