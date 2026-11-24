"""모든 문제 데이터의 사진·소리 링크가 실제로 열리는지 검사한다.
   python3 tools/check_links.py            # 전체 검사 (결과: tools/link_report.json)
   python3 tools/check_links.py --save     # 검사하면서 이미지를 tools/.cache/img 에 저장 (사진 검토용)
"""
import json, os, sys, time, hashlib, urllib.request, urllib.error, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
UA = "SieunStudyBuilder/1.0 (link checker for a non-commercial kids app)"
IMG_DIR = os.path.join(HERE, ".cache", "img"); os.makedirs(IMG_DIR, exist_ok=True)

def collect():
    urls = {}
    for fn in sorted(os.listdir(os.path.join(ROOT, "data"))):
        d = json.load(open(os.path.join(ROOT, "data", fn), encoding="utf-8"))
        def walk(o, where):
            if isinstance(o, dict):
                for k in ("url", "remote"):
                    v = o.get(k)
                    if isinstance(v, str) and (v.startswith("http") or v.startswith("assets/")):
                        urls.setdefault(v, set()).add(where)
                for v in o.values(): walk(v, where)
            elif isinstance(o, list):
                for v in o: walk(v, where)
        for it in d.get("items", []): walk(it, it.get("id", fn))
        for k in ("coins", "objects", "goods"): walk(d.get(k), fn + ":" + k)
    snd = os.path.join(ROOT, "assets", "sounds", "sounds.json")
    if os.path.exists(snd):
        for k, v in json.load(open(snd, encoding="utf-8")).items():
            urls.setdefault(v["url"], set()).add(k)
    return urls

def check(url, save):
    if not url.startswith("http"):
        p = os.path.join(ROOT, url)
        return url, (200 if os.path.exists(p) and os.path.getsize(p) > 500 else 404), None
    path = os.path.join(IMG_DIR, hashlib.sha1(url.encode()).hexdigest() + os.path.splitext(url.split("?")[0])[1][:5])
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return url, 200, path
    for attempt in range(12):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
                ct = r.headers.get("content-type", "")
            if not (ct.startswith("image/") or ct.startswith("audio/")):
                return url, f"bad-type {ct}", None
            if save:
                open(path, "wb").write(data)
            time.sleep(2.5)
            return url, 200, path if save else None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                ra = e.headers.get("retry-after", "")
                t = (int(ra) if ra.isdigit() else 30) + 5
                print(f"   429, {t}s 대기", flush=True); time.sleep(t); continue
            return url, e.code, None
        except Exception as e:
            time.sleep(3 + attempt * 3)
            err = str(e)
    return url, "error " + err, None

def main():
    save = "--save" in sys.argv
    urls = collect()
    print("검사할 링크", len(urls), flush=True)
    bad = {}; ok = 0; files = {}
    with cf.ThreadPoolExecutor(1) as ex:
        for i, (u, st, path) in enumerate(ex.map(lambda u: check(u, save), sorted(urls))):
            if st == 200:
                ok += 1
                if path: files[u] = path
            else:
                bad[u] = {"status": st, "used_by": sorted(urls[u])[:5]}
            if i % 50 == 0: print(" ", i, flush=True)
    json.dump({"ok": ok, "bad": bad, "files": files}, open(os.path.join(HERE, "link_report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"정상 {ok} / 깨짐 {len(bad)}")
    for u, b in list(bad.items())[:50]: print("  ✗", b["status"], u, b["used_by"])
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
