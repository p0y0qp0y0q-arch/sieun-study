"""Resolve media refs to Wikimedia Commons thumbnail URLs + credits.

refs:
  wp:Title      -> lead image of English Wikipedia article
  ko:제목        -> lead image of Korean Wikipedia article
  file:Name.jpg -> a specific Commons file
Results cached in tools/media_cache.json (committed, so builds are reproducible).
"""
import json, os, re, html
import wm

HERE = os.path.dirname(__file__)
CACHE = os.path.join(HERE, "media_cache.json")
OK_LICENSE = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?[- ]?[\d.]*|cc by(-sa)? [\d.]+.*|cc-by(-sa)?-[\d.]+.*)", re.I)
BAD_LICENSE = re.compile(r"nc|nd|fair use|non-free", re.I)

def load():
    if os.path.exists(CACHE):
        return json.load(open(CACHE, encoding="utf-8"))
    return {}

def save(c):
    json.dump(c, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)

def strip_html(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    s = html.unescape(s).strip()
    s = re.sub(r"\s+", " ", s)
    return s[:80]

def thumb(url_original, width):
    # https://upload.wikimedia.org/wikipedia/commons/a/ab/Name.jpg -> .../thumb/a/ab/Name.jpg/500px-Name.jpg
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons)/(\w)/(\w\w)/([^?]+)", url_original)
    if not m:
        return None
    base, a, ab, name = m.groups()
    if name.lower().endswith(".svg"):
        return f"{base}/{a}/{ab}/{name}"  # SVG served directly (flags)
    suffix = ".png" if name.lower().endswith((".tif", ".tiff")) else ""
    return f"{base}/thumb/{a}/{ab}/{name}/{width}px-{name}{suffix}"

def _chunks(xs, n=40):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]

def resolve(refs, cache):
    todo_wp = {}
    for r in refs:
        if r in cache:
            continue
        kind, _, val = r.partition(":")
        if kind in ("wp", "ko"):
            todo_wp.setdefault(kind, []).append(val)
    # 1) article -> pageimage filename
    for kind, titles in todo_wp.items():
        host = "en.wikipedia.org" if kind == "wp" else "ko.wikipedia.org"
        for ch in _chunks(titles):
            print(f"pageimages {kind} x{len(ch)}", flush=True)
            res = wm.api(host, action="query", prop="pageimages", piprop="name", redirects=1, titles="|".join(ch))
            q = res.get("query", {})
            back = {}
            for n in q.get("normalized", []) + q.get("redirects", []):
                back[n["to"]] = back.get(n["from"], n["from"])
            for p in q.get("pages", []):
                orig = p["title"]
                while orig in back and back[orig] != orig:
                    orig = back[orig]
                ref = f"{kind}:{orig}"
                if ref not in [f"{kind}:{t}" for t in ch]:
                    # try matching loosely
                    for t in ch:
                        if t.replace("_", " ") == orig:
                            ref = f"{kind}:{t}"
                fn = p.get("pageimage")
                cache[ref] = {"file": fn} if fn else {"missing": True}
            for t in ch:
                cache.setdefault(f"{kind}:{t}", {"missing": True})
    # 2) filenames -> imageinfo
    files = set()
    for r in refs:
        kind, _, val = r.partition(":")
        if kind == "file":
            files.add(val.replace(" ", "_"))
        elif cache.get(r, {}).get("file"):
            files.add(cache[r]["file"].replace(" ", "_"))
    need = [f for f in files if "file:" + f not in cache]
    for ch in _chunks(sorted(need)):
        print(f"imageinfo x{len(ch)}", flush=True)
        res = wm.api("commons.wikimedia.org", action="query", prop="imageinfo",
                     iiprop="url|extmetadata|size|mime", iiextmetadatafilter="Artist|LicenseShortName|UsageTerms",
                     titles="|".join("File:" + f for f in ch))
        q = res.get("query", {})
        norm = {n["to"]: n["from"] for n in q.get("normalized", [])}
        for p in q.get("pages", []):
            src = norm.get(p["title"], p["title"])[5:].replace(" ", "_")
            ii = (p.get("imageinfo") or [None])[0]
            if not ii or p.get("missing"):
                cache["file:" + src] = {"missing": True}
                continue
            md = ii.get("extmetadata", {})
            lic = strip_html(md.get("LicenseShortName", {}).get("value", ""))
            artist = strip_html(md.get("Artist", {}).get("value", "")) or "Unknown"
            url = ii["url"].split("?")[0]
            cache["file:" + src] = {
                "orig": url, "w": ii.get("width"), "h": ii.get("height"), "mime": ii.get("mime"),
                "license": lic, "artist": artist, "page": ii.get("descriptionurl", "").split("?")[0],
            }
        for f in ch:
            cache.setdefault("file:" + f, {"missing": True})
    return cache

def license_ok(lic):
    l = (lic or "").strip()
    if not l or re.search(r"\b(nc|nd)\b|fair use|non-free|copyrighted\b(?! free)", l, re.I):
        return False
    return bool(re.match(r"(public domain|pd\b|pd-|cc0|cc[ -]by|attribution|copyrighted free use|no restrictions|kogl type 1|fal\b|free art)", l, re.I))

def lookup(ref, cache, width=500, allow_currency=False):
    """Return image dict {url, credit, page} or None."""
    if not ref:
        return None
    kind, _, val = ref.partition(":")
    if kind == "file":
        info = cache.get("file:" + val.replace(" ", "_"))
    else:
        e = cache.get(ref, {})
        if not e.get("file"):
            return None
        info = cache.get("file:" + e["file"].replace(" ", "_"))
    if not info or info.get("missing") or not (license_ok(info.get("license")) or (allow_currency and info.get("license") == "South Korean currency")):
        return None
    if not str(info.get("mime", "image/")).startswith("image/"):
        return None  # 동영상·소리 파일은 사진으로 쓰지 않음
    url = thumb(info["orig"], width)
    if not url:
        return None
    if info.get("w") and info["w"] <= width and not url.endswith(".svg"):
        url = info["orig"]
    return {"url": url, "credit": f'{info["artist"]}, {info["license"]}, Wikimedia Commons', "page": info.get("page", "")}
