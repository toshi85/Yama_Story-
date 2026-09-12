"""Replace book announcements in the longest channel-owned top-level comments."""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

BASE = Path(__file__).resolve().parent
CHANNEL_ID = "UCKAQUNCqCPoly21DfTrClwA"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
BOOK = "▼ 書籍を出しました"
PRODUCTS = "▼ おすすめ商品"
SEPARATOR = "─" * 10


def connect():
    info = json.loads((BASE / "comment_token.json").read_text(encoding="utf-8"))
    creds = Credentials.from_authorized_user_info(info, SCOPES)
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def own_comments(youtube, video_id):
    comments = []
    token = None
    while True:
        kwargs = dict(part="snippet", videoId=video_id, maxResults=100,
                      textFormat="plainText")
        if token:
            kwargs["pageToken"] = token
        response = youtube.commentThreads().list(**kwargs).execute(num_retries=0)
        for thread in response.get("items", []):
            comment = thread["snippet"]["topLevelComment"]
            snippet = comment["snippet"]
            if snippet.get("authorChannelId", {}).get("value") == CHANNEL_ID:
                comments.append({"id": comment["id"],
                                 "text": snippet.get("textOriginal", snippet["textDisplay"])})
        token = response.get("nextPageToken")
        if not token:
            return comments


def strip_book(text) -> str:
    start = text.find(BOOK)
    if start >= 0:
        end = text.find(SEPARATOR, start + len(BOOK))
        if end < 0:
            text = text[:start]
        else:
            tail = text[end + len(SEPARATOR):]
            tail = re.sub(r"^(?:[ \t]*\r?\n)+", "", tail)
            text = text[:start] + tail
    return text


def product_block(keys, products) -> str:
    block = "\n\n".join(products[key]["copy"] + "\n" + products[key]["url"] for key in keys)
    return PRODUCTS + "\n\n" + block + "\n\n" + SEPARATOR + "\n\n"


def replacement(text, keys, items):
    return product_block(keys, items) + strip_book(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--only", help="Comma-separated video IDs")
    args = parser.parse_args()
    items = json.loads((BASE / "affiliate_products.json").read_text(encoding="utf-8"))["items"]
    mapping = json.loads((BASE / "affiliate_video_map.json").read_text(encoding="utf-8"))
    if args.only is not None:
        selected = {v.strip() for v in args.only.split(",") if v.strip()}
        if not selected or selected - mapping.keys():
            parser.error("--only must contain known video IDs")
        mapping = {v: keys for v, keys in mapping.items() if v in selected}
    for keys in mapping.values():
        for key in keys:
            if key not in items:
                parser.error("Unknown product key: " + key)
    counts = dict.fromkeys(["OK", "skip", "NONE", "TOOLONG", "FAIL"], 0)
    backup_dir = BASE / "metadata_backups" / ("pinned_products_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    print("MODE " + ("apply" if args.apply else "dry-run"), flush=True)
    try:
        youtube = connect()
    except Exception as exc:
        for video_id in mapping:
            print(f"FAIL {video_id} 0 error={type(exc).__name__}", flush=True)
        counts["FAIL"] = len(mapping)
        print("SUMMARY " + json.dumps(counts), flush=True)
        return 1
    for video_id, keys in mapping.items():
        length = 0
        try:
            comments = own_comments(youtube, video_id)
            if not comments:
                status = "NONE"
            else:
                comment = max(comments, key=lambda c: len(c["text"]))
                original = comment["text"]
                length = len(original)
                if PRODUCTS in original:
                    status = "skip"
                else:
                    new = replacement(original, keys, items)
                    length = len(new)
                    if length > 9000:
                        status = "TOOLONG"
                    else:
                        if args.apply:
                            backup_dir.mkdir(parents=True, exist_ok=True)
                            with (backup_dir / (video_id + ".json")).open("x", encoding="utf-8") as f:
                                json.dump({"video_id": video_id, "comment_id": comment["id"],
                                           "text": original}, f, ensure_ascii=False, indent=2)
                                f.write("\n")
                            youtube.comments().update(part="snippet", body={"id": comment["id"],
                                "snippet": {"textOriginal": new}}).execute(num_retries=0)
                        status = "OK"
            counts[status] += 1
            print(f"{status} {video_id} {length}", flush=True)
        except Exception as exc:
            counts["FAIL"] += 1
            http_status = getattr(getattr(exc, "resp", None), "status", None)
            print(f"FAIL {video_id} {length} error={type(exc).__name__} http_status={http_status}", flush=True)
    print("SUMMARY " + json.dumps(counts), flush=True)
    if args.apply and backup_dir.exists():
        print("BACKUP " + str(backup_dir), flush=True)
    return int(bool(counts["FAIL"] or counts["TOOLONG"]))


if __name__ == "__main__":
    raise SystemExit(main())
