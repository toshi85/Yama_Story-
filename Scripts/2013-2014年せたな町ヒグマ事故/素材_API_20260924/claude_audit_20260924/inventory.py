#!/usr/bin/env python3
"""納品フォルダの棚卸し: 画像の寸法・モード・実アルファ、動画の尺、SHA256"""
import json, hashlib, subprocess, re, collections
from pathlib import Path
from PIL import Image
D = Path.home() / "Desktop/せたな町_素材_20260924"
rows = {}
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()
for p in sorted((D / "画像").glob("*.png")):
    m = re.match(r"(ASSET-\d{3})_(\w+)\.png", p.name)
    if not m: continue
    with Image.open(p) as im:
        mode, size = im.mode, im.size
        alpha_real = None
        if "A" in mode:
            a = im.getchannel("A")
            lo, hi = a.getextrema()
            # 透明画素の割合
            hist = a.histogram(); transparent = sum(hist[:16]) / (size[0]*size[1])
            alpha_real = {"min": lo, "max": hi, "transparent_ratio": round(transparent, 3)}
    rows.setdefault(m.group(1), {})[m.group(2)] = {"path": f"画像/{p.name}", "size": size, "mode": mode, "alpha": alpha_real, "sha256": sha(p)}
for p in sorted((D / "動画").glob("*.mp4")):
    m = re.match(r"(ASSET-\d{3})_video\.mp4", p.name)
    if not m: continue
    pr = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height,r_frame_rate:format=duration","-of","json",str(p)],capture_output=True,text=True)
    j = json.loads(pr.stdout); st = j["streams"][0]
    rows.setdefault(m.group(1), {})["video"] = {"path": f"動画/{p.name}", "size": [st["width"], st["height"]], "fps": st["r_frame_rate"], "duration": round(float(j["format"]["duration"]),2), "sha256": sha(p)}
Path("inventory.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1)+"\n")
c = collections.Counter()
for a, files in rows.items():
    c[tuple(sorted(files))] += 1
print("assets with files:", len(rows)); print(c)
sizes = collections.Counter((k, tuple(v["size"])) for f in rows.values() for k, v in f.items())
print("sizes:", sizes)
badalpha = [a for a, f in rows.items() if "char" in f and (f["char"]["alpha"] is None or f["char"]["alpha"]["transparent_ratio"] < 0.05)]
print("char without real alpha:", badalpha)
bgalpha = [a for a, f in rows.items() for k in ("still","bg") if k in f and f[k]["alpha"] and f[k]["alpha"]["transparent_ratio"] > 0.01]
print("still/bg with transparency:", bgalpha)
vd = [f["video"]["duration"] for f in rows.values() if "video" in f]
print("video durations: n=%d min=%.1f max=%.1f" % (len(vd), min(vd), max(vd)))
