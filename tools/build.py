"""데이터 빌드: tools/content/*.py → data/*.json
   python3 tools/build.py          (캐시만 사용)
   python3 tools/build.py --fetch  (모르는 사진은 위키미디어에서 찾아 캐시에 저장)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "content"))
import media
import korean, english, mathq, hanja, art, world, nature, store, sports, music, env, people, society, timeq, folktale, world2, idiom, science

SOUNDS = os.path.join(ROOT, "assets", "sounds", "sounds.json")
OVERRIDES = os.path.join(HERE, "image_overrides.json")   # 사진 수동 교체/제외: {"wp:Dog": "file:X.jpg" 또는 null}

def load_sounds():
    if os.path.exists(SOUNDS):
        return json.load(open(SOUNDS, encoding="utf-8"))
    return {}

def all_subjects(sounds):
    math_items, math_objs = mathq.build()
    art_items, art_rows = art.build()
    store_items, store_goods = store.build(None)
    music_items, _ = music.build(sounds)
    return {
        "korean": {"subject": "국어", "items": korean.build()},
        "english": {"subject": "영어", "items": english.build()},
        "calc": {"subject": "연산", "items": [], "generators": mathq.CALC_GENERATORS},
        "math": {"subject": "창의 수학", "items": [i for i in math_items if i["level"] >= 2] + mathq.build_puzzles(), "objects": math_objs, "generators": mathq.GENERATORS},
        "hanja": {"subject": "한자", "items": hanja.build(), "generators": hanja.GENERATORS},
        "art": {"subject": "미술", "items": art_items},
        "world": {"subject": "세계", "items": world.build() + world2.build()},
        "nature": {"subject": "자연", "items": nature.build(sounds)},
        "store": {"subject": "가게", "items": store_items, "goods": store_goods, "generators": store.GENERATORS},
        "sports": {"subject": "운동", "items": sports.build()},
        "music": {"subject": "악기", "items": music_items},
        "env": {"subject": "환경", "items": env.build()},
        "people": {"subject": "사람", "items": people.build()},
        "society": {"subject": "사회", "items": society.build()},
        "science": {"subject": "과학", "items": science.build()},
        "idiom": {"subject": "관용구·속담", "items": idiom.build()},
        "folktale": {"subject": "전래동화", "items": folktale.build()},
        "time": {"subject": "시간", "items": timeq.build(), "generators": timeq.GENERATORS},
    }

COIN_FILES = {10: "file:10_won_2006_obverse.jpeg", 50: "file:50_won_1983_obverse.jpeg", 100: "file:100_won_1983_obverse.jpeg",
              500: "file:500_won_1982_obverse.jpeg", 1000: "file:1000_won_serieIII_obverse.jpeg",
              5000: "file:5000_won_serieV_obverse.jpeg", 10000: "file:10000_won_serieVI_obverse.jpeg"}

def walk_imgs(o, fn):
    if isinstance(o, dict):
        if "fallbackEmoji" in o and "ref" in o:
            fn(o)
        for v in list(o.values()):
            walk_imgs(v, fn)
    elif isinstance(o, list):
        for v in o:
            walk_imgs(v, fn)

def main():
    fetch = "--fetch" in sys.argv
    sounds = load_sounds()
    data = all_subjects(sounds)
    overrides = json.load(open(OVERRIDES, encoding="utf-8")) if os.path.exists(OVERRIDES) else {}
    refs = set(COIN_FILES.values())
    def col(o):
        r = o.get("ref")
        if r in overrides:
            r = overrides[r]
        if r:
            refs.add(r)
    walk_imgs(data, col)
    cache = media.load()
    if fetch:
        media.resolve(sorted(refs), cache)
        media.save(cache)
    missing = []
    local_media = {}
    def res(o):
        r = o.pop("ref")
        if r in overrides:
            r = overrides[r]
        local = o.pop("local", None)
        info = media.lookup(r, cache) if r else None
        if info:
            if local:
                local_media[local] = info["url"]
            o["url"] = local if local and os.path.exists(os.path.join(ROOT, local)) else info["url"]
            o["remote"] = info["url"]
            o["credit"] = info["credit"]
            o["source"] = info["page"]
        elif r:
            missing.append(r)
        for k in [k for k, v in o.items() if v is None]:
            del o[k]
    walk_imgs(data, res)
    coins = {}
    for v, ref in COIN_FILES.items():
        info = media.lookup(ref, cache, width=330, allow_currency=True)  # 한국은행 화폐 이미지 이용 기준에 따라 허용
        coins[str(v)] = {"url": info["url"], "credit": info["credit"], "source": info["page"]} if info else None
    json.dump(local_media, open(os.path.join(HERE, "local_media.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    data["store"]["coins"] = coins
    data["math"]["coins"] = coins  # 창의 수학 동전 세기에도 사용
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    summary = {}
    for key, d in data.items():
        d["key"] = key
        json.dump(d, open(os.path.join(ROOT, "data", key + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        withimg = sum(1 for it in d["items"] if isinstance(it.get("image"), dict) and it["image"].get("url"))
        summary[key] = (len(d["items"]), withimg)
    for k, (n, w) in summary.items():
        print(f"{k:8s} 문제 {n:4d}개  (사진 있는 문제 {w})")
    print("총", sum(n for n, _ in summary.values()))
    if missing:
        print("사진 못 찾은 ref", len(set(missing)), sorted(set(missing))[:400])

if __name__ == "__main__":
    main()
