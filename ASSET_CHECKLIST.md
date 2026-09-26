# 🎨 Yama_Story アセット制作チェックリスト（Phase 2 の単一索引）

> **画像プロンプト・Google Earth座標・編集指示を作る前に、このファイルを最初に読む。**
> 台本（ナレーション）側の索引は `SCRIPT_CHECKLIST.md`。**こちらはその続き＝Phase 2 専用。**
> 策定: 2026-08-19。理由は末尾「なぜ作ったか」。

---

## STEP 0. 着手前に読む順番（この順で通読する）

| 順 | ファイル | 何を得るか | 通読義務 |
|:-:|:--|:--|:-:|
| 1 | **本ファイル** | Phase2 の全ルールの俯瞰 | ✅ |
| 2 | **`Scripts/2025年東成瀬村クマ襲撃事件/Asset_Prompts_Full_人間チェック済み.md`** | **納品物の正本**＝AI生成版を本人が全部読んで直した実物（2026-08-25）。**書式・語彙・注記の有無はこれを写す** | ✅ |
| 3 | `Scripts/羅臼岳ヒグマ襲撃事件/Asset_Prompts_KI.md` | プロンプト本文（英文）の書き方リファレンス（692行・全行） | ✅ |
| 4 | `Scripts/羅臼岳ヒグマ襲撃事件/GoogleEarth指示書.md` | **座標・カメラ指定の書式リファレンス** | ✅ |
| 5 | `Structure_Rules.md` §5 | 素材カテゴリ・文字数ルール・禁止事項 | ✅ |
| 6 | `Generic_Person_Prompts.md` | 名無し人物のテンプレ（CHAR番号を振らない人） | 大量作成時 |
| 7 | `System_Tools/Visual_Style_Guide.md` | 画調の統一（カートゥン調／フォトリアル） | 大量作成時 |
| 8 | `Image_Correction_Log.md` の「未昇格」「据え置き」行 | 本人の修正指示と、直さない判断 | ★2026-09-14 |
| 補 | `Scripts/羅臼岳ヒグマ襲撃事件/Asset_Prompts_SHO.md` `_TEN_KETSU.md` | 10件以上作るときの追加リファレンス | 大型時 |
| 補 | `EDITING_RULES.md` | **編集側の実測基準**（カット平均7.04秒・静止画埋め18.9%/最長6.7秒）。素材数・尺の設計時に参照 | 枚数判断時 |

> ⚠️ **grep の部分参照だけで着手しない。** リファレンスは「形式」を写すために読む。
> 部分参照だと、書式・語彙・粒度が毎回ブレる＝品質が安定しない根本原因。
> フック `guard-yama-asset-reference.sh` が、3 と 4 を読まずに Asset_Prompts を書こうとするとブロックする。

---

## STEP 1. 前提（Phase 1 が終わっているか）

- [ ] ナレーションが**一文一行で確定**している（Phase1 承認済み）
- [ ] `SCRIPT_CHECKLIST.md` STEP5 の検証が全て Exit 0
- [ ] **Phase1 と Phase2 を同時に書かない**（構造ミスの原因。`Structure_Rules.md` §5「2フェーズ分離方式」）

---

## STEP 2. 割り振りの原則

- [ ] **1ナレーション = 1アセット**。孤立アセット禁止。2つ必要ならナレーションを2文に割る
- [ ] **ナレ → 制作メモ → ナレ → 制作メモ の交互配置**。ナレーション2行連続は禁止
- [ ] **素材タイプは文字数で決まる**（文字数が先、タイプが後）

| ナレーション | 選べる素材タイプ |
|:--|:--|
| ≤25字 | 全タイプ可（静止画／キャラアニメ／動画／Google Earth） |
| 26〜50字 | キャラアニメ／動画／Google Earth のみ（**静止画は不可**） |
| 51字以上 | **分割してから**タイプを決める |

- [ ] 連続静止画は2枚まで。AI静止画+Ken Burns が**2分以上連続しない**
- [ ] **Google Earthも連続2回まで**（3連続禁止。3つ目は動画/キャラアニメ等に差し替える） → 2026-08-20 東成瀬村でGE3連続を指摘され恒久ルール化。`validate_yama_prompts.py` チェック26が検査
- [ ] 1本で**4カテゴリ以上**使う（実写／キャラアニメ／Lovart背景／Google Earth／図解）
- [ ] 図解・テロップ演出を**起・承・転結の各パートに最低1箇所**（mass-produced 判定回避）
- [ ] AI動画（Google Flow）は**1本あたり最大60本**。基準は「動きが物語の核心」「静止画で不可能」「感情ピーク」の3つ
- [ ] **冒頭フックの最初のアセットは必ず [Lovart動画]**（テキスト演出・静止画・キャラアニメ不可。日付テロップは動画の上に重ねる） → `feedback_yama_intro_always_video`
- [ ] **末尾（追悼＋視聴御礼）のアセットも必ず [Lovart動画]**＝動画で始まり動画で終わる → `feedback_yama_ending_always_video`
      ※どちらも `validate_yama_prompts.py` チェック23が自動検査（2026-08-20 東成瀬村で冒頭テキスト・末尾静止画にした事故を仕組み化）

---

## STEP 3. プロンプトの書式（リファレンスの形を写す）

### 制作メモの型

```
【制作メモ】ASSET-0XX [Lovart動画]
シーン: （日本語で1〜2文。何が映るか）
```（プロンプト本文＝英語）```
→ 編集者指示: （テロップ・BGM・演出の指示）
```

- [ ] **キャラ画像（1:1）**: 背景透過・**全身（Full body）必須**・カートゥン調（太い輪郭線／フラットカラー／大きな瞳）
  - バストショット・上半身・クローズアップ・横顔バストは**禁止**
  - 背景描写・テキスト・吹き出し・ラベルの混入は**禁止**（フックが検出する）
- [ ] **背景画像（16:9）**: フォトリアル（RED camera風、ドキュメンタリー調）
- [ ] **人物には必ず `Japanese` を明記**（CHAR-XX 参照ありの場合は不要）
- [ ] 名前のない人物は `[Generic group]`。**CHAR-XX は台本で名前がある人物にのみ**振る
- [ ] **再利用は `(CHAR-XX 再利用)` をプロンプトの最先頭**に置く
- [ ] **複数キャラを1枚に入れるときは頭身を数字で書く**。`(CHAR-XX 再利用)` タグだけでは**頭身が引き継がれず、頭の小さいリアル体型で出る**（2026-08-28 実測。ハンター3人で発生）。基準画像に合わせて `a very large head about one third of the total height, a short compact torso and short stubby arms and legs, roughly three heads tall` ＋ `Do NOT draw them with realistic adult proportions — not four, five, six or seven heads tall, not slender, not elongated` を明記する
- [ ] **背景は同一ロケーションでマスター1枚→以降は再使用**（「ASSET-XXXの背景を再使用。ズーム位置・色調で画変わり」と書き、新規生成しない）。統合してよいのは場所・時間帯・演出が同じ場合のみ。人数・時刻・色調が画の意味になっているカットは統合しない → 2026-08-20 生成枚数削減のユーザー指示で恒久化
- [ ] **同一人物の服装は全ASSETで固定**（CHAR定義の服装色を、実写風プロンプト・遠景・シルエットにも同じ色で書く）。複数人が映るカットは**1人ずつ服装で書き分け**、「farm work clothes」等の一括表記で済ませない → 2026-08-20 倒れる4人が同じ服になった指摘の再発防止
- [ ] クマは**四足歩行**。`standing upright` `on two legs` 等は禁止（フックが検出する）
- [ ] **複数人が倒れている・集まっている場面は、配置を意図的に乱す**（姿勢・向き・相互距離を1人ずつ変える。うつ伏せ/横向き/仰向け/半身を混ぜ、小物の散乱も足す。整列した配置は不自然＝2026-08-20指摘）
- [ ] **キャラが操作する小道具（ハンドル・受話器・銃など）は同じカートゥーン調でキャラに持たせてよい**。ただし「Only the ~ as a prop, nothing else around him」を添えて背景要素（車内・部屋・地形）の混入は禁止のまま
- [ ] **血・負傷は「描写として書かない」／「打ち消しとしては必ず書く」**（2026-08-25 人間チェック版で確定。ここを混同して打ち消しが1件も入っていなかった）
      - ❌ 描写に使う: `dark red stains` + 倒れた人 + 襲撃 の組み合わせはポリシー拒否される（2026-08-20 実測）。染みは `dark reddish-brown patches staining the soil` 等の間接表現に留め、拒否されたら人物なしの染みプレートを別生成してCapCutで乗算合成、最後の手段は編集で手描き
      - ✅ 打ち消しに使う: **人物・クマ・襲撃・搬送・医療が写る全プロンプトの末尾に `No blood, no wounds, no gore.` を必ず入れる**
      - 🚫 `no injuries visible` という言い回しは使わない（本人が21件中19件を上の定型に書き換えた）。日本語の禁止事項欄も「負傷の描写」→**「負傷・血液の描写」**と血液を明記する
- [ ] Lovart動画には **Google Flow動画プロンプトを必ず併記**（件数が合わないとフックが警告）
- [ ] **[Lovart動画]の1ブロック目は「静止画」プロンプト**＝手順は 静止画を先に生成→Google Flowで動画化。1ブロック目に動きの記述（slowly / gliding / charging toward / 5 seconds 等）を書かない。**凍結した1コマ**（frozen mid-stride / suspended / captured 等）として描き、動き・カメラワークはFlowプロンプト側だけに書く
      → 2026-08-20 東成瀬村で静止画ブロックに動画用の文を書いた事故の再発防止。`validate_yama_prompts.py` チェック25が検査
- [ ] フリー素材（Pexels/Unsplash等）の使用は**禁止**

### 書くときに必ず入れる定型（2026-08-21 追加・lintに頼らず最初から書く）

| 状況 | プロンプトに必ず入れる |
|:--|:--|
| **屋外の背景プロンプト全部** | **季節を必ず1語書く**（`in late October` 等）。`cold` `grey` `overcast` `pre-dawn` `first light` 系の光だけ書いて季節を書かないと**雪景色になる**（2026-08-28 実測: 秋田の路上が冬に化けた）。lint 14 が自動検査 |
| **秋のシーン全部**（late October/autumn を書いたら） | `No snow anywhere, no frost, no winter.` ／ 山間部・曇天・夜明けは特に雪化しやすい。落ち葉・紅葉の残り・刈り取った田など**秋の物証**も1つ足す |
| **暗いシーン**（pre-dawn / at night / dim / deep shadow / dark room 等） | `dark but NOT pure black — <主要素> stays clearly readable` ／ 黒いクマ＋暗所は最も潰れる |
| **実在の機関・施設**（大学・病院・省庁・市役所・消防・ドクターヘリ等） | `no real institution name, no crest, no emblem, no logo` ＋ **名称はテロップで出す**（AI生成で実在施設の偽映像を作らない） |
| **あるはずの物を消すと不自然になる場合** | **「消す」のでなく「読めなくする」**。看板・ナンバープレート・表札などは `present in their normal place, but small, slightly out of focus and not readable` と書く。`no signage` `no number plates` と書くと、ぽっかり空いた偽物くさい絵になる（2026-08-26 実測。診療所の看板・緊急車両のナンバーの2件で発生） |
| **実在の被害者・公人が関わる実写カット** | 顔を出さない構図にする（手元／肩越し／首から下／POV／後ろ姿）＋ `no face visible`。**カートゥンキャラには適用しない**（定石AC） |
| **日本語の文字を描かせるとき** | ラベルに **【chatGPT推奨】** を付ける（Lovartは日本語を崩す）＋ 描かせる文字は**1〜2個に限定**、残りは `too small to read` |
| **文字を出したくない画** | `No legible text, no signage, no nameplate anywhere` |
| **テロップを乗せる画** | 構図で余白を確保する（`the upper two-thirds is deliberately left as clean negative space for large text`）。指定しないと被写体が画面を埋める |
| **クマが走る／前進するカット** | `ON ALL FOURS` を明記（無いとlintがERROR）＋ `NOT standing upright, NOT on two legs` |
| **クマが出るカット全部** | **体長と体重を必ず書く**（無指定だと必ずグリズリー級に描かれる）＋ **凶暴さの語を3つ以上**。詳細は直下の「クマ専用ルール」 |

### 🐻 クマ専用ルール（2026-08-26 恒久化・lint 32/33 が自動検査）

> 毎回「凶暴さが足りない」「クマが大きすぎる」と差し戻されていた2点を仕組み化した。
> **指摘される前に、最初から入れる。**

**① サイズは必ず書く。種の標準を取り違えない**

生成AIはサイズ無指定だと**どんなクマもグリズリー級**に描く。体長と体重の両方を必ず明記する。

- **台本にその個体の実数値があれば、それを最優先で使う**（例: 東成瀬村＝体長1.2m・約80kgのメス／羅臼岳＝140cm・117kgのメス）
- 台本に無ければ**種の標準体格**を使う。**ツキノワグマとヒグマでは全く違う**ので必ず区別する

| 種 | 学名 | 体長の目安 | 体重の目安 |
|:--|:--|:--|:--|
| **ツキノワグマ** | Ursus thibetanus japonicus | 約110〜130cm | メス約40〜80kg ／ オス約60〜120kg |
| **ヒグマ（エゾヒグマ）** | Ursus arctos yesoensis | 約190〜230cm | メス約100〜200kg ／ オス約150〜400kg |

- 数値だけでは効かない。**比較対象を最低2つ**添える → `its shoulder no higher than an adult's waist` ／ `clearly much smaller than a grizzly or a brown bear` ／ `visibly small next to the wooden shed`
- ツキノワグマの骨格を固定する語も入れる → `rounded ears, a short blunt muzzle, a stocky but slender frame`

**② 凶暴さは毎回入れる — ただし実写／フォトリアルのカットだけ**

> ⚠️ **カートゥンは「牙・歯茎・唾液」までは盛らない**（絵柄と衝突して顔が崩れる）。ただし**何も書かないのは不可**（2026-08-28 修正）。
> カートゥンには**軽量セット**を使い、こちらから**3つ以上**入れる。lint 32 が実写・カートゥンそれぞれの基準で自動検査する。
>
> **カートゥン用の軽量セット**: `mouth wrenched wide open in a roaring snarl with the teeth clearly showing` ／ `ears flattened right back against the skull` ／ `the fur along its neck and shoulders bristled up into a raised ridge` ／ `head dropped low between bunched shoulders` ／ `claws spread` ／ `eyes narrowed and locked on` ／ 総括に `furious` `ferocious`
> ＋ 否定も添える → `It is NOT calm, NOT curious and NOT gentle — it reads as furious at a glance.`

実写カットでは下の語彙から**3つ以上**を必ず入れる。「ferocious」だけでは効かない。**部位ごとの具体描写**が効く。

| 部位 | 書く語 |
|:--|:--|
| 口・牙 | `jaws wrenched wide open in a savage snarl` `long curved canine fangs and the whole row of teeth completely bared` `black lips peeled back off pink gums` |
| 唾液 | `thick ropes of saliva flung from the jaws` |
| 鼻筋 | `muzzle creased into deep folds` |
| 目 | `small eyes narrowed to slits and fixed straight on the lens` `the whites showing at their edges` |
| 耳 | `ears pinned flat against the skull` |
| 毛 | `the fur along its neck, shoulders and spine bristled up into a raised ridge` |
| 筋肉・姿勢 | `head dropped low and driven forward between bunched shoulders` `heavy muscle bunched beneath the coat` |
| 爪 | `claws fully extended and hooked` `tearing up turf` |
| 総括 | `Ferocious, enraged, single-minded predatory fury.` |

**③ 例外 — 凶暴にしてはいけないカット**

一律に凶暴化すると演出が壊れる。次は**あえて凶暴にしない**（lint 32 も自動で除外する）。

- **採食・移動・生態説明**（ブナを食べる／山を歩く／豊作の年に増える母子グマ）
- **逃走・遠景・背面**（走り去る後ろ姿、遠くに小さく写る個体）
- **駆除後・箱わな・鎮静後**
- **「異様に静か」で怖がらせるカット** — 例: 高台に座って人間を見下ろす場面。**動かないことが恐怖の正体**なので、牙をむかせると台無しになる

**⑤ クマが死ぬカットは、この形で固定する**（2026-08-28 恒久化・lint 34 が自動検査）

> ⚠️ **仰向け（belly-up）は禁止。** 「腹を上にして脚が宙に浮く」は**人間の寝姿勢の記述**なので、生成AIが二足歩行の生き物として解釈し、肘をついて座った人のような絵になる（2026-08-28 実測）。

確定形は**うつ伏せ（PRONE）＋四肢を地面に伸ばす＋目はバツ印**。次をそのまま使う。

```
She lies PRONE, flat on her belly on the ground, exactly the way a four-legged animal drops:
her chest and stomach flat against the ground, all four legs splayed straight out limp and flat
on the ground around her — the two front legs stretched forward past her head, the two back legs
stretched out behind her — and her head down flat with her chin and muzzle resting on the ground.
Her mouth is a little open with her tongue just showing.
She is a four-legged animal throughout: NOT sitting, NOT sitting up, NOT reclining, NOT on her back,
NOT belly-up, NOT propped on an elbow, NOT posed like a person, and no leg is raised in the air.
Seen from a low three-quarter front angle so that her head and both X-mark eyes are clearly visible.
BOTH EYES ARE DRAWN AS SIMPLE BLACK X MARKS — two crossed straight lines for each eye.
Do NOT draw open eyes, do NOT draw closed eyelids, do NOT draw pupils or irises — each eye is an X mark and nothing else.
```

- **目のバツ印は必ず否定で固定する**。スタイルヘッダーに `large expressive eyes` が残っているので、書かないと普通の目になる
- **顔が見える角度を指定する**。うつ伏せを真横から描かれると顔が隠れてバツ目が意味を失う
- **傷を負っている個体なら、直前のカットと同じ位置・同じ大きさの痕を1か所だけ残す**（消すと別個体に見える）
- 胸の白い月の輪は「体の下に隠れる」と明記する。無理に見せようとすると体がねじれる

**④ 血の直接語は書かない**（既出ルールの再掲）

`blood` `bleeding` 等はポリシー拒否を招く。凶暴さは**牙・唾液・逆立った毛・筋肉・めくれた土**という被害描写を伴わない要素だけで作る。

### 🧾 プロンプト執筆の定石（2026-08-28 セッションで確定・修正をゼロに近づけるための蓄積）

> **書き直しになった原因をすべて一般化したもの。書く前にこの節を通す。**

**A. 向き・角度は「その角度でしか成立しない条件」で縛る**

「正面を向かせて」「横向きに」と書いても効かない。**幾何学的に1つの角度でしか満たせない条件**を足す。

| 欲しい向き | 効く書き方 |
|:--|:--|
| 正面 | `with BOTH SHOULDERS EQUALLY VISIBLE, shoulder lines parallel to the picture plane`（横向きでは片肩しか見えない） |
| 真横 | `THE WHOLE LENGTH OF THE RIFLE IS VISIBLE across the frame`（正面では前後に潰れる） |
| 真横の寝姿 | `his body lies horizontally across the frame from left to right`（真上からでは放射状になる） |
| 背面 | `only its back, rump and hind legs face the camera, its face is hidden` |
| 正面から迫る | `its chest and both shoulders squared to the camera` |

- **腕を横に伸ばす指示は体ごと回転させる。** 「手を横に出して」→ 体が横向きになる。**手のひらを胸の前でこちらに向ける**に置き換える
- 複数人の向きを揃えるときは `only their eye direction and head tilt may differ`（差は視線と首だけ）
- 否定も添える → `do NOT turn anyone side-on or three-quarter, do NOT twist a body away from the camera`
- **説明している人物は体と顔を視聴者へ向ける。** `BOTH SHOULDERS EQUALLY VISIBLE` で正面を固定する（戸沢村の本人チェック（2026-09-15）：研究所・応接間などの説明カットを正面向きへ修正）

**B. 表情は「極端に」振る。部位ごとに書き、望まない顔を否定で潰す**

> 🚦 **機械検査（lint54・2026-09-25）**: キャラのプロンプト（冒頭の CHAR 基準を含む）に `restrained expression` `neutral pose` `calm expression` 等があれば FAIL。眉・目・口・汗や涙のうち**2つ以上**を大げさに書いていなければ FAIL。せたな町は基準に restrained expression と書いたため、全キャラが無表情で差し戻しになった（本人「なんでずっと冷静な顔なの？」「喜怒哀楽を強調するってルールだよね？」）

> ⚠️ **迷ったら常に大げさな側へ倒す**（2026-08-28 ユーザー指定「極端にするのを意識してもいい。今だと表情のインパクトが弱い」）。
> カートゥン調は誇張して初めて等身大に見える。**控えめに書くと必ず無表情になる。**

`serious` `shocked` だけでは無難な標準顔になる。**眉・目・口・汗**の4点を必ず書き、さらに**振り切った語**を選ぶ。

| 弱い（使わない） | 極端（こちらを使う） |
|:--|:--|
| eyes wide | **eyes bulging almost out of the head, pupils shrunk to tiny dots** |
| mouth open | **mouth stretched wide open in a scream, every tooth showing, tongue visible** |
| eyebrows raised | **eyebrows shot up so hard the forehead is a mass of deep creases** |
| looks worried | **face drained bone white, jaw hanging slack** |
| sweating | **sweat flying off the face in visible droplets** |
| in pain | **eyes screwed shut into tight creases, teeth bared, tendons standing out on the neck** |

- **顔だけでなく体も振る** — のけぞる／膝が抜ける／物を取り落とす／片足が浮く
- **漫符（まんぷ）を足してよい** — 縦線の影／汗マーク／驚きの集中線的な効果は編集側で足す前提で、キャラは大げさな素の表情にする

- 真剣 → `eyebrows driven down hard and pulled together / eyes narrowed to a hard unblinking stare / mouth pressed into a flat grim line with the jaw muscles tight`
- 焦り → `eyebrows shot up and together / eyes stretched wide / mouth open, teeth showing / beads of sweat coming off the temple`
- **否定を並べる** → `not smiling, not startled, not frightened and not hesitant` ／ `NOT calm, NOT composed`
- 最後に**人物像を1文**добавить → `the concentrated face of a man doing something he has done for fifty years`
- **表情はナレーションの感情に合わせる。** 悲しい・真剣・焦り・険しいのどれかを顔の部位と姿勢で具体化する（戸沢村の本人チェック（2026-09-15）：説明人物の無表情を、場面に合う真剣・焦り顔へ修正）

**C. 人物の一貫性 — `(CHAR-XX 再利用)` が引き継がないもの**

参照タグは服と顔立ちを引き継ぐが、**次は引き継がない**。毎回書く。

- **頭身（3頭身・本人裁定 2026-09-25）** … `a very large head about one third of the total height, a short compact torso and short stubby arms and legs, roughly three heads tall` ＋ `Do NOT draw them with realistic adult proportions — not four, five, six or seven heads tall`
- **ひげ** … 高齢キャラは必ず `CLEAN-SHAVEN ... no beard, no moustache, no stubble`（白髪の老人を描くとAIはほぼ必ずひげを足す）
- **老いの見た目** … 年齢の数字だけでは若く出る。`deeply lined face, sunken cheeks, sagging skin at the jaw, sparse thin white hair, age spots` ＋ `NOT middle-aged`
- **身長** … 複数人は `All are the same height as one another apart from the one kneeling`
- **実在人物の若い頃** … 年齢・髪・服装を変えても、現在のCHAR参照と同じ顔立ちを維持する（戸沢村の本人チェック（2026-09-15）：若年時の実在人物を別人顔から同じ顔立ちへ修正）

**D. 背景の画角は3点セットで書く**

「引きで」「近めで」は効かない。**高さ・距離・地面の占有率**を数値で。

```
framed from adult eye height roughly 1.5 metres above the ground and about four metres back,
the camera angled only slightly downward: the ground occupies just the lower third of the frame,
... a clear horizon line visible. The middle of the frame is left as clear open space.
Not a ground-level shot, not a close-up, no macro texture, no worm's-eye angle.
```

- キャラを載せる背景は**中央を必ず空ける**
- 地面すれすれの背景は**キャラが小人に見える**。`Close ground-level view` は原則使わない（意図的な主観カットのみ）

**E. 生成拒否を避ける — 打ち消し文が逆効果になる**

- **`no injuries` `nothing graphic` を並べると、かえって「負傷を描く意図あり」の合図になる**（ASSET-059 実測）。**見えているものだけを書く**のが正解
- 暴力の事後を示す語を外す → `collapsed` `motionless` `torn` `gouged` `struggle` を `lying down on the ground` `dusty and rumpled` `pressed flat in patches` に置換
- 代わりに**時間の範囲を限定**する → `Captured at the moment of collision only, nothing beyond it.`
- **実写で人物を出すより「物だけ」を写す方が安全**（レントゲン、模型、車両、シート）。人物が要るなら手・前腕・後ろ姿だけ
- 拒否されたときの外す順番: ①牙・攻撃描写の一文 →②接触の示唆 →③人と対象を別生成して合成 →**④カートゥンに切り替え（実証済みの確実な逃げ道）**

**F. 失敗した形は「名指しで」禁止する**

抽象的な指示より、**実際に出た失敗の形をそのまま否定語にする**方が効く。

- 前脚が赤く塗られた → `do NOT draw red boots or red socks`
- 肘をついて座った → `NOT propped on an elbow`
- 仰向けが人間ポーズになった → `NOT belly-up, no leg is raised in the air`
- 銃を胸に抱えた → `do NOT draw the rifle hanging at his side or held flat across his chest`

**G. 自分がlintに引っかけがちな語（書く前に避ける）**

| 使ってはいけない語 | 引っかかる検査 | 言い換え |
|:--|:--|:--|
| `blood` `no blood` | 安全ワード | `nothing red and nothing stained` |
| `text` `no legible text` | 禁止ワード | `no lettering` `no readable characters` |
| `thrown` `throwing` `flung` | 投げる動作 | `pitched` `casting` `lifted` |
| `carrying` `holding` `standing` `person` `human` `official` | 背景プロンプト人物矛盾 | `with` `stands`→`sits on` 等／`no signage of any kind` |
| `room` `interior` `overhead` `landscape` | キャラプロンプト環境要素 | `nothing of the surroundings` `NOT looking straight down` |
| `hospital` `university` `police station` | 実在機関 | キャラ側では `patient's gown` 等に言い換え、打ち消しは背景側に書く |
| `diagram` `chart` `infographic` | 禁止ワード | 図解は**編集者指示**に書く（プロンプトには書かない） |

**H. 素材タイプは文字数で自動的に決まる — 先に数える**

- **26〜50字は静止画も図解も使えない。** 実写にするなら [Lovart動画] 一択で、動画枠を1本消費する
- 実写で静止画にしたいなら、**ナレーションが25字以下か先に確認する**

### 🧾 プロンプト執筆の定石（続き・2026-08-29〜30 セッションで確定）

> **前節A〜Hと同じく、実際に差し戻された原因を一般化したもの。lint 35〜39 が機械で見る。**

**I. 屋外は「季節」と「明るさの下限」を必ず書く（冬化・黒つぶれ）**

- 屋外プロンプトには**季節を1語**（`late spring` 等）＋ `No snow anywhere, no frost, no ice, no winter`。**夕暮れ・夜は特に冬に化ける**（lint 39）
- 暗いカットは `dim but NOT pure black — the <主要素> stays clearly readable` を必ず添える（lint 18/30）
- 背景を「無地」にしたいときも季節と場所を書く。書かないと**ただの灰色**になる（ASSET-203 実測）

**J. 群像は番号を振って1人ずつ書く（一般指示は効かない）**

- `every person is a distinct individual` `それぞれ個性を出して` は**まったく効かない**。全員同じ顔になる
- `Left to right: 1) ... 2) ... 3) ...` と番号を振り、**年齢・性別・体格・身長・髪・服・小物**を1人ずつ変える
- 加えて `NO TWO OF THEM SHARE A FACE, A HAIRSTYLE OR AN OUTFIT` `No two of them are the same height`（lint 36）

**K. 目・意識の状態はスタイル指定に負ける**

- スタイル定型の `large expressive eyes` が**閉じ目・バツ目を上書きする**。気絶・意識不明・死亡は `eyes closed` を明示する（lint 37）
- 意識がない人物は**服も乱す**（`clothes torn and dirty`）。きれいな服のままだと「気持ちよさそうに寝ている」画になる（実測で差し戻し）

**L. 「真剣」は怒りに化ける。穏やかな真剣は別の語で書く**

- `serious` に眉を下げる語（`eyebrows driven down` `furrowed`）を足すと**怒った顔・怖い顔**になる
- 穏やかな真剣＝`earnest and level, eyebrows relaxed with no furrow between them, eyes open at their normal width, mouth closed in a soft even line` ＋ `NOT grinning, NOT angry, NOT frightened, NOT grim`
- 前節Bの「極端に振る」は**驚き・恐怖・苦痛**に適用する。**説明・決意・見守りには適用しない**

**M. 幾何が難しいものは、条件を足すのではなく減らす**

- 檻・箱わな・扉のような**内と外がある構造**は、条件を足すほど壊れる（扉が檻から分離する／クマが金網を貫通する）。実測で3回連続失敗
- 直し方は2つだけ → ①**プロンプトを短くする**（520語→157語で解決）②**壊れる要素を画面の外に出す**（檻ごしをやめて檻の中だけを写す 等）
- **同じ型で2回失敗したら3回目を投げない。**型そのものを変える → `feedback_switch_method_after_two_failures.md`
- 物は「使われ方」が絵の中で成立しているか見る（箱わなは**山の中**・**扉が開いている**・**中に餌がある**。そうでないと罠に見えない）

**N. 種の描き分け・文字・編集の分担**

- **ツキノワグマは判別指定がないとヒグマになる** → `jet-black coat` `NO shoulder hump` `large round ears` `short blunt muzzle`（lint 38）
- **数字・見出し・「歴代最悪」等の文言は画像に描かせない。**画像は絵だけにして、文字はすべて編集で載せる（生成AIの日本語は必ず崩れる）
- **キャラプロンプトは1行で書く**。改行すると後段の検査が本文を読めない（背景・実写は分割画面の説明で改行してよい／lint 35）
- **同じ型のカットを繰り返さない。**記者会見・群像などは、2回目は人物・画角・役割のどれかを必ず変える

**O. 直したあとに必ず数える（編集事故の検出）**

- ブロックを正規表現で置換すると、**隣のナレーション行を巻き込んで消す**（実測1件）。編集のたびに
  `grep -c "^ナレーター:" <ファイル>` が**元の本数と一致**することを確認する
- 検査が「正しく書いてあるプロンプト」を落としたら、**検査側の打ち消しマッチのバグを疑う**（`NOT a close-up` が禁止語に当たる型。フックの二足歩行検査・validate_yama_prompts の全身検査で各1回発生）

**P. 実景・証拠を見せるカットは [Lovart動画]（実写）を優先する**

- 風景・空撮・大勢の集まり・県庁などの建物・証拠物は、キャラアニメーションで代用しない。実写素材がなければフォトリアルなLovart静止画を作り、Flowで動画化する
- 戸沢村の本人チェック（2026-09-15）では、ASSET-029・033・060・069・102・160・208・211/212・246・276・279・294をキャラアニメーションから [Lovart動画]（実写）へ修正

**Q. 背景はセリフが行われる場所そのものにする**

- 山道・書斎・研究所・応接間・役場・銃砲店など、ナレーションやセリフが示す場所を背景にする。別の場所の背景を、似た室内・屋外という理由だけで流用しない
- 戸沢村の本人チェック（2026-09-15）では、説明場面の背景使い回しを、実際の書斎・研究所・応接間などへ修正

**R. 同じ作品のクマは怖さと頭数をそろえる**

- 同一個体・同一作品では顔つき、体格、毛色、怖さの水準をそろえる。可愛すぎるクマは既存の怖い基準画像に合わせる
- 1カットに必要なクマは原則1頭。比較の意図がない2頭並べ・3頭並べは1頭へ減らす（戸沢村の本人チェック（2026-09-15））

### 🧾 プロンプト執筆の定石（続き・2026-09-13〜14 戸沢村の本人指摘20件＋機械検品23件から確定）

> **前節A〜Oと同じく、実際に差し戻された原因を一般化したもの。出典: `.codex/handoff/delegations/2026-09-13-tozawa-prompt-fixes.md` §A、同 `2026-09-14-tozawa-prompt-check.md`。**

**S. ナレーションの主題を「映さない」で逃げない（最重要／旧・定石P）**
- 遺体・捕獲したクマなど、ナレーションの主語をプロンプトから外すと、画像はプロンプト通りでも本人差し戻しになる（戸沢村 020・045・069）。機械検品もプロンプト準拠で見るため見逃す
- 主題はカートゥンで描く。遺体＝`pale bluish-white face, eyes closed, mouth slack, one arm at an unnatural angle, clothes badly torn, one boot missing` ＋ `clearly dead and NOT sleeping, NOT peaceful, NOT relaxed`。血は描かない（`No blood, no gore, no open wounds.`）
- 例外は「描くとポリシー拒否になる部位」（削ぎ落とされた筋肉など）だけ。そのときは**当事者の反応**（顔をそむける・上着をかける）で受け、編集者指示に「直接描写はしない」と書く（022・024）
- 生成前に自問: 「ナレーションの主語・主題は、プロンプトのどの文に描かれているか」。答えられない文は書き直す

**T. 群像の人数はナレーションと同数を番号付きで書く**
- ナレーションが「6人」なら 1)〜6) を年齢・体格・服・動作で全員列挙し、`exactly six, count them 1, 2, 3, 4, 5, 6` ＋ `Do NOT draw fewer than six` を添える。3人だけ書いて「他にも」は効かない（036 実測）
- 十数人以上は**前列を番号付き**で描き、後列は `partly hidden by the front row, only heads and shoulders show, drawn a little smaller` ＋ `roughly twenty people in all` ＋ `Do NOT draw only five people`（041）
- 2カット以上に出る無名人物は `[Generic group]` のままにせず **CHAR に登録**して `(CHAR-XX 再利用)` で呼ぶ（戸沢村 CHAR-15〜17）。同一性の崩れは機械検品で最多の項目

**U. ナレーションに出ない人物を足さない**
- 「許可を取る」の場面に窓口係を足す等、語られていない人物は描かない（050）。語られた人物だけを描き、状況は小道具（書類1枚）で示す

**V. 体格差は数値だけでは効かない。失敗の形を名指しで潰す**
- `140cm` と `150cm` を並べると片方が子グマに化ける（200 実測）。`a FULLY GROWN adult, NOT a cub, NOT a juvenile` ＋ `about nine-tenths of its length and height, the top of its back only a hand's width lower` ＋ `Do NOT draw the left bear as a tiny cub` のように、**比率・身近な物差し・否定**の3点で書く

**W. 「背後から襲われた」は真横から描く**
- 真後ろからだと人とクマが重なって伝わらない。真横（`side-on`）にし、人は前を向いたまま（`NOT turning around, NOT looking back`）、クマは後ろから飛びかかる（047）

**X. 地形図（Google Earth）は語る地点を同じ1画面に入れる**
- 高度が高すぎて座標1点だけだと緑一色になる（021・051・059）。集落と現場など**語る地点を全部入れる高度・向き**を書き、集落の屋根と田畑が見分けられる高度にする。遠い地点（役場など）を無理に入れて高度を上げない
- 書き出し: Google Earth Studio 1920×1080 以上・昼の順光・雲とかすみオフ・3D建物ON

**Y. 白い物が主役のキャラは透過で生成し、アルファを機械で確認する**
- 白い布・白い上着などは白背景だと輪郭が消える。`Transparent background, real alpha transparency` で生成し、生成後にアルファチャンネルの有無を検査する（市松模様を描き込んだ偽の透過を弾く）

**Z. 動画の長さはカットの尺以上にする／文字だけのカットは新規生成しない**
- 動画プロンプトの `5 seconds` がカット7.4秒より短いと途中で止まる（001）。尺以上（8秒）を書き、編集者指示に「足りなければ再生速度を落として尺いっぱい」と添える
- 同じ絵に文字を載せるだけのカットは「→ 画像再使用: NNN ＋ テロップ」の編集者指示にし、生成枠を消費しない（048・061・070）

**AA. 書式の事故＝閉じフェンスとラベルを同じ行に書かない**
- 「```背景プロンプト（16:9）:」のように閉じフェンスと次のラベルが同一行だと、validate_yama_prompts が背景本文をキャラプロンプトとして誤読し、誤警告（'at night'）を出す（022 実測）。フェンスは必ず単独行

**AB. [テキストのみ]（黒背景に白字）は日付・時刻の章切り替えだけ。追悼は必ず動画**（2026-09-25 せたな町の本人指摘7件＝177・190・192・195・205・209・219）
- 文字カードにしてよいのは「4月16日午前。」「正午」「2015年3月」のように、**ナレーションが日付・時刻だけの章切り替え**に限る（EDITING_RULES「時刻や日付のチャプター転換は黒画面＋白文字」）
- 説明・数値・結論・呼びかけの文（例: 「一匹のクマがかなりの距離を移動し〜」「現在のせたな町も〜呼びかけています」「体長は1.8メートル〜」）は、文字数ルールどおり静止画・キャラアニメ・動画・Google Earth で**画を作る**。数値は画の上にテロップで載せる
- **地名・位置関係を語る文（「内陸の今金町でした」「かなりの距離を移動し」など）は [Google Earth]**（195 本人指摘）
- **個体の体長・体重・年齢を語る文（「体長2メートル、体重230キロ」など）は実写（フォトリアル）のクマ画像＋数値テロップ**（192 本人指摘）
- **「ご冥福をお祈りします」の追悼カットは必ず [Lovart動画]**（戸沢村「末尾は必ずAI動画（恒久ルール）」・朱鞠内湖「★追悼（必ず動画）」）。現場の山や海の静かな風景に、文言をテロップで載せる
- **文字カードを2カット続けない**（190 本人指摘「なんでここは189と連続でテキストにしてるの？」）。日付カードの直後は必ず画
- 機械検査: validate_phase2_assets.py が、日付・時刻でないナレーションの [テキストのみ]、文字カードの連続、追悼文の非動画を ERROR にする

**AC. カートゥンキャラは顔を見せる・頭身は数字・背景は静止画**（2026-09-24 せたな町で有料生成後に全面差し戻し：全員後ろ向き／頭身の崩れ／キャラの背景が動画）
- **後ろ向きは理由のあるカットだけ。** 制作メモに `向き理由=走り去る` のように1行書く。理由があってもキャラカットの**2割まで**（本人裁定 2026-09-25「後ろ向きのシーンもあるので、後ろはNGだとおかしいのでは？」）
- 「実在の被害者は顔を出さない（後ろ姿）」は**実写カットのルール**。カートゥンキャラ（基準画像 CHAR-xx を含む）へ持ち込まない。せたな町の全員後ろ向きはこの持ち込みが原因
- **頭身は3頭身**（本人裁定 2026-09-25。旧4〜5頭身は廃止。ChatGPT経路の extract_prompts.py と同じ）。定石Cの定型句を毎回書き、`chibi` 等の別の体型語・別の頭身を混ぜない（せたな町は `slightly chibi` と `four-to-five-head` が同居）
- **背景**は透過キャラPNG＋人物なし（`No people`）の16:9静止画を別々に書く。動画を併記するなら編集者指示に「キャラ画の区間は開始画像を背景にする」
- 機械検査: validate_phase2_assets.py lint51〜53（check_prompts_all.py の合格票に含まれる）／Codex側 check_character_generation.py
- **一括生成の前に見本を本人に見せる。** 本人の承認前は、同じ .md から作れるのは素材の種類（キャラ基準・キャラ・背景・静止画・追加素材／動画）ごとに1件の見本だけ。全種類の見本がそろうまで承認できない（System_Tools/generation_gate.py が全生成スクリプトの中で止める）。本人が自分のターミナルで `python System_Tools/generation_gate.py approve <プロンプト.md> --kind image` を打つと全体を作れる。プロンプトは合格票の .md と全文一致したものしか生成に回らない
- **本人に渡す前にAI検品を通す。** ai_image_review.py（Sol→Astra）を今の画像で回し、「直す」を作り直してから check_handoff_folder.py を通す。未検品・「直す」残り・検品後のカット変更は T4 ERROR で止まる（regen.py の書き出しも同じ）

### 🧾 プロンプト執筆の定石（続き・2026-09-26 せたな町の本人指摘 約60件から確定）

**機械で止まるもの**（validate_phase2_assets.py の lint61〜63／imagegen/run.py）
- **実写のクマとキャラを組み合わせない**（lint61）。キャラのカットの背景は "No bear anywhere in the frame."。クマは CHAR-11 のキャラ（追加素材）で出す。写真・足跡・ビラの中のクマは対象外。
- **旧い汎用キャラの型を使わない**（lint62）。「The person reacts to or performs the action…」の型は年齢も顔も決まらず、若い人・後ろ姿・違う絵柄になる。
- **泣き顔は台本かシーン行に「泣く」があるときだけ**（lint63）。それ以外は困る・心配・神妙を眉と口で描き "NO tears, NOT crying"。
- **固定人物は基準画像（images/CHAR-NN.png）が無いと生成しない**（run.py が止める）。基準画像は文章だけで作らない。**いつもの絵柄で既に描けている同じ人物の画像を【絵柄の見本】として添えて作り**、既存の絵と並べて見比べてから使う（写実寄りの基準画像を添えると、その後の絵が全部崩れる）。
- **合格票の後にプロンプトを1字でも変えたら検査をやり直す**（gen_batch.sh は止まった理由を出して終わる）。止めた回の途中結果は次の回で拾わない（送信状態を片付けてから始める）。

**書くときの定石**
- 人物の**年齢を数字で**書く。中高年は "clearly middle-aged, NOT young"。場面の人（山菜採り・証言者）を若く描かない。
- **役割を取り違えない**: 依頼・提案するのは町の職員、引き受けるのが専門家。
- **時系列**: 駆除の後はクマを倒れた姿で。撤収・打ち切りは町へ帰る向きで。
- キャラを置く背景は**立った人の目の高さ**から奥まで見通す構図（地面の接写にしない）。山での捜索は**山の奥の森**。
- 看板・カレンダーなど**文字が主役の物は「」で文字を指定し、読める大きさ**で。
- 人とクマが絡む場面は、**人とクマを同じカートゥンの1枚**、または**別々のキャラ画像**＋クマのいない背景。
- 編集者指示で「キャラは既存の _char.png」と書く前に、**そのファイルがドライブに実在するか**確かめる（074・023・033・038・047・056・125 は無かった）。
- 作り直した素材は**ドライブの今の名前と同じ名前**で渡す。再利用は**番号の若い素材の名前**にそろえる。

**動画の定石**（lint64・65）
- クマ・人が出る動画は**頭数を書く**（"There is exactly one bear in the whole shot"）。奥に小さく写る静止画から「走り去る」動画を作らない（手前に2頭目が描き足される）。主体を手前に大きく置いた静止画から作る。
- 動画は**5秒**。5秒で収まる**ゆっくりした動き1つ**にし、"in real time, NOT sped up" と書く（8秒分の動きは早送りになる）。
- 出来上がった動画は**8コマ以上**で、主体の数・消えた人・速さを確かめる（3コマでは2頭目を見落とした）。

**資料を書き換えるときの定石**
- 差し込み位置を検索で決めたら、見つからなかったときに止める（見つからないまま差し込み、Fix5a が丸ごと二重になった。lint66 が同じ番号のブロック2つを止める）。

**検品の定石**
- 生成した画像は **Claude が全部目で見てから**フォルダにまとめ、チェックリスト（カットごとの本人指示と見る点）を付ける。
- 動画は**元の静止画を目で見て許可したものだけ**発注する（.imagegen/video_ok.txt）。

### 🛡️ 2026-09-26 せたな町の本人指摘 → 止める仕組みの対応表（指摘の型ごと。新しい指摘はこの表に行を足す）

| 本人の指摘（型） | 例 | 止める仕組み |
|:--|:--|:--|
| 若い人・作画が違う・後ろ姿 | 063・069・075・164・166・212 | lint62（旧い汎用キャラの型）・lint67（年齢なし）・run.py（固定人物の基準画像なしで止める）・【絵柄の見本】で基準画像を作る |
| 見本の基準画像がいつもの絵柄でない | CHAR-02〜10 | 基準画像は既存の同一人物画像を見本に添えて作る（make_queue_for_list.py の style_refs・run.py が添付）＋Claude が既存の絵と並べて目視 |
| 実写のクマとキャラの組み合わせ | 159・162・191・125 | lint61・precheck 4-⑤ |
| 理由のない泣き顔 | 019・168 | lint63・precheck 4-④ |
| 役割の取り違え・時系列・向き | 181・191・192・198 | precheck 4-②③（ナレーションと絵の食い違いを判定） |
| キャラ画像がない・参照ファイルが無い | 074・168 | check_editor_refs.py（build_latest_docs.py が毎回実行） |
| 動画のクマが2頭 | 082 | lint64・主体を手前に大きく置いた静止画から作る・8コマ以上で目視 |
| 動画が早送り | 198 | lint65（6秒以上の動きを止める） |
| 合格後の書き換え・二重の資料 | Fix5a | generation_gate（全文一致）・gen_batch.sh が止まった理由を出す・lint66（同じ番号のブロック2つ） |
| 素材名が前と違う | 全体 | make_generation_list.py がドライブの今の名前で作る（後のファイルで上書きしたカットは数えない） |
| 検品が甘い | 全体 | 画像は Claude が全部目視してからフォルダへ・動画は静止画の目視許可後に発注（video_ok.txt）・チェックリスト自動作成（make_fix_folder.py） |

機械で止められないもの（看板の文字の大きさ、ポーズの自然さ、背景の撮る高さ）は、Claude の目視とチェックリストの「要確認」欄で拾う。

### タイプの決め方（機械が判定できる部分は数える）

> 🔧 **2026-09-04: 2つの検査で数え方が食い違っていたのを揃えた。** `validate_yama_prompts.py` だけが句読点を含めて数えており、
> 同じ台本で `validate_phase2_assets.py` と結果が割れていた（戸沢村で11件）。規則の正本は本節の「句読点・記号を除く」。
> あわせて台本突合が推測の太字（`**…**`）を落とさず比べていたのも直した（納品物は Markdown 装飾を使わない規則なので、必ず欠落に見えていた）。
> selftest ㉞ / ㉟

- [ ] **ナレーション文字数を先に数える**（句読点・記号を除く）→ 25字以下=全タイプ／26〜50字=**静止画不可**／51字以上=**分割してからタイプを決める**
- [ ] **同じタイプを続けない**: キャラアニメ**3回まで**（4回目で実写かGoogle Earthを挟む）／静止画**2枚まで**／Google Earth**2回まで**
- [ ] **AI動画（Google Flow）は1本あたり60本まで**。使う基準は「動きが物語の核心」「静止画で不可能」「感情ピーク」の3つ
- [ ] 迷ったら `python System_Tools/validate_phase2_assets.py --prompts <ファイル>` を走らせる。**上の項目は全部この検査が数えてくれる**（rule 23-31）

---

## STEP 3.5. 納品形式（2026-08-25 新設・人間チェック済み版から逆算）

> 根拠: `Scripts/2025年東成瀬村クマ襲撃事件/Asset_Prompts_Full_人間チェック済み.md`
> AI生成286アセットのうち **184件は無修正で通り、89件が直され、13件が丸ごと消された**。
> 直された89件の中身は、プロンプトの英文そのものより **「納品物の作り方」の問題** が大半だった。
> 検査: `python3 System_Tools/validate_asset_deliverable.py <Asset_Prompts_Full.md>`

### 大原則：納品物は「仕様書」ではなく「作業指示書」

AIは自分向けの仕様書を書き、本人はそれを作業指示書に直していた。最初から作業指示書として書く。

| 納品物に**書く**もの | 納品物から**外す**もの（→ `_制作ノート.md` に分ける） |
|:--|:--|
| ナレーション1行 | 「→ **設計の理由**: …」 |
| 【制作メモ】ASSET-XXX [タイプ] 台本LXXX | 「→ **⚠ 確認事項**: …」 |
| シーン:（日本語1〜2文） | 「⚠ 生成後に必ず目視確認: …」 |
| プロンプト本文（英語） | 「→ **数値の出典**: …」 |
| → 編集者指示:（テロップ・BGM・尺） | 「新規生成しない／ズーム位置・トリミング・色調補正で画変わりを付ける」の長文説明 |

- [ ] **Markdown装飾を使わない**（`**強調**` `### 見出し` `` `バッククォート` ` ```コードフェンス``` `）
      → 納品物はGoogleドキュメントに貼って使う。記号がそのまま画面に出る。本人は114箇所の `**` を42まで削った
- [ ] **PART見出し・カテゴリ別サマリー表・動画予算表は納品物に入れない**（本人は全部削除した）
- [ ] **アセット相互参照は番号だけ**（`ASSET-090のキャラ画像` → `090の`／`ASSET-088と重複` → `088と重複`）
- [ ] **[Lovart動画] の2ブロックには必ずラベルを付ける**
      1ブロック目 → `静止画プロンプト（16:9・フォトリアル）:` ／ 2ブロック目 → `Google Flow動画プロンプト:`
      ※ラベル無しの ``` フェンス2連は、操作者がどちらをどこに貼るか読み違える

### 血・負傷の語彙（STEP3と同じ。ここが最多の書き換え箇所）

- [ ] `no injuries visible` → **`No blood, no wounds, no gore.`** に統一（本人が21件→2件まで書き換えた）
- [ ] 日本語の禁止事項欄も「負傷の描写」→**「負傷・血液の描写」**

### 実在の人物を、AIで再現しない

- [ ] **`[実写]` のうち「実在個人が写る／話している映像」には、AIフォールバックを付けない**（本人は10件すべて削除）
      - ❌ 付けない: 目撃者インタビュー／ハンター証言のインタビュー画／研究者の出演画／村長・知事の公式ポートレート／防犯カメラ映像／報道ヘリの中継画
      - ⭕ 付けてよい: 物・風景・動物・手元・現場のカット（爪のクローズアップ、電気柵、箱わな、読影室 等）
      - 理由: 実在個人の発言・肖像・報道映像をAIで作ると、素材が入手できなかったとき **偽の報道映像が納品物に混ざる**

### 生成しないで済ませる（本人は13件の生成枠を消し、15箇所を再利用・テキストに変えた）

> ⚠️ **STEP2の「1ナレーション=1アセット」は崩さない。** 人間チェック済み版でも281ナレ行すべてに指示が付いている。
> 消すのは*生成*であって*枠*ではない。枠は「→ アセットXXXを再利用」「→ 黒背景に白テキスト」で埋める。

- [ ] **抽象・転換・見出しベースのカットは新規生成しない。** 次の3手で置き換える
      1. `→ アセット116を再利用。` / `→ アセット233のまま、色を白黒に変更。` / `→ アセット214と215を画面半分にわけて再利用。`
      2. `→ ここは黒背景に白テキスト。「悲惨な現実」と表示。悲惨は赤字。`（**強調語だけ赤字**が本人の型）
      3. `→ ここはlive映像の画像を使用予定。生成不要。`
- [ ] 特に次のシーン文を書いたら、生成せずに上の3手を先に検討する
      「〜のベース」「転換カット」「〜の再掲」「見出しベース」「回想」「考え込む」「切り出す」「色調が急変」「キャスター風の語り手」
- [ ] **背景の色調違いだけの派生カットは作らない**（元アセット＋「色を白黒に」で足りる）

### Phase1の宿題をPhase2に持ち込まない

- [ ] 「出典が確認できないため出さない」「未検証」「地図を実測して数字が変わったら台本を直す」等の申し送りを納品物に書かない
      → 未確定の数字は **Phase1（台本）側で決着させてから** Phase2に入る
- [ ] **`キャラプロンプト（1:1）` があるカットには必ず短い標準語の `→セリフ「…」`（黙る場面は「・・・」、クマは鳴き声、心の声は `心の声の吹き出しで「…」`）を付け、キャラプロンプトのないカットには付けない**（本人裁定 2026-09-15。型 → `.claude/skills/yama-asset-prompt/references/セリフと画面文字の型.md`）

### デスクトップへ渡す前の検査（2026-09-15 戸沢村で追加）

> 戸沢村の追加素材で、白背景のままのキャラ画像・図解を15枚渡し、本人が1枚ずつ指摘した。チェックリストの説明が実物と違う（203）、フォルダに画像が入っていない（243）も同じ回に起きた。

- [ ] **キャラ画像と、背景に重ねる図解は、必ず背景透過にしてから置く**（Codex の image_gen で "White background" と書くと白背景のまま出る。外周からつながった白だけを抜き、目や白い服は残す）
- [ ] **チェックリストの「見てほしい所」は、置いた最終版の画像を開いて見てから書く**（作り直したら行も書き直す。前の版の説明を残さない）
- [ ] **直した分をもう一度見てもらうときは、直したファイルだけを別フォルダ（`<作品>_作り直し画像_<日付>/`）にコピーし、そのフォルダ専用のチェックリストを入れる**
- [ ] 渡す前に次を実行し、exit 0 にしてから、一覧の jpg を目で見る
      `../System_Tools/kindle/.venv/bin/python System_Tools/imagegen/check_handoff_folder.py ~/Desktop/<フォルダ> --sheet check/handoff_sheet.jpg`
- [ ] **画像の中身は `System_Tools/imagegen/IMAGE_CHECK.md` の項目（A〜F）で確認してから渡す**（Sol が全カットを見て、挙がったカットだけ Astra が詳しく見る）

---

## STEP 4. Google Earth・座標の作り方

**座標の正本は `Scripts/羅臼岳ヒグマ襲撃事件/GoogleEarth指示書.md` の形式。**
台本フォルダに `GoogleEarth指示書.md` を1枚作り、カットごとに次を書く。

```markdown
## カット① 「（対応するナレーション）」

- 検索座標: `44.0930, 145.1060`
- カメラ高度: 5,000〜8,000m
- カメラ角度: 斜め45°、3D地形ON
- 向き: 北西→南東（登山口が手前、山頂が奥）
- 地点A（名称）: `44.1098, 145.0904`（標高230m）
- 地点B（名称）: `44.0758, 145.1222`（標高1,661m）
- 演出: A→Bを赤いラインで結ぶ／ラベル／フライスルー
```

- [ ] **十進法（decimal degrees）で書く**。`44.0930, 145.1060` 形式
      → Google Earth の検索窓にそのまま貼れる。**度分秒（44°04'33"N）は編集者が変換する手間になるので使わない**
      （古い `Asset_Prompts_KI.md` 本文には度分秒が残っているが、指示書側の十進が正）
- [ ] **座標は検証したものだけ書く。** 推定値には `約` を付ける
      → `feedback_no_unverified_coordinates.md`（未検証の座標・標高・距離を書かない）
- [ ] 地点には**必ず標高**を添える（高さの対比が地形図演出の核心）
- [ ] カメラ高度・角度・向きの3点を必ず指定する。**「上空から」だけでは編集者が再現できない**
- [ ] 事件現場は**赤ピン＋ラベル**、ルートは**赤いライン**で統一

---

## STEP 5. 検証（Exit 0 まで出さない）

```bash
python3 System_Tools/validate_phase2_assets.py --prompts <Asset_Prompts.md>
python3 System_Tools/validate_yama_prompts.py  <Asset_Prompts.md>
python3 System_Tools/validate_asset_deliverable.py <Asset_Prompts_Full.md>   # ← 2026-08-25 追加・納品形式
python3 System_Tools/imagegen/precheck_subjects.py <Asset_Prompts.md>   ★2026-09-14新設: ナレーションの主題がプロンプトに描かれているか（FAIL と missing を人が読み、描き直すか据え置くかを決めてから生成する。自動では止めない）
```
**🚦 2026-09-25 から入口は1本**: `python System_Tools/check_prompts_all.py <md>`（上の lint・validate_yama_prompts・precheck_subjects・TODO grep をまとめて走らせる）。失敗0・警告0のときだけ合格票が出て、**票が無いと生成（ChatGPT・fal・Flow のブラウザ操作、生成スクリプト）が関所フックで止まる**。作り直し分だけの抜粋は `--excerpt`、判断で受け入れる警告は `--accept "ASSET-NNN:キー:理由"`（票に残る）。報告は「総合判定」の行をそのまま貼る。precheck の FAIL も、描き直すか `--accept` に理由を書くまで生成できない（せたな町で必読未読・検査1本・警告無視のまま生成しかけた事故の再発防止）
物差しは「ナレーションで言っていることが画面に見えるか」の1本。反応・痕跡・書類・風景で主題を代替していたら FAIL（定石P）
戸沢村で 022・074・125（遺体の傷を描かず後ろ姿＋編集の赤丸）等12カットが本人差し戻しになった事故の再発防止

`validate_asset_deliverable.py` は **人間チェック済み版の実測残存率が合格ライン**（H1〜H7）。
AI生成版はこの検査で8項目全部が超過した＝それが手直しの中身だった。
→ `feedback_calibrate_audits_to_shipped_content.md`（出荷済みの内容が通る値に較正する）

`validate_phase2_assets.py` が自動検出するもの:

| 分類 | 検出項目 |
|:--|:--|
| 生成失敗（14-22） | **冬化（季節未指定＋寒色の光）**／クマ不在／二足歩行／グラフ動画／黒画面／方向あいまい／日本語本文の混入／日本人指定なし／複数人のクローン化 |
| **構成バランス（23-25）** | **キャラアニメ4回以上連続**／**静止画3枚以上連続＝ERROR**／**Google Earth 3回以上連続** |
| **文字数整合（26）** | **51字以上（要分割）**／**26〜50字なのに静止画** ※句読点・記号を除いて数える |
| **予算（27-28）** | **Google Flow動画が60本超**／**素材カテゴリが4種類未満**（50アセット以上のファイルのみ判定） |
| **プロンプト安全（29-31）** | **秋指定なのに `no snow` なし**／**暗いシーンに `NOT pure black` なし**／**実在機関名に打ち消し指定なし** |
| **クマ（32-34）** | **襲撃・威嚇カットに凶暴さの語が3つ未満**（実写は重い基準、カートゥンは軽量セット）／**クマにサイズ指定なし**／**ツキノワグマなのにヒグマ級の体格**／**死亡カットがうつ伏せ＋バツ目になっていない** |
| **書き分け・状態（35-39）** | **キャラプロンプトが複数行＝ERROR**／**複数人が番号付きで書き分けられていない**／**気絶・意識不明に `eyes closed` なし**／**ツキノワグマの判別指定なし（jet-black・no shoulder hump）**／**夕暮れ・夜の屋外に季節も `no snow` もなし** |
| **本人チェックの定番（40・42-44はWARN、41はERROR）** | **セリフの方言語尾**／**キャラプロンプトがあるのにセリフなし**／**14字超のテロップ**／**読点で割ったナレーション**／**テロップ抑制指示** |
| **画像チェック項目（lint 45-50・WARN）** | **単数の話に複数を描かせている**／**向きの指定なし**／**時間帯の指定なし**／**時代の指定なし（2000年より前の事件）**／**テロップ余白の指定なし**／**図解を編集任せ** |

> 45-50は2026-09-16追加（`System_Tools/imagegen/IMAGE_CHECK.md` のうち、プロンプトの文字で見分けられる項目を生成前に止める）。
> 40-44は2026-09-15追加（戸沢村の本人チェック125か所から抽出）。41は本人裁定によりERRORで終了コードへ反映し、40・42・43・44はWARNのままとする。
> 35-39は2026-08-30追加（同じ差し戻しが繰り返された5種。ルール本文はSTEP3「定石 I〜O」）。
> 32-33は2026-08-26追加（クマの凶暴さ不足・サイズ過大が毎回差し戻されていたため）。23-31は2026-08-21追加。東成瀬村セッションで人手で数えていた項目を機械化したもの。
> **AI動画の上限は60本**（2026-08-21にユーザー指定で12→20→40→60へ変更（2026-08-28））。
> 根拠は実測: 朱鞠内湖96本(全242アセット中40%)／星野道夫20本(227中9%)／羅臼岳16本(151中11%)。
> 旧12本は**実際に作られたどの台本とも一致していなかった**（守られていないルールが文書に残っていた）。

- [ ] **納品物は必ず1本の結合版 `Asset_Prompts_Full.md` を生成する**（作業はPART単位で分割してよいが、ユーザーに渡す完成資料は1ファイル。分割版を編集したらFullを再生成して同期）
      → 2026-08-20 東成瀬村で3分割のまま完了報告し「全てがまとまった資料はどこ？」となった事故の再発防止。結合はKI→SHO→TEN_KETSUの順で連結し、結合版にも `validate_yama_prompts.py <Full> <Master.md>` の台本突合を通すこと
- [ ] **完了報告前 grep が0件**
      `grep -nE "（要設定）|要設定|TBD|仮置き|後で埋める|TODO" <ファイル>`
- [ ] 🚨 **編集のたびに `grep -c "^ナレーター:" <ファイル>` が元の本数と一致することを確認**（ブロック置換で隣のナレ行を巻き込んで消す事故が実測1件）
- [ ] PostToolUse フック `validate-asset-prompts.sh` の ❌ が0件（背景混入／テキスト混入／二足歩行／Japanese欠落）
- [ ] **視覚確認するまで「完了」と言わない** → `feedback_no_false_completion_claims.md`
- [ ] 🚨 **直したプロンプトは、必ず本文をチャットに貼る**（2026-08-27 本人指示「毎回この指示をしている」）
      指示されなくても貼る。要約・箇条書きの説明で済ませない。
      **貼るもの**: キャラプロンプト（1:1）／背景プロンプト（16:9）／Google Flow動画プロンプト の本文を、
      そのままコピペできる形で。複数件なら全件（一部省略しない）。
      理由＝本人はそれを Lovart / Google Flow に貼って生成する。貼れない形では作業にならない
      → `feedback_yama_script_changes_show_in_chat.md`

---

## 画像修正の学習ループ（2026-09-14 本人指示）
- 本人が画像の修正を指示したら、Claude はその場で `Image_Correction_Log.md` に原文で記録し、同じセッションで一般化ルールをこの索引の定石へ昇格する
- 「そのままでいい」も記録する（据え置き）。次作で同じ点を過剰に直さない
- 機械で見られるものは validate_phase2_assets.py / precheck_subjects.py に足す候補として台帳に書き、まとめて実装を委任する

## STEP 6. 最小手数の自問（提案前に1行で明示する）

> 「1枚で済むか？ 1キャラで済むか？ 1プロンプトで済むか？ 1テロップで済むか？ 編集者の実装コストは？」

- [ ] 個別要望を勝手に全体ルール化しない。リファレンスに無い指示は「このシーンのみ／今後全体」を確認する

---

## なぜ作ったか

台本側には `SCRIPT_CHECKLIST.md` という単一索引があったのに、**Phase2 には無かった**。
そのため毎回ちがうファイルを部分的に読んで着手し、書式・粒度・座標の精度が回ごとにブレていた。
2026-08-19、台本側で「索引を読まずに自分で選んだ資料だけで書き始める」事故が起きたのと同じ構造。

**この索引と、STEP0 の通読義務（フックで強制）が、Phase2 の品質を毎回同じ水準に固定するための仕組み。**
