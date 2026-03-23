#!/usr/bin/env python3
"""
Yama_Story YouTube Analytics API CLI

YouTube Analytics APIでチャンネルの詳細パフォーマンスデータを取得する。
Data API v3では取れないCTR・視聴維持率・収益データに対応。

使い方:
  python3 Yama_Story/System_Tools/yt_analytics.py overview
  python3 Yama_Story/System_Tools/yt_analytics.py top-videos
  python3 Yama_Story/System_Tools/yt_analytics.py revenue
  python3 Yama_Story/System_Tools/yt_analytics.py video <VIDEO_ID>
  python3 Yama_Story/System_Tools/yt_analytics.py retention <VIDEO_ID>
  python3 Yama_Story/System_Tools/yt_analytics.py traffic <VIDEO_ID>
  python3 Yama_Story/System_Tools/yt_analytics.py demographics
  python3 Yama_Story/System_Tools/yt_analytics.py search-terms
  python3 Yama_Story/System_Tools/yt_analytics.py daily [--days N]
  python3 Yama_Story/System_Tools/yt_analytics.py realtime

オプション:
  --days N    対象期間（デフォルト: 28日）
  --top N     表示件数（デフォルト: 10）
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# パス設定
SCRIPT_DIR = Path(__file__).resolve().parent
YAMA_ROOT = SCRIPT_DIR.parent
PROJECT_ROOT = YAMA_ROOT.parent
ASSETS_DIR = YAMA_ROOT / "ShortsPipeline" / "assets"
CLIENT_SECRET = ASSETS_DIR / "client_secret.json"
TOKEN_FILE = SCRIPT_DIR / "analytics_token.json"

# Analytics APIスコープ（読み取り専用）
SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
    "https://www.googleapis.com/auth/youtube.readonly",
]

# チャンネルID
CHANNEL_ID = "UCKAQUNCqCPoly21DfTrClwA"


def get_authenticated_services():
    """OAuth認証してAnalytics + Data APIクライアントを返す"""
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
            print("ブラウザでOAuth認証を行います...", file=sys.stderr)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())
        print(f"トークン保存: {TOKEN_FILE}", file=sys.stderr)

    analytics = build("youtubeAnalytics", "v2", credentials=creds)
    youtube = build("youtube", "v3", credentials=creds)
    return analytics, youtube


def date_range(days):
    end = datetime.now().date()
    start = end - timedelta(days=days)
    return start.isoformat(), end.isoformat()


def cmd_overview(analytics, youtube, args):
    """チャンネル概要（views, watchTime, subscribers, estimatedRevenue）"""
    start, end = date_range(args.days)
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=start,
        endDate=end,
        metrics="views,estimatedMinutesWatched,subscribersGained,subscribersLost,averageViewDuration,estimatedRevenue",
    ).execute()

    rows = resp.get("rows", [])
    if not rows:
        print("データなし")
        return

    r = rows[0]
    print(f"=== チャンネル概要（過去{args.days}日） ===")
    print(f"視聴回数:       {r[0]:,.0f}")
    print(f"総再生時間:     {r[1]:,.0f}分（{r[1]/60:,.1f}時間）")
    print(f"登録者増加:     +{r[2]:,.0f}")
    print(f"登録者減少:     -{r[3]:,.0f}")
    print(f"登録者純増:     {r[2]-r[3]:+,.0f}")
    print(f"平均視聴時間:   {r[4]:,.0f}秒（{r[4]/60:,.1f}分）")
    print(f"推定収益:       ¥{r[5]*150:,.0f}（${r[5]:,.2f}）")


def cmd_top_videos(analytics, youtube, args):
    """トップ動画（視聴回数順）"""
    start, end = date_range(args.days)
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=start,
        endDate=end,
        metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained",
        dimensions="video",
        sort="-views",
        maxResults=args.top,
    ).execute()

    rows = resp.get("rows", [])
    if not rows:
        print("データなし")
        return

    video_ids = [r[0] for r in rows]
    titles = _get_video_titles(youtube, video_ids)

    print(f"=== トップ{args.top}動画（過去{args.days}日・視聴回数順） ===\n")
    for i, r in enumerate(rows, 1):
        vid = r[0]
        title = titles.get(vid, vid)
        print(f"{i}. {title}")
        print(f"   ID: {vid}")
        print(f"   視聴: {r[1]:,.0f} | 再生時間: {r[2]:,.0f}分 | 平均視聴: {r[3]:.0f}秒 | 維持率: {r[4]:.1f}% | 登録+{r[5]:.0f}")
        print()


def cmd_revenue(analytics, youtube, args):
    """収益詳細"""
    start, end = date_range(args.days)
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=start,
        endDate=end,
        metrics="estimatedRevenue,estimatedAdRevenue,grossRevenue,estimatedRedPartnerRevenue,monetizedPlaybacks,playbackBasedCpm,adImpressions",
    ).execute()

    rows = resp.get("rows", [])
    if not rows:
        print("データなし")
        return

    r = rows[0]
    print(f"=== 収益詳細（過去{args.days}日） ===")
    print(f"推定総収益:       ${r[0]:,.2f}（¥{r[0]*150:,.0f}）")
    print(f"広告収益:         ${r[1]:,.2f}")
    print(f"総収益:           ${r[2]:,.2f}")
    print(f"Premium収益:      ${r[3]:,.2f}")
    print(f"収益化再生:       {r[4]:,.0f}")
    print(f"CPM:              ${r[5]:,.2f}")
    print(f"広告インプレ:     {r[6]:,.0f}")


def cmd_video(analytics, youtube, args):
    """個別動画の詳細"""
    vid = args.video_id
    start, end = date_range(args.days)
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=start,
        endDate=end,
        metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,dislikes,comments,shares,subscribersGained,estimatedRevenue,annotationClickThroughRate,cardClickRate",
        filters=f"video=={vid}",
    ).execute()

    rows = resp.get("rows", [])
    titles = _get_video_titles(youtube, [vid])
    title = titles.get(vid, vid)

    print(f"=== {title} ===")
    print(f"ID: {vid}\n")

    if not rows:
        print("データなし")
        return

    r = rows[0]
    print(f"視聴回数:     {r[0]:,.0f}")
    print(f"再生時間:     {r[1]:,.0f}分")
    print(f"平均視聴:     {r[2]:.0f}秒（{r[2]/60:.1f}分）")
    print(f"維持率:       {r[3]:.1f}%")
    print(f"いいね:       {r[4]:,.0f}")
    print(f"低評価:       {r[5]:,.0f}")
    print(f"コメント:     {r[6]:,.0f}")
    print(f"共有:         {r[7]:,.0f}")
    print(f"登録者獲得:   +{r[8]:,.0f}")
    print(f"収益:         ${r[9]:,.2f}（¥{r[9]*150:,.0f}）")


def cmd_retention(analytics, youtube, args):
    """視聴維持率カーブ（エルボーポイント検出付き）"""
    vid = args.video_id
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate="2020-01-01",
        endDate=datetime.now().date().isoformat(),
        metrics="audienceWatchRatio",
        dimensions="elapsedVideoTimeRatio",
        filters=f"video=={vid}",
        sort="elapsedVideoTimeRatio",
    ).execute()

    rows = resp.get("rows", [])
    titles = _get_video_titles(youtube, [vid])
    title = titles.get(vid, vid)

    print(f"=== 視聴維持率: {title} ===\n")

    if not rows:
        print("データなし（公開後48時間以上必要）")
        return

    print(f"{'時間%':>6} | {'維持率':>6} | グラフ")
    print("-" * 50)

    prev = 100.0
    drops = []
    for r in rows:
        pct = r[0] * 100
        ratio = r[1] * 100
        bar = "█" * int(ratio / 2)
        drop = prev - ratio
        marker = " ◄◄ DROP" if drop > 5 else ""
        if drop > 5:
            drops.append((pct, drop))
        print(f"{pct:5.0f}% | {ratio:5.1f}% | {bar}{marker}")
        prev = ratio

    if drops:
        print(f"\n離脱ポイント:")
        for pct, drop in drops:
            print(f"  {pct:.0f}% 地点で {drop:.1f}% 低下")


def cmd_traffic(analytics, youtube, args):
    """トラフィックソース"""
    vid = args.video_id
    start, end = date_range(args.days)
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=start,
        endDate=end,
        metrics="views,estimatedMinutesWatched",
        dimensions="insightTrafficSourceType",
        filters=f"video=={vid}",
        sort="-views",
    ).execute()

    rows = resp.get("rows", [])
    titles = _get_video_titles(youtube, [vid])
    title = titles.get(vid, vid)

    print(f"=== トラフィックソース: {title} ===\n")

    if not rows:
        print("データなし")
        return

    total_views = sum(r[1] for r in rows)
    for r in rows:
        source = r[0]
        views = r[1]
        watch = r[2]
        share = (views / total_views * 100) if total_views > 0 else 0
        print(f"  {source:<30} {views:>8,.0f}回 ({share:5.1f}%) | {watch:,.0f}分")


def cmd_demographics(analytics, youtube, args):
    """視聴者層（年齢×性別）"""
    start, end = date_range(args.days)
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=start,
        endDate=end,
        metrics="viewerPercentage",
        dimensions="ageGroup,gender",
        sort="-viewerPercentage",
    ).execute()

    rows = resp.get("rows", [])
    print(f"=== 視聴者層（過去{args.days}日） ===\n")

    if not rows:
        print("データなし")
        return

    print(f"{'年齢層':<12} {'性別':<8} {'割合':>6}")
    print("-" * 30)
    for r in rows:
        age = r[0].replace("age", "")
        gender = "男性" if r[1] == "male" else "女性" if r[1] == "female" else r[1]
        print(f"{age:<12} {gender:<8} {r[2]:5.1f}%")


def cmd_search_terms(analytics, youtube, args):
    """YouTube検索キーワード"""
    start, end = date_range(args.days)
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=start,
        endDate=end,
        metrics="views,estimatedMinutesWatched",
        dimensions="insightTrafficSourceDetail",
        filters="insightTrafficSourceType==YT_SEARCH",
        sort="-views",
        maxResults=args.top,
    ).execute()

    rows = resp.get("rows", [])
    print(f"=== 検索キーワードTOP{args.top}（過去{args.days}日） ===\n")

    if not rows:
        print("データなし")
        return

    for i, r in enumerate(rows, 1):
        print(f"{i:2}. {r[0]:<40} {r[1]:>8,.0f}回 | {r[2]:,.0f}分")


def cmd_daily(analytics, youtube, args):
    """日別パフォーマンス"""
    start, end = date_range(args.days)
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=start,
        endDate=end,
        metrics="views,estimatedMinutesWatched,subscribersGained,subscribersLost,estimatedRevenue",
        dimensions="day",
        sort="-day",
    ).execute()

    rows = resp.get("rows", [])
    print(f"=== 日別パフォーマンス（過去{args.days}日） ===\n")

    if not rows:
        print("データなし")
        return

    print(f"{'日付':<12} {'視聴':>8} {'再生分':>8} {'登録±':>6} {'収益$':>8}")
    print("-" * 50)
    for r in rows:
        net_sub = r[3] - r[4]
        print(f"{r[0]:<12} {r[1]:>8,.0f} {r[2]:>8,.0f} {net_sub:>+6,.0f} {r[5]:>8.2f}")


def cmd_realtime(analytics, youtube, args):
    """直近のリアルタイムデータ（過去7日の日別）"""
    start, end = date_range(7)
    resp = analytics.reports().query(
        ids=f"channel=={CHANNEL_ID}",
        startDate=start,
        endDate=end,
        metrics="views,estimatedMinutesWatched,subscribersGained,subscribersLost",
        dimensions="day",
        sort="-day",
    ).execute()

    rows = resp.get("rows", [])
    print(f"=== 直近7日間 ===\n")

    if not rows:
        print("データなし")
        return

    for r in rows:
        net_sub = r[3] - r[4]
        print(f"{r[0]}  視聴:{r[1]:>6,.0f}  再生:{r[2]:>6,.0f}分  登録:{net_sub:>+4,.0f}")


def _get_video_titles(youtube, video_ids):
    """Data APIで動画タイトルを取得"""
    if not video_ids:
        return {}
    titles = {}
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        resp = youtube.videos().list(
            part="snippet",
            id=",".join(batch),
        ).execute()
        for item in resp.get("items", []):
            titles[item["id"]] = item["snippet"]["title"]
    return titles


COMMANDS = {
    "overview": cmd_overview,
    "top-videos": cmd_top_videos,
    "revenue": cmd_revenue,
    "video": cmd_video,
    "retention": cmd_retention,
    "traffic": cmd_traffic,
    "demographics": cmd_demographics,
    "search-terms": cmd_search_terms,
    "daily": cmd_daily,
    "realtime": cmd_realtime,
}


def main():
    parser = argparse.ArgumentParser(description="Yama_Story YouTube Analytics CLI")
    parser.add_argument("command", choices=COMMANDS.keys(), help="実行するコマンド")
    parser.add_argument("video_id", nargs="?", help="動画ID（video/retention/trafficコマンド用）")
    parser.add_argument("--days", type=int, default=28, help="対象期間（デフォルト: 28日）")
    parser.add_argument("--top", type=int, default=10, help="表示件数（デフォルト: 10）")

    args = parser.parse_args()

    if args.command in ("video", "retention", "traffic") and not args.video_id:
        parser.error(f"{args.command} コマンドには動画IDが必要です")

    try:
        analytics, youtube = get_authenticated_services()
        COMMANDS[args.command](analytics, youtube, args)
    except HttpError as e:
        print(f"API Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
