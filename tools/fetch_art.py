"""미술 문제의 명화 사진(퍼블릭 도메인)을 assets/art/ 에 내려받아 앱에 포함한다."""
import os, sys, json, hashlib, shutil, time, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "content"))
import media, art, wm
OUT = os.path.join(ROOT, "assets", "art"); os.makedirs(OUT, exist_ok=True)
IMG = os.path.join(HERE, ".cache", "img")

def main():
    cache = media.load()
    ov = json.load(open(os.path.join(HERE, "image_overrides.json"), encoding="utf-8"))
    _, rows = art.build()
    for i, r in enumerate(rows):
        dst = os.path.join(OUT, f"art-{i:02d}.jpg")
        if os.path.exists(dst):
            continue
        ref = ov.get(r["ref"], r["ref"])
        info = media.lookup(ref, cache)
        if not info:
            print("사진 없음", r["t"]); continue
        url = info["url"]
        cached = os.path.join(IMG, hashlib.sha1(url.encode()).hexdigest() + os.path.splitext(url)[1][:5])
        if os.path.exists(cached):
            shutil.copy(cached, dst); print("복사", r["t"]); continue
        for attempt in range(8):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": wm.UA})
                with urllib.request.urlopen(req, timeout=60) as resp:
                    open(dst, "wb").write(resp.read())
                print("받음", r["t"]); time.sleep(1); break
            except urllib.error.HTTPError as e:
                if e.code != 429: print("실패", r["t"], e); break
                time.sleep(20 * (attempt + 1))

if __name__ == "__main__":
    main()
