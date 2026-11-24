"""받아 둔 사진(tools/.cache/img)을 한눈에 보는 검토용 모음 이미지 만들기."""
import os, sys, json, hashlib, glob
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
IMG = os.path.join(HERE, ".cache", "img")
out_dir = sys.argv[1]
labels = {}
for fn in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
    d = json.load(open(fn, encoding="utf-8"))
    def walk(o, ctx):
        if isinstance(o, dict):
            u = o.get("remote") or o.get("url")
            if isinstance(u, str) and u.startswith("http"):
                labels.setdefault(u, f"{os.path.basename(fn)[:4]} {ctx}")
            for v in o.values(): walk(v, ctx)
        elif isinstance(o, list):
            for v in o: walk(v, ctx)
    for it in d["items"]:
        ans = it.get("choices", [None])[it.get("answer", 0)] if it.get("choices") else ""
        walk(it, ans if isinstance(ans, str) else (ans or {}).get("label", "") if isinstance(ans, dict) else "")
items = []
for u, lab in labels.items():
    p = os.path.join(IMG, hashlib.sha1(u.encode()).hexdigest() + os.path.splitext(u.split("?")[0])[1][:5])
    if os.path.exists(p): items.append((lab, p))
items.sort()
T = 150; cols = 8; rows = 6; per = cols * rows
for s in range(0, len(items), per):
    sheet = Image.new("RGB", (cols * T, rows * (T + 14)), "white"); d = ImageDraw.Draw(sheet)
    for k, (lab, p) in enumerate(items[s:s + per]):
        try:
            im = Image.open(p).convert("RGB"); im.thumbnail((T, T))
        except Exception:
            continue
        x, y = (k % cols) * T, (k // cols) * (T + 14)
        sheet.paste(im, (x + (T - im.width) // 2, y))
        d.text((x + 2, y + T), str(s + k), fill="red")
        print(s + k, lab)
    sheet.save(os.path.join(out_dir, f"sheet_{s // per:02d}.png"))
print(len(items), "장")
