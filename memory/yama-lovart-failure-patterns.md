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

## 6. 構図関連

| 症状 | 指示原因 | 回避表現 |
|---|---|---|
| 顔が小さい・全身入り | フレーミング指示なし | `framed from chest up`（立山実例）・バストアップ明示 |
| 二人が違う向きを向く（複数キャラ同居時） | `both facing the same direction` 単発 | 複数キャラ同居は避け、1人ずつ単独生成→Photopea合成（リファレンスCHAR-01/02と同じ方式） |

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
