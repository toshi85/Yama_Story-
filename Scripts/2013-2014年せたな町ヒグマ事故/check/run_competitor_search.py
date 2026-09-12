#!/usr/bin/env python3
import datetime, hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path
C = Path(__file__).resolve().parent
QUERIES = ["せたな町 ヒグマ", "せたな町 クマ 山菜採り", "2013年 北海道 山菜採り ヒグマ 死亡", "今金町 ヒグマ 捕獲 DNA"]
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name, data):
    # Writes stay inside the authorized check directory.
    (C / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
state = {"status": "starting", "pid": os.getpid(), "started_at": now(), "query_index": 0, "worker_pid": None, "completed_queries": 0, "next_action": "検索終了後、Codexが同一事件の有無を判定し、Layer 0・Master.md執筆・9検査・全文5周・Gemini台本レビューへ進む"}
result = {"started_at": state["started_at"], "status": "running", "method": "yt-dlp youtube:player_client=android; search20; metadata only; no media download", "same_incident_assessment": "pending_manual_review", "searches": []}
save("competitor_search_state.json", state)
save("competitor_search.json", result)
exe = shutil.which("yt-dlp")
try:
    if not exe:
        raise RuntimeError("yt-dlp not found")
    for i, query in enumerate(QUERIES, 1):
        raw = C / f"competitor_search_{i:02d}_raw.json"
        err = C / f"competitor_search_{i:02d}.stderr.log"
        argv = [exe, "--extractor-args", "youtube:player_client=android", "--skip-download", "--dump-single-json", "--ignore-no-formats-error", "--no-progress", "--no-cache-dir", "--retries", "0", "--extractor-retries", "0", "--socket-timeout", "20", "ytsearch20:" + query]
        record = {"query": query, "limit": 20, "argv": argv, "started_at": now(), "raw_json": str(raw), "stderr": str(err)}
        print(f"START query {i}/4 {query}", flush=True)
        with raw.open("w") as output, err.open("w") as errors:
            proc = subprocess.Popen(argv, stdout=output, stderr=errors, stdin=subprocess.DEVNULL)
            state.update(status="running", query_index=i, worker_pid=proc.pid, current_query=query, updated_at=now())
            save("competitor_search_state.json", state)
            try:
                code = proc.wait(timeout=1800)
            except subprocess.TimeoutExpired:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                code = 124
        record.update(exit_code=code, ended_at=now(), raw_sha256=hashlib.sha256(raw.read_bytes()).hexdigest())
        if code != 0:
            result["searches"].append(record)
            raise RuntimeError(f"query {i} failed, exit {code}; subsequent queries stopped; inspect stderr before any retry")
        data = json.loads(raw.read_text())
        entries = []
        for rank, e in enumerate(data.get("entries", []), 1):
            if not isinstance(e, dict):
                continue
            entries.append({"rank": rank, "id": e.get("id"), "title": e.get("title"), "channel": e.get("channel") or e.get("uploader"), "channel_id": e.get("channel_id"), "view_count": e.get("view_count"), "upload_date": e.get("upload_date"), "timestamp": e.get("timestamp"), "webpage_url": e.get("webpage_url"), "description": e.get("description"), "duration": e.get("duration")})
        record.update(entries=entries, entry_count=len(entries), missing_required_fields=[{"rank": e["rank"], "fields": [k for k in ("title", "channel", "view_count", "upload_date") if e[k] is None]} for e in entries if any(e[k] is None for k in ("title", "channel", "view_count", "upload_date"))])
        result["searches"].append(record)
        save("competitor_search.json", result)
        state.update(completed_queries=i, worker_pid=None, updated_at=now())
        save("competitor_search_state.json", state)
        print(f"END query {i}/4 exit={code} entries={len(entries)}", flush=True)
    result.update(status="retrieval_complete_review_required", ended_at=now(), total_entries=sum(r.get("entry_count", 0) for r in result["searches"]), unique_videos=len({e["id"] for r in result["searches"] for e in r.get("entries", [])}))
    state.update(status="retrieval_complete_review_required", worker_pid=None, exit_code=0, ended_at=now())
except Exception as exc:
    result.update(status="failed", error=str(exc), ended_at=now())
    state.update(status="failed", worker_pid=None, exit_code=1, error=str(exc), ended_at=now())
    print(f"STOP: {exc}", flush=True)
finally:
    save("competitor_search.json", result)
    save("competitor_search_state.json", state)
print(f"FINAL status={state['status']} completed_queries={state['completed_queries']}/4", flush=True)
sys.exit(state["exit_code"])
