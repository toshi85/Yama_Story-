---
name: yama-shorts-mac-tasks
description: Yama_Storyショート動画リニューアル — Mac側で実施するタスク一覧
type: project
---

Yama_Storyショート動画のリニューアル作業（Mac側で実施）。2026-03-20策定。

## タスク一覧

### 1. 3作品を新基準（61〜90秒）で再カット
- 対象: 甘粛省ウルトラマラソン / 福岡大ヒグマ事件 / 谷川岳宙吊り事件
- transcript.jsonはMacローカルにのみ存在
- `/yama-shorts-cut` で新基準のcuts.jsonを再生成 → パイプラインで動画再作成
- 予約投稿26件を差し替え

### 2. BGM楽曲の合成をパイプラインに追加
- 指定楽曲を `ShortsPipeline/assets/` に配置
- pipeline.sh STEP4にFFmpegでBGMミックスを追加（ナレーション優先、フェードイン/アウト）
- 楽曲ファイルはユーザーから共有待ち

### 3. Google Sheets自動記入スクリプト作成
- 目的: 楽曲の著作権収益申請（YouTubeショートURLを指定スプレッドシートに自動追記）
- 記入先: Googleスプレッドシート B列9行目から下へ順次追記
- 記入内容: YouTube URLのみ

#### 必要な準備（Mac側）
- Google Cloud Projectでサービスアカウント作成
- サービスアカウントのJSONキー取得・配置
- スプレッドシートにサービスアカウントを編集者として共有
- スプレッドシートIDの取得
- gspreadライブラリのインストール

**Why:** LINEVOOMデータで1分30秒台が2分半台の5倍のインプレッションを記録。短尺化+BGM+収益自動化で効率最大化。

**How to apply:** Mac作業セッション開始時にこのタスクリストを参照。
