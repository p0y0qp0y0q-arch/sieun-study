from common import Q, img, who_kid as who, josa
import random

# 정답|오답1,오답2|이모지|위키 문서(사진)
WORDS = """
사과|사가,사콰|🍎|wp:Apple
스웨터|스왜터,스웨떠|🧥|wp:Sweater
돼지|되지,돠지|🐷|wp:Domestic pig
의자|으자,의쟈|🪑|wp:Chair
병아리|벙아리,병알이|🐥|file:Chicks_(cropped).jpg
원숭이|원숭니,원슝이|🐒|wp:Monkey
거북이|거부기,거북기|🐢|wp:Turtle
해바라기|헤바라기,해바래기|🌻|wp:Common sunflower
게|개,궤|🦀|wp:Crab
귤|굴,궐|🍊|wp:Mandarin orange
연필|연삘,년필|✏️|wp:Pencil
학교|학꾜,핚교|🏫|wp:School
신발|심발,신빨|👟|wp:Sneakers
꽃|꼿,꽂|🌸|wp:Flower
닭|닥,닯|🐔|wp:Chicken
눈썹|눈섭,눈썻|🤨|-
케이크|캐이크,케잌|🎂|wp:Birthday cake
초콜릿|초코렛,쪼꼬렛|🍫|wp:Chocolate
텔레비전|텔레비젼,텔래비전|📺|wp:Television set
컴퓨터|컴퓨타,컴퓨떠|💻|wp:Laptop
로봇|로보트,로봍|🤖|-
괴물|괘물,궤물|👹|-
책상|책쌍,챙상|📚|wp:Desk
국물|궁물,국믈|🍲|wp:Soup
부엌|부억,부얶|🍳|wp:Kitchen
흙|흑,흘|🟫|wp:Soil
옷|옫,옺|👕|wp:T-shirt
떡볶이|떡뽁이,떡복기|🍢|wp:Tteokbokki
개구리|개굴이,깨구리|🐸|wp:Frog
고양이|고양니,괴양이|🐱|wp:Cat
강아지|강아쥐,깡아지|🐶|wp:Puppy
토끼|토기,또끼|🐰|wp:Rabbit
코끼리|코기리,코끼니|🐘|wp:Elephant
기린|기릳,끼린|🦒|wp:Giraffe
사자|싸자,사쟈|🦁|wp:Lion
호랑이|호랭이,호랑니|🐯|wp:Tiger
곰|곤,꼼|🐻|wp:Brown bear
여우|여후,녀우|🦊|wp:Red fox
늑대|늑때,능대|🐺|wp:Wolf
다람쥐|다람지,다람쮜|🐿️|wp:Siberian chipmunk
고래|고레,골래|🐋|wp:Humpback whale
상어|상오,쌍어|🦈|wp:Shark
문어|무너,문오|🐙|wp:Octopus
오징어|오징오,오찡어|🦑|wp:Squid
나비|나뷔,냐비|🦋|wp:Butterfly
꿀벌|꿀뻘,끌벌|🐝|wp:Western honey bee
개미|게미,깨미|🐜|wp:Ant
잠자리|잠짜리,짬자리|🪰|wp:Dragonfly
무당벌레|무당벌래,무당뻘레|🐞|wp:Coccinella septempunctata
달팽이|달팽니,달펭이|🐌|wp:Snail
펭귄|팽귄,펭긴|🐧|wp:Penguin
앵무새|앵무세,엥무새|🦜|wp:Parrot
오리|어리,오릐|🦆|wp:Mallard
독수리|독쑤리,독수니|🦅|wp:Golden eagle
부엉이|부엉니,부헝이|🦉|wp:Eurasian eagle-owl
공룡|공뇽,공용|🦕|-
포도|포두,뽀도|🍇|wp:Grape
딸기|딸끼,달기|🍓|wp:Strawberry
수박|수빡,쑤박|🍉|wp:Watermelon
바나나|버나나,바나너|🍌|wp:Banana
복숭아|복숭이,복쑹아|🍑|wp:Peach
참외|차뫼,참왜|🍈|wp:Oriental melon
배|베,뱨|🍐|wp:Pyrus pyrifolia
감|갑,깜|🟠|wp:Diospyros kaki
레몬|래몬,레먼|🍋|wp:Lemon
파인애플|파인에플,파이내플|🍍|wp:Pineapple
체리|채리,쳬리|🍒|wp:Cherry
토마토|도마도,토마또|🍅|wp:Tomato
당근|당끈,땅근|🥕|wp:Carrot
오이|오의,오히|🥒|wp:Cucumber
감자|깜자,감쟈|🥔|wp:Potato
고구마|고구무,구구마|🍠|wp:Sweet potato
옥수수|옥쑤수,옥수스|🌽|wp:Maize
양파|양빠,양퍄|🧅|wp:Onion
버섯|버섣,버석|🍄|wp:Mushroom
브로콜리|브로컬리,브로꼴리|🥦|wp:Broccoli
김치|김취,낌치|🥬|wp:Kimchi
김밥|김빱,김밮|🍙|wp:Gimbap
라면|나면,라먼|🍜|wp:Ramyeon
만두|만듀,만도|🥟|wp:Mandu (food)
피자|삐자,피쟈|🍕|wp:Pizza
햄버거|헴버거,햄버가|🍔|wp:Hamburger
샌드위치|샌드위지,샌드이치|🥪|wp:Sandwich
아이스크림|아이스끄림,아이쓰크림|🍦|wp:Ice cream
우유|우융,으유|🥛|wp:Milk
주스|쥬스,주쓰|🧃|wp:Juice
빵|방,팡|🍞|wp:Bread
달걀|달길,닭알|🥚|wp:Egg as food
치즈|치쯔,취즈|🧀|wp:Cheese
도넛|도너츠,도낫|🍩|wp:Doughnut
사탕|사땅,샤탕|🍬|wp:Candy
쿠키|쿠끼,큐키|🍪|wp:Cookie
숟가락|숫가락,숟까락|🥄|wp:Spoon
젓가락|젇가락,저까락|🥢|wp:Chopsticks
냉장고|냉짱고,넹장고|🧊|wp:Refrigerator
세탁기|새탁기,세탁끼|🧺|wp:Washing machine
시계|시게,씨계|⏰|wp:Alarm clock
안경|안견,앙경|👓|wp:Glasses
모자|모쟈,머자|🧢|wp:Baseball cap
가방|까방,가빵|🎒|wp:Backpack
우산|우싼,우샨|☂️|wp:Umbrella
장갑|장깝,잔갑|🧤|wp:Glove
양말|양발,얌말|🧦|wp:Sock
바지|바즤,빠지|👖|wp:Jeans
치마|치메,취마|👗|wp:Skirt
단추|단쭈,던추|🔘|wp:Button
가위|가이,까위|✂️|wp:Scissors
지우개|지우게,지유개|🧽|wp:Eraser
공책|공첵,공채|📓|wp:Notebook
크레파스|크래파스,크레빠스|🖍️|wp:Crayon
풍선|풍썬,뿡선|🎈|wp:Balloon
인형|인횽,잉형|🧸|wp:Teddy bear
자전거|자전꺼,자정거|🚲|wp:Bicycle
비행기|비행끼,비헹기|✈️|wp:Airplane
기차|기챠,끼차|🚆|wp:Train
버스|뻐스,버쓰|🚌|wp:Bus
택시|텍시,택씨|🚕|wp:Taxi
소방차|소방짜,소빵차|🚒|wp:Fire engine
헬리콥터|헬리콥타,핼리콥터|🚁|wp:Helicopter
트럭|트러,추럭|🚚|wp:Truck
오토바이|오도바이,오토빠이|🏍️|wp:Motorcycle
로켓|로케트,로껫|🚀|wp:Rocket
무지개|무지게,무찌개|🌈|wp:Rainbow
구름|구룸,꾸름|☁️|wp:Cumulus cloud
눈사람|눈싸람,눈사랑|⛄|wp:Snowman
바다|바따,빠다|🌊|wp:Sea
나무|나므,나묵|🌳|wp:Tree
나뭇잎|나무입,나묻잎|🍃|wp:Leaf
별|벼,볇|⭐|-
달|닯,딸|🌙|wp:Moon
해|헤,햬|☀️|-
바위|바우,빠위|🪨|wp:Rock (geology)
모래|모레,몰래|🏖️|wp:Sand
얼음|어름,얼슴|🧊|wp:Ice cube
손|송,쏜|✋|wp:Hand
발|빨,밟|🦶|wp:Foot
귀|기,긔|👂|wp:Ear
코|꼬,커|👃|wp:Human nose
이빨|이발,이팔|🦷|wp:Tooth
무릎|무릅,무룹|🦵|wp:Knee
할머니|할머이,할먼이|👵|-
할아버지|하라버지,할아부지|👴|-
선생님|선생임,선샌님|🧑‍🏫|-
경찰관|경찰간,갱찰관|👮|wp:Police car
의사|으사,의샤|🧑‍⚕️|wp:Stethoscope
소방관|소방간,쏘방관|🧑‍🚒|wp:Firefighter
요리사|요리싸,여리사|🧑‍🍳|wp:Chef's uniform
왕관|왕간,왕꽌|👑|wp:Crown (headgear)
열쇠|열쐬,열셰|🔑|wp:Key (lock)
거울|거을,꺼울|🪞|wp:Mirror
촛불|초뿔,촛뿔|🕯️|wp:Candle
줄넘기|줄럼기,줄넘끼|🪢|wp:Skipping rope
미끄럼틀|미끄름틀,미끄럼뜰|🛝|wp:Playground slide
그네|그내,끄네|🎠|wp:Swing (seat)
피아노|삐아노,피아누|🎹|wp:Piano
북|붘,뿍|🥁|wp:Drum
축구공|축꾸공,축구꽁|⚽|wp:Ball (association football)
낙타|낙따,락타|🐫|wp:Camel
하마|하머,햐마|🦛|wp:Hippopotamus
얼룩말|얼룽말,얼룩마|🦓|wp:Zebra
캥거루|캥거로,켕거루|🦘|wp:Kangaroo
판다|펜다,빤다|🐼|wp:Giant panda
고슴도치|고슴돗치,고슴도취|🦔|wp:Hedgehog
수영장|수영짱,수용장|🏊|wp:Swimming pool
놀이터|노리터,놀이떠|🛝|wp:Playground
병원|벙원,병언|🏥|wp:Hospital
도서관|도서간,도서꽌|📚|wp:Library
편지|펀지,편찌|✉️|wp:Envelope
선물|섬물,선믈|🎁|wp:Gift wrapping
쥐|지,줘|🐭|wp:House mouse
뱀|벰,뱸|🐍|wp:Snake
소|쏘,서|🐄|wp:Cattle
말|맑,마|🐴|wp:Horse
양|얀,냥|🐑|wp:Sheep
염소|염쏘,엄소|🐐|wp:Goat
꿀|꿇,끌|🍯|wp:Honey
밤|빰,반|🌰|wp:Chestnut
땅콩|땅꽁,당콩|🥜|wp:Peanut
호박|호빡,허박|🎃|wp:Pumpkin
수건|수껀,쑤건|🧺|wp:Towel
칫솔|치솔,칟솔|🪥|wp:Toothbrush
비누|비뉴,삐누|🧼|wp:Soap
휴지|휴즤,후지|🧻|wp:Toilet paper
쓰레기통|쓰래기통,스레기통|🗑️|wp:Waste container
계단|게단,계딴|🪜|wp:Stairs
창문|창뭉,짱문|🪟|wp:Window
베개|베게,배개|🛏️|wp:Pillow
찌개|찌게,지개|🍲|wp:Jjigae
설거지|설겆이,설거쥐|🍽️|wp:Washing-up
회전목마|회전몽마,훼전목마|🎠|wp:Carousel
색연필|생연필,색년필|🖍️|wp:Colored pencil
씨앗|시앗,씨앋|🌱|wp:Seed
꽃병|꼿병,꽃뼝|🏺|wp:Vase
화분|화뿐,하분|🪴|wp:Flowerpot
돋보기|돗보기,돋뽀기|🔍|wp:Magnifying glass
망원경|망원갱,만원경|🔭|wp:Telescope
사다리|사따리,싸다리|🪜|wp:Ladder
망치|망취,만치|🔨|wp:Hammer
바구니|바고니,빠구니|🧺|wp:Basket
주전자|주잔자,주전쟈|🫖|wp:Kettle
컵|겁,컾|🥤|wp:Mug
접시|접씨,젚시|🍽️|wp:Plate (dishware)
꽈배기|꽈베기,과배기|🥨|wp:Kkwabaegi
눈사람|눈싸람,눈살람|⛄|-
횃불|햇불,홰불|🔥|wp:Torch
왼손|웬손,왠손|🤚|-
웨딩드레스|왜딩드레스,웨딩드래스|👰|wp:Wedding dress
돼지저금통|되지저금통,돼지저끔통|🐖|wp:Piggy bank
가위바위보|가이바위보,가위바이보|✊|-
궤도열차|괘도열차,궤도열챠|🚝|wp:Monorail
외투|왜투,웨투|🧥|wp:Overcoat
참새|참세,찹새|🐦|wp:Eurasian tree sparrow
까치|가치,까취|🐦|wp:Oriental magpie
비둘기|비들기,삐둘기|🕊️|wp:Rock dove
갈매기|갈메기,갈매끼|🐦|wp:Seagull
""".strip().splitlines()

# 문장 속 빈칸 (레벨 3): 문장(□ 자리) | 정답 | 오답들
SENTENCES = """
할머니 댁에 □|갔어요|갓어요,같어요
밥을 맛있게 □|먹었다|머걷다,먹엇다
@는 그림을 □|그렸어요|그렷어요,그려써요
친구랑 공원에서 □|놀았어요|노랐어요,놀앗어요
날씨가 □|맑아요|말가요,막아요
꽃이 □ 피었어요|활짝|활짞,할짝
□ 이렇게 일찍 왔니?|웬일로|왠일로,웬닐로
□ 기분이 좋아요|왠지|웬지,왼지
숙제를 다 □|했어요|햇어요,핬어요
손을 깨끗이 □|씻어요|씨서요,씼어요
방을 □ 치웠어요|깨끗이|깨끗히,깨끄시
의자에 □ 앉아 있어요|가만히|가만이,가마니
□ 생각해 봐요|곰곰이|곰곰히,곰고미
@는 커서 의사가 □ 싶어요|되고|돼고,뒈고
뛰면 안 □|돼요|되요,대요
□ 동안 비가 왔어요|며칠|몇일,몇칠
비가 오면 □?|어떡해|어떻해,어떠케
@는 하나도 □ 무서워요|안|않,앙
□ 다 먹었어요|금세|금새,금쎄
엄마랑 □를 했어요|설거지|설겆이,설꺼지
□를 베고 잠을 자요|베개|베게,배개
된장□가 맛있어요|찌개|찌게,지개
□ 할머니를 만났어요|오랜만에|오랫만에,오랜마네
연극에서 토끼 □을 맡았어요|역할|역활,여칼
□가 아삭아삭 맛있어요|깍두기|깍뚜기,깎두기
□, 같이 놀자!|얘들아|애들아,얘드라
청소는 제가 □|할게요|할께요,할개요
사탕 하나 □|줄게|줄께,쥴게
내일 또 □|갈게|갈께,갈개
우리 같이 □?|놀까요|놀가요,놀까여
□ 다시 만나자|이따가|있다가,이따까
퀴즈 정답을 □|맞혔어요|맞쳤어요,마쳤어요
공책에 스티커를 □|붙였어요|부쳤어요,붙엿어요
감기가 다 □|나았어요|낳았어요,낫았어요
닭이 알을 □|낳았어요|나았어요,낫았어요
놀이터에서 장갑을 □|잃어버렸어요|잊어버렸어요,일어버렸어요
준비물을 깜빡 □|잊어버렸어요|잃어버렸어요,이저버렸어요
손가락으로 달을 □|가리켰어요|가르쳤어요,가리컸어요
선생님께서 한글을 □ 주셨어요|가르쳐|가리켜,가르처
오늘은 기분이 □|좋아요|조아요,좋와요
넘어졌지만 □|괜찮아요|괜찬아요,갠찮아요
딸기를 □ 먹었어요|많이|만이,만히
동화책을 □|읽었어요|일겄어요,익었어요
의자에 □|앉았어요|안잤어요,앉앗어요
지우개가 □|없어요|업어요,없서요
운동장이 아주 □|넓어요|널버요,넙어요
연필이 너무 □|짧아요|짤바요,짭아요
오늘 밤은 달이 □|밝아요|발가요,박아요
물이 보글보글 □|끓어요|끌어요,끓허요
@는 엄마를 □|닮았어요|달맜어요,담았어요
달걀을 □|삶았어요|살맜어요,삼았어요
칼로 사과를 □|깎았어요|깍았어요,깟았어요
빨강과 파랑 물감을 □|섞었어요|석었어요,섞엇어요
자기 전에 이를 □|닦았어요|닥았어요,딲았어요
엄마가 □ 주셨어요|안아|아나,안와
문을 □ 들어가요|열고|열꼬,엵고
버스를 □ 학교에 가요|타고|따고,타코
아기가 □ 자고 있어요|쌔근쌔근|쌔근새근,새근쌔근
@는 □ 한글을 읽을 수 있어요|벌써|벌서,뻘써
고양이가 □ 울어요|야옹야옹|야웅야옹,야옹야웅
강아지가 꼬리를 □|흔들어요|흔드러요,흔들러요
""".strip().splitlines()

PROMPTS_A = [
    "{w}가 그림일기에 쓰려고 해요. 바른 글자는 어느 것일까요?",
    "그림에 맞는 바른 글자를 골라요.",
    "{w}가 이 그림의 이름을 쓰려고 해요. 바르게 쓴 것은?",
    "바르게 쓴 낱말을 찾아봐요.",
    "{w}는 이 그림 이름을 알아요. 맞춤법이 바른 것은?",
    "이 그림의 이름을 바르게 쓴 것을 골라요.",
]
PROMPTS_B = [
    "{w}가 받아쓰기를 했어요. 틀리게 쓴 낱말은 어느 것일까요?",
    "셋 중에 틀린 글자를 찾아봐요!",
    "{w}가 쓴 글에서 잘못 쓴 낱말을 찾아요.",
    "맞춤법이 틀린 낱말은 어느 것일까요?",
]
PROMPTS_C = [
    "{w}가 일기를 써요. 빈칸에 들어갈 바른 말은?",
    "빈칸에 알맞은 바른 글자를 골라요.",
    "문장을 바르게 완성해 봐요.",
]

def build():
    out = []
    words = []
    seen = set()
    for line in WORDS:
        w, wrong, emo, ref = line.split("|")
        if w in seen:
            continue
        seen.add(w)
        words.append((w, wrong.split(","), emo, None if ref == "-" else ref))
    n = 0
    for i, (w, wrong, emo, ref) in enumerate(words):
        n += 1
        lv = 1 if i < 60 else 2
        p = PROMPTS_A[i % len(PROMPTS_A)]
        pw = who(i, 1)
        prompt = p.replace("{w}가", pw["가"]).replace("{w}는", pw["는"])
        ch = [w] + (wrong[:1] if lv == 1 else wrong[:2])
        out.append(Q(f"kor-{n:03d}", "국어", prompt, ch, 0, level=lv,
                     image=img(ref, emo), speakChoices=False, group="kor-a"))
    # 유형 B: 틀린 낱말 찾기 (정답=틀린 것), 다른 두 낱말은 매번 바뀜(pool)
    allw = [w for w, *_ in words]
    for i, (w, wrong, emo, ref) in enumerate(words):
        n += 1
        pw = who(i, 2)
        prompt = PROMPTS_B[i % len(PROMPTS_B)].replace("{w}가", pw["가"])
        pool = [x for x in allw if x != w and len(x) <= 5]
        r = random.Random(i)
        others = r.sample(pool, 2)
        out.append(Q(f"kor-{n:03d}", "국어", prompt, [wrong[i % 2]] + others, 0, level=2,
                     pool=pool, speakChoices=False, group="kor-b"))
    for i, line in enumerate(SENTENCES):
        s, ans, wr = line.split("|")
        n += 1
        pw = who(i, 3)
        s = s.replace("@는", pw["는"]).replace("@가", pw["가"])
        prompt = PROMPTS_C[i % len(PROMPTS_C)].replace("{w}가", pw["가"])
        out.append(Q(f"kor-{n:03d}", "국어", prompt, [ans] + wr.split(","), 0, level=3,
                     display=s.replace("□", "(  ?  )"), speak=prompt + " " + s.replace("□", ", 빈칸,"), speakChoices=False, group="kor-c"))
    return out
