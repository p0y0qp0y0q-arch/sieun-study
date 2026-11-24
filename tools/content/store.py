from common import Q, img, who, josa
import random

# 물건|가격|사진|이모지
ITEMS = """
지우개|300|wp:Eraser|🧽
연필|500|wp:Pencil|✏️
공책|1000|wp:Notebook|📓
사탕|100|wp:Candy|🍬
막대사탕|200|wp:Lollipop|🍭
초콜릿|1000|wp:Chocolate bar|🍫
우유|800|wp:Milk|🥛
바나나|500|wp:Banana|🍌
사과|700|wp:Apple|🍎
아이스크림|1000|wp:Ice cream|🍦
풍선|300|wp:Balloon|🎈
스티커|500|-|⭐
빵|1500|wp:Bread|🍞
주스|1200|wp:Juice|🧃
색연필|3000|wp:Colored pencil|🖍️
가위|2000|wp:Scissors|✂️
풀|700|wp:Glue stick|🧴
껌|500|wp:Chewing gum|🍬
과자|1500|wp:Potato chip|🥔
도넛|1000|wp:Doughnut|🍩
달걀|300|wp:Egg as food|🥚
귤|200|wp:Mandarin orange|🍊
""".strip().splitlines()

SHOPS = """
빵집|wp:Bakery|🥐|빵,케이크,도넛,식빵
약국|wp:Pharmacy (shop)|💊|감기약,밴드,연고
꽃집|wp:Floristry|💐|장미꽃,꽃다발,화분
문구점|wp:Stationery|✏️|연필,공책,지우개
서점|wp:Bookselling|📚|동화책,그림책,잡지
과일가게|wp:Greengrocer|🍎|사과,바나나,포도
생선가게|wp:Fishmonger|🐟|고등어,오징어,조개
정육점|wp:Butcher|🥩|소고기,돼지고기,닭고기
미용실|wp:Hairdresser|💇|머리 자르기,파마
세탁소|wp:Laundry|👔|양복 세탁,옷 수선
주유소|wp:Filling station|⛽|휘발유,경유
우체국|wp:Post office|📮|편지 부치기,우표,택배
은행|wp:Bank|🏦|저금하기,돈 찾기
안경점|wp:Optician|👓|안경,선글라스
신발가게|wp:Shoe shop|👟|운동화,구두,장화
장난감 가게|wp:Toy store|🧸|인형,블록,장난감 자동차
""".strip().splitlines()

# 상황 문제 템플릿 (숫자는 앱이 매번 바꿈)
#  a,b: 물건 가격 슬롯(아이템 랜덤) / m: 가진 돈
SIT = [
    ("{N가} {i1}{와} {i2}{를} 샀어요. 모두 얼마일까요?", "sum2"),
    ("{i1} 한 개는 {p1}원이에요. {i1} 2개는 얼마일까요?", "double"),
    ("{N는} {m}원을 가지고 있어요. {i1}({p1}원)를 사면 얼마가 남을까요?", "change"),
    ("{m}원으로 살 수 있는 것은 어느 것일까요?", "canbuy"),
    ("{N가} {m}원을 냈어요. {p1}원짜리 {i1}{를} 사면 거스름돈은 얼마일까요?", "change"),
    ("{i1}{와} {i2} 중에서 더 비싼 것은?", "pricier"),
    ("{i1}{와} {i2} 중에서 더 싼 것은?", "cheaper"),
    ("{N는} 100원짜리 동전으로 {p1}원을 내려고 해요. 동전 몇 개가 필요할까요?", "count100"),
    ("{N는} {i1}{를} 사려고 {have}원을 모았어요. 얼마가 더 필요할까요?", "needmore"),
]

def build(coins):
    out = []
    n = 0
    items = []
    for l in ITEMS:
        nm, p, ref, emo = l.split("|")
        items.append({"name": nm, "price": int(p), "image": img(None if ref == "-" else ref, emo)})
    # 상황 문제: 템플릿 × 물건 묶음  (물건과 금액은 앱이 매번 섞음)
    for i, (t, kind) in enumerate(SIT):
        for v in range(12):
            n += 1
            out.append({"id": f"sto-s{n:03d}", "subject": "가게", "type": "shop", "template": t, "kind": kind,
                        "level": 2 if kind in ("sum2", "double", "pricier", "cheaper", "canbuy") else 3,
                        "seed": v, "group": "sto-" + kind})
    shopnames = [s.split("|")[0] for s in SHOPS]
    for i, l in enumerate(SHOPS):
        nm, ref, emo, goods = l.split("|")
        R = random.Random(i)
        pool = [x for x in shopnames if x != nm]
        n += 1
        pw = who(i, 61)
        out.append(Q(f"sto-{n:03d}", "가게", f"{pw['가']} 이 가게에 왔어요. 어떤 가게일까요?" if i % 2 else "사진 속 가게는 어떤 가게일까요?",
                     [nm] + R.sample(pool, 2), 0, level=1, image=img(ref, emo), pool=pool, group="sto-shop"))
        for g in goods.split(","):
            n += 1
            pw = who(n, 62)
            out.append(Q(f"sto-{n:03d}", "가게", f"{pw['가']} {g}{josa(g,'을','를')} 사려고 해요. 어느 가게에 가야 할까요?",
                         [nm] + R.sample(pool, 2), 0, level=1, image=img(None, emo), pool=pool, group="sto-where"))
    return out, items

GENERATORS = [
    {"id": "gen-money-count", "gen": "moneyCount", "level": 2, "weight": 4, "title": "동전·지폐 세기"},
    {"id": "gen-money-which", "gen": "moneyWhich", "level": 1, "weight": 2, "title": "이 돈은 얼마?"},
    {"id": "gen-money-make", "gen": "moneyMake", "level": 3, "weight": 2, "title": "같은 금액 만들기"},
]
