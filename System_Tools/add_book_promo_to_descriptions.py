#!/usr/bin/env python3
"""
公開中の全動画の概要欄の先頭に書籍の告知を、末尾にAmazonアソシエイトの表記を入れる。
既に入っている動画は飛ばす。snippet と localizations(ja) の両方を更新する。
dry-run が既定。--apply で実際に反映。
"""
import json, sys, argparse, datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from update_video_metadata import get_youtube_service

RULE = "━" * 16
MARK_TOP = "▼ 書籍を出しました"
MARK_BOTTOM = "Amazonアソシエイト・プログラムの参加者です"

HEADER = f"""{MARK_TOP}
『秋田 クマ襲撃事件 ── 2016-2025 クマは、もう暮らしのすぐ隣にいる』

Kindle 299円（Kindle Unlimitedなら0円）／紙の本 1,320円
https://link.amazon/B05HZc0AN

Kindle Unlimited（30日間無料体験）
https://www.amazon.co.jp/kindle-dbs/hz/signup?tag=a120a-22

{RULE}

"""

FOOTER = f"""

{RULE}
当チャンネルは、amazon.co.jpを宣伝しリンクすることによってサイトが紹介料を獲得できる手段を提供することを目的に設定されたアフィリエイトプログラムである、{MARK_BOTTOM}。"""

LIMIT = 5000


def decorate(desc: str) -> str:
    out = desc
    if MARK_TOP not in out:
        out = HEADER + out
    if MARK_BOTTOM not in out:
        out = out + FOOTER
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", help="動画IDをカンマ区切りで指定（試し打ち用）")
    args = ap.parse_args()

    yt = get_youtube_service()
    ch = yt.channels().list(part="contentDetails", mine=True).execute()
    uploads = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=uploads,
                                    maxResults=50, pageToken=tok).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok:
            break

    items = []
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part="snippet,localizations,status",
                             id=",".join(ids[i:i + 50]), maxResults=50).execute()
        items += r["items"]

    targets = [v for v in items if v["status"]["privacyStatus"] == "public"]
    if args.only:
        keep = set(args.only.split(","))
        targets = [v for v in targets if v["id"] in keep]

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bdir = SCRIPT_DIR / "metadata_backups" / f"book_promo_{stamp}"
    bdir.mkdir(parents=True, exist_ok=True)

    done = skipped = toolong = 0
    for v in targets:
        vid = v["id"]
        snip = v["snippet"]
        locs = v.get("localizations", {})
        new_desc = decorate(snip["description"])

        if new_desc == snip["description"] and all(
            decorate(l.get("description", "")) == l.get("description", "") for l in locs.values() if l.get("description")
        ):
            print(f"skip  {vid}  既に入っている  {snip['title'][:30]}")
            skipped += 1
            continue

        new_locs = {}
        for lang, l in locs.items():
            nl = dict(l)
            if lang == "ja" and l.get("description"):
                nl["description"] = decorate(l["description"])
            new_locs[lang] = nl

        over = [("snippet", len(new_desc))] + [(k, len(x.get("description", ""))) for k, x in new_locs.items()]
        over = [(k, n) for k, n in over if n > LIMIT]
        if over:
            print(f"SKIP  {vid}  5000字超過 {over}  {snip['title'][:30]}")
            toolong += 1
            continue

        (bdir / f"{vid}.json").write_text(
            json.dumps({"snippet": snip, "localizations": locs}, ensure_ascii=False, indent=2))

        if not args.apply:
            print(f"dry   {vid}  {len(snip['description'])}→{len(new_desc)}字  loc={list(locs)}  {snip['title'][:30]}")
            done += 1
            continue

        snip = dict(snip)
        snip["description"] = new_desc
        body = {"id": vid, "snippet": snip}
        part = "snippet"
        if new_locs:
            body["localizations"] = new_locs
            part = "snippet,localizations"
        yt.videos().update(part=part, body=body).execute()
        print(f"OK    {vid}  {len(new_desc)}字  {snip['title'][:30]}")
        done += 1

    print(f"\n対象{len(targets)}本 / 更新{done} 既存{skipped} 超過{toolong}")
    print(f"バックアップ: {bdir}")


if __name__ == "__main__":
    main()
