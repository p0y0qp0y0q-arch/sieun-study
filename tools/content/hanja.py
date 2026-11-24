from common import Q, img, who
from hanja_hints import HINTS, ancient_ref, ancient_local
import random

# 한자|훈음|레벨|사진ref|이모지|낱말(뜻풀이)들 ; 낱말은 "화산:불 화" 처럼 한자가 들어가는 글자
CHARS = """
一|한 일|1|-|1️⃣|일등,일월
二|두 이|1|-|2️⃣|이층,이월
三|석 삼|1|-|3️⃣|삼촌,삼월
四|넉 사|1|-|4️⃣|사촌,사월
五|다섯 오|1|-|5️⃣|오월,오십
六|여섯 육|1|-|6️⃣|육각형,육십
七|일곱 칠|1|-|7️⃣|칠월,칠십
八|여덟 팔|1|-|8️⃣|팔월,팔십
九|아홉 구|1|-|9️⃣|구월,구십
十|열 십|1|-|🔟|십원,십자
山|메 산|1|wp:Mountain|⛰️|등산,화산
水|물 수|1|wp:Water|💧|수영,생수
火|불 화|1|wp:Campfire|🔥|화산,소화기
日|날 일|1|wp:Sunrise|☀️|생일,일요일
月|달 월|1|wp:Moon|🌙|월요일,일월
人|사람 인|1|-|🧍|인형,거인
口|입 구|1|wp:Lip|👄|입구,출구
木|나무 목|2|wp:Tree|🌳|목요일,목수
金|쇠 금|2|wp:Gold|🪙|금요일,황금
土|흙 토|2|wp:Soil|🟫|토요일,국토
大|큰 대|2|wp:Elephant|🐘|대문,대한민국
小|작을 소|2|wp:House mouse|🐭|소인,소형차
上|윗 상|2|-|⬆️|옥상,상하
下|아래 하|2|-|⬇️|지하철,하교
中|가운데 중|2|-|🎯|중학교,중간
父|아비 부|2|-|👨|부모,부녀
母|어미 모|2|-|👩|모녀,부모
子|아들 자|2|-|👦|부자,모자
女|계집 녀|2|-|👧|여자,소녀
王|임금 왕|2|wp:Crown (headgear)|👑|왕자,여왕
門|문 문|3|wp:Door|🚪|대문,교문
白|흰 백|3|wp:Snow|⬜|백조,흑백
青|푸를 청|3|wp:Sky|🟦|청소년,청바지
年|해 년|3|-|📅|내년,학년
生|날 생|3|wp:Seedling|🌱|생일,학생
先|먼저 선|3|-|🥇|선생님,선수
學|배울 학|3|wp:School|🏫|학교,학생
校|학교 교|3|wp:School|🏫|교문,교장
東|동녘 동|3|wp:Sunrise|🌅|동쪽,동해
西|서녘 서|3|wp:Sunset|🌇|서쪽,서해
南|남녘 남|3|-|🧭|남쪽,남한
北|북녘 북|3|-|🧭|북쪽,북극
國|나라 국|3|wp:Flag of South Korea|🇰🇷|국기,외국
韓|한국 한|3|wp:Flag of South Korea|🇰🇷|한국,한복
民|백성 민|3|-|👨‍👩‍👧|국민,민속
軍|군사 군|3|-|🪖|군인,해군
兄|형 형|3|-|👦|형제,형님
弟|아우 제|3|-|🧒|형제,제자
外|바깥 외|3|-|🚪|외국,외출
萬|일만 만|3|-|💯|만원,만세
寸|마디 촌|3|-|📏|삼촌,사촌
長|긴 장|3|-|📏|교장,장화
室|집 실|3|wp:Classroom|🏠|교실,화장실
教|가르칠 교|3|wp:Classroom|🧑‍🏫|교실,교과서
""".strip().splitlines()

def hint_of(h):
    emo, story = HINTS[h]
    ref = ancient_ref(h)
    d = {"emoji": emo, "story": story}
    if ref:
        d["ancient"] = img(ref, "📜", flag=True, local=ancient_local(h))
    return d

def build():
    rows = []
    for line in CHARS:
        h, hm, lv, ref, emo, words = line.split("|")
        rows.append({"h": h, "hm": hm, "lv": int(lv), "ref": None if ref == "-" else ref, "emo": emo, "words": words.split(",")})
    allh = [r["h"] for r in rows]
    allhm = [r["hm"] for r in rows]
    out = []
    n = 0
    for i, r in enumerate(rows):
        R = random.Random(i)
        pool = [x for x in allh if x != r["h"]]
        poolhm = [x for x in allhm if x != r["hm"]]
        # 1) 그림 보고 한자 고르기 (사진 있는 글자)
        if r["ref"]:
            n += 1
            pw = who(i, 21)
            out.append(Q(f"han-{n:03d}", "한자", f"{pw['가']} 본 이 사진과 어울리는 한자는?" if i % 2 else "사진을 보고 알맞은 한자를 골라요.",
                         [r["h"]] + R.sample(pool, 2), 0, level=r["lv"], image=img(r["ref"], r["emo"]), pool=pool,
                         big=True, speakChoices=False, explain=f"{r['h']}  {r['hm']}", group="han-pic", _h=r["h"]))
        else:
            n += 1
            out.append(Q(f"han-{n:03d}", "한자", "그림과 어울리는 한자는?", [r["h"]] + R.sample(pool, 2), 0, level=r["lv"],
                         image=img(None, r["emo"]), pool=pool, big=True, speakChoices=False, explain=f"{r['h']}  {r['hm']}", group="han-pic", _h=r["h"]))
        # 2) 한자 → 훈음 (보기 읽어주기)
        n += 1
        out.append(Q(f"han-{n:03d}", "한자", "이 한자의 뜻과 소리는 무엇일까요?", [r["hm"]] + R.sample(poolhm, 2), 0, level=r["lv"],
                     display=r["h"], big=True, pool=poolhm, speakChoices=True, explain=f"{r['h']}  {r['hm']}", group="han-read", _h=r["h"]))
        # 3) 훈음 → 한자
        n += 1
        pw = who(i, 22)
        out.append(Q(f"han-{n:03d}", "한자", f"'{r['hm']}' 은 어느 한자일까요?", [r["h"]] + R.sample(pool, 2), 0, level=r["lv"],
                     pool=pool, big=True, speakChoices=False, explain=f"{r['h']}  {r['hm']}", group="han-find", showHint=True, _h=r["h"]))
        # 4) 낱말 속 한자 찾기
        for j, w in enumerate(r["words"]):
            syl = r["hm"].split()[-1]
            # 낱말 속 해당 글자 (두음법칙 녀→여, 년→내년/새해 등 고려해 첫 일치 음절)
            cand = [syl, {"녀": "여", "년": "년"}.get(syl, syl)]
            pos = next((k for k, ch in enumerate(w) if ch in cand), None)
            if pos is None:
                continue
            n += 1
            ws = w[pos]
            out.append(Q(f"han-{n:03d}", "한자", f"'{w}'의 '{ws}'는 어느 한자일까요?", [r["h"]] + R.sample(pool, 2), 0,
                         level=max(2, r["lv"]), pool=pool, big=True, speakChoices=False, display=w,
                         explain=f"{w}: {r['h']} {r['hm']}", group="han-word", _h=r["h"]))
    # 옛날 모양(갑골문 등) 보고 오늘날 한자 고르기
    for i, r in enumerate(rows):
        ref = ancient_ref(r["h"])
        if not ref:
            continue
        R = random.Random(700 + i)
        pool = [x for x in allh if x != r["h"]]
        n += 1
        out.append(Q(f"han-{n:03d}", "한자", "아주 옛날 사람들이 쓰던 글자 모양이에요. 오늘날 어떤 한자가 되었을까요?",
                     [r["h"]] + R.sample(pool, 2), 0, level=max(1, r["lv"]), image=img(ref, "📜", flag=True, local=ancient_local(r["h"])), pool=pool,
                     big=True, speakChoices=False, explain=f"{r['h']}  {r['hm']}", group="han-ancient", _h=r["h"]))
    for q in out:
        h = q.get("_h")
        if h:
            q["hanjaHint"] = hint_of(h)
            q["explain"] = q.get("explain", "") + " · " + HINTS[h][1]
            q.pop("_h")
    return out

GENERATORS = [{"id": "gen-hanja-count", "gen": "hanjaCount", "level": 1, "weight": 3, "title": "숫자 한자 세기"}]
