from common import Q, img, who, josa
import random

# 종목|사진(경기)|이모지|공/도구 사진|도구 이름|여름/겨울/기타
SPORTS = """
축구|wp:Association football|⚽|wp:Ball (association football)|축구공|여름
야구|wp:Baseball|⚾|wp:Baseball (ball)|야구공과 글러브|기타
농구|wp:Basketball|🏀|wp:Basketball (ball)|농구공|여름
배구|wp:Volleyball|🏐|wp:Volleyball (ball)|배구공|여름
테니스|wp:Tennis|🎾|wp:Tennis ball|테니스공과 라켓|여름
탁구|wp:Table tennis|🏓|wp:Table tennis racket|탁구채|여름
배드민턴|wp:Badminton|🏸|wp:Shuttlecock|셔틀콕|여름
골프|wp:Golf|⛳|wp:Golf ball|골프공|여름
볼링|wp:Bowling|🎳|wp:Bowling pin|볼링 핀|기타
럭비|wp:Rugby union|🏉|wp:Rugby ball|럭비공|여름
미식축구|wp:American football|🏈|wp:American football (ball)|미식축구공|기타
핸드볼|wp:Handball|🤾|-|핸드볼공|여름
하키|wp:Field hockey|🏑|-|하키 스틱|여름
아이스하키|wp:Ice hockey|🏒|wp:Hockey puck|퍽|겨울
수영|wp:Swimming (sport)|🏊|wp:Goggles|물안경|여름
다이빙|wp:Diving (sport)|🤿|-|다이빙대|여름
육상 달리기|wp:Sprint (running)|🏃|wp:Starting blocks|스타팅 블록|여름
마라톤|wp:Marathon|🏃|-|운동화|여름
높이뛰기|wp:High jump|🤸|-|가로대|여름
멀리뛰기|wp:Long jump|🦘|-|모래판|여름
체조|wp:Artistic gymnastics|🤸|wp:Balance beam|평균대|여름
리듬체조|wp:Rhythmic gymnastics|🎀|-|리본|여름
태권도|wp:Taekwondo|🥋|-|도복과 띠|여름
유도|wp:Judo|🥋|-|유도복|여름
씨름|wp:Ssireum|🤼|-|샅바|기타
펜싱|wp:Fencing|🤺|-|검|여름
양궁|wp:Archery|🏹|wp:Archery target|과녁|여름
역도|wp:Olympic weightlifting|🏋️|wp:Barbell|역기|여름
자전거|wp:Road bicycle racing|🚴|wp:Bicycle helmet|헬멧|여름
승마|wp:Equestrianism|🏇|-|말안장|여름
조정|wp:Rowing (sport)|🚣|-|노|여름
카누|wp:Canoe sprint|🛶|wp:Paddle|노|여름
요트|wp:Sailing|⛵|-|돛|여름
서핑|wp:Surfing|🏄|wp:Surfboard|서핑 보드|여름
스키|wp:Alpine skiing|⛷️|wp:Ski|스키|겨울
스노보드|wp:Snowboarding|🏂|wp:Snowboard|스노보드|겨울
스케이트|wp:Speed skating|⛸️|wp:Ice skate|스케이트화|겨울
피겨 스케이팅|wp:Figure skating|⛸️|-|스케이트화|겨울
컬링|wp:Curling|🥌|wp:Curling stone|스톤|겨울
봅슬레이|wp:Bobsleigh|🛷|-|썰매|겨울
스키 점프|wp:Ski jumping|🎿|-|점프대|겨울
줄넘기|wp:Skipping rope|🪢|wp:Skipping rope|줄|기타
등산|wp:Hiking|🥾|wp:Hiking boot|등산화|기타
클라이밍|wp:Sport climbing|🧗|-|홀드|여름
스케이트보드|wp:Skateboarding|🛹|wp:Skateboard|스케이트보드|여름
""".strip().splitlines()

RULES = [
    ("축구에서 골키퍼가 아닌 선수는 공을 손으로 만질 수 있을까요?", "아니요, 손을 쓸 수 없어요", "네, 손으로 잡아도 돼요"),
    ("농구는 공을 어디에 넣으면 점수를 얻을까요?", "바구니 모양 골대", "땅에 있는 구멍"),
    ("축구 공은 손 대신 무엇으로 찰까요?", "발", "손"),
    ("수영장에서 수영하기 전에 꼭 해야 할 것은?", "준비 운동", "과자 먹기"),
    ("탁구는 어디에서 공을 주고받을까요?", "탁자 위", "모래밭"),
    ("야구에서 공을 치는 막대기는 무엇일까요?", "방망이", "라켓"),
    ("배드민턴에서 치는 깃털 달린 공은?", "셔틀콕", "럭비공"),
    ("태권도는 어느 나라에서 시작된 운동일까요?", "대한민국", "브라질"),
    ("양궁은 화살을 어디로 쏠까요?", "과녁", "골대"),
    ("컬링은 무엇 위에서 하는 경기일까요?", "얼음", "잔디"),
    ("볼링은 공을 굴려서 무엇을 쓰러뜨릴까요?", "핀", "나무"),
    ("마라톤은 어떤 경기일까요?", "아주 먼 거리를 달려요", "물속에서 헤엄쳐요"),
    ("배구에서 공이 우리 편 바닥에 떨어지면?", "상대편이 점수를 얻어요", "우리 편이 점수를 얻어요"),
    ("자전거를 탈 때 머리를 지키려면 무엇을 쓸까요?", "헬멧", "왕관"),
    ("스키는 어느 계절에 많이 탈까요?", "겨울", "여름"),
    ("서핑은 어디에서 할까요?", "바다의 파도 위", "눈 쌓인 산"),
    ("씨름에서 상대를 넘어뜨리려고 잡는 천 띠를 무엇이라 할까요?", "샅바", "리본"),
    ("올림픽 1등은 어떤 메달을 받을까요?", "금메달", "동메달"),
    ("올림픽 2등은 어떤 메달을 받을까요?", "은메달", "금메달"),
    ("올림픽 3등은 어떤 메달을 받을까요?", "동메달", "은메달"),
    ("올림픽 깃발의 동그라미(오륜)는 몇 개일까요?", "5개", "3개"),
    ("운동을 하고 나면 무엇을 마시면 좋을까요?", "물", "콜라"),
    ("테니스에서 공은 무엇으로 칠까요?", "라켓", "발"),
    ("골프는 작은 공을 어디에 넣는 경기일까요?", "구멍(홀)", "농구 골대"),
    ("펜싱 선수가 얼굴을 보호하려고 쓰는 것은?", "마스크", "모자"),
    ("수영할 때 눈을 보호하려고 쓰는 것은?", "물안경", "선글라스"),
    ("축구 경기에서 한 팀은 몇 명이 뛸까요?", "11명", "5명"),
    ("농구 경기에서 한 팀은 몇 명이 뛸까요?", "5명", "11명"),
    ("야구에서 공을 던지는 선수를 무엇이라 할까요?", "투수", "골키퍼"),
    ("축구에서 골대를 지키는 선수는?", "골키퍼", "투수"),
]
WARMUP = [
    ("팔을 머리 위로 쭉 뻗어요! 이 동작은?", "기지개 켜기", ["쪼그려 앉기", "제자리 뛰기"], "🙆"),
    ("무릎을 굽혔다 폈다 해요. 이 동작은?", "앉았다 일어나기", ["팔 돌리기", "목 돌리기"], "🧎"),
    ("제자리에서 콩콩 뛰어요. 이 동작은?", "제자리 뛰기", ["기지개 켜기", "허리 숙이기"], "🦘"),
    ("팔을 크게 빙글빙글 돌려요. 이 동작은?", "팔 돌리기", ["발목 돌리기", "제자리 뛰기"], "🔄"),
    ("고개를 천천히 빙글 돌려요. 이 동작은?", "목 돌리기", ["팔 돌리기", "앉았다 일어나기"], "🙂"),
    ("허리를 숙여 손끝으로 발끝을 잡아요. 이 동작은?", "허리 숙이기", ["제자리 뛰기", "기지개 켜기"], "🙇"),
    ("발목을 살살 돌려요. 운동 전에 왜 할까요?", "다치지 않으려고", ["배가 고파서", "졸려서"], "🦶"),
    ("운동 전에 몸을 푸는 것을 무엇이라 할까요?", "준비 운동", ["낮잠", "간식"], "🤸"),
    ("양손을 허리에 대고 옆으로 기울여요. 어디가 늘어날까요?", "옆구리", ["코", "귀"], "🧍"),
    ("다리를 앞뒤로 벌리고 무릎을 굽혀요. 어디가 튼튼해질까요?", "다리", ["머리카락", "손톱"], "🦵"),
]

def build():
    out = []
    n = 0
    rows = [dict(zip(["nm", "ref", "emo", "gref", "gear", "season"], l.split("|"))) for l in SPORTS]
    names = [r["nm"] for r in rows]
    for i, r in enumerate(rows):
        R = random.Random(i)
        pool = [x for x in names if x != r["nm"]]
        im = img(r["ref"], r["emo"])
        pw = who(i, 71)
        n += 1
        out.append(Q(f"spo-{n:03d}", "운동", f"{pw['가']} 텔레비전으로 이 경기를 보고 있어요. 어떤 운동일까요?" if i % 2 == 0 else "사진 속 운동은 무엇일까요?",
                     [r["nm"]] + R.sample(pool, 2), 0, level=1 if i < 20 else 2, image=im, pool=pool, group="spo-photo"))
        n += 1
        others = [x for x in rows if x["nm"] != r["nm"]]
        o = R.sample(others, 2)
        out.append(Q(f"spo-{n:03d}", "운동", f"{r['nm']} 경기 사진은 어느 것일까요?", [im] + [img(x["ref"], x["emo"]) for x in o], 0,
                     type="imageChoice", level=2, display=r["nm"], poolImages=[img(x["ref"], x["emo"]) for x in others], group="spo-name2pic"))
        if r["gref"] != "-":
            n += 1
            out.append(Q(f"spo-{n:03d}", "운동", f"이 {r['gear']}{josa(r['gear'],'은','는')} 어떤 운동에 쓸까요?" if i % 2 else "사진 속 물건은 어떤 운동에 쓸까요?",
                         [r["nm"]] + R.sample(pool, 2), 0, level=2, image=img(r["gref"], r["emo"]), pool=pool, group="spo-gear"))
        if r["season"] in ("여름", "겨울") and i % 2 == 0 or r["season"] == "겨울":
            n += 1
            out.append(Q(f"spo-{n:03d}", "운동", f"{r['nm']}{josa(r['nm'],'은','는')} 여름 올림픽 종목일까요, 겨울 올림픽 종목일까요?",
                         [r["season"] + " 올림픽", ("겨울" if r["season"] == "여름" else "여름") + " 올림픽"], 0, level=3, image=im, group="spo-olympic"))
    for i, (q, a, w) in enumerate(RULES):
        n += 1
        out.append(Q(f"spo-{n:03d}", "운동", q, [a, w], 0, level=2, image=img(None, "🏅"), group="spo-rule"))
    for i, (q, a, w, emo) in enumerate(WARMUP):
        n += 1
        pw = who(i, 72)
        out.append(Q(f"spo-{n:03d}", "운동", f"{pw['랑']} 같이 몸을 풀어요! " + q, [a] + w, 0, level=1, image=img(None, emo), group="spo-warmup"))
    return out
