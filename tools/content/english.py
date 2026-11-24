from common import Q, img, who
import random

# 영단어|뜻|이모지|사진ref|분류
WORDS = """
dog|강아지|🐶|wp:Dog|animal
cat|고양이|🐱|wp:Cat|animal
pig|돼지|🐷|wp:Domestic pig|animal
cow|소|🐄|wp:Cattle|animal
horse|말|🐴|wp:Horse|animal
sheep|양|🐑|wp:Sheep|animal
duck|오리|🦆|wp:Mallard|animal
chicken|닭|🐔|wp:Chicken|animal
rabbit|토끼|🐰|wp:Rabbit|animal
lion|사자|🦁|wp:Lion|animal
tiger|호랑이|🐯|wp:Tiger|animal
elephant|코끼리|🐘|wp:Elephant|animal
monkey|원숭이|🐒|wp:Monkey|animal
bear|곰|🐻|wp:Brown bear|animal
fish|물고기|🐟|wp:Goldfish|animal
bird|새|🐦|wp:Eurasian blue tit|animal
frog|개구리|🐸|wp:Frog|animal
snake|뱀|🐍|wp:Snake|animal
mouse|쥐|🐭|wp:House mouse|animal
giraffe|기린|🦒|wp:Giraffe|animal
zebra|얼룩말|🦓|wp:Zebra|animal
penguin|펭귄|🐧|wp:Penguin|animal
whale|고래|🐋|wp:Humpback whale|animal
owl|부엉이|🦉|wp:Eurasian eagle-owl|animal
turtle|거북|🐢|wp:Turtle|animal
apple|사과|🍎|wp:Apple|fruit
banana|바나나|🍌|wp:Banana|fruit
grape|포도|🍇|wp:Grape|fruit
orange|오렌지|🍊|wp:Orange (fruit)|fruit
strawberry|딸기|🍓|wp:Strawberry|fruit
watermelon|수박|🍉|wp:Watermelon|fruit
lemon|레몬|🍋|wp:Lemon|fruit
peach|복숭아|🍑|wp:Peach|fruit
pear|배|🍐|wp:Pear|fruit
cherry|체리|🍒|wp:Cherry|fruit
pineapple|파인애플|🍍|wp:Pineapple|fruit
tomato|토마토|🍅|wp:Tomato|food
carrot|당근|🥕|wp:Carrot|food
potato|감자|🥔|wp:Potato|food
corn|옥수수|🌽|wp:Maize|food
bread|빵|🍞|wp:Bread|food
milk|우유|🥛|wp:Milk|food
egg|달걀|🥚|wp:Egg as food|food
cheese|치즈|🧀|wp:Cheese|food
cake|케이크|🎂|wp:Birthday cake|food
pizza|피자|🍕|wp:Pizza|food
rice|밥|🍚|wp:Cooked rice|food
cookie|쿠키|🍪|wp:Cookie|food
ice cream|아이스크림|🍦|wp:Ice cream|food
juice|주스|🧃|wp:Juice|food
candy|사탕|🍬|wp:Candy|food
car|자동차|🚗|wp:Car|vehicle
bus|버스|🚌|wp:Bus|vehicle
train|기차|🚆|wp:Train|vehicle
airplane|비행기|✈️|wp:Airplane|vehicle
ship|배|🚢|wp:Ship|vehicle
bicycle|자전거|🚲|wp:Bicycle|vehicle
truck|트럭|🚚|wp:Truck|vehicle
taxi|택시|🚕|wp:Taxi|vehicle
helicopter|헬리콥터|🚁|wp:Helicopter|vehicle
rocket|로켓|🚀|wp:Rocket|vehicle
boat|보트|🛶|wp:Canoe|vehicle
motorcycle|오토바이|🏍️|wp:Motorcycle|vehicle
fire truck|소방차|🚒|wp:Fire engine|vehicle
eye|눈|👁️|wp:Human eye|body
ear|귀|👂|wp:Ear|body
nose|코|👃|wp:Human nose|body
mouth|입|👄|wp:Lip|body
hand|손|✋|wp:Hand|body
foot|발|🦶|wp:Foot|body
hair|머리카락|💇|wp:Hair|body
tooth|이|🦷|wp:Tooth|body
book|책|📕|wp:Book|thing
pencil|연필|✏️|wp:Pencil|thing
bag|가방|🎒|wp:Backpack|thing
chair|의자|🪑|wp:Chair|thing
desk|책상|🗄️|wp:Desk|thing
ball|공|⚽|wp:Ball (association football)|thing
cup|컵|🥤|wp:Mug|thing
clock|시계|⏰|wp:Alarm clock|thing
hat|모자|🎩|wp:Baseball cap|thing
shoe|신발|👟|wp:Sneakers|thing
umbrella|우산|☂️|wp:Umbrella|thing
bed|침대|🛏️|wp:Bed|thing
door|문|🚪|wp:Door|thing
key|열쇠|🔑|wp:Key (lock)|thing
phone|전화기|📱|wp:Smartphone|thing
house|집|🏠|wp:House|thing
doll|인형|🧸|wp:Teddy bear|thing
kite|연|🪁|wp:Kite|thing
balloon|풍선|🎈|wp:Balloon|thing
spoon|숟가락|🥄|wp:Spoon|thing
scissors|가위|✂️|wp:Scissors|thing
glasses|안경|👓|wp:Glasses|thing
sock|양말|🧦|wp:Sock|thing
sun|해|☀️|wp:Sunrise|nature
moon|달|🌙|wp:Moon|nature
star|별|⭐|-|nature
tree|나무|🌳|wp:Tree|nature
flower|꽃|🌸|wp:Flower|nature
rain|비|🌧️|wp:Rain|nature
snow|눈|❄️|wp:Snow|nature
cloud|구름|☁️|wp:Cumulus cloud|nature
rainbow|무지개|🌈|wp:Rainbow|nature
sea|바다|🌊|wp:Sea|nature
mountain|산|⛰️|wp:Mountain|nature
leaf|나뭇잎|🍃|wp:Leaf|nature
""".strip().splitlines()

COLORS = [("red", "빨강", "#e53935"), ("blue", "파랑", "#1e63d6"), ("yellow", "노랑", "#fdd835"),
          ("green", "초록", "#43a047"), ("purple", "보라", "#8e24aa"), ("pink", "분홍", "#f48fb1"),
          ("black", "검정", "#212121"), ("white", "하양", "#ffffff"), ("brown", "갈색", "#795548"),
          ("orange", "주황", "#fb8c00"), ("gray", "회색", "#9e9e9e")]
NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

def build():
    out = []
    n = 0
    rows = []
    for line in WORDS:
        w, ko, emo, ref, cat = line.split("|")
        rows.append((w, ko, emo, None if ref == "-" else ref, cat))
    bycat = {}
    for r in rows:
        bycat.setdefault(r[4], []).append(r)
    for i, (w, ko, emo, ref, cat) in enumerate(rows):
        pool = [x[0] for x in bycat[cat] if x[0] != w]
        r = random.Random(i)
        wr = r.sample(pool, 2)
        pw = who(i, 11)
        lv = 1 if cat in ("animal", "fruit") else 2
        # 1) 사진 → 단어
        n += 1
        out.append(Q(f"eng-{n:03d}", "영어", f"{pw['가']} 본 이것은 영어로 뭘까요?" if i % 2 == 0 else "사진에 맞는 영어 단어를 골라요.",
                     [w] + wr, 0, level=lv, image=img(ref, emo), pool=pool, choiceLang="en-US", speakChoices=True, group="eng-pic2word"))
        # 2) 단어 → 사진
        n += 1
        others = [x for x in bycat[cat] if x[0] != w]
        o = r.sample(others, 2)
        ch = [img(ref, emo, label=None)] + [img(x[3], x[2]) for x in o]
        out.append(Q(f"eng-{n:03d}", "영어", f"'{w}' 는 어느 그림일까요?", ch, 0, type="imageChoice", level=lv,
                     display=w, displayLang="en-US", sayWord={"text": w, "lang": "en-US"},
                     poolImages=[img(x[3], x[2]) for x in others], group="eng-word2pic"))
        # 3) 듣고 고르기
        n += 1
        out.append(Q(f"eng-{n:03d}", "영어", "잘 듣고 알맞은 그림을 골라요.", ch, 0, type="imageChoice", level=lv + 1,
                     sayWord={"text": w, "lang": "en-US"}, listenOnly=True,
                     poolImages=[img(x[3], x[2]) for x in others], group="eng-listen"))
    # 색깔
    for i, (w, ko, hexc) in enumerate(COLORS):
        pool = [c[0] for c in COLORS if c[0] != w]
        n += 1
        out.append(Q(f"eng-{n:03d}", "영어", "이 색깔은 영어로 뭘까요?", [w] + random.Random(i).sample(pool, 2), 0, level=1,
                     image={"color": hexc, "fallbackEmoji": "🎨"}, pool=pool, choiceLang="en-US", group="eng-color"))
        n += 1
        others = [c for c in COLORS if c[0] != w]
        o = random.Random(i + 50).sample(others, 2)
        out.append(Q(f"eng-{n:03d}", "영어", f"'{w}' 는 어떤 색일까요?", [{"color": hexc, "fallbackEmoji": "🎨"}] + [{"color": c[2], "fallbackEmoji": "🎨"} for c in o], 0,
                     type="imageChoice", level=1, display=w, displayLang="en-US", sayWord={"text": w, "lang": "en-US"},
                     poolImages=[{"color": c[2], "fallbackEmoji": "🎨"} for c in others], group="eng-color2"))
    # 숫자
    for i, w in enumerate(NUMBERS):
        pool = [x for x in NUMBERS if x != w]
        n += 1
        out.append(Q(f"eng-{n:03d}", "영어", "동그라미가 몇 개예요? 영어로 골라요.", [w] + random.Random(i).sample(pool, 2), 0, level=1,
                     dots=i + 1, pool=pool, choiceLang="en-US", group="eng-number"))
        n += 1
        nums = [str(k) for k in range(1, 11) if k != i + 1]
        out.append(Q(f"eng-{n:03d}", "영어", f"'{w}' 는 숫자 몇일까요?", [str(i + 1)] + random.Random(i + 7).sample(nums, 2), 0, level=1,
                     display=w, displayLang="en-US", sayWord={"text": w, "lang": "en-US"}, pool=nums, big=True, group="eng-number2"))
    # 알파벳 대소문자
    import string
    U, L = string.ascii_uppercase, string.ascii_lowercase
    for i in range(26):
        n += 1
        pool = [c for c in L if c != L[i]]
        out.append(Q(f"eng-{n:03d}", "영어", "대문자와 짝인 소문자를 골라요.", [L[i]] + random.Random(i).sample(pool, 2), 0, level=1,
                     display=U[i], displayLang="en-US", sayWord={"text": U[i], "lang": "en-US"}, pool=pool, big=True, speakChoices=False, group="eng-abc"))
        n += 1
        pool = [c for c in U if c != U[i]]
        out.append(Q(f"eng-{n:03d}", "영어", "소문자와 짝인 대문자를 골라요.", [U[i]] + random.Random(i + 3).sample(pool, 2), 0, level=1,
                     display=L[i], displayLang="en-US", sayWord={"text": L[i], "lang": "en-US"}, pool=pool, big=True, speakChoices=False, group="eng-abc2"))
    return out
