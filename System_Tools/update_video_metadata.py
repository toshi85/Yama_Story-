#!/usr/bin/env python3
"""
YouTube動画メタデータ更新ツール（説明文・タグ・ハッシュタグ）
dry-run モード（デフォルト）で変更内容を表示、--apply で実際に反映。
"""

import argparse
import json
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCRIPT_DIR = Path(__file__).resolve().parent
YAMA_ROOT = SCRIPT_DIR.parent
ASSETS_DIR = YAMA_ROOT / "ShortsPipeline" / "assets"
CLIENT_SECRET = ASSETS_DIR / "client_secret.json"
TOKEN_FILE = SCRIPT_DIR / "update_token.json"  # 書き込み用は別トークン
BACKUP_DIR = SCRIPT_DIR / "metadata_backups"

# 書き込みスコープ
SCOPES = [
    "https://www.googleapis.com/auth/youtube",        # 書き込み
    "https://www.googleapis.com/auth/youtube.readonly",
]


def get_youtube_service():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("トークンをリフレッシュ中...", file=sys.stderr)
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                print(f"ERROR: {CLIENT_SECRET} が見つかりません", file=sys.stderr)
                sys.exit(1)
            print("ブラウザでOAuth認証を行います（書き込み権限）...", file=sys.stderr)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def backup_metadata(youtube, video_id):
    """更新前のメタデータをバックアップ"""
    resp = youtube.videos().list(part="snippet", id=video_id).execute()
    items = resp.get("items", [])
    if not items:
        print(f"ERROR: 動画 {video_id} が見つかりません", file=sys.stderr)
        sys.exit(1)

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_file = BACKUP_DIR / f"{video_id}_backup.json"
    backup_file.write_text(json.dumps(items[0], ensure_ascii=False, indent=2))
    print(f"バックアップ保存: {backup_file}", file=sys.stderr)
    return items[0]


def update_video(youtube, video_id, new_snippet_fields, dry_run=True):
    """動画のsnippetを更新"""
    # 現在のデータ取得
    resp = youtube.videos().list(part="snippet", id=video_id).execute()
    item = resp["items"][0]
    snippet = item["snippet"]

    print(f"\n{'='*60}")
    print(f"動画: {snippet['title']}")
    print(f"ID:   {video_id}")
    print(f"{'='*60}")

    # 変更内容を表示
    if "description" in new_snippet_fields:
        print(f"\n--- 説明文の変更 ---")
        old_lines = snippet["description"].split("\n")[:5]
        new_lines = new_snippet_fields["description"].split("\n")[:5]
        print(f"【現在の冒頭】")
        for l in old_lines:
            print(f"  {l}")
        print(f"\n【変更後の冒頭】")
        for l in new_lines:
            print(f"  {l}")

    if "tags" in new_snippet_fields:
        print(f"\n--- タグの変更 ---")
        print(f"【現在】 {snippet.get('tags', [])}")
        print(f"【変更後】 {new_snippet_fields['tags']}")

    if dry_run:
        print(f"\n⚠️  dry-run モードです。実際の更新は行われません。")
        print(f"   --apply フラグを付けて実行すると反映されます。")
        return

    # 実際に更新
    for key, value in new_snippet_fields.items():
        snippet[key] = value

    youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": snippet,
        },
    ).execute()
    print(f"\n✅ 更新完了！")


def main():
    parser = argparse.ArgumentParser(description="YouTube動画メタデータ更新")
    parser.add_argument("config", help="更新設定JSONファイル")
    parser.add_argument("--apply", action="store_true", help="実際に更新を実行（デフォルトはdry-run）")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"ERROR: {config_path} が見つかりません", file=sys.stderr)
        sys.exit(1)

    updates = json.loads(config_path.read_text())
    youtube = get_youtube_service()

    for entry in updates:
        video_id = entry["video_id"]
        backup_metadata(youtube, video_id)
        update_video(youtube, video_id, entry["snippet"], dry_run=not args.apply)


if __name__ == "__main__":
    main()
