from common import Q, img, who
import random

# 나라|대륙|국기 파일명(Commons)
COUNTRIES = """
대한민국|아시아|Flag_of_South_Korea.svg
일본|아시아|Flag_of_Japan.svg
중국|아시아|Flag_of_the_People's_Republic_of_China.svg
몽골|아시아|Flag_of_Mongolia.svg
베트남|아시아|Flag_of_Vietnam.svg
태국|아시아|Flag_of_Thailand.svg
필리핀|아시아|Flag_of_the_Philippines.svg
인도네시아|아시아|Flag_of_Indonesia.svg
말레이시아|아시아|Flag_of_Malaysia.svg
싱가포르|아시아|Flag_of_Singapore.svg
인도|아시아|Flag_of_India.svg
네팔|아시아|Flag_of_Nepal.svg
파키스탄|아시아|Flag_of_Pakistan.svg
방글라데시|아시아|Flag_of_Bangladesh.svg
스리랑카|아시아|Flag_of_Sri_Lanka.svg
캄보디아|아시아|Flag_of_Cambodia.svg
라오스|아시아|Flag_of_Laos.svg
미얀마|아시아|Flag_of_Myanmar.svg
카자흐스탄|아시아|Flag_of_Kazakhstan.svg
우즈베키스탄|아시아|Flag_of_Uzbekistan.svg
사우디아라비아|아시아|Flag_of_Saudi_Arabia.svg
아랍에미리트|아시아|Flag_of_the_United_Arab_Emirates.svg
이스라엘|아시아|Flag_of_Israel.svg
튀르키예|아시아|Flag_of_Turkey.svg
이란|아시아|Flag_of_Iran.svg
카타르|아시아|Flag_of_Qatar.svg
영국|유럽|Flag_of_the_United_Kingdom.svg
프랑스|유럽|Flag_of_France.svg
독일|유럽|Flag_of_Germany.svg
이탈리아|유럽|Flag_of_Italy.svg
스페인|유럽|Flag_of_Spain.svg
포르투갈|유럽|Flag_of_Portugal.svg
네덜란드|유럽|Flag_of_the_Netherlands.svg
벨기에|유럽|Flag_of_Belgium.svg
스위스|유럽|Flag_of_Switzerland.svg
오스트리아|유럽|Flag_of_Austria.svg
스웨덴|유럽|Flag_of_Sweden.svg
노르웨이|유럽|Flag_of_Norway.svg
덴마크|유럽|Flag_of_Denmark.svg
핀란드|유럽|Flag_of_Finland.svg
아이슬란드|유럽|Flag_of_Iceland.svg
아일랜드|유럽|Flag_of_Ireland.svg
폴란드|유럽|Flag_of_Poland.svg
체코|유럽|Flag_of_the_Czech_Republic.svg
헝가리|유럽|Flag_of_Hungary.svg
그리스|유럽|Flag_of_Greece.svg
러시아|유럽|Flag_of_Russia.svg
우크라이나|유럽|Flag_of_Ukraine.svg
루마니아|유럽|Flag_of_Romania.svg
크로아티아|유럽|Flag_of_Croatia.svg
불가리아|유럽|Flag_of_Bulgaria.svg
에스토니아|유럽|Flag_of_Estonia.svg
미국|북아메리카|Flag_of_the_United_States.svg
캐나다|북아메리카|Flag_of_Canada_(Pantone).svg
멕시코|북아메리카|Flag_of_Mexico.svg
쿠바|북아메리카|Flag_of_Cuba.svg
자메이카|북아메리카|Flag_of_Jamaica.svg
파나마|북아메리카|Flag_of_Panama.svg
코스타리카|북아메리카|Flag_of_Costa_Rica.svg
브라질|남아메리카|Flag_of_Brazil.svg
아르헨티나|남아메리카|Flag_of_Argentina.svg
칠레|남아메리카|Flag_of_Chile.svg
페루|남아메리카|Flag_of_Peru.svg
콜롬비아|남아메리카|Flag_of_Colombia.svg
베네수엘라|남아메리카|Flag_of_Venezuela.svg
우루과이|남아메리카|Flag_of_Uruguay.svg
에콰도르|남아메리카|Flag_of_Ecuador.svg
볼리비아|남아메리카|Flag_of_Bolivia.svg
이집트|아프리카|Flag_of_Egypt.svg
남아프리카 공화국|아프리카|Flag_of_South_Africa.svg
케냐|아프리카|Flag_of_Kenya.svg
나이지리아|아프리카|Flag_of_Nigeria.svg
에티오피아|아프리카|Flag_of_Ethiopia.svg
모로코|아프리카|Flag_of_Morocco.svg
가나|아프리카|Flag_of_Ghana.svg
탄자니아|아프리카|Flag_of_Tanzania.svg
세네갈|아프리카|Flag_of_Senegal.svg
카메룬|아프리카|Flag_of_Cameroon.svg
마다가스카르|아프리카|Flag_of_Madagascar.svg
알제리|아프리카|Flag_of_Algeria.svg
튀니지|아프리카|Flag_of_Tunisia.svg
호주|오세아니아|Flag_of_Australia_(converted).svg
뉴질랜드|오세아니아|Flag_of_New_Zealand.svg
피지|오세아니아|Flag_of_Fiji.svg
파푸아뉴기니|오세아니아|Flag_of_Papua_New_Guinea.svg
""".strip().splitlines()

# 명소|나라|사진ref
LANDMARKS = """
에펠탑|프랑스|wp:Eiffel Tower
개선문|프랑스|wp:Arc de Triomphe
몽생미셸|프랑스|wp:Mont-Saint-Michel
피라미드|이집트|wp:Giza pyramid complex
스핑크스|이집트|wp:Great Sphinx of Giza
만리장성|중국|wp:Great Wall of China
자금성|중국|wp:Forbidden City
자유의 여신상|미국|wp:Statue of Liberty
금문교|미국|wp:Golden Gate Bridge
그랜드 캐니언|미국|wp:Grand Canyon
타지마할|인도|wp:Taj Mahal
콜로세움|이탈리아|wp:Colosseum
피사의 사탑|이탈리아|wp:Leaning Tower of Pisa
베네치아|이탈리아|wp:Venice
빅벤|영국|wp:Big Ben
타워 브리지|영국|wp:Tower Bridge
스톤헨지|영국|wp:Stonehenge
오페라 하우스|호주|wp:Sydney Opera House
울루루|호주|wp:Uluru
후지산|일본|wp:Mount Fuji
금각사|일본|wp:Kinkaku-ji
경복궁|대한민국|wp:Gyeongbokgung
남산타워|대한민국|wp:N Seoul Tower
불국사|대한민국|wp:Bulguksa
숭례문|대한민국|wp:Namdaemun
첨성대|대한민국|wp:Cheomseongdae
한라산|대한민국|wp:Hallasan
사그라다 파밀리아|스페인|wp:Sagrada Família
알함브라 궁전|스페인|wp:Alhambra
파르테논 신전|그리스|wp:Parthenon
산토리니|그리스|wp:Santorini
노이슈반슈타인 성|독일|wp:Neuschwanstein Castle
브란덴부르크 문|독일|wp:Brandenburg Gate
성 바실리 대성당|러시아|wp:Saint Basil's Cathedral
앙코르 와트|캄보디아|wp:Angkor Wat
마추픽추|페루|wp:Machu Picchu
예수상|브라질|wp:Christ the Redeemer (statue)
이과수 폭포|아르헨티나|wp:Iguazu Falls
나이아가라 폭포|캐나다|wp:Niagara Falls
킬리만자로산|탄자니아|wp:Mount Kilimanjaro
부르즈 할리파|아랍에미리트|wp:Burj Khalifa
마리나 베이 샌즈|싱가포르|wp:Marina Bay Sands
페트로나스 타워|말레이시아|wp:Petronas Towers
치첸이트사|멕시코|wp:Chichen Itza
풍차 마을|네덜란드|wp:Kinderdijk
마터호른|스위스|wp:Matterhorn
""".strip().splitlines()

# 음식|나라|사진
FOODS = """
김치|대한민국|wp:Kimchi
비빔밥|대한민국|wp:Bibimbap
초밥|일본|wp:Sushi
라멘|일본|wp:Ramen
피자|이탈리아|wp:Pizza
스파게티|이탈리아|wp:Spaghetti
햄버거|미국|wp:Hamburger
크루아상|프랑스|wp:Croissant
바게트|프랑스|wp:Baguette
딤섬|중국|wp:Dim sum
베이징 덕|중국|wp:Peking duck
쌀국수|베트남|wp:Pho
똠얌꿍|태국|wp:Tom yum
카레|인도|wp:Curry
타코|멕시코|wp:Taco
파에야|스페인|wp:Paella
소시지|독일|wp:Bratwurst
피시 앤드 칩스|영국|wp:Fish and chips
케밥|튀르키예|wp:Doner kebab
와플|벨기에|wp:Waffle
퐁뒤|스위스|wp:Fondue
보르시|우크라이나|wp:Borscht
""".strip().splitlines()

# 동물|나라|사진
ANIMALS = """
판다|중국|wp:Giant panda
캥거루|호주|wp:Kangaroo
코알라|호주|wp:Koala
키위새|뉴질랜드|wp:Kiwi (bird)
대머리독수리|미국|wp:Bald eagle
비버|캐나다|wp:North American beaver
라마|페루|wp:Llama
벵골호랑이|인도|wp:Bengal tiger
여우원숭이|마다가스카르|wp:Ring-tailed lemur
낙타|이집트|wp:Dromedary
진돗개|대한민국|wp:Korean Jindo
시바견|일본|wp:Shiba Inu
""".strip().splitlines()

GREETINGS = """
안녕하세요|대한민국|ko-KR
곤니치와|일본|ja-JP
니하오|중국|zh-CN
헬로|미국|en-US
봉주르|프랑스|fr-FR
구텐 탁|독일|de-DE
차오|이탈리아|it-IT
올라|스페인|es-ES
즈드라스트부이체|러시아|ru-RU
나마스테|인도|hi-IN
싸왓디|태국|th-TH
씬 짜오|베트남|vi-VN
메르하바|튀르키예|tr-TR
올라 (봉 지아)|브라질|pt-BR
잠보|케냐|sw-KE
""".strip().splitlines()
GREET_NATIVE = {"ja-JP": "こんにちは", "zh-CN": "你好", "en-US": "Hello", "fr-FR": "Bonjour", "de-DE": "Guten Tag",
                "it-IT": "Ciao", "es-ES": "Hola", "ru-RU": "Здравствуйте", "hi-IN": "नमस्ते", "th-TH": "สวัสดี",
                "vi-VN": "Xin chào", "tr-TR": "Merhaba", "pt-BR": "Olá, bom dia", "sw-KE": "Jambo", "ko-KR": "안녕하세요"}

def build():
    out = []
    n = 0
    cs = [l.split("|") for l in COUNTRIES]
    names = [c[0] for c in cs]
    flag = {c[0]: img("file:" + c[2], "🏳️", flag=True) for c in cs}
    for i, (nm, cont, f) in enumerate(cs):
        R = random.Random(i)
        pool = [x for x in names if x != nm]
        same = [x for x in names if x != nm and dict((c[0], c[1]) for c in cs)[x] == cont]
        pw = who(i, 41)
        n += 1
        out.append(Q(f"wld-{n:03d}", "세계", "이 국기는 어느 나라 국기일까요?",
                     [nm] + R.sample(same if len(same) >= 2 else pool, 2), 0, level=1 if i < 30 else 2,
                     image=flag[nm], pool=same if len(same) >= 4 else pool, group="wld-flag"))
        n += 1
        o = R.sample(same if len(same) >= 2 else pool, 2)
        out.append(Q(f"wld-{n:03d}", "세계", f"{nm}의 국기는 어느 것일까요?", [flag[nm]] + [flag[x] for x in o], 0,
                     type="imageChoice", level=2, poolImages=[flag[x] for x in (same if len(same) >= 4 else pool)], group="wld-flag2"))
        if i % 2 == 0:
            n += 1
            conts = ["아시아", "유럽", "아프리카", "북아메리카", "남아메리카", "오세아니아"]
            out.append(Q(f"wld-{n:03d}", "세계", f"{nm}{'은' if (ord(nm[-1])-0xAC00)%28 else '는'} 어느 대륙에 있을까요?",
                         [cont] + R.sample([c for c in conts if c != cont], 2), 0, level=3, image=flag[nm],
                         pool=[c for c in conts if c != cont], group="wld-continent"))
    for i, l in enumerate(LANDMARKS):
        nm, c, ref = l.split("|")
        R = random.Random(100 + i)
        pool = [x for x in sorted(set(x.split("|")[1] for x in LANDMARKS)) if x != c]
        pw = who(i, 42)
        n += 1
        out.append(Q(f"wld-{n:03d}", "세계", f"{pw['가']} 비행기를 타고 {nm}{'을' if (ord(nm[-1])-0xAC00)%28 else '를'} 보러 왔어요. 여기는 어느 나라일까요?",
                     [c] + R.sample(pool, 2), 0, level=2, image=img(ref, "🗺️"), pool=pool, group="wld-landmark"))
        n += 1
        lp = [x.split("|")[0] for x in LANDMARKS if x.split("|")[0] != nm]
        out.append(Q(f"wld-{n:03d}", "세계", "사진 속 이곳의 이름은 무엇일까요?", [nm] + R.sample(lp, 2), 0, level=3,
                     image=img(ref, "🗺️"), pool=lp, group="wld-landmark-name"))
    for i, l in enumerate(FOODS):
        nm, c, ref = l.split("|")
        R = random.Random(200 + i)
        pool = [x for x in sorted(set(x.split("|")[1] for x in FOODS)) if x != c]
        pw = who(i, 43)
        n += 1
        out.append(Q(f"wld-{n:03d}", "세계", f"{pw['가']} 여행 가서 {nm}{'을' if (ord(nm[-1])-0xAC00)%28 else '를'} 먹었어요. 어느 나라 음식일까요?",
                     [c] + R.sample(pool, 2), 0, level=2, image=img(ref, "🍽️"), pool=pool, group="wld-food"))
    for i, l in enumerate(ANIMALS):
        nm, c, ref = l.split("|")
        R = random.Random(300 + i)
        pool = [x for x in sorted(set(x.split("|")[1] for x in ANIMALS)) if x != c]
        n += 1
        out.append(Q(f"wld-{n:03d}", "세계", f"{nm}{'은' if (ord(nm[-1])-0xAC00)%28 else '는'} 어느 나라를 대표하는 동물일까요?",
                     [c] + R.sample(pool, 2), 0, level=2, image=img(ref, "🐾"), pool=pool, group="wld-animal"))
    for i, l in enumerate(GREETINGS):
        g, c, lang = l.split("|")
        R = random.Random(400 + i)
        pool = [x.split("|")[1] for x in GREETINGS if x.split("|")[1] != c]
        n += 1
        out.append(Q(f"wld-{n:03d}", "세계", f"'{g}' 는 어느 나라 인사말일까요?", [c] + R.sample(pool, 2), 0, level=2,
                     display=GREET_NATIVE[lang], sayWord={"text": GREET_NATIVE[lang], "lang": lang},
                     pool=pool, image=flag.get(c) and None, group="wld-greet"))
        n += 1
        gp = [x.split("|")[0] for x in GREETINGS if x.split("|")[1] != c]
        pw = who(i, 44)
        out.append(Q(f"wld-{n:03d}", "세계", f"{pw['가']} {c}에 갔어요. 뭐라고 인사할까요?", [g] + R.sample(gp, 2), 0, level=2,
                     image=flag[c], pool=gp, group="wld-greet2"))
    return out
