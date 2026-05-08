# 2023年 大千軒岳ヒグマ事件 素材プロンプト一括リスト

> Lovartにコピペするだけの流れ作業用。生成順＝台本の登場順。
> **シーン単位グルーピング版**: 1ASSET = ナレーション1〜3行。各ASSETのプロンプトはナレーション内容に映像的に一致。

> **2026-04-25 分割済み**: AI精度向上のため、PARTごとに分割しました。

| ファイル | 内容 | アセット |
|:---|:---|:---|
| `Asset_Prompts_KI.md` | 起（フック〜舞台）+ CHAR基準画像 | ASSET-001〜020 |
| `Asset_Prompts_SHO.md` | 承（10月29日〜消防士襲撃〜下山） | ASSET-021〜075 |
| `Asset_Prompts_TEN_KETSU.md` | 転・結（保存食〜DNA鑑定〜教訓〜エンディング） | ASSET-076〜130 |

> 編集時は該当PARTのファイルのみ開いてください。

---

## 0. キャラ基準画像（最初に生成→一貫性キャラ機能の参照画像にする）

> **スタイル方針**: キャラ画像 = カートゥン調イラスト（太い輪郭線、フラットカラー、大きな瞳、子供向けアニメ風）
> 背景・シーン画像/動画 = フォトリアル（RED camera風、ドキュメンタリー調）
> Lovartでは1プロンプトにつき3枚同時生成。ベスト1枚を一貫性キャラの参照画像として採用。

### CHAR-01: 屋名池奏人（やないけ かなと）さん（22歳）— 北大水産学部4年生・被害者

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. An attractive Japanese man, 22 years old, university student, slim athletic build, short black hair neatly cut, fair skin tone, intelligent gentle face. Wearing a beige hiking jacket, dark green hiking pants, brown hiking boots, and a navy daypack. Calm thoughtful expression. Generate 3 separate images, each showing only this one character.
```

### CHAR-02: 大原巧海（おおはら たくみ）さん（41歳）— 福島消防署員・刃渡り5cmのナイフでヒグマに反撃した人物

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A handsome Japanese man, 41 years old, firefighter, muscular sturdy build, short black hair, weathered tan skin tone, strong determined face with calm courage. Wearing dark gray mountain pre-survey clothing — tactical jacket, cargo pants, sturdy hiking boots — with a tactical vest carrying a small folding knife on his hip. Resolute steady expression. Generate 3 separate images, each showing only this one character.
```

### CHAR-03: 阿部達也（あべ たつや）さん（36歳）— 福島消防署員・3人の捜索チームの一人

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. An attractive Japanese man, 36 years old, firefighter, lean athletic build, short black hair with slight side part, medium skin tone, alert focused face. Wearing dark olive mountain survey clothing — softshell jacket, hiking pants, mountaineering boots — with a small daypack and signal flare pistol holstered at his side. Earnest determined expression. Generate 3 separate images, each showing only this one character.
```

### CHAR-04: 船板克志（ふないた かつし）さん（41歳）— 知内消防署員・最初に襲われた人物

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A handsome Japanese man, 41 years old, firefighter, broad-shouldered powerful build, short black hair slightly graying at temples, weathered medium skin tone, kind firm face. Wearing dark navy mountain survey clothing — outdoor jacket, technical pants, hiking boots — with a bear bell on his pack and a whistle around his neck. Steady reliable expression. Generate 3 separate images, each showing only this one character.
```

### CHAR-05: 加害個体ヒグマ（4〜5歳・雄・体長1.7m）— 「人を恐れず積極的に攻撃」した個体

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A young male Hokkaido brown bear (Ursus arctos yesoensis), 4 to 5 years old, body length about 1.7 meters, weighing over 100kg, dark brown fur with slightly lighter muzzle, small rounded ears, powerful shoulders and thick limbs, intense unafraid eyes, slightly visible claws. Standing on all fours. Generate 3 separate images, each showing only this one character.
```

---

## 全パート別ファイル参照

- 起: `Asset_Prompts_KI.md`
- 承: `Asset_Prompts_SHO.md`
- 転・結: `Asset_Prompts_TEN_KETSU.md`

---

## Google Earth 座標・カメラ設定まとめ

| 素材ID | 座標 | カメラ指示 |
|--------|------|-----------|
| ASSET-008 | 41°33'00"N 140°15'00"E（大千軒岳全景） | 北海道全域→渡島半島南端へズームイン |
| ASSET-013 | 41°28'00"N 140°16'00"E（福島町・松前町） | 渡島半島南端を俯瞰 |
| ASSET-052 | 41°34'15"N 140°14'40"E（7合目付近） | 大千軒岳の登山ルート、7合目にピン |
| ASSET-097 | 41°34'15"N 140°14'40"E（消防士襲撃地点） | 7合目付近、ピンで強調 |
| ASSET-115 | 41°34'00"N 140°15'00"E（ヘア・トラップ調査エリア） | 大千軒岳と周辺を赤い円で表示 |

---

## 素材カテゴリ別サマリー

| カテゴリ | 件数 | 自分の作業 | 編集者の作業 |
|----------|------|-----------|------------|
| Lovart生成（静止画） | 約65枚 | コピペ→選ぶ | なし |
| Lovart生成（動画→Flow） | 25本 | コピペ→選ぶ→Flow | なし |
| キャラアニメーション（CHAR+背景） | 約32箇所 | コピペ→選ぶ | CapCutで合成 |
| Lovart＋編集者（図解系） | 約8件 | コピペ→選ぶ | テキスト/数値追加 |
| Google Earth | 5箇所 | なし | 座標見て録画 |
| キャラ基準画像 | 5件 | コピペ→選ぶ | なし |
| **合計** | **約140件** | **Lovart 約135回** | **図解約8件 + GE 5箇所** |
| **動画/アニメ比率** | **約41%** | **目標: 40%以上** | — |

---

## 動画予算サマリー

| 項目 | 数 |
|:--|--:|
| Lovart動画（Google Flow使用） | 25本 |
| Veo Fastクレジット消費 | 25 × 20 = 500cr |
| 月間予算（4本/月） | 500 × 4 = 2,000cr |
| AIプロ月間枠 | ~2,500cr |
| 判定 | ✅ 予算内 |
