# Yama_Story Session Queue

## 最優先: Rausu_Asset_Prompts.md 全面再生成

### 概要
ユーザーが改行データ（1ブロック=1ASSET）を作成済み。このデータに従ってAsset_Promptsを全面再生成する。

### 改行データ
- ファイル: `Yama_Story/Rausu_改行データ.txt`
- 326ブロック（= 326 ASSET必要）
- 複数行ブロックは1件のみ（年表3行: L496-498）
- ユーザー指示: 回想シーンでいけそうな箇所は回想として素材を再利用OK

### 作業手順
1. `Rausu_改行データ.txt` を読み、各ブロックに対してASSET-001〜326を生成
2. CHAR定義（CHAR-01〜03）は既存をそのまま使用
3. 各ブロックに対してカテゴリ分類（キャラアニメ40-45% / 動画 / 静止画+編集者 / GE）
4. 英語プロンプト生成（フォトリアル背景 / カートゥンキャラ）
5. 回想シーン（セクション8以降の過去回想）は彩度低め+ビネット指示
6. バリデーション実行 → 台本突合チェック
7. TXT・GitHub反映

### 比率目標
- キャラアニメーション: 40-45%
- 動画/アニメ合計: 55%以上
- 静止画2連続禁止

### 参照ファイル
- 台本: `Yama_Story/Scripts/羅臼岳ヒグマ襲撃事件_Master.md`
- 改行データ: `Yama_Story/Rausu_改行データ.txt`
- 既存プロンプト: `Yama_Story/Rausu_Asset_Prompts.md`（CHAR定義のみ流用）
- バリデーター: `Yama_Story/System_Tools/validate_yama_prompts.py`
