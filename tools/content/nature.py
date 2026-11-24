from common import Q, img, who, josa
import random

# 이름|사는 곳|먹이|알/새끼|사진|이모지|분류
ANIMALS = """
사자|초원|고기|새끼|wp:Lion|🦁|포유류
호랑이|숲|고기|새끼|wp:Tiger|🐯|포유류
코끼리|초원|풀|새끼|wp:African bush elephant|🐘|포유류
기린|초원|나뭇잎|새끼|wp:Giraffe|🦒|포유류
얼룩말|초원|풀|새끼|wp:Plains zebra|🦓|포유류
하마|강·연못|풀|새끼|wp:Hippopotamus|🦛|포유류
코뿔소|초원|풀|새끼|wp:White rhinoceros|🦏|포유류
치타|초원|고기|새끼|wp:Cheetah|🐆|포유류
표범|숲|고기|새끼|wp:Leopard|🐆|포유류
하이에나|초원|고기|새끼|wp:Spotted hyena|🐺|포유류
고릴라|숲|나뭇잎|새끼|wp:Gorilla|🦍|포유류
침팬지|숲|열매|새끼|wp:Chimpanzee|🐒|포유류
오랑우탄|숲|열매|새끼|wp:Orangutan|🦧|포유류
판다|숲|대나무|새끼|wp:Giant panda|🐼|포유류
레서판다|숲|대나무|새끼|wp:Red panda|🐼|포유류
코알라|숲|나뭇잎|새끼|wp:Koala|🐨|포유류
캥거루|초원|풀|새끼|wp:Red kangaroo|🦘|포유류
반달가슴곰|숲|열매|새끼|wp:Asian black bear|🐻|포유류
북극곰|극지방|물고기|새끼|wp:Polar bear|🐻‍❄️|포유류
불곰|숲|물고기|새끼|wp:Brown bear|🐻|포유류
늑대|숲|고기|새끼|wp:Wolf|🐺|포유류
여우|숲|고기|새끼|wp:Red fox|🦊|포유류
사막여우|사막|벌레|새끼|wp:Fennec fox|🦊|포유류
북극여우|극지방|고기|새끼|wp:Arctic fox|🦊|포유류
너구리|숲|열매|새끼|wp:Common raccoon dog|🦝|포유류
라쿤|숲|열매|새끼|wp:Raccoon|🦝|포유류
다람쥐|숲|열매|새끼|wp:Siberian chipmunk|🐿️|포유류
고슴도치|숲|벌레|새끼|wp:Hedgehog|🦔|포유류
두더지|숲|벌레|새끼|wp:European mole|🐀|포유류
수달|강·연못|물고기|새끼|wp:Eurasian otter|🦦|포유류
비버|강·연못|나뭇잎|새끼|wp:North American beaver|🦫|포유류
사슴|숲|풀|새끼|wp:Red deer|🦌|포유류
순록|극지방|풀|새끼|wp:Reindeer|🦌|포유류
낙타|사막|풀|새끼|wp:Dromedary|🐫|포유류
라마|초원|풀|새끼|wp:Llama|🦙|포유류
박쥐|숲|벌레|새끼|wp:Fruit bat|🦇|포유류
나무늘보|숲|나뭇잎|새끼|wp:Sloth|🦥|포유류
개미핥기|숲|벌레|새끼|wp:Giant anteater|🐜|포유류
토끼|농장|풀|새끼|wp:Rabbit|🐰|포유류
강아지|집|사료|새끼|wp:Dog|🐶|포유류
고양이|집|사료|새끼|wp:Cat|🐱|포유류
햄스터|집|씨앗|새끼|wp:Golden hamster|🐹|포유류
소|농장|풀|새끼|wp:Cattle|🐄|포유류
말|농장|풀|새끼|wp:Horse|🐴|포유류
돼지|농장|사료|새끼|wp:Domestic pig|🐷|포유류
양|농장|풀|새끼|wp:Sheep|🐑|포유류
염소|농장|풀|새끼|wp:Goat|🐐|포유류
당나귀|농장|풀|새끼|wp:Donkey|🫏|포유류
고래|바다|물고기|새끼|wp:Humpback whale|🐋|포유류
돌고래|바다|물고기|새끼|wp:Common bottlenose dolphin|🐬|포유류
물개|바다|물고기|새끼|wp:Fur seal|🦭|포유류
바다사자|바다|물고기|새끼|wp:California sea lion|🦭|포유류
바다코끼리|극지방|조개|새끼|wp:Walrus|🦭|포유류
해달|바다|조개|새끼|wp:Sea otter|🦦|포유류
펭귄|극지방|물고기|알|wp:Emperor penguin|🐧|새
타조|초원|풀|알|wp:Common ostrich|🦤|새
독수리|숲|고기|알|wp:Golden eagle|🦅|새
부엉이|숲|쥐|알|wp:Eurasian eagle-owl|🦉|새
앵무새|숲|열매|알|wp:Scarlet macaw|🦜|새
홍학|강·연못|새우|알|wp:American flamingo|🦩|새
백조|강·연못|풀|알|wp:Mute swan|🦢|새
오리|강·연못|풀|알|wp:Mallard|🦆|새
닭|농장|씨앗|알|wp:Chicken|🐔|새
공작|숲|씨앗|알|wp:Indian peafowl|🦚|새
딱따구리|숲|벌레|알|wp:Great spotted woodpecker|🐦|새
참새|마을|씨앗|알|wp:Eurasian tree sparrow|🐦|새
까치|마을|벌레|알|wp:Oriental magpie|🐦|새
비둘기|마을|씨앗|알|wp:Rock dove|🕊️|새
갈매기|바다|물고기|알|wp:European herring gull|🐦|새
펠리컨|바다|물고기|알|wp:Brown pelican|🐦|새
두루미|강·연못|물고기|알|wp:Red-crowned crane|🐦|새
제비|마을|벌레|알|wp:Barn swallow|🐦|새
벌새|숲|꿀|알|wp:Hummingbird|🐦|새
큰부리새|숲|열매|알|wp:Toco toucan|🐦|새
악어|강·연못|고기|알|wp:Nile crocodile|🐊|파충류
거북|강·연못|풀|알|wp:Turtle|🐢|파충류
바다거북|바다|해초|알|wp:Green sea turtle|🐢|파충류
뱀|숲|쥐|알|wp:Corn snake|🐍|파충류
카멜레온|숲|벌레|알|wp:Veiled chameleon|🦎|파충류
이구아나|숲|나뭇잎|알|wp:Green iguana|🦎|파충류
도마뱀|사막|벌레|알|wp:Lizard|🦎|파충류
개구리|강·연못|벌레|알|wp:Frog|🐸|양서류
도롱뇽|강·연못|벌레|알|wp:Salamander|🦎|양서류
상어|바다|물고기|새끼|wp:Great white shark|🦈|물고기
금붕어|집|사료|알|wp:Goldfish|🐠|물고기
흰동가리|바다|플랑크톤|알|wp:Ocellaris clownfish|🐠|물고기
복어|바다|조개|알|wp:Pufferfish|🐡|물고기
연어|강·연못|벌레|알|wp:Salmon|🐟|물고기
가오리|바다|조개|새끼|wp:Manta ray|🐟|물고기
해마|바다|플랑크톤|새끼|wp:Seahorse|🐴|물고기
문어|바다|게|알|wp:Octopus|🐙|연체동물
오징어|바다|물고기|알|wp:Squid|🦑|연체동물
해파리|바다|플랑크톤|알|wp:Jellyfish|🪼|기타
불가사리|바다|조개|알|wp:Starfish|⭐|기타
게|바다|조개|알|wp:Crab|🦀|기타
새우|바다|플랑크톤|알|wp:Shrimp|🦐|기타
달팽이|숲|나뭇잎|알|wp:Snail|🐌|연체동물
꿀벌|숲|꿀|알|wp:Western honey bee|🐝|곤충
나비|숲|꿀|알|wp:Butterfly|🦋|곤충
개미|숲|벌레|알|wp:Ant|🐜|곤충
무당벌레|숲|진딧물|알|wp:Coccinella septempunctata|🐞|곤충
잠자리|강·연못|벌레|알|wp:Dragonfly|🪰|곤충
매미|숲|나무즙|알|wp:Cicada|🪲|곤충
메뚜기|초원|풀|알|wp:Grasshopper|🦗|곤충
사슴벌레|숲|나무즙|알|wp:Stag beetle|🪲|곤충
장수풍뎅이|숲|나무즙|알|wp:Allomyrina dichotoma|🪲|곤충
반딧불이|숲|달팽이|알|wp:Firefly|✨|곤충
귀뚜라미|초원|풀|알|wp:Cricket (insect)|🦗|곤충
""".strip().splitlines()

PLANTS = """
해바라기|꽃|wp:Common sunflower|🌻
장미|꽃|wp:Rose|🌹
튤립|꽃|wp:Tulip|🌷
민들레|꽃|wp:Taraxacum officinale|🌼
무궁화|꽃|wp:Hibiscus syriacus|🌺
벚꽃|꽃|wp:Cherry blossom|🌸
진달래|꽃|wp:Rhododendron mucronulatum|🌸
개나리|꽃|wp:Forsythia koreana|🌼
나팔꽃|꽃|wp:Ipomoea nil|🌺
코스모스|꽃|wp:Cosmos bipinnatus|🌸
연꽃|꽃|wp:Nelumbo nucifera|🪷
백합|꽃|wp:Lilium|🌷
국화|꽃|wp:Chrysanthemum|🌼
선인장|식물|wp:Cactus|🌵
소나무|나무|wp:Pinus densiflora|🌲
단풍나무|나무|wp:Acer palmatum|🍁
은행나무|나무|wp:Ginkgo biloba|🍂
대나무|나무|wp:Bamboo|🎋
야자나무|나무|wp:Coconut|🌴
클로버|식물|wp:Trifolium repens|☘️
""".strip().splitlines()

FRUITS = """
사과|나무|wp:Apple|🍎
배|나무|wp:Pyrus pyrifolia|🍐
감|나무|wp:Diospyros kaki|🟠
복숭아|나무|wp:Peach|🍑
귤|나무|wp:Mandarin orange|🍊
포도|덩굴|wp:Grape|🍇
딸기|땅|wp:Strawberry|🍓
수박|땅|wp:Watermelon|🍉
참외|땅|wp:Oriental melon|🍈
바나나|나무|wp:Banana|🍌
파인애플|땅|wp:Pineapple|🍍
블루베리|나무|wp:Blueberry|🫐
키위|덩굴|wp:Kiwifruit|🥝
체리|나무|wp:Cherry|🍒
밤|나무|wp:Chestnut|🌰
""".strip().splitlines()

DINOS = """
티라노사우루스|고기|wp:Tyrannosaurus|🦖
트리케라톱스|풀|wp:Triceratops|🦕
스테고사우루스|풀|wp:Stegosaurus|🦕
브라키오사우루스|풀|wp:Brachiosaurus|🦕
안킬로사우루스|풀|wp:Ankylosaurus|🦕
프테라노돈|물고기|wp:Pteranodon|🦅
벨로키랍토르|고기|wp:Velociraptor|🦖
파키케팔로사우루스|풀|wp:Pachycephalosaurus|🦕
스피노사우루스|물고기|wp:Spinosaurus|🦖
파라사우롤로푸스|풀|wp:Parasaurolophus|🦕
""".strip().splitlines()

SEASONS = [("봄", "wp:Cherry blossom", "🌸", ["벚꽃이 피어요", "새싹이 돋아요", "개나리가 노랗게 피어요"]),
           ("여름", "wp:Beach", "🏖️", ["바닷가에서 수영해요", "매미가 맴맴 울어요", "덥고 비가 많이 와요"]),
           ("가을", "wp:Autumn leaf color", "🍁", ["나뭇잎이 빨갛고 노랗게 물들어요", "벼가 노랗게 익어요", "밤과 감을 따요"]),
           ("겨울", "wp:Snowman", "⛄", ["눈사람을 만들어요", "눈이 펑펑 와요", "털장갑을 껴요"])]
WEATHER = [("맑음", "wp:Sky", "☀️"), ("비", "wp:Rain", "🌧️"), ("눈", "wp:Snow", "❄️"), ("흐림", "wp:Overcast", "☁️"),
           ("번개", "wp:Lightning", "⚡"), ("무지개", "wp:Rainbow", "🌈"), ("안개", "wp:Fog", "🌫️"), ("바람", "wp:Wind", "🌬️")]
WEATHER_Q = [
    ("비가 오는 날에는 무엇을 챙길까요?", "우산", ["선글라스", "부채"], "☔"),
    ("햇볕이 쨍쨍한 여름날 밖에 나갈 때 쓰면 좋은 것은?", "모자", ["털장갑", "목도리"], "🧢"),
    ("눈이 펑펑 오는 날 할 수 있는 놀이는?", "눈사람 만들기", ["물놀이", "모래성 쌓기"], "⛄"),
    ("번개가 칠 때는 어디에 있어야 안전할까요?", "집 안", ["큰 나무 아래", "넓은 운동장"], "⚡"),
    ("비가 그치고 해가 나면 하늘에 무엇이 생길 수 있을까요?", "무지개", ["눈", "별똥별"], "🌈"),
    ("바람이 많이 부는 날 하기 좋은 놀이는?", "연날리기", ["물총놀이", "눈썰매"], "🪁"),
    ("구름이 해를 가려서 하늘이 회색이에요. 이런 날씨는?", "흐림", ["맑음", "눈"], "☁️"),
    ("추운 겨울에 물이 얼면 무엇이 될까요?", "얼음", ["수증기", "구름"], "🧊"),
    ("물이 끓으면 하얀 김이 나와요. 이 김은 무엇일까요?", "수증기", ["얼음", "모래"], "♨️"),
    ("하늘에서 떨어지는 작은 얼음 알갱이는?", "우박", ["무지개", "이슬"], "🌨️"),
    ("아침에 풀잎에 맺힌 작은 물방울은?", "이슬", ["눈", "우박"], "💧"),
    ("황사가 심한 날에는 무엇을 쓰면 좋을까요?", "마스크", ["수영모", "왕관"], "😷"),
]
GROWTH = [
    ("씨앗이 자라는 순서에서 맨 처음은?", "씨앗", ["꽃", "열매"], "🌱"),
    ("씨앗 → 싹 → 줄기와 잎 → 꽃 → ?", "열매", ["씨앗", "뿌리"], "🍎"),
    ("씨앗을 심고 나서 가장 먼저 나오는 것은?", "싹", ["열매", "꽃"], "🌱"),
    ("식물이 자라려면 꼭 필요한 것이 아닌 것은?", "사탕", ["햇빛", "물"], "🌞"),
    ("식물이 땅속에서 물을 빨아들이는 부분은?", "뿌리", ["꽃", "잎"], "🌿"),
    ("알 → 애벌레 → 번데기 → ? 나비가 되는 순서예요", "나비", ["알", "올챙이"], "🦋"),
    ("개구리는 어릴 때 무엇이라고 부를까요?", "올챙이", ["애벌레", "병아리"], "🐸"),
    ("닭은 어릴 때 무엇이라고 부를까요?", "병아리", ["올챙이", "강아지"], "🐥"),
    ("개는 어릴 때 무엇이라고 부를까요?", "강아지", ["송아지", "망아지"], "🐶"),
    ("소는 어릴 때 무엇이라고 부를까요?", "송아지", ["망아지", "병아리"], "🐄"),
    ("말은 어릴 때 무엇이라고 부를까요?", "망아지", ["송아지", "강아지"], "🐴"),
    ("나비의 애벌레가 실을 감고 쉬는 모습은?", "번데기", ["올챙이", "알"], "🐛"),
    ("모기의 애벌레는 무엇이라고 부를까요?", "장구벌레", ["올챙이", "병아리"], "🦟"),
]
# 동물 소리 (사운드 파일은 tools/fetch_sounds.py 가 assets/sounds/ 에 만듦)
ANIMAL_SOUNDS = ["강아지", "고양이", "소", "닭", "오리", "양", "염소", "말", "돼지", "개구리", "부엉이", "사자",
                 "코끼리", "늑대", "까치", "갈매기", "귀뚜라미", "매미", "당나귀", "돌고래", "참새", "비둘기", "칠면조", "뻐꾸기"]

def build(sounds):
    out = []
    n = 0
    rows = [dict(zip(["nm", "hab", "food", "birth", "ref", "emo", "cls"], l.split("|"))) for l in ANIMALS]
    names = [r["nm"] for r in rows]
    for i, r in enumerate(rows):
        R = random.Random(i)
        im = img(r["ref"], r["emo"])
        pw = who(i, 51)
        pool = [x for x in names if x != r["nm"]]
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", f"{pw['가']} 동물원에서 이 동물을 만났어요. 이름이 뭘까요?" if i % 2 == 0 else "이 동물의 이름은 무엇일까요?",
                     [r["nm"]] + R.sample(pool, 2), 0, level=1 if i < 50 else 2, image=im, pool=pool, group="nat-name"))
        habs = ["바다", "숲", "사막", "극지방", "초원", "강·연못", "농장", "집", "마을"]
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", f"{r['nm']}{josa(r['nm'],'은','는')} 주로 어디에 살까요?",
                     [r["hab"]] + R.sample([h for h in habs if h != r["hab"]], 2), 0, level=2, image=im,
                     pool=[h for h in habs if h != r["hab"]], group="nat-habitat"))
        if i % 2 == 0 or r["food"] in ("대나무", "꿀", "나무즙", "물고기", "고기"):
            foods = ["풀", "고기", "물고기", "벌레", "꿀", "나뭇잎", "열매", "대나무", "씨앗", "조개", "나무즙", "플랑크톤"]
            n += 1
            out.append(Q(f"nat-{n:03d}", "자연", f"{r['nm']}{josa(r['nm'],'이','가')} 좋아하는 먹이는 무엇일까요?",
                         [r["food"]] + R.sample([f for f in foods if f != r["food"] and f not in ("사료",)], 2), 0, level=2, image=im,
                         pool=[f for f in foods if f != r["food"]], group="nat-food"))
        if r["cls"] in ("포유류", "새", "파충류") or r["nm"] in ("상어", "해마", "가오리", "개구리"):
            n += 1
            out.append(Q(f"nat-{n:03d}", "자연", f"{r['nm']}{josa(r['nm'],'은','는')} 알을 낳을까요, 새끼를 낳을까요?",
                         ["알을 낳아요" if r["birth"] == "알" else "새끼를 낳아요",
                          "새끼를 낳아요" if r["birth"] == "알" else "알을 낳아요"], 0, level=2, image=im, group="nat-birth"))
    # 이름 → 사진
    for i, r in enumerate(rows[::2]):
        R = random.Random(1000 + i)
        others = [x for x in rows if x["nm"] != r["nm"]]
        o = R.sample(others, 2)
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", f"{r['nm']}{josa(r['nm'],'은','는')} 어느 사진일까요?",
                     [img(r["ref"], r["emo"])] + [img(x["ref"], x["emo"]) for x in o], 0, type="imageChoice", level=1,
                     poolImages=[img(x["ref"], x["emo"]) for x in others], display=r["nm"], group="nat-name2pic"))
    # 울음소리
    byname = {r["nm"]: r for r in rows}
    extra = {"칠면조": ("wp:Wild turkey", "🦃"), "뻐꾸기": ("wp:Common cuckoo", "🐦")}
    for i, nm in enumerate(ANIMAL_SOUNDS):
        snd = sounds.get("animal:" + nm)
        if not snd:
            continue
        ref, emo = (byname[nm]["ref"], byname[nm]["emo"]) if nm in byname else extra[nm]
        cands = [x for x in ANIMAL_SOUNDS if x != nm and (x in byname or x in extra)]
        R = random.Random(2000 + i)
        def mk(x):
            rr, ee = (byname[x]["ref"], byname[x]["emo"]) if x in byname else extra[x]
            return img(rr, ee, label=x)
        o = R.sample(cands, 2)
        pw = who(i, 52)
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", f"{pw['가']} 숲에서 이 소리를 들었어요. 어떤 동물일까요?" if i % 2 else "잘 듣고, 이 소리를 내는 동물을 골라요.",
                     [mk(nm)] + [mk(x) for x in o], 0, type="imageChoice", level=2, sound=snd,
                     poolImages=[mk(x) for x in cands], group="nat-sound"))
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", "이 소리는 어떤 동물의 울음소리일까요?", [nm] + o, 0, level=2, sound=snd, pool=cands, group="nat-sound2"))
    for i, l in enumerate(PLANTS):
        nm, kind, ref, emo = l.split("|")
        R = random.Random(3000 + i)
        pool = [x.split("|")[0] for x in PLANTS if x.split("|")[0] != nm]
        n += 1
        pw = who(i, 53)
        out.append(Q(f"nat-{n:03d}", "자연", f"{pw['가']} 산책하다가 이 {kind}{josa(kind,'을','를')} 봤어요. 이름은?",
                     [nm] + R.sample(pool, 2), 0, level=2, image=img(ref, emo), pool=pool, group="nat-plant"))
    for i, l in enumerate(FRUITS):
        nm, where, ref, emo = l.split("|")
        R = random.Random(4000 + i)
        pool = [x.split("|")[0] for x in FRUITS if x.split("|")[0] != nm]
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", "이 과일의 이름은 무엇일까요?", [nm] + R.sample(pool, 2), 0, level=1,
                     image=img(ref, emo), pool=pool, group="nat-fruit"))
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", f"{nm}{josa(nm,'은','는')} 어디에서 열릴까요?",
                     {"나무": ["나무에 열려요", "땅에서 자라요", "덩굴에 열려요"], "땅": ["땅에서 자라요", "나무에 열려요", "덩굴에 열려요"],
                      "덩굴": ["덩굴에 열려요", "땅에서 자라요", "나무에 열려요"]}[where], 0, level=3, image=img(ref, emo), group="nat-fruit-where"))
    for i, l in enumerate(DINOS):
        nm, food, ref, emo = l.split("|")
        R = random.Random(5000 + i)
        pool = [x.split("|")[0] for x in DINOS if x.split("|")[0] != nm]
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", "이 공룡의 이름은 무엇일까요? (복원 그림)", [nm] + R.sample(pool, 2), 0, level=3,
                     image=img(ref, emo), pool=pool, group="nat-dino"))
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", f"{nm}{josa(nm,'은','는')} 무엇을 먹었을까요?",
                     [food] + [x for x in ["고기", "풀", "물고기"] if x != food], 0, level=3, image=img(ref, emo), group="nat-dino-food"))
    seasons = [s[0] for s in SEASONS]
    for i, (s, ref, emo, facts) in enumerate(SEASONS):
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", "사진 속 계절은 언제일까요?", [s] + [x for x in seasons if x != s][:2], 0, level=1,
                     image=img(ref, emo), pool=[x for x in seasons if x != s], group="nat-season"))
        for j, f in enumerate(facts):
            n += 1
            pw = who(i * 5 + j, 54)
            out.append(Q(f"nat-{n:03d}", "자연", f"'{f}' 이런 계절은 언제일까요?", [s] + [x for x in seasons if x != s][:2], 0, level=1,
                         image=img(None, emo), pool=[x for x in seasons if x != s], group="nat-season2"))
    wn = [w[0] for w in WEATHER]
    for i, (w, ref, emo) in enumerate(WEATHER):
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", "사진 속 날씨는 어떤가요?", [w] + random.Random(i).sample([x for x in wn if x != w], 2), 0, level=1,
                     image=img(ref, emo), pool=[x for x in wn if x != w], group="nat-weather"))
    for i, (q, a, wr, emo) in enumerate(WEATHER_Q + GROWTH):
        n += 1
        out.append(Q(f"nat-{n:03d}", "자연", q, [a] + wr, 0, level=2, image=img(None, emo), group="nat-qa"))
    return out
