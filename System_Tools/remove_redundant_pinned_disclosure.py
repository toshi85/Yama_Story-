"""Remove one exact redundant disclosure line from channel pinned comments."""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

from googleapiclient.errors import HttpError

from update_pinned_comments_products import BASE, CHANNEL_ID, connect


TARGET = "※Amazonのアソシエイトとして、事故ログは適格販売により収入を得ています。"
PLAN_DIR = BASE / "metadata_backups" / "pinned_disclosure_cleanup_20260924"
PLAN = PLAN_DIR / "plan.json"
RESULT = PLAN_DIR / "result.json"


def remove_line(text):
    if text.count(TARGET) != 1:
        raise ValueError("Expected exactly one disclosure line")
    for suffix, replacement in ((TARGET + "\n\n", ""), (TARGET + "\n", ""), (TARGET, "")):
        if suffix in text:
            new = text.replace(suffix, replacement, 1)
            if not new.strip():
                raise ValueError("Replacement would be empty")
            return new
    raise AssertionError("unreachable")


def owned_top_level(snippet):
    return (snippet.get("authorChannelId", {}).get("value") == CHANNEL_ID
            and not snippet.get("parentId"))


def uploads(youtube):
    channels = youtube.channels().list(part="contentDetails", mine=True).execute(num_retries=0)["items"]
    channel = next(c for c in channels if c["id"] == CHANNEL_ID)
    playlist = channel["contentDetails"]["relatedPlaylists"]["uploads"]
    videos = []
    token = None
    while True:
        request = {"part": "contentDetails", "playlistId": playlist, "maxResults": 50}
        if token:
            request["pageToken"] = token
        response = youtube.playlistItems().list(**request).execute(num_retries=0)
        videos.extend(item["contentDetails"]["videoId"] for item in response.get("items", []))
        token = response.get("nextPageToken")
        if not token:
            return videos


def read_comment(youtube, comment_id, video):
    response = youtube.commentThreads().list(part="snippet", id=comment_id,
                                             textFormat="plainText").execute(num_retries=0)
    items = response.get("items", [])
    if len(items) != 1:
        raise ValueError("Pinned comment ID missing")
    thread = items[0]
    comment = thread["snippet"]["topLevelComment"]
    snippet = comment["snippet"]
    if (thread["snippet"].get("videoId") != video or comment["id"] != comment_id
            or not owned_top_level(snippet)):
        raise ValueError("Pinned ID is not a channel-owned top-level comment on the video")
    return snippet["textOriginal"]


def unlisted_own_comments(youtube, video):
    comments = []
    token = None
    while True:
        request = {"part": "snippet", "videoId": video, "maxResults": 100,
                   "order": "relevance", "textFormat": "plainText"}
        if token:
            request["pageToken"] = token
        try:
            response = youtube.commentThreads().list(**request).execute(num_retries=0)
        except HttpError as exc:
            if exc.resp.status == 403 and b"commentsDisabled" in exc.content:
                return [], "comments_disabled"
            raise
        for thread in response.get("items", []):
            comment = thread["snippet"]["topLevelComment"]
            snippet = comment["snippet"]
            if thread["snippet"].get("videoId") == video and owned_top_level(snippet):
                comments.append({"id": comment["id"], "text": snippet["textOriginal"]})
        token = response.get("nextPageToken")
        if not token:
            return comments, "scanned"


def prepare(youtube):
    videos = uploads(youtube)
    pinned = json.loads((BASE / "pinned_comment_ids.json").read_text())
    if not set(pinned).issubset(videos):
        raise ValueError("Pinned ID ledger includes a video outside channel uploads")
    plan = {"created_at": datetime.now().isoformat(), "target": TARGET,
            "channel_id": CHANNEL_ID, "videos": videos, "edits": [], "scanned": []}
    for video in videos:
        if video in pinned:
            comment_id = pinned[video]["pinned_comment_id"]
            if not comment_id:
                raise ValueError(f"Pinned ID missing: {video}")
            text = read_comment(youtube, comment_id, video)
            candidates = [{"id": comment_id, "text": text}]
            source = "measured_pinned_id"
            scan_status = "scanned"
        else:
            candidates, scan_status = unlisted_own_comments(youtube, video)
            source = "unmapped_channel_comment"
        matches = [c for c in candidates if TARGET in c["text"]]
        if source == "unmapped_channel_comment" and matches:
            raise ValueError(f"Disclosure found on video without measured pinned ID: {video}")
        for c in matches:
            plan["edits"].append({"video_id": video, "comment_id": c["id"],
                                  "source": source, "old": c["text"],
                                  "new": remove_line(c["text"])})
        plan["scanned"].append({"video_id": video, "source": source,
                                "status": scan_status, "own_comments": len(candidates),
                                "matches": len(matches)})
    PLAN_DIR.mkdir(parents=True, exist_ok=True)
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"uploads": len(videos), "known_pinned": len(pinned),
                      "edits": len(plan["edits"]), "plan": str(PLAN)}, ensure_ascii=False))


def apply(youtube):
    plan = json.loads(PLAN.read_text())
    if plan["channel_id"] != CHANNEL_ID or plan["target"] != TARGET:
        raise ValueError("Plan target or channel mismatch")
    results = []
    for edit in plan["edits"]:
        video, cid = edit["video_id"], edit["comment_id"]
        current = read_comment(youtube, cid, video)
        if current == edit["new"]:
            status = "already_updated"
        elif current != edit["old"]:
            status = "changed_since_plan"
        else:
            youtube.comments().update(part="snippet", body={"id": cid,
                "snippet": {"textOriginal": edit["new"]}}).execute(num_retries=0)
            after = ""
            for attempt in range(5):
                if attempt:
                    time.sleep(1)
                after = read_comment(youtube, cid, video)
                if after == edit["new"]:
                    break
            status = "verified" if after == edit["new"] else "verification_failed"
        results.append({"video_id": video, "comment_id": cid, "status": status})
        RESULT.write_text(json.dumps({"results": results}, ensure_ascii=False, indent=2) + "\n")
        print(status, video, flush=True)
        if status not in ("verified", "already_updated"):
            raise RuntimeError(f"Stopped at {video}: {status}")
    print(json.dumps({"verified": len(results), "result": str(RESULT)}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "apply"])
    args = parser.parse_args()
    youtube = connect()
    if args.action == "prepare":
        prepare(youtube)
    else:
        apply(youtube)
