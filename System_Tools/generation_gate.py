#!/usr/bin/env python3
"""Yama素材の生成スクリプト共通の関所（2026-09-25 新設）。

誰が（Claude・Codex・人間）、どの経路で（fal有料API・ChatGPTブラウザ・Codex内蔵生成）生成しても、
生成スクリプトの中で次の4つを必ず通す。フックはAIの種類ごとに効き方が違うが、ここはスクリプト自身が止める。

  1. 合格票: 生成する全プロンプトの全文（1文ずつ）が、check_prompts_all.py の合格票がある .md に含まれる。
     2026-09-25 までの照合は先頭200文字だけで、201文字目以降に足した文が素通りしていた。
  2. 見本の本人確認: 本人の承認前は、同じ .md（基準キャラ部分が同じ版）から作れるのは素材の種類
     （キャラ基準・キャラ・背景・静止画・追加素材／動画）ごとに1件の見本だけ。全種類の見本がそろうまで承認できない。
     承認は本人が自分のターミナルで `python generation_gate.py approve <md> --kind image` を打つ（AIの非対話実行では通らない）。
     2026-09-24 せたな町で、見本を見ずに全件を有料発注し、全員後ろ向き・頭身崩れで全面差し戻しになった。
  3. 発注記録: 生成の直前に、ID・全文・合格票・経路を <作品>/発注記録/ に書く（gitで残る）。
     2026-09-24 の有料発注の計画ファイルが別PCにしか無く、何を発注したか後から確かめられなかった。
  4. 本人に渡す前のAI検品: 渡す画像は、今の中身・今のカットで ai_image_review.py（Sol→Astra）を通り、
     「直す」判定が残っていないこと（check_handoff_folder.py・regen.py の書き出しで止める）。
  5. 失敗は止める側に倒す: .md が特定できない・票が読めない等はすべて停止。

使い方（スクリプトから）:
    from generation_gate import require
    allowed = require('image', [{'id': 'ASSET-019_char', 'prompt': '...'}], tool='fal_queue.py', paid=True, paths=[...])
本人の承認（本人のターミナルで）:
    python Yama_Story-/System_Tools/generation_gate.py approve <Asset_Prompts.md> --kind image
状態の確認:
    python Yama_Story-/System_Tools/generation_gate.py status <Asset_Prompts.md>
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
YAMA_REPO = HERE.parent
ROOT = YAMA_REPO.parent                       # D:\0（Mac では Antigravity）
STATE = ROOT / ".claude" / ".state"
STAMPS = STATE / "prompt_checks"
APPROVALS = STATE / "sample_approvals"
USAGE = STATE / "sample_usage"
REVIEWS = STATE / "image_reviews"
YAMA_DIRS = {"Yama_Story", "Yama_Story-"}


class GateError(RuntimeError):
    pass


def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def is_yama(*paths):
    """Yamaの作品か。リポジトリ配下・作品フォルダ名・デスクトップの「<作品>_素材_」を見る。"""
    names = set()
    scripts = YAMA_REPO / "Scripts"
    if scripts.is_dir():
        names = {p.name for p in scripts.iterdir() if p.is_dir()}
    for p in paths:
        if not p:
            continue
        parts = Path(str(p)).parts
        if YAMA_DIRS & set(parts) or names & set(parts):
            return True
        if any(any(n and n.split("年")[-1][:4] in part and "_素材_" in part for n in names) for part in parts):
            return True
    return False


def owner_machine():
    """本人のPCか（Yama_Story- の親に Antigravity 本体＝.claude/settings.json がある）。受講生の環境では False。"""
    return (ROOT / ".claude" / "settings.json").is_file()


def valid_stamps():
    """[(票, .mdのパス, 正規化本文)]。票の sha256 が .md の今の中身と一致するものだけ。"""
    out = []
    if not STAMPS.is_dir():
        return out
    for f in STAMPS.glob("*.json"):
        if f.name == "last_run.json":
            continue
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
            p = Path(rec["file"])
            if rec.get("status") == "PASS" and p.is_file() \
                    and hashlib.sha256(p.read_bytes()).hexdigest() == rec["sha256"]:
                out.append((rec, p, norm(p.read_text(encoding="utf-8"))))
        except Exception:
            continue
    return out


def allowed_prompts(md_path):
    """その .md から生成してよいプロンプト全文の集合（正規化済み）。

    (a) .md のコードブロックそのもの（fal・Codex の経路。一字一句そのまま使う）
    (b) extract_prompts.py が .md から作るキューの文面（ChatGPT 経路。画風文だけコードで差し替える）
    2026-09-25: 先頭200文字や1文ごとの部分一致では、後から足した文や1語だけの文面が通った。全文一致に変更。
    """
    text = Path(md_path).read_text(encoding="utf-8")
    out = {norm(b) for b in re.findall(r"```[^\n]*\n(.*?)```", text, re.S) if norm(b)}
    try:
        sys.path.insert(0, str(HERE / "imagegen"))
        import extract_prompts as ep
        out |= {norm(it["prompt"]) for it in ep.parse(Path(md_path)) if norm(it.get("prompt", ""))}
    except Exception:
        pass
    return out


def source_md(items, stamps):
    """全アイテムの全文を含む票付き .md（1つ）。見つからなければ None。"""
    for rec, path, body in stamps:
        allowed = allowed_prompts(path)
        if all(norm(it["prompt"]) in allowed for it in items):
            return path, body
    return None, None


def header_key(md_path):
    """見本承認の単位＝.md のパス＋冒頭（基準キャラ・画風）部分。本文カットの修正では承認は切れない。"""
    text = Path(md_path).read_text(encoding="utf-8")
    m = re.search(r"^(?:ナレーター:|\*\*ナレ行\*\*:)", text, re.M)
    head = text[:m.start()] if m else text
    return hashlib.sha256((str(Path(md_path).resolve()) + "\n" + head).encode("utf-8")).hexdigest()[:16]


def slot_of(item_id, kind):
    """見本の種類。キャラ基準（CHAR-xx）・キャラ・背景・静止画・追加素材、動画は1種類。"""
    if kind == "video":
        return "video"
    s = str(item_id)
    if re.match(r"CHAR-\d+", s):
        return "char_ref"
    m = re.match(r"ASSET-\d+_(char|bg|still|overlay)\b", s)
    if m:
        return m.group(1)
    if s.startswith("typed:"):
        return "typed"
    return "other"


def slots_in_md(md_path, kind):
    """その .md から作る素材の種類（見本がそろっているかの判定用）。"""
    if kind == "video":
        return {"video"}
    try:
        sys.path.insert(0, str(HERE / "imagegen"))
        import extract_prompts as ep
        return {slot_of(it["id"], kind) for it in ep.parse(Path(md_path))}
    except Exception:
        return set()


def approved(md_path, kind):
    f = APPROVALS / f"{header_key(md_path)}_{kind}.json"
    return f.is_file()


def _usage_file(md_path, kind):
    return USAGE / f"{header_key(md_path)}_{kind}.json"


def require(kind, items, *, tool, paid, paths=(), record=True):
    """関所本体。通ってよいアイテムのリストを返す（承認前は見本枠の分だけ）。止めるときは GateError。

    kind: 'image' | 'video'   items: [{'id','prompt'}]   paid: 有料APIなら True
    有料（paid=True）は見本枠を超える分を黙って間引かず、全体を止める（何が作られなかったか曖昧にしない）。
    """
    if kind not in {"image", "video"}:
        raise GateError(f"種類の指定が不正: {kind}")
    items = [{"id": str(i.get("id")), "prompt": str(i.get("prompt") or "")} for i in items]
    if not items:
        return []
    howto = ("\n  先に: python Yama_Story-/System_Tools/check_prompts_all.py <プロンプト.md> を失敗0・警告0で通し、"
             "生成するプロンプトはその .md から一字一句そのまま使う。")
    empty = [i["id"] for i in items if not norm(i["prompt"])]
    if empty:
        raise GateError(f"プロンプトが空のアイテムがあるため止めました: {', '.join(empty[:10])}")
    stamps = valid_stamps()
    if not stamps:
        raise GateError("有効な合格票が1枚もないため止めました。" + howto)
    md, body = source_md(items, stamps)
    if md is None:
        pool = set().union(*(allowed_prompts(p) for _, p, _ in stamps))
        bad = [i for i in items if norm(i["prompt"]) not in pool]
        if bad:
            sample = "; ".join(f"{i['id']}: 「{norm(i['prompt'])[:90]}…」" for i in bad[:5])
            raise GateError(f"合格票のある .md のプロンプトと全文一致しないものが {len(bad)}件あるため止めました"
                            f"（1文でも足す・削る・書き換えると別物）。{sample}" + howto)
        raise GateError("全アイテムを含む合格票付きの .md が1つに特定できないため止めました（複数の .md にまたがる発注は分ける）。" + howto)

    # ブラウザ入力（typed:…）は .md のどのカットかに読み替える（見本の種類を正しく数えるため）
    if any(i["id"].startswith("typed:") for i in items):
        try:
            sys.path.insert(0, str(HERE / "imagegen"))
            import extract_prompts as ep
            by_prompt = {norm(it["prompt"]): it["id"] for it in ep.parse(Path(md))}
            for i in items:
                if i["id"].startswith("typed:"):
                    i["id"] = by_prompt.get(norm(i["prompt"]), i["id"])
        except Exception:
            pass

    allowed = items
    if not approved(md, kind):
        # 承認前は「種類（キャラ基準・キャラ・背景・静止画・追加素材／動画）ごとに1件」だけ。
        # 2026-09-25: 先頭3件を見本にすると背景3枚だけで承認でき、キャラの崩れを見ずに全体へ進めた
        uf = _usage_file(md, kind)
        used = json.loads(uf.read_text(encoding="utf-8")) if uf.is_file() else []
        sampled = {slot_of(u, kind) for u in used}
        keep, extra = set(used), []
        for i in items:
            if i["id"] in keep:
                continue
            s = slot_of(i["id"], kind)
            if s in sampled:
                extra.append(i["id"])
            else:
                keep.add(i["id"])
                sampled.add(s)
        if extra:
            msg = (f"本人が見本を承認する前なので、作れるのは種類ごとに1件の見本だけです（見本済み: {', '.join(sorted(sampled))}）。"
                   f"止めた {len(extra)}件: {', '.join(extra[:8])}{' …' if len(extra) > 8 else ''}\n"
                   f"  見本を本人に見せ、本人が自分のターミナルで次を打ってから全体を作る:\n"
                   f"    python {HERE / 'generation_gate.py'} approve \"{md}\" --kind {kind}")
            if paid:
                raise GateError(msg + "\n  （有料発注は間引かず全体を止めます。--only で見本だけを指定して発注する）")
            allowed = [i for i in items if i["id"] in keep]
            if not allowed:
                raise GateError(msg)
            print("⚠️ " + msg + f"\n  → 今回は見本 {', '.join(i['id'] for i in allowed if i['id'] not in used) or 'なし'} だけ作ります。", flush=True)
        USAGE.mkdir(parents=True, exist_ok=True)
        uf.write_text(json.dumps(sorted(set(used) | {i["id"] for i in allowed}), ensure_ascii=False), encoding="utf-8")

    if record:
        # 一括の確認のあと1件ずつ再確認するスクリプトでも、同じIDの記録は1回だけ書く
        fresh = [i for i in allowed if (str(md), kind, i["id"]) not in _RECORDED]
        if fresh:
            write_record(md, kind, fresh, tool=tool, paid=paid, paths=paths)
            _RECORDED.update((str(md), kind, i["id"]) for i in fresh)
    return allowed


_RECORDED = set()


def record_image_review(image_sha, rec):
    """ai_image_review.py が1枚ごとに書く検品記録。キー＝画像の中身の sha256 ＋カット番号
    （再利用カットは同じ中身の画像が複数のカットに入るため、中身だけだと記録がぶつかる）。"""
    REVIEWS.mkdir(parents=True, exist_ok=True)
    rec = dict(rec, at=datetime.datetime.now().isoformat(timespec="seconds"))
    (REVIEWS / f"{image_sha}_{int(rec['asset']):03d}.json").write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")


def image_review(image_sha, asset):
    f = REVIEWS / f"{image_sha}_{int(asset):03d}.json"
    try:
        return json.loads(f.read_text(encoding="utf-8")) if f.is_file() else None
    except Exception:
        return None


def check_reviewed(paths):
    """本人に渡す前の関所。ASSET-NNN_*.png が「今の中身・今のカット」でAI検品（Sol→Astra）を通っているか。

    問題の一覧を返す（空なら渡してよい）。「本人判断」は渡してよい（一覧.md で本人が決める）。
    2026-09-25: 検品ツールはあったが手順書にあるだけで、飛ばしても本人に渡せた。
    """
    sys.path.insert(0, str(HERE / "imagegen"))
    import ai_image_review as air
    problems, digests = [], {}
    for p in sorted(Path(x) for x in paths):
        if not re.match(r"ASSET-\d{3}_", p.name) or p.suffix.lower() != ".png":
            continue
        rec = image_review(hashlib.sha256(p.read_bytes()).hexdigest(), int(p.name[6:9]))
        if not rec:
            problems.append(f"{p.name}: AI検品（ai_image_review.py）をまだ通っていない（差し替えた画像も検品し直す）")
            continue
        md = rec.get("md", "")
        if md not in digests:
            try:
                digests[md] = {c.asset: air.cut_digest(c) for c in air.parse_cuts(Path(md))}
            except Exception:
                digests[md] = {}
        if digests[md].get(rec.get("asset")) != rec.get("cut_digest"):
            problems.append(f"{p.name}: 検品のあとでナレーション・シーン・プロンプトが変わった（検品し直す）")
        elif rec.get("sol_flag") and rec.get("astra_verdict") is None:
            problems.append(f"{p.name}: Sol が指摘したのに Astra の判定が無い（検品をやり直す）")
        elif rec.get("astra_verdict") == "直す":
            problems.append(f"{p.name}: AI検品で「直す」判定（作り直して検品し直す）")
    return problems


def write_record(md, kind, items, *, tool, paid, paths):
    out = Path(md).parent / "発注記録"
    out.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now()
    f = out / f"{now:%Y%m%d_%H%M%S}_{kind}_{re.sub(r'[^A-Za-z0-9_.-]', '_', tool)}.json"
    f.write_text(json.dumps({
        "at": now.isoformat(timespec="seconds"), "tool": tool, "kind": kind, "paid": paid,
        "md": str(md), "md_sha256": hashlib.sha256(Path(md).read_bytes()).hexdigest(),
        "sample_approved": approved(md, kind), "paths": [str(p) for p in paths if p],
        "items": items,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    return f


def cmd_approve(a):
    md = Path(a.md).resolve()
    if not md.is_file():
        sys.exit(f"見つかりません: {md}")
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        sys.exit("承認は本人が自分のターミナルで打つものです（AIの非対話実行からは承認できません）。")
    uf = _usage_file(md, a.kind)
    used = json.loads(uf.read_text(encoding="utf-8")) if uf.is_file() else []
    missing = slots_in_md(md, a.kind) - {slot_of(u, a.kind) for u in used}
    if missing:
        sys.exit(f"見本がそろっていないため承認できません。まだ見本が無い種類: {', '.join(sorted(missing))}"
                 "（キャラ・背景・静止画など、この .md で作る種類ごとに1件ずつ見本を作ってから承認する）")
    print(f"対象: {md}\n種類: {a.kind}\n見本: {', '.join(used)}\n"
          "見本の画像・動画を自分の目で見て、向き・頭身・背景・画風に問題がなければ「承認」と入力してください。")
    if input("> ").strip() != "承認":
        sys.exit("承認しませんでした。")
    APPROVALS.mkdir(parents=True, exist_ok=True)
    f = APPROVALS / f"{header_key(md)}_{a.kind}.json"
    f.write_text(json.dumps({"md": str(md), "kind": a.kind, "at": datetime.datetime.now().isoformat(timespec="seconds")},
                            ensure_ascii=False), encoding="utf-8")
    print(f"承認しました: {f.name}（この .md の冒頭＝基準キャラ・画風を書き換えると承認は切れます）")


def cmd_status(a):
    md = Path(a.md).resolve()
    stamped = any(p.resolve() == md for _, p, _ in valid_stamps())
    print(f"合格票: {'あり' if stamped else 'なし'}")
    for kind in ("image", "video"):
        uf = _usage_file(md, kind)
        used = json.loads(uf.read_text(encoding="utf-8")) if uf.is_file() else []
        need = slots_in_md(md, kind) - {slot_of(u, kind) for u in used}
        print(f"{kind}: 見本承認={'済' if approved(md, kind) else '未'}／見本 {used}／まだ見本が無い種類 {sorted(need) or 'なし'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("approve")
    p.add_argument("md")
    p.add_argument("--kind", choices=["image", "video"], required=True)
    p.set_defaults(func=cmd_approve)
    p = sub.add_parser("status")
    p.add_argument("md")
    p.set_defaults(func=cmd_status)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
