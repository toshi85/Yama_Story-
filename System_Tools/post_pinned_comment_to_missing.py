#!/usr/bin/env python3
"""
固定コメントが無い動画に、他の動画と同じ本文（書籍の告知＋再生リスト）を投稿する。
APIでは「固定」ができないので、投稿後にStudioで固定する操作だけ人がやる。
投稿したコメントのURLを最後に出すので、それを開いて⋮→固定を押せばよい。
dry-run が既定。--apply で投稿。
"""
import json, sys, argparse
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).resolve().parent
CLIENT_SECRET = SCRIPT_DIR.parent / "ShortsPipeline" / "assets" / "client_secret.json"
TOKEN_FILE = SCRIPT_DIR / "comment_token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

HEADER = """▼ 書籍を出しました
『秋田 クマ襲撃事件 ── 2016-2025 クマは、もう暮らしのすぐ隣にいる』

Kindle 299円（Kindle Unlimitedなら0円）／紙の本 1,320円
https://link.amazon/B05HZc0AN

Kindle Unlimited（30日間無料体験）
https://www.amazon.co.jp/kindle-dbs/hz/signup?tag=a120a-22

──────────

"""


def service():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES).run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pinned_json")
    ap.add_argument("body_txt", help="他の動画と同じ本文（再生リストの案内）")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    data = json.loads(Path(args.pinned_json).read_text())
    body = Path(args.body_txt).read_text().rstrip() + "\n"
    text = HEADER + body
    targets = [(k, v) for k, v in data.items() if not v.get("pinned_id")]

    if not args.apply:
        print(f"対象 {len(targets)}本 / 投稿する本文 {len(text)}字\n")
        print(text)
        for vid, v in targets:
            print(f"dry   {vid}  {v.get('title','')}")
        return

    yt = service()
    posted = []
    for vid, v in targets:
        try:
            r = yt.commentThreads().insert(part="snippet", body={"snippet": {
                "videoId": vid,
                "topLevelComment": {"snippet": {"textOriginal": text}},
            }}).execute()
            cid = r["snippet"]["topLevelComment"]["id"]
            posted.append((vid, cid))
            print(f"OK    {vid}  {v.get('title','')}")
        except Exception as e:
            print(f"FAIL  {vid}  {e}")

    print("\n■ ここから先は手作業（APIでは固定できない）")
    print("下のURLを開き、自分のコメントの右上の ⋮ →「固定」→「固定」を押す")
    for vid, cid in posted:
        print(f"  https://www.youtube.com/watch?v={vid}&lc={cid}")


if __name__ == "__main__":
    main()
