#!/usr/bin/env python3
"""
Yama_Story 自動パフォーマンス分析システム

YouTube Data API v3でチャンネル全動画の統計を取得し、
コードベースの統計分析でパターンを抽出する（外部AI API不要）。

使い方:
  python3 Yama_Story/Tools/yama_auto_analyzer.py
"""

import json
import logging
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from glob import glob as globfn
from pathlib import Path

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("ERROR: google-api-python-client がインストールされていません")
    print("  pip install google-api-python-client")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv がインストールされていません")
    print("  pip install python-dotenv")
    sys.exit(1)

# パス設定
SCRIPT_DIR = Path(__file__).resolve().parent
YAMA_ROOT = SCRIPT_DIR.parent
PROJECT_ROOT = YAMA_ROOT.parent
PERF_DATA_DIR = YAMA_ROOT / "Performance_Data"
LOG_MD = YAMA_ROOT / "Video_Performance_Log.md"
PATTERNS_MD = YAMA_ROOT / "Learned_Patterns_Yama.md"

# .env 読み込み
for env_path in [PROJECT_ROOT / ".env", SCRIPT_DIR / ".env"]:
    if env_path.exists():
        load_dotenv(env_path)
        break

# ログ設定
PERF_DATA_DIR.mkdir(parents=True, exist_ok=True)
log_path = PERF_DATA_DIR / "analyzer.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# 環境変数
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YAMA_CHANNEL_ID = os.getenv("YAMA_CHANNEL_ID", "UCKAQUNCqCPoly21DfTrClwA")

# テーマ分類キーワード
THEME_KEYWORDS = {
    "熊事件": ["熊", "ヒグマ", "クマ", "熊襲撃", "熊事件", "人喰い"],
    "雪山・冬山": ["雪山", "冬山", "吹雪", "猛吹雪", "雪崩", "凍", "低体温"],
    "滑落": ["滑落", "転落"],
    "遭難（一般）": ["遭難", "行方不明", "下山"],
    "総集編": ["総集編"],
    "海外": ["海外", "ランナー", "マラソン"],
}


def parse_duration(duration_iso):
    """ISO 8601 duration → 秒数"""
    if not duration_iso:
        return 0
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_iso)
    if not match:
        return 0
    h = int(match.group(1) or 0)
    m = int(match.group(2) or 0)
    s = int(match.group(3) or 0)
    return h * 3600 + m * 60 + s


def format_number(n):
    """数字を日本語表記（1.2万 等）"""
    if n is None:
        return "N/A"
    n = int(n)
    if n >= 10_000:
        return f"{n / 10_000:.1f}万"
    if n >= 1_000:
        return f"{n / 1_000:.1f}千"
    return str(n)


def format_duration_min(seconds):
    """秒数→分表記"""
    if seconds <= 0:
        return "0分"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}分"
    hours = minutes // 60
    remaining = minutes % 60
    return f"{hours}時間{remaining}分"


def classify_theme(title):
    """タイトルからテーマを分類"""
    for theme, keywords in THEME_KEYWORDS.items():
        for kw in keywords:
            if kw in title:
                return theme
    return "その他"


def classify_duration_bucket(duration_sec):
    """尺をバケットに分類"""
    minutes = duration_sec // 60
    if minutes <= 15:
        return "〜15分"
    elif minutes <= 25:
        return "16〜25分"
    elif minutes <= 35:
        return "26〜35分"
    elif minutes <= 60:
        return "36〜60分"
    else:
        return "60分超（総集編）"


# ============================================================
# Step 1: YouTube API で全動画統計を取得
# ============================================================

def fetch_all_videos(youtube):
    """チャンネルの全動画統計を取得"""
    logger.info(f"チャンネル {YAMA_CHANNEL_ID} の動画を取得中...")

    ch_resp = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        id=YAMA_CHANNEL_ID,
    ).execute()

    if not ch_resp.get("items"):
        logger.error(f"チャンネル {YAMA_CHANNEL_ID} が見つかりません")
        sys.exit(1)

    ch_info = ch_resp["items"][0]
    uploads_playlist = ch_info["contentDetails"]["relatedPlaylists"]["uploads"]
    ch_stats = ch_info["statistics"]
    logger.info(
        f"チャンネル: {ch_info['snippet']['title']} | "
        f"登録者: {format_number(ch_stats.get('subscriberCount'))} | "
        f"総動画数: {ch_stats.get('videoCount')}"
    )

    # uploadsプレイリストから全動画IDを取得
    video_ids = []
    next_page = None
    while True:
        pl_resp = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist,
            maxResults=50,
            pageToken=next_page,
        ).execute()
        for item in pl_resp.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])
        next_page = pl_resp.get("nextPageToken")
        if not next_page:
            break

    logger.info(f"動画ID取得完了: {len(video_ids)}本")

    # 動画詳細を50件ずつ取得
    videos = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        detail_resp = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(batch),
        ).execute()

        for item in detail_resp.get("items", []):
            stats = item.get("statistics", {})
            duration_sec = parse_duration(
                item.get("contentDetails", {}).get("duration", "PT0S")
            )
            published = item["snippet"]["publishedAt"]
            published_date = published[:10]

            pub_dt = datetime.strptime(published_date, "%Y-%m-%d")
            weekday_jp = ["月", "火", "水", "木", "金", "土", "日"][pub_dt.weekday()]

            title = item["snippet"]["title"]
            videos.append({
                "video_id": item["id"],
                "title": title,
                "published": published_date,
                "weekday": weekday_jp,
                "duration_sec": duration_sec,
                "duration_label": format_duration_min(duration_sec),
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0)),
                "url": f"https://www.youtube.com/watch?v={item['id']}",
                "theme": classify_theme(title),
                "duration_bucket": classify_duration_bucket(duration_sec),
            })

    videos.sort(key=lambda x: x["published"], reverse=True)
    logger.info(f"動画詳細取得完了: {len(videos)}本")

    return {
        "channel_id": YAMA_CHANNEL_ID,
        "channel_name": ch_info["snippet"]["title"],
        "subscribers": int(ch_stats.get("subscriberCount", 0)),
        "total_videos": int(ch_stats.get("videoCount", 0)),
        "snapshot_date": datetime.now().strftime("%Y-%m-%d"),
        "videos": videos,
    }


# ============================================================
# Step 2: スナップショット保存 & 差分計算
# ============================================================

def save_snapshot(data):
    """JSONスナップショットを保存"""
    date_str = data["snapshot_date"]
    path = PERF_DATA_DIR / f"snapshot_{date_str}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"スナップショット保存: {path}")
    return path


def load_previous_snapshot():
    """前回のスナップショットを読み込む"""
    pattern = str(PERF_DATA_DIR / "snapshot_*.json")
    files = sorted(globfn(pattern))
    if len(files) < 2:
        return None
    prev_path = files[-2]
    logger.info(f"前回スナップショット: {prev_path}")
    with open(prev_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_diff(current, previous):
    """前回との差分を計算"""
    if not previous:
        return None

    prev_map = {v["video_id"]: v for v in previous["videos"]}
    diff = {
        "period": f"{previous['snapshot_date']} → {current['snapshot_date']}",
        "new_videos": [],
        "growing": [],
        "stagnant": [],
        "total_view_change": 0,
    }

    prev_total = sum(v["views"] for v in previous["videos"])
    curr_total = sum(v["views"] for v in current["videos"])
    diff["total_view_change"] = curr_total - prev_total

    for video in current["videos"]:
        vid = video["video_id"]
        if vid not in prev_map:
            diff["new_videos"].append(video)
            continue

        prev_views = prev_map[vid]["views"]
        curr_views = video["views"]
        if prev_views == 0:
            growth = 100.0 if curr_views > 0 else 0.0
        else:
            growth = (curr_views - prev_views) / prev_views * 100

        entry = {
            **video,
            "prev_views": prev_views,
            "view_growth": curr_views - prev_views,
            "growth_rate": round(growth, 1),
        }

        if growth >= 20:
            diff["growing"].append(entry)
        elif growth < 5:
            diff["stagnant"].append(entry)

    diff["growing"].sort(key=lambda x: x["growth_rate"], reverse=True)
    diff["stagnant"].sort(key=lambda x: x["views"], reverse=True)

    return diff


# ============================================================
# Step 3: 統計分析（コードベース、AI API不要）
# ============================================================

def analyze_statistics(data, diff):
    """全動画データから統計パターンを抽出"""
    videos = data["videos"]
    if not videos:
        return {}

    total_views = sum(v["views"] for v in videos)
    avg_views = total_views // len(videos)

    # --- テーマ別パフォーマンス ---
    theme_stats = defaultdict(lambda: {"views": [], "titles": []})
    for v in videos:
        theme_stats[v["theme"]]["views"].append(v["views"])
        theme_stats[v["theme"]]["titles"].append(v["title"][:40])

    theme_perf = {}
    for theme, stats in theme_stats.items():
        views = stats["views"]
        avg = sum(views) // len(views)
        theme_perf[theme] = {
            "count": len(views),
            "avg_views": avg,
            "max_views": max(views),
            "total_views": sum(views),
            "vs_avg": round((avg - avg_views) / avg_views * 100, 1) if avg_views > 0 else 0,
        }

    # --- 尺別パフォーマンス ---
    bucket_stats = defaultdict(list)
    for v in videos:
        bucket_stats[v["duration_bucket"]].append(v["views"])

    duration_perf = {}
    for bucket, views in bucket_stats.items():
        avg = sum(views) // len(views)
        duration_perf[bucket] = {
            "count": len(views),
            "avg_views": avg,
            "vs_avg": round((avg - avg_views) / avg_views * 100, 1) if avg_views > 0 else 0,
        }

    # --- 曜日別パフォーマンス ---
    weekday_stats = defaultdict(list)
    for v in videos:
        weekday_stats[v["weekday"]].append(v["views"])

    weekday_perf = {}
    for day, views in weekday_stats.items():
        avg = sum(views) // len(views)
        weekday_perf[day] = {
            "count": len(views),
            "avg_views": avg,
            "vs_avg": round((avg - avg_views) / avg_views * 100, 1) if avg_views > 0 else 0,
        }

    # --- いいね率（エンゲージメント） ---
    for v in videos:
        v["like_rate"] = round(v["likes"] / v["views"] * 100, 2) if v["views"] > 0 else 0

    # --- 伸びるパターン / 伸びないパターン ---
    sorted_by_views = sorted(videos, key=lambda x: x["views"], reverse=True)
    top_half = sorted_by_views[:len(sorted_by_views) // 2]
    bottom_half = sorted_by_views[len(sorted_by_views) // 2:]

    # TOP動画の共通特徴
    top_themes = defaultdict(int)
    top_buckets = defaultdict(int)
    top_weekdays = defaultdict(int)
    for v in top_half:
        top_themes[v["theme"]] += 1
        top_buckets[v["duration_bucket"]] += 1
        top_weekdays[v["weekday"]] += 1

    bottom_themes = defaultdict(int)
    bottom_buckets = defaultdict(int)
    for v in bottom_half:
        bottom_themes[v["theme"]] += 1
        bottom_buckets[v["duration_bucket"]] += 1

    # --- タイトル構造分析 ---
    title_patterns = {
        "数字あり": 0,
        "疑問形": 0,
        "省略記号（…）": 0,
        "【】タグ": 0,
        "結末系": 0,
    }
    title_pattern_views = defaultdict(list)
    for v in videos:
        t = v["title"]
        if re.search(r"\d+人|[\d]+名|[\d]+歳|\d{4}年", t):
            title_patterns["数字あり"] += 1
            title_pattern_views["数字あり"].append(v["views"])
        if "？" in t or "?" in t or "なぜ" in t or "とは" in t:
            title_patterns["疑問形"] += 1
            title_pattern_views["疑問形"].append(v["views"])
        if "…" in t or "..." in t:
            title_patterns["省略記号（…）"] += 1
            title_pattern_views["省略記号（…）"].append(v["views"])
        if "【" in t:
            title_patterns["【】タグ"] += 1
            title_pattern_views["【】タグ"].append(v["views"])
        if "結果" in t or "末路" in t or "結末" in t:
            title_patterns["結末系"] += 1
            title_pattern_views["結末系"].append(v["views"])

    title_perf = {}
    for pattern, views in title_pattern_views.items():
        if views:
            avg = sum(views) // len(views)
            title_perf[pattern] = {
                "count": len(views),
                "avg_views": avg,
                "vs_avg": round((avg - avg_views) / avg_views * 100, 1) if avg_views > 0 else 0,
            }

    return {
        "total_views": total_views,
        "avg_views": avg_views,
        "video_count": len(videos),
        "theme_perf": theme_perf,
        "duration_perf": duration_perf,
        "weekday_perf": weekday_perf,
        "title_perf": title_perf,
        "top_videos": sorted_by_views[:5],
        "bottom_videos": sorted_by_views[-5:],
        "top_themes": dict(top_themes),
        "bottom_themes": dict(bottom_themes),
    }


def format_analysis_report(stats, diff):
    """統計分析結果をMarkdownレポートに整形"""
    lines = []

    # --- 伸びるパターン ---
    lines.append("## 伸びるパターン")
    lines.append("| パターン | 根拠動画数 | 平均再生数 | チャンネル平均比 |")
    lines.append("|:--|--:|--:|--:|")

    all_patterns = []

    for theme, data in stats["theme_perf"].items():
        if data["vs_avg"] > 0:
            all_patterns.append((f"テーマ: {theme}", data["count"], data["avg_views"], data["vs_avg"]))

    for bucket, data in stats["duration_perf"].items():
        if data["vs_avg"] > 0:
            all_patterns.append((f"尺: {bucket}", data["count"], data["avg_views"], data["vs_avg"]))

    for pattern, data in stats["title_perf"].items():
        if data["vs_avg"] > 0:
            all_patterns.append((f"タイトル: {pattern}", data["count"], data["avg_views"], data["vs_avg"]))

    for day, data in stats["weekday_perf"].items():
        if data["vs_avg"] > 20 and data["count"] >= 2:
            all_patterns.append((f"投稿曜日: {day}曜", data["count"], data["avg_views"], data["vs_avg"]))

    all_patterns.sort(key=lambda x: x[3], reverse=True)
    for name, count, avg, vs in all_patterns:
        lines.append(f"| {name} | {count}本 | {format_number(avg)} | +{vs}% |")
    lines.append("")

    # --- 伸びないパターン ---
    lines.append("## 伸びないパターン")
    lines.append("| パターン | 根拠動画数 | 平均再生数 | チャンネル平均比 |")
    lines.append("|:--|--:|--:|--:|")

    bad_patterns = []
    for theme, data in stats["theme_perf"].items():
        if data["vs_avg"] < -20:
            bad_patterns.append((f"テーマ: {theme}", data["count"], data["avg_views"], data["vs_avg"]))
    for bucket, data in stats["duration_perf"].items():
        if data["vs_avg"] < -20:
            bad_patterns.append((f"尺: {bucket}", data["count"], data["avg_views"], data["vs_avg"]))
    for pattern, data in stats["title_perf"].items():
        if data["vs_avg"] < -20:
            bad_patterns.append((f"タイトル: {pattern}", data["count"], data["avg_views"], data["vs_avg"]))

    bad_patterns.sort(key=lambda x: x[3])
    for name, count, avg, vs in bad_patterns:
        lines.append(f"| {name} | {count}本 | {format_number(avg)} | {vs}% |")
    lines.append("")

    # --- テーマ別パフォーマンス ---
    lines.append("## テーマ別パフォーマンス")
    lines.append("| テーマ | 動画数 | 平均再生数 | 最高再生数 | 平均比 |")
    lines.append("|:--|--:|--:|--:|--:|")
    for theme, data in sorted(stats["theme_perf"].items(), key=lambda x: x[1]["avg_views"], reverse=True):
        sign = "+" if data["vs_avg"] >= 0 else ""
        lines.append(
            f"| {theme} | {data['count']}本 | {format_number(data['avg_views'])} | "
            f"{format_number(data['max_views'])} | {sign}{data['vs_avg']}% |"
        )
    lines.append("")

    # --- 尺別パフォーマンス ---
    lines.append("## 尺別パフォーマンス")
    lines.append("| 尺 | 動画数 | 平均再生数 | 平均比 |")
    lines.append("|:--|--:|--:|--:|")
    bucket_order = ["〜15分", "16〜25分", "26〜35分", "36〜60分", "60分超（総集編）"]
    for bucket in bucket_order:
        if bucket in stats["duration_perf"]:
            data = stats["duration_perf"][bucket]
            sign = "+" if data["vs_avg"] >= 0 else ""
            lines.append(f"| {bucket} | {data['count']}本 | {format_number(data['avg_views'])} | {sign}{data['vs_avg']}% |")
    lines.append("")

    # --- 曜日別パフォーマンス ---
    lines.append("## 曜日別パフォーマンス")
    lines.append("| 曜日 | 動画数 | 平均再生数 | 平均比 |")
    lines.append("|:--|--:|--:|--:|")
    for day in ["月", "火", "水", "木", "金", "土", "日"]:
        if day in stats["weekday_perf"]:
            data = stats["weekday_perf"][day]
            sign = "+" if data["vs_avg"] >= 0 else ""
            lines.append(f"| {day} | {data['count']}本 | {format_number(data['avg_views'])} | {sign}{data['vs_avg']}% |")
    lines.append("")

    # --- タイトル構造分析 ---
    lines.append("## タイトル構造パフォーマンス")
    lines.append("| パターン | 該当動画数 | 平均再生数 | 平均比 |")
    lines.append("|:--|--:|--:|--:|")
    for pattern, data in sorted(stats["title_perf"].items(), key=lambda x: x[1]["avg_views"], reverse=True):
        sign = "+" if data["vs_avg"] >= 0 else ""
        lines.append(f"| {pattern} | {data['count']}本 | {format_number(data['avg_views'])} | {sign}{data['vs_avg']}% |")
    lines.append("")

    # --- TOP / BOTTOM 動画 ---
    lines.append("## TOP5 動画")
    for i, v in enumerate(stats["top_videos"], 1):
        lines.append(f"{i}. **{v['title'][:50]}** — {format_number(v['views'])}再生（{v['theme']} / {v['duration_label']} / {v['weekday']}曜）")
    lines.append("")

    lines.append("## BOTTOM5 動画")
    for i, v in enumerate(stats["bottom_videos"], 1):
        lines.append(f"{i}. **{v['title'][:50]}** — {format_number(v['views'])}再生（{v['theme']} / {v['duration_label']} / {v['weekday']}曜）")
    lines.append("")

    # --- 前回比較 ---
    if diff:
        lines.append(f"## 週間変動（{diff['period']}）")
        lines.append(f"- 総再生数変化: +{format_number(diff['total_view_change'])}")
        lines.append(f"- 成長動画（+20%以上）: {len(diff['growing'])}本")
        lines.append(f"- 停滞動画（+5%未満）: {len(diff['stagnant'])}本")
        lines.append(f"- 新規投稿: {len(diff['new_videos'])}本")
        if diff["growing"]:
            lines.append("\n### 成長動画TOP")
            for v in diff["growing"][:5]:
                lines.append(f"- {v['title'][:40]}: {format_number(v['prev_views'])}→{format_number(v['views'])}（+{v['growth_rate']}%）")
        if diff["new_videos"]:
            lines.append("\n### 新規動画")
            for v in diff["new_videos"]:
                lines.append(f"- {v['title'][:40]}: {format_number(v['views'])}再生")
        lines.append("")

    return "\n".join(lines)


# ============================================================
# Step 4: Markdown ファイル更新
# ============================================================

def update_performance_log(data):
    """Video_Performance_Log.md を更新"""
    today = data["snapshot_date"]

    lines = [
        "# Yama_Story Video Performance Log",
        "",
        f"最終更新: {today} | 動画数: {len(data['videos'])}本 | "
        f"登録者: {format_number(data['subscribers'])}",
        "",
        "## 全動画パフォーマンス（再生数順）",
        "",
        "| # | タイトル | 再生数 | いいね | コメント | 公開日 | 曜日 | 尺 | テーマ |",
        "|:--|:--|--:|--:|--:|:--|:--|:--|:--|",
    ]

    sorted_videos = sorted(data["videos"], key=lambda x: x["views"], reverse=True)
    for i, v in enumerate(sorted_videos, 1):
        lines.append(
            f"| {i} | {v['title'][:50]} | {v['views']:,} | "
            f"{v['likes']:,} | {v['comments']:,} | {v['published']} | "
            f"{v['weekday']} | {v['duration_label']} | {v['theme']} |"
        )

    total_views = sum(v["views"] for v in data["videos"])
    avg_views = total_views // len(data["videos"]) if data["videos"] else 0
    total_likes = sum(v["likes"] for v in data["videos"])
    avg_duration = (
        sum(v["duration_sec"] for v in data["videos"]) // len(data["videos"])
        if data["videos"] else 0
    )

    lines.extend([
        "",
        "## サマリー",
        "",
        f"- 総再生数: {total_views:,}",
        f"- 平均再生数: {avg_views:,}",
        f"- 総いいね数: {total_likes:,}",
        f"- 平均尺: {format_duration_min(avg_duration)}",
        f"- 最高再生: {sorted_videos[0]['title'][:40]}（{sorted_videos[0]['views']:,}回）" if sorted_videos else "",
    ])

    with open(LOG_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    logger.info(f"Performance Log 更新: {LOG_MD}")


def update_learned_patterns(data, diff, analysis_report):
    """Learned_Patterns_Yama.md を更新"""
    today = data["snapshot_date"]

    total_views = sum(v["views"] for v in data["videos"])
    avg_views = total_views // len(data["videos"]) if data["videos"] else 0

    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    recent = [v for v in data["videos"] if v["published"] >= cutoff]
    recent_views = sum(v["views"] for v in recent)

    # 既存の分析履歴を保持
    history_section = ""
    if PATTERNS_MD.exists():
        existing = PATTERNS_MD.read_text(encoding="utf-8")
        hist_match = re.search(r"(## 分析履歴\n.+)", existing, re.DOTALL)
        if hist_match:
            history_section = hist_match.group(1)

    # 新しいエントリを追加
    new_entry = f"### {today}\n\n{analysis_report}\n"

    if history_section:
        history_section = history_section.replace(
            "## 分析履歴\n",
            f"## 分析履歴\n\n{new_entry}\n---\n\n",
            1,
        )
    else:
        history_section = f"## 分析履歴\n\n{new_entry}"

    content = f"""# Yama_Story パフォーマンス学習DB

> このファイルは毎週月曜に自動更新されます。
> Yamaスキル（/write-yama-script, /research-yama-idea 等）が参照し、
> 伸びるパターンに基づいた企画・台本・サムネを提案します。

## 最新分析サマリー（{today}）
- 動画総数: {len(data['videos'])}本
- チャンネル登録者: {format_number(data['subscribers'])}
- チャンネル平均再生数: {format_number(avg_views)}
- 直近30日の新規動画: {len(recent)}本（合計{format_number(recent_views)}再生）

{analysis_report}

{history_section}
"""

    with open(PATTERNS_MD, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Learned Patterns 更新: {PATTERNS_MD}")


# ============================================================
# メイン処理
# ============================================================

def main():
    logger.info("=" * 60)
    logger.info("Yama_Story 自動パフォーマンス分析 開始")
    logger.info("=" * 60)

    if not YOUTUBE_API_KEY:
        logger.error("YOUTUBE_API_KEY が .env に設定されていません")
        sys.exit(1)

    # Step 1: YouTube API で全動画統計を取得
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    try:
        data = fetch_all_videos(youtube)
    except HttpError as e:
        if e.resp.status == 403:
            logger.error("YouTube API クォータ制限に達しました")
        else:
            logger.error(f"YouTube API エラー: {e}")
        sys.exit(1)

    if not data["videos"]:
        logger.warning("動画が0本です。処理を中断します。")
        sys.exit(0)

    # Step 2: スナップショット保存 & 差分計算
    save_snapshot(data)
    previous = load_previous_snapshot()
    diff = compute_diff(data, previous)

    if diff:
        logger.info(
            f"前回比較: 成長{len(diff['growing'])}本 / "
            f"新規{len(diff['new_videos'])}本 / "
            f"停滞{len(diff['stagnant'])}本"
        )
    else:
        logger.info("初回実行（前回データなし）")

    # Step 3: 統計分析
    stats = analyze_statistics(data, diff)
    analysis_report = format_analysis_report(stats, diff)

    # Step 4: Markdown ファイル更新
    update_performance_log(data)
    update_learned_patterns(data, diff, analysis_report)

    logger.info("=" * 60)
    logger.info("Yama_Story 自動パフォーマンス分析 完了")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
