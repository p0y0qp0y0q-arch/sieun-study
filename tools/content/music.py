from common import Q, img, who, josa
import random

# 악기|분류(때리는/부는/줄)|사진|이모지|국악기여부
INSTR = """
피아노|때리는|wp:Piano|🎹|0
바이올린|줄|wp:Violin|🎻|0
비올라|줄|wp:Viola|🎻|0
첼로|줄|wp:Cello|🎻|0
콘트라베이스|줄|wp:Double bass|🎻|0
기타|줄|wp:Classical guitar|🎸|0
우쿨렐레|줄|wp:Ukulele|🪕|0
하프|줄|wp:Harp|🪉|0
플루트|부는|wp:Western concert flute|🪈|0
클라리넷|부는|wp:Clarinet|🎷|0
오보에|부는|wp:Oboe|🎷|0
바순|부는|wp:Bassoon|🎷|0
색소폰|부는|wp:Saxophone|🎷|0
트럼펫|부는|wp:Trumpet|🎺|0
트롬본|부는|wp:Trombone|🎺|0
호른|부는|wp:French horn|📯|0
튜바|부는|wp:Tuba|🎺|0
리코더|부는|wp:Recorder (musical instrument)|🪈|0
하모니카|부는|wp:Harmonica|🎵|0
아코디언|부는|wp:Accordion|🪗|0
오르간|부는|wp:Pipe organ|🎹|0
드럼|때리는|wp:Drum kit|🥁|0
실로폰|때리는|wp:Xylophone|🎶|0
탬버린|때리는|wp:Tambourine|🪘|0
트라이앵글|때리는|wp:Triangle (musical instrument)|🔺|0
심벌즈|때리는|wp:Cymbal|🥁|0
팀파니|때리는|wp:Timpani|🥁|0
마라카스|때리는|wp:Maraca|🪇|0
캐스터네츠|때리는|wp:Castanets|🎶|0
장구|때리는|wp:Janggu|🪘|1
북|때리는|wp:Buk (drum)|🥁|1
꽹과리|때리는|wp:Kkwaenggwari|🥁|1
징|때리는|wp:Jing (instrument)|🥁|1
가야금|줄|wp:Gayageum|🪕|1
거문고|줄|wp:Geomungo|🪕|1
해금|줄|wp:Haegeum|🎻|1
대금|부는|wp:Daegeum|🪈|1
단소|부는|wp:Danso|🪈|1
피리|부는|wp:Piri|🪈|1
""".strip().splitlines()

CLS = {"때리는": "두드리거나 흔드는 악기", "부는": "입으로 부는 악기", "줄": "줄을 켜거나 튕기는 악기"}

EXTRA = [
    ("오케스트라에서 지휘자는 무엇을 들고 있을까요?", "지휘봉", ["연필", "숟가락"], "🎼"),
    ("오케스트라에서 가장 큰 줄 악기는?", "콘트라베이스", ["바이올린", "플루트"], "🎻"),
    ("음악회에서 연주가 끝나면 어떻게 할까요?", "박수를 쳐요", ["소리를 질러요", "뛰어다녀요"], "👏"),
    ("음악회에서 연주를 들을 때는 어떻게 해야 할까요?", "조용히 들어요", ["큰 소리로 떠들어요", "과자를 바스락 먹어요"], "🤫"),
    ("피아노 건반은 무슨 색일까요?", "흰색과 검은색", ["빨간색과 파란색", "초록색"], "🎹"),
    ("사물놀이에 쓰는 악기 네 가지가 아닌 것은?", "바이올린", ["장구", "꽹과리"], "🥁"),
    ("가야금은 줄이 몇 개일까요? (옛 가야금)", "12줄", ["1줄", "4줄"], "🪕"),
    ("바이올린은 무엇으로 줄을 문질러서 소리를 낼까요?", "활", ["북채", "숟가락"], "🎻"),
    ("드럼은 무엇으로 두드릴까요?", "스틱", ["활", "입"], "🥁"),
    ("기타 줄은 보통 몇 개일까요?", "6개", ["2개", "20개"], "🎸"),
]

def build(sounds):
    out = []
    n = 0
    rows = [dict(zip(["nm", "cls", "ref", "emo", "kor"], l.split("|"))) for l in INSTR]
    names = [r["nm"] for r in rows]
    mk = lambda r: img(r["ref"], r["emo"], label=r["nm"])
    for i, r in enumerate(rows):
        R = random.Random(i)
        pool = [x for x in names if x != r["nm"]]
        im = img(r["ref"], r["emo"])
        snd = sounds.get("instr:" + r["nm"])
        pw = who(i, 81)
        # 1) 사진 → 이름
        n += 1
        out.append(Q(f"mus-{n:03d}", "악기", f"{pw['가']} 음악실에서 이 악기를 봤어요. 이름이 뭘까요?" if i % 2 else "이 악기의 이름은 무엇일까요?",
                     [r["nm"]] + R.sample(pool, 2), 0, level=1 if i < 25 else 2, image=im, sound=snd, soundAfter=True,
                     pool=pool, group="mus-name"))
        # 2) 이름 → 사진
        others = [x for x in rows if x["nm"] != r["nm"]]
        o = R.sample(others, 2)
        n += 1
        out.append(Q(f"mus-{n:03d}", "악기", f"{r['nm']}{josa(r['nm'],'은','는')} 어느 것일까요?", [mk(r)] + [mk(x) for x in o], 0,
                     type="imageChoice", level=2, display=r["nm"], poolImages=[mk(x) for x in others], group="mus-name2pic"))
        # 3) 분류
        n += 1
        cl = list(CLS.values())
        out.append(Q(f"mus-{n:03d}", "악기", f"{r['nm']}{josa(r['nm'],'은','는')} 어떤 악기일까요?", [CLS[r["cls"]]] + [c for c in cl if c != CLS[r["cls"]]], 0,
                     level=2, image=im, group="mus-class"))
        # 4) 소리 → 악기 그림
        if snd:
            withsnd = [x for x in rows if x["nm"] != r["nm"] and sounds.get("instr:" + x["nm"])]
            o2 = R.sample(withsnd, 2)
            n += 1
            out.append(Q(f"mus-{n:03d}", "악기", f"{pw['가']} 음악회에 갔어요. 이 소리는 어떤 악기일까요?" if i % 2 == 0 else "잘 듣고, 어떤 악기 소리인지 골라요.",
                         [mk(r)] + [mk(x) for x in o2], 0, type="imageChoice", level=2, sound=snd,
                         poolImages=[mk(x) for x in withsnd], group="mus-sound"))
            n += 1
            out.append(Q(f"mus-{n:03d}", "악기", "이 소리를 내는 악기의 이름은?", [r["nm"]] + [x["nm"] for x in o2], 0, level=3, sound=snd,
                         pool=[x["nm"] for x in withsnd], group="mus-sound2"))
        if r["kor"] == "1":
            n += 1
            out.append(Q(f"mus-{n:03d}", "악기", f"{r['nm']}{josa(r['nm'],'은','는')} 우리나라 전통 악기(국악기)일까요?", ["네, 국악기예요", "아니요, 서양 악기예요"], 0,
                         level=2, image=im, group="mus-korean"))
    # 분류별: 이 중 부는 악기는?
    for c, desc in CLS.items():
        ins = [r for r in rows if r["cls"] == c]
        outs = [r for r in rows if r["cls"] != c]
        for k, r in enumerate(ins[:8]):
            R = random.Random(hash(c) % 1000 + k)
            o = R.sample(outs, 2)
            n += 1
            out.append(Q(f"mus-{n:03d}", "악기", f"이 중에서 {desc}는 어느 것일까요?", [mk(r)] + [mk(x) for x in o], 0, type="imageChoice", level=3,
                         poolImages=[mk(x) for x in outs], group="mus-classpick"))
    for i, (q, a, w, emo) in enumerate(EXTRA):
        n += 1
        out.append(Q(f"mus-{n:03d}", "악기", q, [a] + w, 0, level=2, image=img(None, emo), group="mus-qa"))
    # 연주 모습 / 오케스트라
    PERF = [("wp:Orchestra", "오케스트라", ["밴드 행진", "합창단"], "🎼"),
            ("wp:Samul nori", "사물놀이", ["오케스트라", "합창단"], "🥁"),
            ("wp:Marching band", "행진하는 악대", ["오케스트라", "사물놀이"], "🎺"),
            ("wp:Choir", "합창단", ["사물놀이", "오케스트라"], "🎤"),
            ("wp:String quartet", "현악 사중주", ["사물놀이", "행진하는 악대"], "🎻")]
    for i, (ref, a, w, emo) in enumerate(PERF):
        n += 1
        pw = who(i, 82)
        out.append(Q(f"mus-{n:03d}", "악기", f"{pw['가']} 본 이 연주 모습은 무엇일까요?", [a] + w, 0, level=3, image=img(ref, emo), group="mus-perf"))
    return out, rows
