#!/usr/bin/env python3
"""
Yama_Story 日次データ収集スクリプト

macOS launchdで毎日自動実行。PCスリープ中は次回起動時に未収集分をまとめて取得。
既存 yt_analytics.py のAPI認証を流用。

出力: Yama_Story/Analytics/daily/YYYY-MM-DD.json
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# yt_analytics.py と同じディレクトリから認証関数をインポート
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from yt_analytics import get_authenticated_services, CHANNEL_ID

ANALYTICS_DIR = SCRIPT_DIR.parent / "Analytics" / "daily"
ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

MAX_BACKFILL_DAYS = 30  # 最大30日分のバックフィル


def _is_incomplete(json_path):
    """ファイルが存在してもデータがnull/空なら未収集扱い"""
    try:
        data = json.loads(json_path.read_text())
        return data.get("overview") is None and len(data.get("top_videos", [])) == 0
    except (json.JSONDecodeError, OSError):
        return True


def get_missing_dates():
    """未収集 or データ不完全の日付リストを返す（3日前まで。APIは2-3日遅延）"""
    today = datetime.now().date()
    latest = today - timedelta(days=3)  # APIの遅延を考慮

    missing = []
    for i in range(MAX_BACKFILL_DAYS):
        d = latest - timedelta(days=i)
        json_path = ANALYTICS_DIR / f"{d.isoformat()}.json"
        if not json_path.exists() or _is_incomplete(json_path):
            missing.append(d)

    missing.sort()  # 古い順
    return missing


def collect_overview(analytics, date_str):
    """チャンネル概要指標（1日分）"""
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=date_str,
        endDate=date_str,
        metrics="views,estimatedMinutesWatched,subscribersGained,subscribersLost,averageViewDuration,estimatedRevenue",
    ).execute()
    rows = resp.get("rows", [])
    if not rows:
        return None
    r = rows[0]
    return {
        "views": r[0],
        "watch_minutes": r[1],
        "subs_gained": r[2],
        "subs_lost": r[3],
        "avg_view_duration_sec": r[4],
        "revenue_usd": r[5],
    }


def collect_top_videos(analytics, date_str, max_results=10):
    """その日のトップ動画"""
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=date_str,
        endDate=date_str,
        metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained",
        dimensions="video",
        sort="-views",
        maxResults=max_results,
    ).execute()
    rows = resp.get("rows", [])
    return [
        {
            "video_id": r[0],
            "views": r[1],
            "watch_minutes": r[2],
            "avg_view_duration_sec": r[3],
            "avg_view_percentage": r[4],
            "subs_gained": r[5],
        }
        for r in rows
    ]


def collect_traffic_sources(analytics, date_str):
    """トラフィックソース（チャンネル全体）"""
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=date_str,
        endDate=date_str,
        metrics="views,estimatedMinutesWatched",
        dimensions="insightTrafficSourceType",
        sort="-views",
    ).execute()
    rows = resp.get("rows", [])
    return [
        {
            "source": r[0],
            "views": r[1],
            "watch_minutes": r[2],
        }
        for r in rows
    ]


def collect_search_terms(analytics, date_str, max_results=20):
    """検索キーワード"""
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=date_str,
        endDate=date_str,
        metrics="views,estimatedMinutesWatched",
        dimensions="insightTrafficSourceDetail",
        filters="insightTrafficSourceType==YT_SEARCH",
        sort="-views",
        maxResults=max_results,
    ).execute()
    rows = resp.get("rows", [])
    return [
        {
            "term": r[0],
            "views": r[1],
            "watch_minutes": r[2],
        }
        for r in rows
    ]


def main():
    missing = get_missing_dates()
    if not missing:
        print("全日分収集済み。スキップ。")
        return

    print(f"未収集: {len(missing)}日分（{missing[0]} ～ {missing[-1]}）")

    analytics, youtube = get_authenticated_services()
    collected = 0

    for date in missing:
        date_str = date.isoformat()
        print(f"  収集中: {date_str} ...", end=" ", flush=True)

        try:
            overview = collect_overview(analytics, date_str)
            top_videos = collect_top_videos(analytics, date_str)

            if overview is None and len(top_videos) == 0:
                print("SKIP (APIデータなし)")
                continue

            data = {
                "date": date_str,
                "collected_at": datetime.now().isoformat(),
                "overview": overview,
                "top_videos": top_videos,
                "traffic_sources": collect_traffic_sources(analytics, date_str),
                "search_terms": collect_search_terms(analytics, date_str),
            }

            out_path = ANALYTICS_DIR / f"{date_str}.json"
            out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
            print("OK")
            collected += 1

        except Exception as e:
            print(f"ERROR: {e}")
            continue

    print(f"\n完了: {collected}/{len(missing)}日分を収集")


if __name__ == "__main__":
    main()
