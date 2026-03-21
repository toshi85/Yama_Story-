# Yama_Story Session Queue

## 最優先: Rausu_Asset_Prompts.md 最終仕上げ

### 現状
- 151 ASSET、306/306ナレーション行カバー（台本突合PASS）
- ただし60行は「テキスト挿入のみ」で専用プロンプトなし
- それらが隣接ASSETのシーンでカバーされるか要確認

### 残タスク

#### 1. 60行の所属確認
- 台本原文から強制挿入した60行を確認
- 各行が隣接するASSETのシーンに映像的に合っているかチェック
- 合っていない行には新規ASSET追加（枚数増加の可能性あり）

#### 2. バリデーションFAIL修正
- プロンプト内禁止ワード
- カメラ専門用語
- その他のFAIL項目

#### 3. 最終TXT・GitHub反映

### 重要ルール（再発防止）
- **エージェントにナレーション行を書かせない** — 台本原文をプログラムでコピーする
- **台本突合チェックは毎回実行** — `python3 validate_yama_prompts.py <asset.md> <master.md>`
- **キャラアニメ比率40-45%**

### 参照ファイル
- 台本: `Yama_Story/Scripts/羅臼岳ヒグマ襲撃事件_Master.md`
- プロンプト: `Yama_Story/Rausu_Asset_Prompts.md`（151 ASSET版）
- 改行データ: `Yama_Story/Rausu_改行データ.txt`
- バリデーター: `Yama_Story/System_Tools/validate_yama_prompts.py`
