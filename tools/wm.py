"""Polite Wikimedia API helper with caching and retry (no API key needed)."""
import json, time, urllib.request, urllib.parse, urllib.error, os, hashlib

UA = "SieunStudyBuilder/1.0 (non-commercial kids learning app; python-urllib)"
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)
_last = [0.0]

def get(url, params=None, cache=True, binary=False, min_gap=1.2):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    key = hashlib.sha1(url.encode()).hexdigest()
    path = os.path.join(CACHE_DIR, key + (".bin" if binary else ".json"))
    if cache and os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        return data if binary else json.loads(data)
    for attempt in range(8):
        wait = min_gap - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if cache:
                with open(path, "wb") as f:
                    f.write(data)
            return data if binary else json.loads(data)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503, 502):
                ra = e.headers.get("retry-after")
                t = int(ra) + 1 if ra and ra.isdigit() else 5 * (attempt + 1)
                print(f"  rate limited ({e.code}), sleeping {t}s", flush=True)
                time.sleep(t)
                continue
            raise
        except Exception as e:
            print("  error", e, "retrying", flush=True)
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("failed: " + url)

def api(host, **params):
    params.setdefault("format", "json")
    params.setdefault("formatversion", "2")
    return get(f"https://{host}/w/api.php", params)
