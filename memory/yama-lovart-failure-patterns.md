---
name: Yama Lovart生成 失敗パターン蓄積
description: サムネ・キャラプロンプト生成で発生したNG事象と、その原因・回避表現を1行ずつ蓄積。次回プロンプトに最初から組み込む
type: reference
---

# Lovart生成失敗パターン集（Yama_Story）

## 使い方
- 新しい失敗が発生したら、該当カテゴリに1行追記
- 次回プロンプト作成前にこのファイルを必ず Read（特にサムネ系）
- カラム: `症状` / `指示原因` / `回避表現`

---

## 1. 目線・カメラ目線関連

| 症状 | 指示原因 | 回避表現 |
|---|---|---|
| 目線が正面じゃなく横/上を向く | `looking directly at the viewer` 単発・弱い | `his entire face squared dead-front toward the camera. Both pupils centered and pointed STRAIGHT FORWARD into the camera lens. NOT looking up, NOT looking down, NOT looking sideways, NOT looking away` |
| 笑いで目が完全に閉じる | `eyes squinting with joy` を強く書きすぎ・`eyes tightly squinted shut into happy crescents` | `Both eyes remain wide open and fully visible — do NOT squint shut, do NOT close eyes from laughter` を明示 |

## 2. 笑顔・表情関連

| 症状 | 指示原因 | 回避表現 |
|---|---|---|
| 歯がほとんど見えない控えめ微笑 | `gentle smile` `confident smile` `bright cheerful smile` | `mouth wide open laughing joyfully showing perfect white teeth, ecstatic exhilarated expression`（立山実例準拠） |
| 「ニッと歯見せ」止まりで口が開かない | `big bright toothy smile, beaming grin` | `MOUTH WIDE OPEN LAUGHING JOYFULLY in a mid-laugh moment — jaw dropped open in an active laugh ... the inside of the mouth clearly seen` |

## 3. 容姿・イケメン度関連

| 症状 | 指示原因 | 回避表現 |
|---|---|---|
| 平凡な顔立ち | `attractive` 単発 / `Extremely attractive handsome` だけだと日本人平均顔 | **2026-05-24採用**: 職業ベース `Japanese male fashion model with the looks of a Japanese drama heart-throb lead actor` + 顔骨格具体記述（V字小顔・二重・高鼻筋・8頭身） |
| 三重強調で逆に不自然・CG感 | `The most extraordinarily breathtakingly attractive` + 3職業以上重ね | **2職業まで（fashion model + drama actor）はOK**。3つ以上重ね禁止 |
| イケメン度足りない | 顔骨格の具体記述なし | `Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid almond-shaped eyes with long thick eyelashes, 8-head body proportions` |

## 4. 動き・ポーズ関連

| 症状 | 指示原因 | 回避表現 |
|---|---|---|
| 棒立ち・スタジオ撮影感 | 動き要素ゼロ | `stylish short black hair gently blown by mountain wind. Wind gently blowing his hair and the collar of his jacket`（立山実例） |
| motion blur過剰で人物がブレる | `autumn leaves mid-air ... fog swirling actively ... daypack strap swaying` を複数併用 | 1〜2要素に絞る（風で髪+襟だけ等） |

## 5. 背景関連

| 症状 | 指示原因 | 回避表現 |
|---|---|---|
| 背景無地・スタジオ感 | `Plain solid dark slate-gray background` | Channel_Master §7「暗めの山岳風景必須」遵守 |
| 背景ヒグマが目立ちすぎ・人物を食う | `lunging forward aggressively, mouth wide open, motion blur` | `faint shadowy silhouette barely visible deep in the misty background`（立山実例） |
| 背景にヒグマを入れるとユーザーNG（事件により異なる） | 背景にヒグマシルエットを自動追加 | 大千軒岳のように「背景クマ不要」と指示されたら立山方式（風景＋暗い空のみ）にする。ユーザーに確認してから入れる |
| 季節が勝手に冬（雪・氷）になる | 有名地名が特定季節と強く結びついている（朱鞠内湖=冬のワカサギ氷上釣り）+ `cold daylight` 等の語が連想を後押し | 季節を文頭で明示 `Late spring in mid-May` + `fresh green leaves, open dark blue water` + 末尾に `No snow, no ice, no frozen lake`。地名を固有名で書かず `a vast lake in Hokkaido` に匿名化するのも有効（朱鞠内湖ASSET-064実例 2026-07-22） |
| 上記対策でもまだ冬になる | `Hokkaido` + `lake` + `cold/tense grey light` の組み合わせが残っていると冬連想が復活する | 完全版: ①先頭を `Fresh green season, late May:` で開始 ②`lush green forest in full fresh leaf, vivid green trees covering the shores` と新緑を面で描写 ③`Hokkaido` も削除 ④光は `overcast soft daylight`（cold/grey禁止） ⑤末尾 `Absolutely no snow, no ice, no frozen water, no bare leafless trees, no winter scenery`（朱鞠内湖ASSET-067実例 2026-07-22） |
| 冬化対策で地名を消すと人物が外国人になる | `Hokkaido`/`Lake Shumarinai` 削除で日本情報がゼロになり、デフォルトの西洋人が出る | 場所ではなく人物側に日本を付与: 文頭 `rural Japan` + 人物ごとに `Japanese` + `all East Asian with black hair` + 末尾 `All people are Japanese — no Western-looking people`（朱鞠内湖ASSET-093実例 2026-07-22） |

## 6. 構図関連

| 症状 | 指示原因 | 回避表現 |
|---|---|---|
| 顔が小さい・全身入り | フレーミング指示なし | `framed from chest up`（立山実例）・バストアップ明示 |
| 二人が違う向きを向く（複数キャラ同居時） | `both facing the same direction` 単発 | **2026-07-24ルール変更（ユーザー指示）: 複数キャラは1枚に同居させて生成するのが標準**（AI精度向上により崩れが減ったため）。各キャラの配置と向きを位置語で明示（`On the left ... On the right ... facing each other` / `both running in the same direction`）+キャラ間の距離（`with a clear gap, no contact`）+二重スタイル宣言（ASSET-027方式）。崩れた場合のみ1人ずつ単独生成→Photopea合成にフォールバック |

## 6.5 複数人物関連

| 症状 | 指示原因 | 回避表現 |
|---|---|---|
| 群衆・複数人が全員同じ服装のクローンになる | `ten anglers in fishing gear and orange life vests` のように全員を同一属性でまとめて記述 | 一人ずつ書き分ける: `Every person is a distinct individual with different build, age, height and outfit: one in olive waders, one in a green rain jacket, one in a navy fleece...` + `No two people wear the same outfit.` を明示（朱鞠内湖ASSET-025実例 2026-07-22） |
| 白背景キャラが意味不明なポーズになる（舟なしで操船・何もない所から降りる等） | アクションに必須の乗り物・大道具をプロンプトから省き、キャラ単体+ジェスチャーだけで表現 | 乗り物/大道具はキャラプロンプトに含めて一緒に描く: `A small silver aluminium guide boat shown in full side view. CHAR-02 standing at the stern steering...The entire boat and the character fully visible.`（朱鞠内湖ASSET-027〜029実例 2026-07-22） |
| 複数人+乗り物でテイスト崩壊（洋風大人カートゥーン化・小さい瞳・水面まで描かれる） | 人物数・服装詳細・否定形が増えて文頭のスタイル指定が希釈される。`across the water` 等の語が背景を誘発 | ①スタイル指定を先頭と末尾で二重化し `very large shiny anime eyes` を明示 ②服装詳細を圧縮 ③`Pure white background — no water, no waves, no scenery` を明示 ④可能なら一貫性キャラ参照を併用（朱鞠内湖ASSET-027実例 2026-07-22） |
| クマ2頭の自然なやり取りでディズニー映画風（ブラザー・ベア調）になる | 「成獣オスが亜成獣を追う」等の野生動物2頭の題材が海外アニメ映画の学習データと強く結びつく | `Cute Japanese cartoon` + `NOT a realistic western animated movie style` を文頭で宣言（朱鞠内湖ASSET-126実例 2026-07-23） |
| chibi強化しすぎで動物が二足立ちのぬいぐるみ化・子グマが子犬になる | `strongly chibi + soft rounded simple shapes` で体型指示が四足指示に勝つ。`ears drooping` は犬の垂れ耳として描かれる | chibiは `slightly` 止まり。四足は047の解剖学定型文（`two front legs and two hind legs clearly separated...no standing upright`）を各個体に付ける。耳は `small round bear ears on top of the head` + `clearly a bear cub, not a dog, not a puppy`。しょんぼりは耳ではなく `head lowered timidly + big sad worried anime eyes` で表現（朱鞠内湖ASSET-126実例 2026-07-23） |
| 画像内に「CHAR-03」等のラベル文字が描き込まれる | **一貫性キャラの参照画像を添付せずに生成**すると、プロンプト内の `CHAR-XX:` ラベルが文字として描かれることがある（プロンプト表記自体は問題ではない・ユーザー確認済み 2026-07-22） | CHAR-XXが登場するプロンプトは必ず該当キャラの基準画像を一貫性参照に添付して生成する。保険として文字禁止文を添えるのは有効 |
| キャラが宙に浮く | `jumping back in shock` 等のジャンプ系動詞 | `both feet planted on the ground, leaning backward in shock` のように接地を明示（朱鞠内湖ASSET-047実例 2026-07-22） |
| 四足動物の体が破綻（脚の本数・配置ぐちゃぐちゃ・胴のねじれ） | `head lowered + aggressive stance + walking` など動的姿勢の重ねがけ | ポーズは静的な横向きに固定: `clean natural side profile, anatomically correct body: two front legs and two hind legs clearly separated and properly placed, level straight back. Simple stable standing pose — no twisting, no crouching, no lunging, no extra limbs.` 凶暴さは顔（眼光・牙）のみで表現（朱鞠内湖ASSET-047実例 2026-07-22） |

## 7. 動物キャラ関連

| 症状 | 指示原因 | 回避表現 |
|---|---|---|
| クマの背中に黒いタテガミ状の剛毛（モヒカン風）が生える | `bristling raised hackles along its shoulders`（毛の逆立ち指示）をカートゥーン調で文字通り誇張描画 | hackles系の語は使わない。凶暴さは `fierce menacing glare` + `baring sharp fangs` + `long sharp claws` + `head lowered in an aggressive stance` で表現し、毛は `smooth even fur all over the body` と明示（朱鞠内湖CHAR-03実例 2026-07-22） |
| 走るクマが二足歩行（擬人化ラン）になる | カートゥーン調 + `running forward at speed in pursuit` だけだと人間型の走りに解釈される。`head lowered aggressive stance` との動的重ねがけも破綻を助長 | 走りは四足ギャロップを明示: `running ON ALL FOURS in a clean natural side profile, a horizontal quadruped galloping stride with its body parallel to the ground` + 047の解剖学定型文（`two front legs and two hind legs clearly separated...level back`）+ 末尾に `NOT standing upright, NOT running on two legs, no bipedal pose, no human-like running posture`。動的姿勢の重ねがけ（head lowered等）は外し凶暴さは顔のみで（朱鞠内湖ASSET-143実例 2026-07-24） |

## 7.5 グラフ・インフォグラフィック関連

| 症状 | 指示原因 | 回避表現 |
|---|---|---|
| ほぼ真っ黒な画面が生成される | `Dark charcoal background + subdued cinematic lighting` に細い線・少要素の構成→暗部に全て沈む | 背景は `dark slate-blue background (NOT pure black)`、要素側を明示的に明るく: `bold white Japanese text` `thick bright red line` `light grey axis lines and grid lines` + `All chart elements bright, high-contrast and clearly visible` + `flat vector style`（照明語cinematic lightingは使わない）（朱鞠内湖ASSET-174実例 2026-07-24） |

## 8. 血痕・痕跡描写関連

| 症状 | 指示原因 | 回避表現 |
|---|---|---|
| 血痕を指示しても地面にほぼ描かれない（うっすら滲む程度） | ①`dark red bloodstains` が暗い泥地と同化して視認不可 ②文中に埋もれて優先度が低い ③末尾の `No gore` を生成AIが過剰適用し血ごと抑制 | ①血を文頭で主役化: `Pools and smears of fresh bright red blood clearly visible ... the main focus of the image` ②`vivid crimson` + `strong contrast against wet grey stones` で色と対比を明示 ③`No gore` は使わず `No body, no flesh, no wounds — only blood on the ground` に置換（残酷描写は防ぎつつ血は許可）（朱鞠内湖ASSET-060実例 2026-07-22） |
| モザイク資料写真でモザイク下に人体シルエットが描かれる | `forensic evidence photograph` + ブルーシート + 大きな検閲領域 → 検証写真=遺体と連想し人型に | 「屋外シート+大きな塊」をやめ「検査室のステンレストレイ+小さな平らな山」に変更。`a flat shapeless censored area with no outline, no silhouette` + `absolutely no body, no human shape, no animal shape, no limbs` を明示（朱鞠内湖ASSET-110実例 2026-07-23） |

---

## テンプレ（次回サムネ系プロンプト着手時の最小実装）

```
Photorealistic cinematic close-up portrait shot, framed from chest up.
Extremely attractive handsome [年代] Japanese [属性], strikingly good-looking,
sharp jawline, high cheekbones, clear smooth skin, stylish short black hair
gently blown by mountain wind, deep expressive eyes,
mouth wide open laughing joyfully showing perfect white teeth, ecstatic exhilarated expression,
facing the camera, looking directly at the viewer, [危険無自覚 or 決意].
Wind gently blowing his hair and the collar of his [服]. He is wearing [服装].
Behind him, [暗い山岳背景] with dim filtered light, fog rising,
a faint shadowy silhouette of a massive brown bear barely visible deep in the misty background.
Dramatic warm lighting on the man's face, dark cold shadows behind.
Shallow depth of field, background slightly blurred.
No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

**Why:** 1要素ずつ後付け修正するとプロンプトが肥大化し不自然化する。最初から立山実例構造で書けば1回で済む

**How to apply:** サムネ系着手時に validate-thumbnail-prompt-checklist hook が走る → このファイルを Read → テンプレベースで作成
