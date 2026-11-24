from common import Q, img, who, josa
import random, hashlib

# 초등 저학년 수준: 유명한 화가·그림 위주, "무엇이 그려져 있나요?" 같은 쉬운 문제 포함
# 제목|화가|그림 속 내용(쉬운 설명)|사진ref
WORKS = """
별이 빛나는 밤|고흐|소용돌이치는 밤하늘과 별|wp:The Starry Night
해바라기|고흐|꽃병에 꽂힌 해바라기|wp:Sunflowers (Van Gogh series)
밤의 카페 테라스|고흐|밤거리의 노란 카페|wp:Café Terrace at Night
아를의 침실|고흐|침대와 의자가 있는 방|wp:Bedroom in Arles
꽃 피는 아몬드 나무|고흐|파란 하늘과 하얀 꽃 핀 나뭇가지|wp:Almond Blossoms
붓꽃|고흐|보라색 붓꽃이 가득한 꽃밭|wp:Irises (painting)
인상, 해돋이|모네|바다 위에 뜨는 빨간 해와 작은 배|wp:Impression, Sunrise
수련|모네|연못에 동동 떠 있는 수련 꽃|wp:Water Lilies (Monet series)
양산을 든 여인|모네|양산을 쓰고 언덕에 선 사람|wp:Woman with a Parasol – Madame Monet and Her Son
수련 연못 위의 다리|모네|연못 위의 둥근 다리|wp:Bridge over a Pond of Water Lilies
건초더미|모네|들판에 쌓아 놓은 건초더미|wp:Haystacks (Monet series)
모나리자|다빈치|살짝 미소 짓는 여인|wp:Mona Lisa
이삭 줍는 사람들|밀레|밭에서 이삭을 줍는 세 사람|wp:The Gleaners
만종|밀레|들판에서 기도하는 두 사람|wp:The Angelus (painting)
그랑드 자트 섬의 일요일 오후|쇠라|작은 점을 콕콕 찍어 그린 공원|wp:A Sunday Afternoon on the Island of La Grande Jatte
진주 귀고리를 한 소녀|페르메이르|파란 두건을 쓴 소녀|wp:Girl with a Pearl Earring
우유 따르는 여인|페르메이르|그릇에 우유를 따르는 여인|wp:The Milkmaid (Vermeer)
가나가와 해변의 높은 파도|호쿠사이|커다란 파도와 작은 배|wp:The Great Wave off Kanagawa
붉은 후지산|호쿠사이|빨갛게 물든 산|wp:Fine Wind, Clear Morning
씨름|김홍도|씨름하는 두 사람과 구경꾼들|file:Danwon_Ssireum.jpg
서당|김홍도|훈장님과 공부하는 아이들|file:Danwon_Seodang.jpg
무동|김홍도|춤추는 아이와 악기 연주하는 사람들|file:Danwon-Mudong.jpg
월하정인|신윤복|달빛 아래 이야기하는 두 사람|file:Hyewon-Wolha-jeongin-2.jpg
미인도|신윤복|한복을 입은 여인|file:Hyewon-Miindo.jpg
인왕제색도|정선|비가 그친 뒤의 바위산|file:Inwangjesaekdo.jpg
초충도|신사임당|풀과 꽃과 벌레|file:Shin.Saimdang-Chochungdo-01.jpg
수박과 들쥐|신사임당|수박을 갉아 먹는 쥐|file:Shin.Saimdang-Chochungdo-02.jpg
꿩 깃털을 가지고 노는 강아지|이암|깃털을 물고 노는 강아지|file:Attributed_to_Yi_Am,_Korean_-_Puppy_Playing_with_a_Pheasant_Feather_-_Google_Art_Project.jpg
피아노 치는 소녀들|르누아르|피아노를 치는 두 소녀|wp:Two Young Girls at the Piano
물랭 드 라 갈레트의 무도회|르누아르|햇살 아래 춤추는 사람들|wp:Bal du moulin de la Galette
키스|클림트|금빛 옷을 입고 안고 있는 두 사람|wp:The Kiss (Klimt)
빨강, 파랑, 노랑의 구성|몬드리안|검은 선과 빨강·파랑·노랑 네모|file:Piet_Mondriaan,_1930_-_Mondrian_Composition_II_in_Red,_Blue,_and_Yellow.jpg
베르툼누스|아르침볼도|과일과 채소로 만든 얼굴|wp:Vertumnus (painting)
여름|아르침볼도|여름 과일로 만든 얼굴|wp:Summer (Arcimboldo)
열대 폭풍 속의 호랑이|루소|정글 속에 숨은 호랑이|wp:Tiger in a Tropical Storm
발레 수업|드가|발레를 연습하는 아이들|wp:The Ballet Class (Degas, Musée d'Orsay)
사과 바구니|세잔|탁자 위의 사과와 바구니|wp:The Basket of Apples
아이들의 놀이|브뤼헐|여러 가지 놀이를 하는 많은 아이들|wp:Children's Games (Bruegel)
바벨탑|브뤼헐|하늘까지 닿을 듯 높은 탑|wp:The Tower of Babel (Bruegel)
""".strip().splitlines()

# 화가를 쉽게 기억하는 힌트
PAINTER = {
    "고흐": "고흐는 꿈틀꿈틀 굵은 붓 자국으로 노랑과 파랑을 많이 칠했어요.",
    "모네": "모네는 빛과 물, 연못의 수련을 즐겨 그렸어요.",
    "다빈치": "다빈치는 〈모나리자〉를 그린 이탈리아의 천재 화가예요.",
    "밀레": "밀레는 밭에서 일하는 농부들을 그렸어요.",
    "쇠라": "쇠라는 작은 점을 콕콕 찍어서 그림을 그렸어요.",
    "페르메이르": "페르메이르는 창문으로 들어오는 부드러운 빛을 잘 그렸어요.",
    "호쿠사이": "호쿠사이는 커다란 파도와 후지산을 그린 일본 화가예요.",
    "김홍도": "김홍도는 옛날 우리나라 사람들의 생활을 재미있게 그렸어요.",
    "신윤복": "신윤복은 한복 입은 사람들을 고운 색으로 그린 우리나라 화가예요.",
    "정선": "정선은 우리나라 산과 경치를 그린 화가예요.",
    "신사임당": "신사임당은 풀, 꽃, 벌레를 예쁘게 그렸어요. 5만 원 지폐에 나오는 분이에요.",
    "이암": "이암은 귀여운 강아지 그림으로 유명한 우리나라 화가예요.",
    "르누아르": "르누아르는 밝고 행복한 사람들의 모습을 그렸어요.",
    "클림트": "클림트는 반짝이는 금색을 많이 쓴 화가예요.",
    "몬드리안": "몬드리안은 검은 선과 빨강·파랑·노랑 네모로 그림을 그렸어요.",
    "아르침볼도": "아르침볼도는 과일과 채소로 사람 얼굴을 만들었어요.",
    "루소": "루소는 초록 정글과 동물을 그렸어요.",
    "드가": "드가는 발레하는 무용수들을 많이 그렸어요.",
    "세잔": "세잔은 사과 같은 과일을 여러 번 그렸어요.",
    "브뤼헐": "브뤼헐은 사람이 아주 많이 나오는 그림을 그렸어요.",
}
KOREAN = {"김홍도", "신윤복", "정선", "신사임당", "이암"}

def local_name(ref):
    return "assets/art/" + hashlib.sha1(ref.encode()).hexdigest()[:12] + ".jpg"

def build():
    rows = []
    for line in WORKS:
        t, a, what, ref = line.split("|")
        rows.append({"t": t, "a": a, "what": what, "ref": ref})
    titles = [r["t"] for r in rows]
    artists = sorted(set(r["a"] for r in rows))
    whats = [r["what"] for r in rows]
    mk = lambda r, **kw: img(r["ref"], "🖼️", local=local_name(r["ref"]), **kw)
    out = []
    n = 0
    for i, r in enumerate(rows):
        R = random.Random(i)
        im = mk(r)
        pw = who(i, 31)
        ex = f"〈{r['t']}〉 — {r['a']}. {PAINTER[r['a']]}"
        # 1) 무엇이 그려져 있나요? (가장 쉬움)
        n += 1
        wp = [w for w in whats if w != r["what"]]
        out.append(Q(f"art-{n:03d}", "미술", f"{pw['가']} 미술관에서 이 그림을 봤어요. 무엇이 그려져 있나요?" if i % 2 == 0 else "그림을 잘 보세요. 무엇이 그려져 있나요?",
                     [r["what"]] + R.sample(wp, 2), 0, level=1, image=im, pool=wp, group="art-what", explain=ex))
        # 2) 제목 고르기 (힌트: 그림 내용)
        n += 1
        tp = [x for x in titles if x != r["t"]]
        out.append(Q(f"art-{n:03d}", "미술", "이 그림의 제목은 무엇일까요?", [r["t"]] + R.sample(tp, 2), 0, level=1,
                     image=im, pool=tp, group="art-title", explain=ex))
        # 3) 화가 고르기 (힌트를 문제에 같이)
        n += 1
        ap = [x for x in artists if x != r["a"]]
        out.append(Q(f"art-{n:03d}", "미술", "이 그림을 그린 화가는 누구일까요?", [r["a"]] + R.sample(ap, 2), 0, level=2,
                     image=im, pool=ap, group="art-artist", explain=ex, hint=PAINTER[r["a"]]))
        # 4) 우리나라 그림?
        if i % 2 == 0 or r["a"] in KOREAN:
            n += 1
            kr = r["a"] in KOREAN
            out.append(Q(f"art-{n:03d}", "미술", "이 그림은 우리나라 옛 그림일까요, 다른 나라 그림일까요?",
                         ["🇰🇷 우리나라 그림", "🌍 다른 나라 그림"], 0 if kr else 1, level=1, fixedOrder=True,
                         image=im, group="art-korea", explain=ex))
    # 5) 이 화가의 그림은? (보기가 그림)
    by = {}
    for r in rows:
        by.setdefault(r["a"], []).append(r)
    for a, lst in by.items():
        for k, r in enumerate(lst[:3]):
            n += 1
            others = [x for x in rows if x["a"] != a]
            R = random.Random(n)
            o = R.sample(others, 2)
            pw = who(n, 33)
            out.append(Q(f"art-{n:03d}", "미술", f"{pw['가']} {a}의 그림을 찾고 있어요. 어느 것일까요?",
                         [mk(r)] + [mk(x) for x in o], 0, type="imageChoice", level=2, hint=PAINTER[a],
                         poolImages=[mk(x) for x in others], group="art-byartist", explain=f"〈{r['t']}〉 — {a}. {PAINTER[a]}"))
    # 6) 화가 이야기 (그림 없이)
    for k, (a, h) in enumerate(PAINTER.items()):
        if a not in by:
            continue
        n += 1
        R = random.Random(900 + k)
        ap = [x for x in artists if x != a]
        out.append(Q(f"art-{n:03d}", "미술", f"'{h.replace(a + '는', '이 화가는').replace(a + '은', '이 화가는')}' 이 화가는 누구일까요?",
                     [a] + R.sample(ap, 2), 0, level=2, pool=ap, image=img(None, "🎨"), group="art-painterstory", explain=h))
    return out, rows
