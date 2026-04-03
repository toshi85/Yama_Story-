---
name: yama-shorts-multiplatform
description: Yama_Storyショート動画のマルチプラットフォーム投稿戦略・著作権収益情報
type: project
---

Yama_Storyショート動画のマルチプラットフォーム展開方針（2026-03-20策定）

## 投稿プラットフォームと収益構造

| プラットフォーム | 広告収益 | 著作権収益 | 方法 | 単価目安 |
|---|---|---|---|---|
| YouTube Shorts | ✅ | ✅ | BGM焼き込み → URL申請（スプレッドシート） | 契約次第 |
| TikTok | ✅ | ✅ 実績あり | アプリ内楽曲登録 → 投稿時に後付け | 約0.001円/再生 |
| Instagram Reels | ✅ | ✅ 実績あり | 同上 | 約0.0015円/再生 |
| Facebook | ✅ | ✅ 実績あり | 同上 | — |
| LINE VOOM | ✅ | ❌ 非対応 | 楽曲検索機能なし | — |
| ニコニコ | △(2026春〜) | ❓ 調査中 | 間の会社に確認依頼 | — |

## 著作権収益の仕組み（2系統）
1. **YouTube方式**: BGMを動画に焼き込み → スプレッドシートにURLを申請
2. **TikTok/Instagram/Facebook方式**: BGMなし版を投稿 → アプリ内で登録楽曲を後付け → 自動で収益発生

**Why:** 間の会社（JASRAC経由）に確認済み。URL申請はYouTubeのみだが、今後TikTok等でもURL申請対応になる可能性あり（JASRAC担当と協議中）。

## パイプラインでの対応
- BGMあり版: YouTube用（BGM焼き込み）
- BGMなし版: TikTok / Instagram / Facebook / LINE VOOM用（TikTok・Instagram・FBはアプリ内で後付け、LINE VOOMはBGMなしのまま）

## シャドウバン対策
- TikTok: 自分の端末・回線から投稿必須（IPアドレス単位で監視）
- LINE VOOM: 外注可能だがリスク低め
- X（Twitter）: JASRAC包括契約なし → BGM付き投稿は使用料発生（50,000円/10曲）→ 投稿非推奨

## 未対応タスク
- 間の会社にアプリ内楽曲登録を依頼（TikTok + Instagram + Facebook）
- ニコニコ動画の著作権収益対応を調査依頼
- パイプラインにBGMあり/なし2バージョン自動生成を実装（Mac側タスク）
