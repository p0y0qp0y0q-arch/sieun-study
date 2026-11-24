from common import Q, img, who, josa
import random

BINS = {"페트": "🧴", "플라스틱": "🥡", "캔": "🥫", "종이": "📦", "종이팩": "🧃", "유리": "🍾", "비닐": "🛍️", "일반쓰레기": "🗑️", "음식물": "🍎"}
BIN_LABEL = {"페트": "투명 페트병", "플라스틱": "플라스틱", "캔": "캔·고철", "종이": "종이", "종이팩": "종이팩(우유팩)", "유리": "유리병",
             "비닐": "비닐", "일반쓰레기": "일반쓰레기", "음식물": "음식물"}

# 물건|통|사진|이모지|팁
ITEMS = """
생수 페트병|페트|wp:Bottled water|🧴|라벨을 떼고 납작하게 눌러서 버려요
음료수 페트병|페트|wp:Plastic bottle|🧴|뚜껑을 닫고 라벨을 떼요
우유팩|종이팩|wp:Gable top|🥛|물로 헹구고 펼쳐서 종이팩으로 따로 모아요
주스팩|종이팩|wp:Carton|🧃|빨대는 빼고 종이팩으로 버려요
두유팩|종이팩|-|🧃|헹구고 말려서 종이팩으로
멸균팩|종이팩|-|🧃|우유팩처럼 종이팩으로 따로 모아요
음료수 캔|캔|wp:Beverage can|🥫|안을 헹구고 납작하게 눌러요
참치캔|캔|wp:Canned fish|🥫|기름을 닦고 헹궈서 캔으로
통조림 캔|캔|wp:Tin can|🥫|헹궈서 캔으로
분유통(철)|캔|-|🥫|뚜껑을 분리해요
냄비|캔|wp:Cookware and bakeware|🍲|쇠로 된 냄비는 고철이에요
프라이팬|캔|wp:Frying pan|🍳|쇠로 된 것은 고철로
부탄가스통|캔|wp:Portable stove|🔥|구멍을 뚫어 가스를 빼고 버려요
병뚜껑(쇠)|캔|-|🔩|쇠 뚜껑은 캔·고철로
택배 상자|종이|wp:Cardboard box|📦|테이프와 송장을 떼고 펼쳐요
신문지|종이|wp:Newspaper|📰|묶어서 종이로
공책|종이|wp:Notebook|📓|스프링은 빼요
종이컵|종이팩|wp:Paper cup|🥤|헹궈서 종이팩이나 종이컵 함으로
과자 상자|종이|wp:Folding carton|📦|펼쳐서 종이로
책|종이|wp:Book|📕|비닐 표지는 벗겨요
달걀판(종이)|종이|wp:Egg carton|🥚|종이로 된 것은 종이로
휴지심|종이|-|🧻|종이로
전단지|종이|wp:Flyer (pamphlet)|📄|종이로
포장지|종이|wp:Wrapping paper|🎁|비닐 코팅이 없으면 종이로
영수증|일반쓰레기|wp:Receipt|🧾|영수증은 종이가 아니라 일반쓰레기예요
사용한 휴지|일반쓰레기|wp:Facial tissue|🤧|더러운 휴지는 일반쓰레기
기저귀|일반쓰레기|wp:Diaper|👶|일반쓰레기로
물티슈|일반쓰레기|wp:Wet wipe|🧻|물티슈는 플라스틱 섞인 일반쓰레기예요
코팅된 종이|일반쓰레기|-|📄|코팅 종이는 일반쓰레기
사진|일반쓰레기|-|🖼️|사진 종이는 일반쓰레기
음료수 유리병|유리|wp:Glass bottle|🍾|뚜껑을 빼고 헹궈요
잼 병|유리|wp:Mason jar|🫙|헹군 다음 유리병으로
간장병|유리|-|🍶|유리로 된 병은 유리병으로
깨진 유리컵|일반쓰레기|-|🥃|깨진 유리는 신문지에 싸서 일반쓰레기(불연성)로
깨진 그릇|일반쓰레기|-|🍽️|도자기는 재활용이 안 돼요. 일반쓰레기(불연성)로
거울|일반쓰레기|wp:Mirror|🪞|거울은 유리병이 아니에요. 일반쓰레기로
도자기 컵|일반쓰레기|wp:Mug|☕|도자기는 일반쓰레기(불연성)로
전구|일반쓰레기|wp:Incandescent light bulb|💡|일반 전구는 일반쓰레기
라면 봉지|비닐|wp:Instant noodle|🍜|비닐로 모아요
과자 봉지|비닐|wp:Potato chip|🥔|안을 털고 비닐로
비닐봉지|비닐|wp:Plastic bag|🛍️|비닐로
뽁뽁이|비닐|wp:Bubble wrap|🫧|비닐로
빵 봉지|비닐|-|🍞|비닐로
지퍼백|비닐|wp:Zipper storage bag|🛍️|씻어서 비닐로
랩|비닐|wp:Plastic wrap|🛍️|깨끗하면 비닐로
요구르트병|플라스틱|wp:Yogurt|🥛|헹궈서 플라스틱으로
샴푸통|플라스틱|wp:Shampoo|🧴|안을 헹구고 플라스틱으로
세제통|플라스틱|wp:Laundry detergent|🧴|헹궈서 플라스틱으로
배달 용기|플라스틱|wp:Take-out|🥡|음식을 씻어 내고 플라스틱으로
컵라면 용기(스티로폼)|플라스틱|wp:Cup noodles|🍜|깨끗이 씻은 스티로폼은 스티로폼끼리
스티로폼 상자|플라스틱|wp:Polystyrene|📦|테이프를 떼고 스티로폼으로
플라스틱 장난감|일반쓰레기|wp:Toy|🧸|여러 재료가 섞인 장난감은 일반쓰레기
칫솔|일반쓰레기|wp:Toothbrush|🪥|칫솔은 일반쓰레기
볼펜|일반쓰레기|wp:Ballpoint pen|🖊️|볼펜은 일반쓰레기
크레파스|일반쓰레기|wp:Crayon|🖍️|일반쓰레기로
고무장갑|일반쓰레기|wp:Rubber glove|🧤|고무는 일반쓰레기
빨대|일반쓰레기|wp:Drinking straw|🥤|작은 빨대는 일반쓰레기
일회용 숟가락|일반쓰레기|-|🥄|작은 플라스틱은 일반쓰레기
마스크|일반쓰레기|wp:Surgical mask|😷|접어서 끈을 자르고 일반쓰레기로
껌|일반쓰레기|wp:Chewing gum|🍬|종이에 싸서 일반쓰레기
연필 깎은 부스러기|일반쓰레기|-|✏️|일반쓰레기로
고무줄|일반쓰레기|wp:Rubber band|➰|일반쓰레기로
솜|일반쓰레기|wp:Cotton wool|☁️|일반쓰레기로
수세미|일반쓰레기|-|🧽|일반쓰레기로
사과 껍질|음식물|wp:Apple|🍎|과일 껍질은 음식물
바나나 껍질|음식물|wp:Banana|🍌|음식물로
먹다 남은 밥|음식물|wp:Cooked rice|🍚|물기를 빼고 음식물로
수박 껍질|음식물|wp:Watermelon|🍉|잘게 잘라서 음식물로
귤 껍질|음식물|wp:Mandarin orange|🍊|음식물로
남은 국수|음식물|wp:Noodle|🍜|물기를 빼고 음식물로
채소 찌꺼기|음식물|wp:Vegetable|🥬|음식물로
상한 빵|음식물|wp:Bread|🍞|음식물로
김치 찌꺼기|음식물|wp:Kimchi|🥬|물에 헹궈서 음식물로
달걀 껍데기|일반쓰레기|wp:Eggshell|🥚|딱딱한 달걀 껍데기는 일반쓰레기예요
닭 뼈|일반쓰레기|-|🍗|뼈는 동물이 못 먹어서 일반쓰레기
조개껍데기|일반쓰레기|wp:Seashell|🐚|딱딱한 껍데기는 일반쓰레기
복숭아 씨|일반쓰레기|wp:Peach|🍑|딱딱한 씨는 일반쓰레기
양파 껍질|일반쓰레기|wp:Onion|🧅|마른 양파 껍질은 일반쓰레기
옥수수 껍질|일반쓰레기|wp:Maize|🌽|질긴 옥수숫대·껍질은 일반쓰레기
차 티백|일반쓰레기|wp:Tea bag|🍵|티백은 일반쓰레기
커피 찌꺼기|일반쓰레기|wp:Coffee|☕|말려서 일반쓰레기
페트병 라벨|비닐|-|🏷️|비닐 라벨은 떼서 비닐로
페트병 뚜껑|플라스틱|wp:Bottle cap|🧢|플라스틱 뚜껑은 플라스틱으로
알루미늄 호일|캔|wp:Aluminium foil|🥈|깨끗하면 캔·고철로
쇠 숟가락|캔|wp:Spoon|🥄|쇠는 고철로
옷걸이(쇠)|캔|wp:Clothes hanger|🧥|쇠 옷걸이는 고철로
못|캔|wp:Nail (fastener)|🔩|고철로
우산|일반쓰레기|wp:Umbrella|☂️|천과 쇠를 분리하면 좋아요. 아니면 일반쓰레기
깨진 화분|일반쓰레기|wp:Flowerpot|🪴|도자기 화분은 일반쓰레기(불연성)
고무공|일반쓰레기|-|⚽|고무는 일반쓰레기
신발|일반쓰레기|wp:Sneakers|👟|헌 옷 수거함이 없으면 일반쓰레기
양말|일반쓰레기|wp:Sock|🧦|구멍 난 양말은 일반쓰레기
종이 쇼핑백|종이|wp:Paper bag|🛍️|손잡이 끈을 떼고 종이로
피자 상자|종이|wp:Pizza box|🍕|기름 묻은 부분은 일반쓰레기, 깨끗한 부분은 종이
공책 스프링|캔|-|➰|쇠 스프링은 고철로
화장지 비닐 포장|비닐|wp:Toilet paper|🧻|비닐로
과일 망|비닐|-|🍑|스티로폼 망은 비닐·스티로폼으로
아이스크림 막대|일반쓰레기|wp:Ice pop|🍦|나무 막대는 일반쓰레기
나무젓가락|일반쓰레기|wp:Chopsticks|🥢|일반쓰레기로
""".strip().splitlines()

TIPS = [
    ("페트병은 버리기 전에 라벨을 떼요.", True), ("우유팩은 종이와 똑같이 버리면 돼요.", False),
    ("우유팩은 헹군 다음 펼쳐서 따로 모아요.", True), ("영수증은 종이로 재활용해요.", False),
    ("깨진 유리는 신문지에 싸서 버려요.", True), ("음료수 캔은 내용물을 비우고 버려요.", True),
    ("음식물 쓰레기는 물기를 빼고 버려요.", True), ("닭 뼈는 음식물 쓰레기예요.", False),
    ("택배 상자는 테이프를 떼고 버려요.", True), ("과자 봉지는 비닐로 모아요.", True),
    ("깨끗하지 않은 휴지는 종이로 재활용해요.", False), ("달걀 껍데기는 일반쓰레기예요.", True),
    ("유리병 안에 담배꽁초를 넣어서 버려도 돼요.", False), ("페트병은 납작하게 눌러서 버리면 좋아요.", True),
    ("분리수거를 하면 쓰레기를 다시 쓸 수 있어요.", True), ("도자기 그릇은 유리병과 함께 버려요.", False),
    ("물티슈는 일반쓰레기예요.", True), ("재활용 쓰레기는 씻지 않고 버려도 돼요.", False),
    ("투명 페트병은 따로 모아요.", True), ("거울은 유리병으로 재활용해요.", False),
]

def build():
    out = []
    n = 0
    rows = [dict(zip(["nm", "bin", "ref", "emo", "tip"], l.split("|"))) for l in ITEMS]
    allbins = list(BINS)
    for i, r in enumerate(rows):
        R = random.Random(i)
        pw = who(i, 91)
        wrong = [b for b in allbins if b != r["bin"]]
        n += 1
        out.append(Q(f"rec-{n:03d}", "분리수거", f"{pw['가']} {r['nm']}{josa(r['nm'],'을','를')} 버리려고 해요. 어디에 버릴까요?" if i % 2 == 0 else f"{r['nm']}{josa(r['nm'],'은','는')} 어느 통에 넣을까요?",
                     [BIN_LABEL[r["bin"]]] + [BIN_LABEL[b] for b in R.sample(wrong, 2)], 0, type="sort", level=1 if i < 40 else 2,
                     image=img(None if r["ref"] == "-" else r["ref"], r["emo"]), item=r["nm"],
                     pool=[BIN_LABEL[b] for b in wrong], binIcons={BIN_LABEL[k]: v for k, v in BINS.items()},
                     explain=r["tip"], group="rec-sort"))
    # 이 통에 들어가는 것은?
    for b in allbins:
        ins = [r for r in rows if r["bin"] == b]
        outs = [r for r in rows if r["bin"] != b]
        for k, r in enumerate(ins[:5]):
            R = random.Random(hash(b) % 997 + k)
            o = R.sample(outs, 2)
            mk = lambda x: img(None if x["ref"] == "-" else x["ref"], x["emo"], label=x["nm"])
            n += 1
            out.append(Q(f"rec-{n:03d}", "분리수거", f"'{BIN_LABEL[b]}' 통에 넣는 것은 어느 것일까요?", [mk(r)] + [mk(x) for x in o], 0,
                         type="imageChoice", level=2, poolImages=[mk(x) for x in outs], display=BINS[b] + " " + BIN_LABEL[b],
                         explain=r["nm"] + ": " + r["tip"], group="rec-bin"))
    for i, (s, ok) in enumerate(TIPS):
        n += 1
        out.append(Q(f"rec-{n:03d}", "분리수거", "맞으면 ⭕, 틀리면 ❌를 골라요.", ["⭕ 맞아요", "❌ 틀려요"], 0 if ok else 1,
                     level=2, fixedOrder=True, display=s, speak="맞으면 동그라미, 틀리면 엑스를 골라요. " + s, image=img(None, "♻️"), group="rec-ox"))
    return out
