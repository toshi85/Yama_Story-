---
name: Yama サムネプロンプト 標準テンプレ
description: 2026-05-24 大千軒岳サムネで採用された「立山実例ベース・背景クマなし・イケメン強化（V字小顔/二重/8頭身/モデル俳優職業）」のシンプル構造を全Yamaサムネの標準テンプレとして固定。
type: reference
---

# Yama サムネプロンプト 標準テンプレ（2026-05-24 確定・イケメン強化版）

## 採用経緯
- 2026-05-24 大千軒岳サムネで以下の試行錯誤後に確定:
  1. 強調語三重掛け+motion blur過剰+背景ヒグマlunging → CG感・不自然でNG
  2. 立山実例レベルのシンプル＋背景ヒグマなし → 構造はOKだがイケメン度不足
  3. **シンプル構造＋イケメン具体要素（V字小顔/二重/高鼻筋/8頭身/モデル俳優職業）→ ユーザー採用** ✅
- 以降の全Yamaサムネで本テンプレを最初の1回目から使う（後付け強化禁止）

## 構造ルール（5ブロック）
1. **冒頭**: `Photorealistic cinematic close-up portrait shot, framed from chest up.`
2. **人物属性ブロック**: 「fashion model + drama lead actor」職業＋V字小顔/二重/高鼻筋/8頭身など顔骨格＋髪
3. **表情/視線ブロック**: 口大開け笑い＋カメラ目線＋危険無自覚/決意
4. **服装+風（自然な動き）ブロック**
5. **背景ブロック**: 暗い山岳風景＋不穏な空（ヒグマ等の動物シルエット**は入れない・ユーザー指示時のみ追加**）＋末尾規格

## A案テンプレ（若い人物・例: 北大生22歳）

```
Photorealistic cinematic close-up portrait shot, framed from chest up. A Japanese male fashion model in his [年代] ([年齢]歳) with the looks of a Japanese drama heart-throb lead actor, strikingly handsome with clean-cut idol-level features. Small V-shaped face, sharp slim defined jawline tapering to a pointed slim chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid almond-shaped eyes with long thick eyelashes, well-shaped full lips, porcelain-smooth flawless fair skin without a single blemish, glossy thick perfectly styled short black hair with natural side sweep gently blown by mountain wind. Lean tall model build with elegant 8-head body proportions. Mouth wide open laughing joyfully showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, [危険無自覚 or 決意]. Wind gently blowing his hair and the collar of his [服色] [服種]. He is wearing [服装具体: 色+ジャケット+シャツ+ザックストラップ等]. Behind him, the dark moody [季節] forest of [山名] in [地域] with dim filtered light through dense [樹種] trees, fog rising between the trunks, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Dramatic warm lighting on his face like a fashion magazine cover, [季節] earth tones glowing warmly, dark cold shadows behind. Shallow depth of field, background slightly blurred. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

## B案テンプレ（中年人物・例: 消防士41歳）

```
Photorealistic cinematic close-up portrait shot, framed from chest up. A Japanese male fashion model in his [年代] ([年齢]歳) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with rugged refined mature features. Sharp strong defined V-shaped jawline tapering to a firm pointed chin, high prominent commanding cheekbones, very high straight strong nose bridge, deep-set double-eyelid intense piercing dark eyes with steady gaze, well-shaped full lips, smooth handsome tan skin with mature masculine appeal, glossy perfectly styled short black hair gently blown by mountain wind. Tall broad-shouldered muscular powerful model build, commanding heroic presence like an action movie protagonist. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, calm and unafraid. Wind gently blowing his hair and the collar of his [服種]. He is wearing [服装具体]. Behind him, [暗い山岳風景具体] with dim filtered light, the sky above heavy and overcast with rolling grey clouds. Dramatic warm lighting on his face like a fashion magazine cover, dark cold shadows behind. Shallow depth of field, background slightly blurred. No text, no words, no letters, no logos, no specific agency name. 16:9 aspect ratio. Generate 5 images.
```

## 必須要素チェック（7項目・最初の1回目から全部入れる）

| # | 要素 | 標準表現 |
|---|---|---|
| 1 | **職業ベース容姿**（2職業重ねOK） | `Japanese male fashion model with the looks of a Japanese drama heart-throb lead actor` / `Japanese male fashion model with the looks of a Japanese prime-time drama leading-man actor` |
| 2 | **顔骨格**（V字小顔・二重・高鼻筋・8頭身） | `Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid almond-shaped eyes with long thick eyelashes, lean tall model build with elegant 8-head body proportions` |
| 3 | **肌**（年齢別） | A: `porcelain-smooth flawless fair skin without a single blemish` / B: `smooth handsome tan skin with mature masculine appeal` |
| 4 | **カメラ目線** | `facing the camera, looking directly at the viewer` |
| 5 | **口大開け笑い** | `mouth wide open laughing joyfully showing perfect white teeth, ecstatic exhilarated expression` |
| 6 | **自然な動き** | `hair gently blown by mountain wind. Wind gently blowing his hair and the collar` |
| 7 | **暗い山岳背景＋不穏な空** | `dark moody [季節] forest ... fog rising ... sky heavy and overcast with rolling grey clouds` |
| 8 | **ライティング** | `Dramatic warm lighting on his face like a fashion magazine cover, dark cold shadows behind` |

## 禁止表現（不自然化・NG生成の原因）

| 禁止 | 理由 |
|---|---|
| `The most extraordinarily breathtakingly attractive` 三重強調 | CG感・不自然 |
| 3職業以上重ね（`magazine cover model + drama lead + K-pop idol + 俳優`） | 顔が混乱。**2職業まで（fashion model + drama actor）はOK** |
| 落ち葉mid-air + 霧渦巻き + ストラップ揺れ + motion blur の複数同時併用 | 人物がブレる |
| 背景ヒグマlunging + mouth wide open + motion blur | 人物を食う。**デフォルトはクマシルエット自体入れない** |
| `eyes tightly squinted shut` / `closed eyes from laughter` | 目線ルール違反（カメラ目線必須） |
| 大文字強調（`MOUTH WIDE OPEN`, `EYE CONTACT (must hold)`） | 文体不統一・不自然 |
| `do NOT squint, do NOT look away` 否定形強調 | プロンプト肥大化・効果薄い |
| 顔パーツの過剰列挙（眼窩・瞳孔・首・歯の内側・舌） | プロンプト肥大化・効果なし |

## 背景にヒグマシルエットを入れる判断

- **デフォルト: 入れない**（立山実例方式・暗い空のみで脅威を暗示）
- **入れる場合**: ユーザーが明示的に「ヒグマシルエット入れて」と指示した時のみ
  - 表現: `a faint shadowy silhouette of a massive Hokkaido brown bear barely visible deep in the misty background`
  - `lunging forward aggressively` 等の動的表現は禁止（人物を食う）

## フォント仕様（Photopea配置時）

| パーツ | 旧仕様（実例運用中・Hiragino系） | 新仕様（プロデザイン・LightNovelPOPv2系） |
|---|---|---|
| 上部（慢心セリフ） | Hiragino Mincho Pro W3 | LightNovelPOPv2 |
| 下部（衝撃オチ） | Source Han Sans Heavy | Source Han Sans JP Heavy |
| フッター | Hiragino Mincho Pro Medium | Source Han Sans JP Medium |

カギカッコ: 上部セリフに「」付き / 下部オチはなし / 1行表示・改行禁止

## 完成例（2026-05-24 大千軒岳・採用版）

### A案（北大生・屋名池さん想定）
```
Photorealistic cinematic close-up portrait shot, framed from chest up. A Japanese male fashion model in his early 20s (22 years old) with the looks of a Japanese drama heart-throb lead actor, strikingly handsome with clean-cut idol-level features. Small V-shaped face, sharp slim defined jawline tapering to a pointed slim chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid almond-shaped eyes with long thick eyelashes, well-shaped full lips, porcelain-smooth flawless fair skin without a single blemish, glossy thick perfectly styled short black hair with natural side sweep gently blown by mountain wind. Lean tall model build with elegant 8-head body proportions. Mouth wide open laughing joyfully showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his beige hiking jacket. He is wearing a beige modern hiking jacket, dark green hiking shirt visible at the collar, with a navy daypack strap on his left shoulder. Behind him, the dark moody autumn forest of Mount Daisengen in Hokkaido with dim filtered light through dense cedar and birch trees, fog rising between the trunks, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Dramatic warm lighting on his face like a fashion magazine cover, autumn earth tones glowing warmly, dark cold shadows behind. Shallow depth of field, background slightly blurred. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

### B案（消防士・大原さん想定）
```
Photorealistic cinematic close-up portrait shot, framed from chest up. A Japanese male fashion model in his early 40s (41 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with rugged refined mature features. Sharp strong defined V-shaped jawline tapering to a firm pointed chin, high prominent commanding cheekbones, very high straight strong nose bridge, deep-set double-eyelid intense piercing dark eyes with steady gaze, well-shaped full lips, smooth handsome tan skin with mature masculine appeal, glossy perfectly styled short black hair gently blown by mountain wind. Tall broad-shouldered muscular powerful model build, commanding heroic presence like an action movie protagonist. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, calm and unafraid. Wind gently blowing his hair and the collar of his tactical jacket. He is wearing a dark gray tactical mountain survey jacket with a plain subtle generic emblem (no readable text or specific agency name), a dark tactical vest, and a small folding knife holstered on his right hip. Behind him, a narrow Hokkaido mountain trail flanked by tall ominous bamboo grass walls (Chishimazasa) in dim foggy light, the sky above heavy and overcast with rolling grey clouds. Dramatic warm lighting on his face like a fashion magazine cover, dark cold shadows behind. Shallow depth of field, background slightly blurred. No text, no words, no letters, no logos, no specific agency name. 16:9 aspect ratio. Generate 5 images.
```

**Why:** イケメン度は「強調語の強さ」ではなく「具体的な顔骨格パーツ（V字・二重・高鼻筋・8頭身）と職業ベース（fashion model + drama actor）」で出る。立山実例の汎用「handsome」だけだと日本人平均顔になる。
**How to apply:** サムネプロンプト作成時は本テンプレを Read → A案/B案を流用 → 年代・服装・山名・季節だけ置換。**完成例をコピーして必要箇所を書き換える**のが最速。
