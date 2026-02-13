# Yama Story Script Structural Rules (Physically Enforced)

## 1. The "Golden Ratio" (1:7:2)
All scripts MUST adhere to the following character count distribution:

| Section | Role | Target Ratio | Tolerance |
| :--- | :--- | :--- | :--- |
| **起 (Ki)** | Introduction / Hook | **10%** | ±5% (5-15%) |
| **承 (Sho)** | The Incident / **Human Action** | **70%** | ±10% (60-80%) |
| **転結 (Ten-Ketsu)** | Conclusion / Lesson | **20%** | ±5% (15-25%) |

## 2. Mandatory Markers
Scripts must explicitly demarcate these sections using HTML comments to allow the Validator to parse them physically.

```markdown
<!-- PART: KI -->
## 1. Introduction...

<!-- PART: SHO -->
## 2. The incident...

<!-- PART: TEN-KETSU -->
## 11. Conclusion...
```

## 3. Action Density (The "System 2" Check)
The **承 (Sho)** section must focus on "Human Action", not just explanation.
The Validator checks for "Visual/Action Keywords" in the production notes (Col E equivalent / AI Video Prompts) of this section.

## 4. Validator Execution
Before any script is presented to the user, you MUST run:
`python3 Yama_Story/System_Tools/validate_yama_structure.py <script_path>`

## 5. 素材制作ガイドライン（2026年2月策定）

### 素材カテゴリと優先順位

| 優先度 | カテゴリ | 用途 | ツール |
|:---:|:---|:---|:---|
| 1 | 実写素材 | 実在人物・実在の場所 | Web検索で取得 |
| 2 | キャラアニメーション | 人物が登場するシーン | Lovart(1:1) + 背景(16:9) + CapCut |
| 3 | Lovart背景静止画 | 風景・物・抽象シーン | Lovart(16:9) + Ken Burnsエフェクト |
| 4 | AI動画（Google Flow） | 最重要シーンのみ | Lovart静止画 → Google Flow動画化 |
| 5 | Google Earth | 地理的な位置説明 | Google Earth Studio |
| 6 | 図解/テキスト演出 | データ・メカニズム説明 | CapCut/AE + Lovart背景 |

### 禁止事項
- **フリー素材の使用禁止**: 全てLovart AI画像で生成する。フリー素材サイト（Pexels, Unsplash等）からのダウンロードは行わない
- **AI動画の過剰使用禁止**: 1本の動画あたりAI動画は最大12本まで（Google Flowクレジット予算: 月250クレジット/本）

### AI動画（Google Flow）の使用基準
AI動画はクレジットコストが高いため、以下の基準を満たすシーンのみに使用する:
1. **動きが物語の核心**: 動きそのものがストーリーの転換点になるシーン
2. **静止画では表現不可能**: Ken Burnsエフェクトでは伝わらない動的表現
3. **視聴者の感情ピーク**: 衝撃・感動・恐怖の最高潮シーン

AI動画に該当しないシーンの代替手段:
- 人物が登場 → **キャラアニメーション**（Lovartキャラ + 背景合成 + CapCutキーフレーム）
- 風景・物 → **Ken Burns付き静止画**（Lovart静止画 + CapCutズーム/パン）

### 実写素材の使用ルール
実在の人物・場所の実写素材はAI生成より説得力があるため積極的に使用する。ただし以下のチェックリストを必ず確認:

#### 著作権チェックリスト（全実写素材共通）
使用前に以下を全て確認すること:
- [ ] クリエイティブ・コモンズライセンスまたはフェアユース適用可能か
- [ ] YouTubeコンテンツポリシー（再利用コンテンツ）に抵触しないか
- [ ] 報道目的の引用として適切な範囲か（数秒以内、全体の一部）
- [ ] 権利者のクレジット表記が必要か → 必要な場合は概要欄に記載
- [ ] 確認できない場合はLovartフォールバックプロンプトを使用

#### 実写素材の優先ソース
1. Wikimedia Commons（CC-BY-SA、パブリックドメイン）
2. 政府機関・公的機関の報道写真（新華社等）
3. 報道機関の写真（フェアユース引用として最小限の使用）

### Lovartプロンプトの標準仕様
- **キャラ画像**: 1:1、背景透過、カートゥン調（太い輪郭線、フラットカラー、大きな瞳）
- **背景画像**: 16:9、フォトリアル（RED camera風、ドキュメンタリー調）
- **生成枚数**: 1プロンプトにつき5枚同時生成 → ベスト1枚を採用
- **一貫性キャラ機能**: CHAR-XX として参照画像を登録、以降は [CHAR-XX reference] で再利用

### 5秒ルール（映像密度基準）
- 静止画: ≤25文字（≒5秒）
- 動画: ≤50文字（≒10秒）
- 全体平均: ≤35文字/ASSET
- 連続静止画は2枚まで（3枚連続禁止）
