#!/usr/bin/env python3
"""
Yama_Story 週次トレンド分析スクリプト

daily/ のJSONを読み、前週比・異常値・トレンドを検出。
結果はJSONで出力し、Claude Codeが読んで仮説生成するためのインプット。

出力: stdout（JSON）— SessionStart hookがClaude Codeに渡す
"""

import json
import statistics
import sys
from datetime import datetime, timedelta
from pathlib import Path

ANALYTICS_DIR = Path(__file__).resolve().parent.parent / "Analytics" / "daily"


def load_week_data(end_date, days=7):
    """指定終了日から過去N日分のdaily JSONを読む"""
    data = []
    for i in range(days):
        d = end_date - timedelta(days=i)
        path = ANALYTICS_DIR / f"{d.isoformat()}.json"
        if path.exists():
            with open(path) as f:
                data.append(json.load(f))
    data.sort(key=lambda x: x["date"])
    return data


def summarize_week(data):
    """週のサマリー指標を計算"""
    if not data:
        return None

    overviews = [d["overview"] for d in data if d.get("overview")]
    if not overviews:
        return None

    return {
        "days_collected": len(overviews),
        "total_views": sum(o["views"] for o in overviews),
        "total_watch_minutes": sum(o["watch_minutes"] for o in overviews),
        "total_subs_net": sum(o["subs_gained"] - o["subs_lost"] for o in overviews),
        "total_revenue_usd": sum(o["revenue_usd"] for o in overviews),
        "avg_daily_views": statistics.mean([o["views"] for o in overviews]),
        "avg_view_duration_sec": statistics.mean([o["avg_view_duration_sec"] for o in overviews]),
    }


def compare_weeks(this_week, prev_week):
    """前週比を計算"""
    if not this_week or not prev_week:
        return None

    def pct_change(curr, prev):
        if prev == 0:
            return None
        return round((curr - prev) / prev * 100, 1)

    return {
        "views_change_pct": pct_change(this_week["total_views"], prev_week["total_views"]),
        "watch_minutes_change_pct": pct_change(this_week["total_watch_minutes"], prev_week["total_watch_minutes"]),
        "subs_change_pct": pct_change(this_week["total_subs_net"], prev_week["total_subs_net"]),
        "revenue_change_pct": pct_change(this_week["total_revenue_usd"], prev_week["total_revenue_usd"]),
        "avg_duration_change_pct": pct_change(this_week["avg_view_duration_sec"], prev_week["avg_view_duration_sec"]),
    }


def detect_anomalies(this_week_data, baseline_data):
    """異常値を検出（過去4週の平均±2σ）"""
    if len(baseline_data) < 14:
        return []

    baseline_views = []
    for d in baseline_data:
        if d.get("overview"):
            baseline_views.append(d["overview"]["views"])

    if len(baseline_views) < 7:
        return []

    mean_views = statistics.mean(baseline_views)
    stdev_views = statistics.stdev(baseline_views) if len(baseline_views) > 1 else 0

    anomalies = []
    for d in this_week_data:
        if not d.get("overview"):
            continue
        views = d["overview"]["views"]
        if stdev_views > 0 and abs(views - mean_views) > 2 * stdev_views:
            direction = "spike" if views > mean_views else "dip"
            anomalies.append({
                "date": d["date"],
                "views": views,
                "mean": round(mean_views),
                "stdev": round(stdev_views),
                "direction": direction,
                "sigma": round((views - mean_views) / stdev_views, 1),
            })

    return anomalies


def analyze_search_trends(this_week_data, prev_week_data):
    """検索キーワードの変化を検出"""
    def aggregate_terms(data):
        terms = {}
        for d in data:
            for t in d.get("search_terms", []):
                term = t["term"]
                terms[term] = terms.get(term, 0) + t["views"]
        return terms

    this_terms = aggregate_terms(this_week_data)
    prev_terms = aggregate_terms(prev_week_data)

    # 新出キーワード（前週にはなかった）
    new_terms = {k: v for k, v in this_terms.items() if k not in prev_terms and v >= 3}

    # 急上昇キーワード（前週比2倍以上）
    rising = {}
    for k, v in this_terms.items():
        if k in prev_terms and prev_terms[k] > 0:
            ratio = v / prev_terms[k]
            if ratio >= 2.0:
                rising[k] = {"views": v, "prev_views": prev_terms[k], "ratio": round(ratio, 1)}

    # 消失キーワード（前週あったが今週ゼロ）
    disappeared = {k: v for k, v in prev_terms.items() if k not in this_terms and v >= 5}

    return {
        "new_terms": dict(sorted(new_terms.items(), key=lambda x: -x[1])[:10]),
        "rising_terms": dict(sorted(rising.items(), key=lambda x: -x[1]["ratio"])[:10]),
        "disappeared_terms": dict(sorted(disappeared.items(), key=lambda x: -x[1])[:10]),
        "top_terms_this_week": dict(sorted(this_terms.items(), key=lambda x: -x[1])[:15]),
    }


def analyze_traffic_trends(this_week_data, prev_week_data):
    """トラフィックソースの変化"""
    def aggregate_traffic(data):
        sources = {}
        for d in data:
            for t in d.get("traffic_sources", []):
                src = t["source"]
                sources[src] = sources.get(src, 0) + t["views"]
        return sources

    this_traffic = aggregate_traffic(this_week_data)
    prev_traffic = aggregate_traffic(prev_week_data)

    changes = {}
    all_sources = set(list(this_traffic.keys()) + list(prev_traffic.keys()))
    for src in all_sources:
        curr = this_traffic.get(src, 0)
        prev = prev_traffic.get(src, 0)
        if prev > 0:
            change = round((curr - prev) / prev * 100, 1)
        elif curr > 0:
            change = None  # 新規ソース
        else:
            continue
        changes[src] = {
            "views": curr,
            "prev_views": prev,
            "change_pct": change,
        }

    return changes


def analyze_top_video_trends(this_week_data):
    """今週のトップ動画パフォーマンス"""
    video_stats = {}
    for d in this_week_data:
        for v in d.get("top_videos", []):
            vid = v["video_id"]
            if vid not in video_stats:
                video_stats[vid] = {
                    "video_id": vid,
                    "total_views": 0,
                    "total_watch_minutes": 0,
                    "days_in_top": 0,
                    "avg_view_pct": [],
                }
            video_stats[vid]["total_views"] += v["views"]
            video_stats[vid]["total_watch_minutes"] += v["watch_minutes"]
            video_stats[vid]["days_in_top"] += 1
            if v["avg_view_percentage"] > 0:
                video_stats[vid]["avg_view_pct"].append(v["avg_view_percentage"])

    # 平均維持率を計算
    for v in video_stats.values():
        pcts = v["avg_view_pct"]
        v["avg_view_percentage"] = round(statistics.mean(pcts), 1) if pcts else 0
        del v["avg_view_pct"]

    # 視聴回数順でソート
    ranked = sorted(video_stats.values(), key=lambda x: -x["total_views"])
    return ranked[:10]


def main():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    # 今週と前週のデータを読む
    this_week_data = load_week_data(yesterday, days=7)
    prev_week_end = yesterday - timedelta(days=7)
    prev_week_data = load_week_data(prev_week_end, days=7)

    # 異常値検出用に過去28日分を読む
    baseline_data = load_week_data(prev_week_end, days=21)

    if not this_week_data:
        print(json.dumps({"error": "今週のデータがありません。daily_collector.py を先に実行してください。"}, ensure_ascii=False))
        sys.exit(1)

    this_summary = summarize_week(this_week_data)
    prev_summary = summarize_week(prev_week_data)
    comparison = compare_weeks(this_summary, prev_summary)

    report = {
        "report_date": today.isoformat(),
        "period": {
            "this_week": f"{this_week_data[0]['date']} ~ {this_week_data[-1]['date']}",
            "prev_week": f"{prev_week_data[0]['date']} ~ {prev_week_data[-1]['date']}" if prev_week_data else None,
        },
        "this_week_summary": this_summary,
        "prev_week_summary": prev_summary,
        "week_over_week": comparison,
        "anomalies": detect_anomalies(this_week_data, baseline_data),
        "search_trends": analyze_search_trends(this_week_data, prev_week_data),
        "traffic_trends": analyze_traffic_trends(this_week_data, prev_week_data),
        "top_videos": analyze_top_video_trends(this_week_data),
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
