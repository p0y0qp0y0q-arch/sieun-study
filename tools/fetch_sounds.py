"""악기·동물 실제 녹음 소리를 받아 2~4초 mp3로 만든다 → assets/sounds/*.mp3, sounds.json
- 악기: tonejs-instruments 샘플 (CC BY 3.0, github.com/nbrosowsky/tonejs-instruments) 의 실제 녹음 3음을 이어 붙임
- 그 밖: 위키미디어 커먼즈 오디오 (라이선스 확인 후 사용)
"""
import json, os, subprocess, sys, tempfile, urllib.request, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import wm, media
OUT = os.path.join(ROOT, "assets", "sounds")
RAW = os.path.join(HERE, "raw_sounds")
TONE = "https://raw.githubusercontent.com/nbrosowsky/tonejs-instruments/master/samples/{}/{}.mp3"
TONE_SET = {
    "피아노": ("piano", ["C4", "E4", "G4"]), "바이올린": ("violin", ["C4", "E4", "G4"]), "첼로": ("cello", ["C3", "E4", "A3"]),
    "콘트라베이스": ("contrabass", ["E2", "A2", "Cs3"]), "기타": ("guitar-nylon", ["A3", "E4", "A4"]), "하프": ("harp", ["D4", "F4", "A4"]),
    "플루트": ("flute", ["C4", "E4", "C5"]), "클라리넷": ("clarinet", ["D4", "F4", "As4"]), "바순": ("bassoon", ["A3", "C4", "E4"]),
    "색소폰": ("saxophone", ["C4", "E4", "G4"]), "트럼펫": ("trumpet", ["Ds4", "F4", "As4"]), "트롬본": ("trombone", ["As2", "D3", "F3"]),
    "호른": ("french-horn", ["D3", "F3", "A3"]), "튜바": ("tuba", ["F2", "As2", "D3"]), "오르간": ("organ", ["C4", "A4", "C5"]),
    "실로폰": ("xylophone", ["G4", "C5", "G5"]),
}
COMMONS = {
    "instr:드럼": "Drum_beat.ogg", "instr:탬버린": "Tambourine.ogg", "instr:트라이앵글": "LatinTriangle.ogg", "instr:리코더": "SopranoRecorder.ogg",
    "instr:하모니카": "Harmonica_playing.ogg", "instr:아코디언": "Accordion_chords-01.ogg", "instr:비올라": "Viola-walshimprov.ogg",
    "instr:우쿨렐레": "Ukulele_playing.ogg", "instr:오보에": "Ferling_Oboe_Study_No_28_Aaron_Hill.ogg", "instr:심벌즈": "Crash_cymbal.ogg",
    "instr:팀파니": "Timpani_F_major_triad.ogg", "instr:마라카스": "Maracas.ogg", "instr:캐스터네츠": "Castañuelas.ogg", "instr:장구": "Janggu.ogg",
    "animal:강아지": "Barking_of_a_dog.ogg", "animal:고양이": "Meow_domestic_cat.ogg", "animal:소": "Single_Cow_Moo.ogg",
    "animal:닭": "Rooster_crowing.ogg", "animal:오리": "Pekin_duck_&_mallard.ogg", "animal:양": "Sheep_bleating.ogg",
    "animal:염소": "Herd_of_goats_bleating.ogg", "animal:말": "Wiehern.ogg", "animal:돼지": "Mudchute_pig_1.ogg",
    "animal:개구리": "Single_Frog_Croak.oga", "animal:부엉이": "Bubo_bubo_-_Eurasian_Eagle-Owl_XC461330.mp3",
    "animal:코끼리": "Elephant_voice_-_trumpeting.ogg", "animal:늑대": "Wolf_howls.ogg",
    "animal:갈매기": "Larus_argentatus_-_European_Herring_Gull_XC488995.mp3", "animal:귀뚜라미": "Field_cricket_unedited.ogg",
    "animal:매미": "Cicada_orni_(Singing).ogg", "animal:참새": "Passer_montanus_-_Eurasian_Tree_Sparrow_XC347807.mp3",
    "animal:칠면조": "Meleagris_gallopavo_-_Wild_Turkey_XC134155.ogg", "animal:뻐꾸기": "Cuculus_canorus_-_Common_Cuckoo_XC554785.mp3",
}
# 시작 위치(초) 수동 조정
START = {}
# 아주 짧은 소리는 여러 번 반복
LOOP = {"instr:캐스터네츠": 4, "animal:돼지": 3}
DUR = {"animal:칠면조": 4.0, "animal:부엉이": 4.0, "instr:오보에": 4.0, "instr:비올라": 4.0, "animal:늑대": 4.0, "animal:뻐꾸기": 4.0, "animal:코끼리": 3.5}

def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)

def dl(url, path):
    import time, urllib.error
    for attempt in range(15):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": wm.UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                open(path, "wb").write(r.read())
            time.sleep(2)
            return
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            ra = e.headers.get("retry-after", ""); t = (int(ra) if ra.isdigit() else 30) + 5
            print("  429, 대기", t, flush=True); time.sleep(t)
    raise RuntimeError("429 계속")

def slug(k):
    return k.replace(":", "-")

def main():
    sj = os.path.join(OUT, "sounds.json")
    out = json.load(open(sj, encoding="utf-8")) if os.path.exists(sj) else {}
    tmp = tempfile.mkdtemp()
    # 1) tonejs
    for nm, (folder, notes) in TONE_SET.items():
        key = "instr:" + nm
        if key in out: continue
        dst = os.path.join(OUT, slug(key) + ".mp3")
        parts = []
        for i, n in enumerate(notes):
            p = os.path.join(tmp, f"{folder}-{n}.mp3"); dl(TONE.format(folder, n), p)
            q = os.path.join(tmp, f"{folder}-{n}.wav")
            d = 1.4 if i == len(notes) - 1 else 0.85
            ff("-i", p, "-t", str(d), "-af", f"afade=t=out:st={d - 0.15}:d=0.15", "-ac", "1", "-ar", "44100", q)
            parts.append(q)
        lst = os.path.join(tmp, folder + ".txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        ff("-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-16:TP=-1.5", "-ac", "1", "-b:a", "64k", dst)
        out[key] = {"url": f"assets/sounds/{slug(key)}.mp3", "credit": "tonejs-instruments 샘플 (Nicholaus Brosowsky), CC BY 3.0",
                    "source": f"https://github.com/nbrosowsky/tonejs-instruments/tree/master/samples/{folder}"}
        print("ok", key, flush=True)
    # 2) commons
    cache = media.load()
    need = ["file:" + f for f in COMMONS.values() if ("file:" + f) not in cache]
    if need:
        media.resolve(need, cache); media.save(cache)
    for key, f in COMMONS.items():
        if key in out: continue
        info = cache.get("file:" + f)
        if not info or info.get("missing"):
            print("없음", key, f); continue
        if not media.license_ok(info["license"]):
            print("라이선스 제외", key, info["license"]); continue
        # 직접 받아 둔 파일이 tools/raw_sounds/ 에 있으면 그걸 씀 (위키미디어가 막힐 때)
        local = [os.path.join(RAW, x) for x in os.listdir(RAW)] if os.path.isdir(RAW) else []
        norm = lambda x: urllib.parse.unquote(os.path.basename(x)).replace(" ", "_").lower()
        hit = [x for x in local if norm(x) == norm(f)]
        if hit:
            src = hit[0]; print("  직접 받은 파일 사용:", os.path.basename(src))
        else:
            src = os.path.join(tmp, slug(key) + os.path.splitext(f)[1])
            try:
                dl(info["orig"], src)
            except Exception as e:
                print("받기 실패", key, e); continue
        dst = os.path.join(OUT, slug(key) + ".mp3")
        dur = DUR.get(key, 3.0)
        st = START.get(key)
        pre = ["-ss", str(st)] if st is not None else []
        af = "" if st is not None else "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.05,"
        if key in LOOP:
            looped = os.path.join(tmp, slug(key) + "-loop.wav")
            ff("-i", src, "-af", "apad=pad_dur=0.25", "-ac", "1", "-ar", "44100", os.path.join(tmp, "one.wav"))
            ff("-stream_loop", str(LOOP[key] - 1), "-i", os.path.join(tmp, "one.wav"), looped)
            src = looped; af = ""
        ff(*pre, "-i", src, "-af", f"{af}atrim=0:{dur},afade=t=in:d=0.05,afade=t=out:st={dur - 0.4}:d=0.4,loudnorm=I=-16:TP=-1.5", "-ac", "1", "-ar", "44100", "-b:a", "64k", dst)
        out[key] = {"url": f"assets/sounds/{slug(key)}.mp3", "credit": f'{info["artist"]}, {info["license"]}, Wikimedia Commons', "source": info["page"]}
        print("ok", key, info["license"], flush=True)
    json.dump(out, open(os.path.join(OUT, "sounds.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("소리", len(out))

if __name__ == "__main__":
    main()
