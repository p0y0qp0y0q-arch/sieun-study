from common import Q, img, who, josa
import random

# 질문|정답|오답1,오답2|이모지|사진
QA = """
양치할 때 물을 아끼려면 어떻게 할까요?|컵에 물을 받아서 해요|물을 계속 틀어 놔요,물을 세게 틀어요|🪥|-
방에서 나갈 때 전기를 아끼려면?|불을 꺼요|불을 켜 둬요,창문을 열어요|💡|-
안 보는 텔레비전은 어떻게 할까요?|꺼요|소리를 크게 해요,계속 켜 둬요|📺|-
나무가 우리에게 주는 것은?|맑은 공기|플라스틱,쓰레기|🌳|wp:Tree
나무가 만들어 주는 것 중 숨 쉴 때 필요한 것은?|산소|모래,연기|🌲|-
종이는 무엇으로 만들까요?|나무|돌,물고기|📄|wp:Paper
나무 그늘은 어떤 날 좋을까요?|더운 여름날|추운 겨울밤,비 오는 날|🌳|-
장 보러 갈 때 무엇을 챙기면 좋을까요?|장바구니|비닐봉지 10장,종이컵|🛍️|wp:Shopping bag
음료수를 마실 때 무엇을 쓰면 좋을까요?|내 컵(텀블러)|일회용 컵,일회용 빨대 여러 개|🥤|wp:Travel mug
일회용품을 줄이는 방법은?|여러 번 쓰는 물건 쓰기|일회용 컵 많이 쓰기,새 비닐 자주 쓰기|♻️|-
가까운 곳에 갈 때 환경을 지키는 방법은?|걷거나 자전거 타기|혼자 자동차 타기,택시 타기|🚲|-
쓰레기를 길에 버리면 어떻게 될까요?|동물과 자연이 아파요|꽃이 더 잘 자라요,바다가 깨끗해져요|🚯|-
바다에 플라스틱이 많아지면 누가 아플까요?|바다 동물|구름,별|🐢|wp:Green sea turtle
남은 음식을 줄이려면?|먹을 만큼만 덜어요|많이 덜고 남겨요,버려요|🍚|-
냉장고 문은 어떻게 할까요?|빨리 닫아요|오래 열어 둬요,활짝 열고 놀아요|🧊|wp:Refrigerator
샤워는 어떻게 하면 물을 아낄까요?|짧게 해요|한 시간 해요,물을 틀어 놓고 놀아요|🚿|-
여름에 에어컨 온도는?|너무 낮지 않게 해요|아주 춥게 해요,창문 열고 켜요|❄️|-
겨울에 집 안을 따뜻하게 하려면?|옷을 따뜻하게 입어요|창문을 활짝 열어요,반바지를 입어요|🧣|-
지구가 너무 더워지는 것을 무엇이라 할까요?|지구 온난화|지구 냉장고,지구 놀이터|🌍|-
지구가 더워지면 북극의 얼음은?|녹아요|더 커져요,색이 바뀌어요|🧊|wp:Sea ice
북극의 얼음이 녹으면 살 곳이 줄어드는 동물은?|북극곰|낙타,사자|🐻‍❄️|wp:Polar bear
햇빛으로 전기를 만드는 것은?|태양광 발전|석탄 난로,가스레인지|☀️|wp:Photovoltaic system
바람으로 전기를 만드는 것은?|풍력 발전기|선풍기,드라이어|🌬️|wp:Wind turbine
자동차 연기가 많으면 공기가 어떻게 될까요?|더러워져요|깨끗해져요,향기로워져요|🚗|-
미세먼지가 많은 날 밖에 나갈 때는?|마스크를 써요|창문을 열어요,뛰어놀아요|😷|-
꽃과 나무를 아끼는 방법은?|꺾지 않고 바라봐요|꽃을 마구 꺾어요,나무에 낙서해요|🌷|-
공원에서 먹은 과자 봉지는?|집에 가져가서 버려요|풀숲에 숨겨요,벤치에 두고 가요|🧺|-
물을 더럽히지 않으려면?|기름을 하수구에 붓지 않아요|세제를 많이 써요,쓰레기를 강에 버려요|💧|-
헌 옷은 어떻게 할까요?|동생이나 이웃에게 물려줘요|바로 버려요,불에 태워요|👕|-
종이를 아끼는 방법은?|종이 양면을 다 써요|한 줄 쓰고 버려요,종이비행기 100개 접어요|📄|-
지구를 지키는 날인 '지구의 날'에 하면 좋은 일은?|불 끄고 잠시 쉬기|전기 많이 쓰기,쓰레기 버리기|🌎|-
벌이 없어지면 무엇이 어려워질까요?|꽃가루받이(열매 맺기)|비 내리기,눈 내리기|🐝|wp:Western honey bee
숲이 사라지면 동물들은?|살 곳이 없어져요|더 행복해져요,더 많아져요|🦧|wp:Orangutan
재활용을 하면 좋은 점은?|쓰레기가 줄어요|쓰레기가 늘어요,물이 더러워져요|♻️|-
비닐봉지 대신 쓸 수 있는 것은?|천 가방(에코백)|비닐봉지 두 장,종이컵|👜|-
양치할 때 쓰는 물을 아끼면 누구에게 좋을까요?|지구와 우리 모두|아무도 없어요,벌레만|🌍|-
""".strip().splitlines()

# 멸종 위기 동물
ENDANGERED = """
호랑이|wp:Siberian tiger|🐯
반달가슴곰|wp:Asian black bear|🐻
수달|wp:Eurasian otter|🦦
북극곰|wp:Polar bear|🐻‍❄️
판다|wp:Giant panda|🐼
오랑우탄|wp:Orangutan|🦧
고릴라|wp:Gorilla|🦍
코뿔소|wp:Black rhinoceros|🦏
아프리카코끼리|wp:African bush elephant|🐘
바다거북|wp:Green sea turtle|🐢
두루미|wp:Red-crowned crane|🐦
눈표범|wp:Snow leopard|🐆
산양|wp:Long-tailed goral|🐐
황새|wp:Oriental stork|🐦
상괭이|wp:Narrow-ridged finless porpoise|🐬
레서판다|wp:Red panda|🐼
치타|wp:Cheetah|🐆
""".strip().splitlines()

# 좋은 행동 / 안 좋은 행동
ACTIONS = [("쓰레기를 쓰레기통에 버려요", True, "🚮"), ("길에 쓰레기를 버려요", False, "🚯"),
           ("나무를 심어요", True, "🌱"), ("꽃을 마구 꺾어요", False, "🥀"),
           ("물을 틀어 놓고 딴짓해요", False, "🚰"), ("방을 나갈 때 불을 꺼요", True, "💡"),
           ("장바구니를 가지고 가요", True, "🛍️"), ("일회용 컵을 하루에 다섯 개 써요", False, "🥤"),
           ("분리수거를 해요", True, "♻️"), ("강에 쓰레기를 던져요", False, "🌊"),
           ("가까운 곳은 걸어서 가요", True, "🚶"), ("음식을 잔뜩 남겨요", False, "🍱"),
           ("텀블러를 써요", True, "🧋"), ("동물에게 돌을 던져요", False, "🪨"),
           ("이면지에 그림을 그려요", True, "📝"), ("안 쓰는 전기 플러그를 뽑아요", True, "🔌"),
           ("새 둥지를 건드려요", False, "🪺"), ("바닷가 쓰레기를 주워요", True, "🏖️"),
           ("벽에 낙서를 해요", False, "🖍️"), ("화분에 물을 줘요", True, "🪴")]

def build():
    out = []
    n = 0
    for i, l in enumerate(QA):
        q, a, w, emo, ref = l.split("|")
        pw = who(i, 101)
        if i % 3 == 0:
            pass
        n += 1
        out.append(Q(f"env-{n:03d}", "환경", q, [a] + w.split(","), 0, level=2, image=img(None if ref == "-" else ref, emo), group="env-qa"))
    names = [l.split("|")[0] for l in ENDANGERED]
    for i, l in enumerate(ENDANGERED):
        nm, ref, emo = l.split("|")
        R = random.Random(i)
        pool = [x for x in names if x != nm]
        n += 1
        out.append(Q(f"env-{n:03d}", "환경", "지켜 줘야 하는 멸종 위기 동물이에요. 이름이 뭘까요?", [nm] + R.sample(pool, 2), 0, level=2,
                     image=img(ref, emo), pool=pool, group="env-endangered"))
        n += 1
        out.append(Q(f"env-{n:03d}", "환경", f"{nm}{josa(nm,'이','가')} 사라지지 않게 우리가 할 수 있는 일은?",
                     ["사는 곳(숲·바다)을 지켜 줘요", "마구 잡아요", "쓰레기를 버려요"], 0, level=2, image=img(ref, emo), group="env-protect"))
    for i, (s, good, emo) in enumerate(ACTIONS):
        pw = who(i, 102)
        n += 1
        out.append(Q(f"env-{n:03d}", "환경", f"'{s}' 이것은 좋은 행동일까요?", ["😊 좋은 행동", "😢 안 좋은 행동"], 0 if good else 1,
                     level=1, fixedOrder=True, image=img(None, emo), group="env-goodbad"))
    # 좋은 행동 고르기 (보기 3개)
    goods = [a for a in ACTIONS if a[1]]
    bads = [a for a in ACTIONS if not a[1]]
    for i, g in enumerate(goods):
        R = random.Random(500 + i)
        b = R.sample(bads, 2)
        n += 1
        out.append(Q(f"env-{n:03d}", "환경", "지구를 지키는 좋은 행동은 어느 것일까요?", [g[2] + " " + g[0]] + [x[2] + " " + x[0] for x in b], 0, level=1,
                     pool=[x[2] + " " + x[0] for x in bads], group="env-pickgood"))
    for i, b in enumerate(bads):
        R = random.Random(600 + i)
        g = R.sample(goods, 2)
        n += 1
        out.append(Q(f"env-{n:03d}", "환경", "지구를 아프게 하는 행동은 어느 것일까요?", [b[2] + " " + b[0]] + [x[2] + " " + x[0] for x in g], 0, level=1,
                     pool=[x[2] + " " + x[0] for x in goods], group="env-pickbad"))
    # 계절·날씨 변화
    SEASON = [("봄이 되면 나무에는 무엇이 생길까요?", "새싹과 꽃", ["눈", "얼음"], "🌸"),
              ("가을이 되면 나뭇잎은 어떻게 될까요?", "빨갛고 노랗게 물들어요", ["파랗게 변해요", "커져요"], "🍁"),
              ("겨울이 되면 개구리는 무엇을 할까요?", "겨울잠을 자요", ["수영해요", "알을 낳아요"], "🐸"),
              ("곰은 추운 겨울에 무엇을 할까요?", "겨울잠을 자요", ["바다에 가요", "꽃을 따요"], "🐻"),
              ("여름에 많이 우는 곤충은?", "매미", ["무당벌레", "개미"], "🪲"),
              ("가을에 남쪽으로 날아가는 새는?", "제비", ["참새", "닭"], "🐦"),
              ("겨울에 우리나라로 날아오는 새는?", "두루미", ["제비", "뻐꾸기"], "🐦"),
              ("봄에 노랗게 피는 꽃은?", "개나리", ["코스모스", "국화"], "🌼"),
              ("가을에 들판에서 노랗게 익는 곡식은?", "벼", ["수박", "딸기"], "🌾"),
              ("여름에 장마가 오면 무엇이 많이 올까요?", "비", ["눈", "우박만"], "🌧️"),
              ("겨울에 물웅덩이가 얼면?", "얼음이 돼요", ["뜨거워져요", "사라져요"], "🧊"),
              ("봄에 나비는 무엇을 찾아다닐까요?", "꽃", ["눈", "돌"], "🦋")]
    for i, (q, a, w, emo) in enumerate(SEASON):
        n += 1
        out.append(Q(f"env-{n:03d}", "환경", q, [a] + w, 0, level=1, image=img(None, emo), group="env-season"))
    return out
