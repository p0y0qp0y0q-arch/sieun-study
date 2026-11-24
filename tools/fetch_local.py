"""앱에 직접 넣을 이미지(명화, 한자 옛 글자)를 내려받는다. 목록은 build.py 가 만든 tools/local_media.json.
위키미디어 요청 제한(429)을 만나면 안내된 시간만큼 기다렸다가 다시 시도한다."""
import os, json, time, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
UA = "SieunStudyBuilder/1.0 (non-commercial kids learning app; python-urllib)"

def main():
    todo = json.load(open(os.path.join(HERE, "local_media.json"), encoding="utf-8"))
    done = 0
    for local, url in todo.items():
        dst = os.path.join(ROOT, local)
        if os.path.exists(dst) and os.path.getsize(dst) > 0:
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        for attempt in range(15):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                    open(dst, "wb").write(r.read())
                done += 1; print("받음", local, flush=True); time.sleep(1.5); break
            except urllib.error.HTTPError as e:
                if e.code != 429:
                    print("실패", local, e.code, flush=True); break
                ra = e.headers.get("retry-after", ""); t = (int(ra) if ra.isdigit() else 30) + 5
                print("  429, 대기", t, flush=True); time.sleep(t)
    print("새로 받은 파일", done)

if __name__ == "__main__":
    main()
