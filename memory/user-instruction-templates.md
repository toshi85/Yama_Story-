---
name: Yama ユーザー指示文テンプレ集
description: 2026-05-24確定。過去のミスパターン（リファレンス未読・数値推測・1要素ずつ後付け修正・「読んだフリ」着手）を物理的に防ぐ指示文テンプレ。タスク種類別。
type: reference
---

# Yama_Story タスク用 ユーザー指示文テンプレ集

過去ミス事例（羅臼岳片道7時間=誤情報・サムネ連発NG・概要欄肥大化等）から逆算。冒頭にコピペするだけで AI に必読・検証・最小手数を強制できる。

---

## 共通プレフィックス（全タスク冒頭に貼る）

```
【着手前ルール】
1. リファレンス全件 Read（grep禁止）→ 読了ファイル一覧を先に報告
2. 最小手数自問を1行で明示
3. 個別要望 vs 全体ルール の区別を申告
4. 数値・事実は Playwright MCP / WebSearch で検証してから記述

【NGパターン】
- 「読んだフリ」で着手
- 1要素ずつ後付け修正で肥大化
- 推測で数値を書く（時間・距離・標高）
- 完了報告に「（要設定）」プレースホルダ残し
```

---

## A. 新規台本作成

```
【タスク】<事件名>の台本作成

【必須参照】
- Yama_Story/Channel_Master_Prompt_Yama.md（文体・NGワード・構造ルール）
- Yama_Story/Scripts/羅臼岳ヒグマ襲撃事件/Master.md（リファレンス）
- Yama_Story/memory/yama-script-cut-patterns.md（カットされやすいセクション）
- Yama_Story/Learned_Patterns_Yama.md（勝ちパターン公式）
- Yama_Story/memory/feedback_yama_research_direct_webfetch.md（リサーチ品質ルール・必読）
- Yama_Story/memory/feedback_yama_quote_source_verified.md（引用原典確認ルール・必読）

【リサーチ品質ルール（2026-05-25確定）】
- エージェント要約に依存禁止。メインエージェントが直接WebFetchで全主要ソースを取得
- 競合動画はyoutube-transcript-apiで字幕一括取得→実データで構成分析
- ソース最低取得数: 日本語Wikipedia1+英語Wikipedia1+公的機関1+報道3+ブログ3+競合動画字幕3 = 計12件以上
- 引用フレーズは一次資料で原典確認必須。確認不可なら削除 or 「と伝えられる」等の婉曲表現
- 引用には必ず <!-- src: 書籍名 出版社 刊行年 pXX --> 形式で原典明記

【数値検証】
- 時間/距離/標高は Playwright MCP で環境省・YAMAP・山と高原地図の3点クロスチェック
- 各数値の同一行 or 前後3行に <!-- src: ソース名 日付 --> を必ず添える

【完了条件】
- python3 Yama_Story/System_Tools/audit_numeric_facts.py <ファイル> で未検証0件
- validate-yama-quote-source.sh 警告0件（引用原典確認）
- yama-fact-checker スキル通過
- 「（要設定）」「TBD」「仮置き」grep 0件
- 競合動画字幕の実データ分析レポート添付（カバー率比較表）

【構成密度】
- 25-30セクション上限（動画25分想定なら）
- 対比演出だけのセクション・教訓もし系は独立化禁止（カット対象）
- 核心キーワードは先出し→科学解説で裏付ける構造
```

---

## B. 既存台本のシーン追加・修正

```
【タスク】<台本名> ASSET-<番号> または <セリフ抜粋> の修正

【必須参照】
- Yama_Story/Scripts/羅臼岳ヒグマ襲撃事件/Asset_Prompts_KI.md 全行通読
- 該当 Master.md のシーン前後10行
- Asset_Prompts.md の CHAR定義（属性引用元）

【最小手数自問】
- 1枚で済むか？1キャラで済むか？1プロンプトで済むか？編集者の実装コストは？

【スコープ】
- このシーンのみ / 全体ルール のどちら？（リファレンスにないルールは全体化禁止）

【規格】
- キャラプロンプト: 固定スタイルヘッダー6要素 + (CHAR-XX 再利用) + white background + Generate N separate images.
- 背景プロンプト: Photorealistic + RED camera + 16:9 + No people + Generate N separate images.
- AI動画: 静止画+Google Flow動画の2ブロック必須

【完了条件】
- python3 Yama_Story/System_Tools/validate_yama_prompts.py <ファイル> 違反0件
```

---

## C. サムネプロンプト作成

```
【タスク】<事件名>のサムネプロンプト

【必須参照】（hook自動発動するが念のため）
- Yama_Story/memory/yama-thumbnail-prompt-template.md（標準テンプレA案/B案）
- Yama_Story/memory/yama-lovart-failure-patterns.md（過去NG事例）
- 該当 Master.md タイトル候補10案

【7要素必須】
1. 職業ベース（fashion model + drama actor の2職業重ね）
2. 顔骨格（V字小顔・二重・高鼻筋・8頭身）
3. 肌（年代別）
4. カメラ目線（最重要）
5. 口を大開けで歯出し笑い
6. 自然な動き（風で髪のみ）
7. 暗い山岳背景+不穏な空（クマシルエットはユーザー指示時のみ）

【テキスト構成】
- 上段: 日常会話・10字以内・カギカッコ付き
- 下段: 映像浮かぶ・6字以内・タイトル独占キーワードと重複禁止
- A1/A2は下段固定・上段だけ変えるクリーンテスト

【禁止】
- 三重強調 / 3職業以上 / 大文字強調 / 否定形強調過剰
```

---

## D. 概要欄・タイトル・タグ作成

```
【タスク】<事件名>のメタデータ

【必須参照】
- .claude/skills/yama-metadata/SKILL.md
- Yama_Story/Scripts/<近接テーマ>/Metadata.md（実例）
- 該当 Master.md タイトル候補10案

【タイトル】
- 25-50字（実例範囲）
- カテゴリA/B/Cの3案
- Learned_Patterns適合（結末系・数字・省略記号・山舐め度高）
- NGワード回避（死亡/殺害/遺体→帰らぬ人/事件/姿）

【概要欄】
- 冒頭3行（フック・SEOキーワード集中）+ 本文（SKILL.md目安400-600字）
- 目次（XX:XX 仮置き or 動画完成後に確定）
- 参考資料（Tier1/Tier2優先）

【タグ】
- 5-30個・タイトル内キーワード反映
- 検索流入導線をカバー
```

---

## E. 事実検証依頼

```
【タスク】<台本/数値箇所>の事実確認

【検証手段】
- Playwright MCP で公的情報源（環境省・気象庁・知床財団・自治体）アクセス
- 並列で複数ソース確認（最低3点クロスチェック）

【結果報告】
- ソース名・URL・該当数値・台本記述との一致/不一致
- 不一致なら推奨修正案を提示

【完了後】
- 該当箇所に <!-- src: ソース名 日付 --> を添える
```

---

## F. 完了報告前チェック（AIへの必須リマインド）

```
【完了報告前に確認】
1. python3 Yama_Story/System_Tools/validate_yama_prompts.py <ファイル> 違反0件か
2. python3 Yama_Story/System_Tools/audit_numeric_facts.py <ファイル> 未検証0件か
3. grep -E "（要設定）|TBD|仮置き" <ファイル> ヒット0件か
4. CHAR定義からの属性引用は完全一致しているか
5. 「読んだファイル一覧」を報告に含めたか
```

---

## 使い方

1. ユーザーが新規セッションでYama関連タスクを開始する時、上記テンプレの該当パートをチャットに貼る
2. AI（私）は冒頭プレフィックスを見て、必読リファレンスを物理的に通読
3. 各タスク別テンプレで規格・検証方法・完了条件が明示される
4. 完了報告前チェックでgrep / validateを必ず通す

**Why:** 過去のミスは「ユーザーが知らないルール（リファレンス通読義務・数値検証義務・最小手数自問）を AI が守らなかった」ことが原因。テンプレに明文化すれば、ユーザー側でも「これを貼れば AI が間違えない」が可視化される
**How to apply:** 新規セッションで Yama タスク開始時、ユーザーは本ファイルを開いて該当テンプレをコピペ。AI はテンプレ要件を守って着手
