#!/usr/bin/env python3
"""
各動画の固定コメントの先頭に書籍の告知を差し込む。
固定コメントは編集しても固定のまま残るので、既存の本文を書き換える形で入れる。
固定コメントのIDは yt-dlp で集めた pinned.json から読む。
dry-run が既定。--apply で反映。
※コメント操作には youtube.force-ssl 権限が要る（別トークン comment_token.json）。
"""
import json, sys, argparse, datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).resolve().parent
CLIENT_SECRET = SCRIPT_DIR.parent / "ShortsPipeline" / "assets" / "client_secret.json"
TOKEN_FILE = SCRIPT_DIR / "comment_token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

MARK = "▼ 書籍を出しました"
HEADER = f"""{MARK}
『秋田 クマ襲撃事件 ── 2016-2025 クマは、もう暮らしのすぐ隣にいる』

Kindle 299円（Kindle Unlimitedなら0円）／紙の本 1,320円
https://link.amazon/B05HZc0AN

Kindle Unlimited（30日間無料体験）
https://www.amazon.co.jp/kindle-dbs/hz/signup?tag=a120a-22

──────────

"""
LIMIT = 9000


def service():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("ブラウザでYouTubeの認証を行います（コメント編集の権限）", file=sys.stderr)
            creds = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES).run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pinned_json")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    data = json.loads(Path(args.pinned_json).read_text())
    yt = service() if args.apply else None

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bdir = SCRIPT_DIR / "metadata_backups" / f"pinned_comments_{stamp}"
    bdir.mkdir(parents=True, exist_ok=True)

    done = skipped = nopin = failed = 0
    for vid, d in data.items():
        cid, text = d.get("pinned_id"), d.get("pinned_text")
        if not cid:
            print(f"NOPIN {vid}  固定コメントなし  {d.get('title','')}")
            nopin += 1
            continue
        if MARK in text:
            print(f"skip  {vid}  既に入っている")
            skipped += 1
            continue
        new = HEADER + text
        if len(new) > LIMIT:
            print(f"SKIP  {vid}  長すぎる {len(new)}字")
            failed += 1
            continue
        (bdir / f"{vid}.json").write_text(json.dumps({"comment_id": cid, "text": text}, ensure_ascii=False, indent=2))
        if not args.apply:
            print(f"dry   {vid}  {len(text)}→{len(new)}字  {d.get('title','')}")
            done += 1
            continue
        try:
            yt.comments().update(part="snippet", body={"id": cid, "snippet": {"textOriginal": new}}).execute()
            print(f"OK    {vid}  {len(new)}字  {d.get('title','')}")
            done += 1
        except Exception as e:
            print(f"FAIL  {vid}  {e}")
            failed += 1

    print(f"\n更新{done} 既存{skipped} 固定なし{nopin} 失敗{failed}")
    print(f"バックアップ: {bdir}")


if __name__ == "__main__":
    main()
