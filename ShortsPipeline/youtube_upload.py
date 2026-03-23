#!/usr/bin/env python3
"""
YouTube Shorts 予約投稿スクリプト
使い方:
  python3 youtube_upload.py projects/甘粛省ウルトラマラソン/
  python3 youtube_upload.py projects/甘粛省ウルトラマラソン/ --start-date 2026-03-19
  python3 youtube_upload.py projects/谷川岳遭難事故1960/ --resume   # 未投稿分から再開
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube"]
SCRIPT_DIR = Path(__file__).parent
ASSETS_DIR = SCRIPT_DIR / "assets"
CLIENT_SECRET = ASSETS_DIR / "client_secret.json"
TOKEN_FILE = ASSETS_DIR / "youtube_token.json"

PLAYLIST_NAME = "事故ログ【ショート】"

# 投稿スケジュール設定（JST）
JST = timezone(timedelta(hours=9))
MORNING_HOUR = 7   # 朝7:00
EVENING_HOUR = 20  # 夜20:00


def get_youtube_service():
    """YouTube API認証（初回はブラウザ認証）"""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                print("❌ client_secret.json が見つかりません")
                print(f"   {CLIENT_SECRET} に配置してください")
                print("   Google Cloud Console → 認証情報 → OAuthクライアントID → JSONダウンロード")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print("✅ YouTube認証完了（トークン保存済み）")

    return build("youtube", "v3", credentials=creds)


def find_playlist(youtube, name):
    """再生リストを名前で検索してIDを返す"""
    request = youtube.playlists().list(part="snippet", mine=True, maxResults=50)
    response = request.execute()
    for item in response.get("items", []):
        if item["snippet"]["title"] == name:
            return item["id"]
    return None


def add_to_playlist(youtube, playlist_id, video_id):
    """動画を再生リストに追加"""
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    ).execute()


def generate_schedule(total_parts, start_date):
    """投稿スケジュール生成（朝7:00 / 夜20:00）"""
    schedule = []
    current_date = start_date
    slot = "morning"  # morning or evening

    for i in range(total_parts):
        if slot == "morning":
            publish_time = current_date.replace(
                hour=MORNING_HOUR, minute=0, second=0, microsecond=0,
                tzinfo=JST
            )
            slot = "evening"
        else:
            publish_time = current_date.replace(
                hour=EVENING_HOUR, minute=0, second=0, microsecond=0,
                tzinfo=JST
            )
            slot = "morning"
            current_date += timedelta(days=1)

        schedule.append(publish_time)

    return schedule


def upload_video(youtube, file_path, title, description, publish_at=None):
    """動画をYouTubeにアップロード（予約投稿対応）"""
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["shorts", "山岳事故", "ドキュメンタリー"],
            "categoryId": "22",  # People & Blogs
            "defaultLanguage": "ja",
            "defaultAudioLanguage": "ja"
        },
        "status": {
            "selfDeclaredMadeForKids": False
        }
    }

    if publish_at:
        body["status"]["privacyStatus"] = "private"
        body["status"]["publishAt"] = publish_at.isoformat()
    else:
        body["status"]["privacyStatus"] = "public"

    media = MediaFileUpload(
        str(file_path),
        mimetype="video/mp4",
        resumable=True,
        chunksize=10 * 1024 * 1024  # 10MB chunks
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print(f"  📤 アップロード中: {file_path.name}")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"  📊 {progress}%", end="\r")

    video_id = response["id"]
    print(f"  ✅ 完了: https://youtube.com/shorts/{video_id}")
    return video_id


def main():
    parser = argparse.ArgumentParser(description="YouTube Shorts 予約投稿")
    parser.add_argument("project_dir", help="プロジェクトフォルダのパス")
    parser.add_argument("--start-date", help="投稿開始日 (YYYY-MM-DD)", default=None)
    parser.add_argument("--immediate", action="store_true", help="予約なしで即時公開")
    parser.add_argument("--playlist", default=PLAYLIST_NAME, help=f"追加先の再生リスト名 (デフォルト: {PLAYLIST_NAME})")
    parser.add_argument("--no-playlist", action="store_true", help="再生リストへの追加をスキップ")
    parser.add_argument("--dry-run", action="store_true", help="実際にはアップロードしない")
    parser.add_argument("--resume", action="store_true", help="youtube_uploads.jsonから未投稿分を再開")
    parser.add_argument("--yes", "-y", action="store_true", help="確認をスキップして即実行")
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    if not project_dir.is_absolute():
        project_dir = SCRIPT_DIR / project_dir

    # cuts.json読み込み
    cuts_file = project_dir / "cuts.json"
    if not cuts_file.exists():
        print(f"❌ cuts.json が見つかりません: {cuts_file}")
        sys.exit(1)

    with open(cuts_file) as f:
        data = json.load(f)

    total = len(data["cuts"])
    source_name = data.get("source", project_dir.name)
    display_title = data.get("display_title", project_dir.name)
    # 改行を除去してベースタイトルに
    base_title = display_title.replace("\n", " ").strip()

    # 既存アップロード結果を読み込み（--resume用）
    results_file = project_dir / "youtube_uploads.json"
    uploaded_episodes = set()
    existing_uploads = []
    if args.resume and results_file.exists():
        with open(results_file) as f:
            prev_data = json.load(f)
        existing_uploads = prev_data.get("uploads", [])
        uploaded_episodes = {u["episode"] for u in existing_uploads}
        print(f"📋 既存アップロード: {len(uploaded_episodes)}本（ep{sorted(uploaded_episodes)}）")

    # 出力ファイル確認
    output_dir = project_dir / "output"
    videos = []
    for cut in data["cuts"]:
        ep = cut["episode"]
        if ep in uploaded_episodes:
            continue
        video_path = output_dir / f"ep{ep:02d}_short.mp4"
        if not video_path.exists():
            print(f"❌ 動画ファイルが見つかりません: {video_path}")
            sys.exit(1)
        videos.append((ep, video_path))

    if not videos:
        print("✅ 全エピソードがアップロード済みです")
        return

    # スケジュール生成（残りの本数分だけ）
    if args.start_date:
        start = datetime.strptime(args.start_date, "%Y-%m-%d")
    else:
        start = datetime.now() + timedelta(days=1)  # 明日から

    schedule = generate_schedule(len(videos), start)

    # スケジュール表示
    print("==========================================")
    print("📅 YouTube Shorts 投稿スケジュール")
    print(f"📁 プロジェクト: {project_dir.name}")
    if uploaded_episodes:
        print(f"🔄 再開モード: {len(uploaded_episodes)}本済み → 残り{len(videos)}本")
    else:
        print(f"🎬 全{total}本")
    print("==========================================")

    for i, (ep, video_path) in enumerate(videos):
        publish_time = schedule[i] if not args.immediate else None
        title = f"{base_title} Part {ep}/{total}"
        time_str = publish_time.strftime("%m/%d %H:%M") if publish_time else "即時公開"
        print(f"  Part {ep}: {time_str} - {title}")

    if args.dry_run:
        print("\n🔍 ドライラン完了（実際のアップロードなし）")
        return

    # 確認
    if not args.yes:
        print("")
        confirm = input("この内容でアップロードしますか？ (y/N): ")
        if confirm.lower() != "y":
            print("キャンセルしました")
            return

    # YouTube API認証
    youtube = get_youtube_service()

    # 再生リスト検索
    playlist_id = None
    if not args.no_playlist:
        playlist_id = find_playlist(youtube, args.playlist)
        if playlist_id:
            print(f"📋 再生リスト「{args.playlist}」に自動追加します")
        else:
            print(f"⚠️  再生リスト「{args.playlist}」が見つかりません（追加スキップ）")

    # アップロード実行
    print("\n📤 アップロード開始...")
    new_uploads = []

    for i, (ep, video_path) in enumerate(videos):
        publish_time = schedule[i] if not args.immediate else None
        title = f"{base_title} Part {ep}/{total}"
        description = (
            f"{base_title}\n\n"
            f"Part {ep}/{total}\n\n"
            f"#shorts #山岳事故 #ドキュメンタリー #遭難"
        )

        print(f"\n🎬 Part {ep}/{total}")
        video_id = upload_video(youtube, video_path, title, description, publish_time)

        if playlist_id:
            add_to_playlist(youtube, playlist_id, video_id)
            print(f"  📋 再生リストに追加済み")

        new_uploads.append({
            "episode": ep,
            "video_id": video_id,
            "publish_at": publish_time.isoformat() if publish_time else "immediate"
        })

        # 1本ごとに結果を保存（途中停止に備える）
        all_uploads = existing_uploads + new_uploads
        all_uploads.sort(key=lambda x: x["episode"])
        with open(results_file, "w") as f:
            json.dump({"uploads": all_uploads}, f, indent=2, ensure_ascii=False)

    print("\n==========================================")
    print("🎉 全動画のアップロード完了！")
    print(f"📄 結果: {results_file}")
    print("==========================================")


if __name__ == "__main__":
    main()
