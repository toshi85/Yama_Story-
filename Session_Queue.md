# Yama_Story Session Queue

## 最優先: Rausu_Asset_Prompts.md クリーンアップ

### 現状
- 142 ASSET、306ナレーション行カバー済み
- キャラアニメ58枚(41%) / 静止画43枚(30%) / 動画26枚(18%) / GE14枚(10%)

### 残タスク

#### 1. 重複ナレーション行のクリーンアップ
- fix_asset_narration.pyが追加した個別行と、エージェントが生成した結合行が共存
- 例: ASSET-071にL295-L297の結合行と個別行が両方ある
- **対応**: スクリプトで重複を自動検出・削除

#### 2. 3行以上ASSETの分割（58件）
- 1つのプロンプトで3行以上のナレーションをカバーしているASSET
- シーンが変わるポイントで分割が必要
- 特に問題: ASSET-074(6行), ASSET-083(6行), ASSET-087(6行), ASSET-121(8行), ASSET-127(5行)
- **対応**: 各ASSETのナレーション内容を確認し、映像的に異なるシーンで分割

#### 3. バリデーションFAIL修正
- プロンプト内禁止ワード (6件)
- カメラ専門用語 (3件)
- キャラプロンプト環境要素 (2件)
- 静止画25文字超過 (5件)

#### 4. 最終TXT・GitHub反映

### 参照ファイル
- 台本: `Yama_Story/Scripts/羅臼岳ヒグマ襲撃事件_Master.md`
- プロンプト: `Yama_Story/Rausu_Asset_Prompts.md`
- バリデーター: `Yama_Story/System_Tools/validate_yama_prompts.py`
- 自動補完: `Yama_Story/System_Tools/fix_asset_narration.py`
