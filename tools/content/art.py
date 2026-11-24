from common import Q, img, who
import random

# 제목|화가|사진ref   (저작권 끝난 작품만, 누드·무서운 장면 제외)
WORKS = """
별이 빛나는 밤|빈센트 반 고흐|wp:The Starry Night
해바라기|빈센트 반 고흐|wp:Sunflowers (Van Gogh series)
밤의 카페 테라스|빈센트 반 고흐|wp:Café Terrace at Night
아를의 침실|빈센트 반 고흐|wp:Bedroom in Arles
붓꽃|빈센트 반 고흐|wp:Irises (painting)
꽃 피는 아몬드 나무|빈센트 반 고흐|wp:Almond Blossoms
론강의 별이 빛나는 밤|빈센트 반 고흐|wp:Starry Night Over the Rhône
인상, 해돋이|클로드 모네|wp:Impression, Sunrise
수련|클로드 모네|wp:Water Lilies (Monet series)
양산을 든 여인|클로드 모네|wp:Woman with a Parasol – Madame Monet and Her Son
수련 연못 위의 다리|클로드 모네|wp:Bridge over a Pond of Water Lilies
건초더미|클로드 모네|wp:Haystacks (Monet series)
모나리자|레오나르도 다빈치|wp:Mona Lisa
흰 담비를 안은 여인|레오나르도 다빈치|wp:Lady with an Ermine
이삭 줍는 사람들|장 프랑수아 밀레|wp:The Gleaners
만종|장 프랑수아 밀레|wp:The Angelus (painting)
그랑드 자트 섬의 일요일 오후|조르주 쇠라|wp:A Sunday Afternoon on the Island of La Grande Jatte
진주 귀고리를 한 소녀|요하네스 페르메이르|wp:Girl with a Pearl Earring
우유 따르는 여인|요하네스 페르메이르|wp:The Milkmaid (Vermeer)
델프트 풍경|요하네스 페르메이르|wp:View of Delft
가나가와 해변의 높은 파도|가쓰시카 호쿠사이|wp:The Great Wave off Kanagawa
붉은 후지산|가쓰시카 호쿠사이|wp:Fine Wind, Clear Morning
씨름|김홍도|file:Danwon_Ssireum.jpg
서당|김홍도|file:Danwon_Seodang.jpg
무동|김홍도|file:Danwon-Mudong.jpg
우물가|김홍도|file:Danwon-Umulga.jpg
길쌈|김홍도|file:Danwon-Gilssam.jpg
빨래터|김홍도|file:Danwon-Bbalrae.teo.jpg
월하정인|신윤복|file:Hyewon-Wolha-jeongin-2.jpg
미인도|신윤복|file:Hyewon-Miindo.jpg
인왕제색도|정선|file:Inwangjesaekdo.jpg
금강전도|정선|file:Jeong_Seon-Geumgangjeondo.jpg
세한도|김정희|file:Sehando.jpg
초충도|신사임당|file:Shin.Saimdang-Chochungdo-01.jpg
수박과 들쥐 (초충도)|신사임당|file:Shin.Saimdang-Chochungdo-02.jpg
꿩 깃털을 가지고 노는 강아지|이암|file:Attributed_to_Yi_Am,_Korean_-_Puppy_Playing_with_a_Pheasant_Feather_-_Google_Art_Project.jpg
피아노 치는 소녀들|피에르 오귀스트 르누아르|wp:Two Young Girls at the Piano
뱃놀이 일행의 점심|피에르 오귀스트 르누아르|wp:Luncheon of the Boating Party
물랭 드 라 갈레트의 무도회|피에르 오귀스트 르누아르|wp:Bal du moulin de la Galette
키스|구스타프 클림트|wp:The Kiss (Klimt)
아델레 블로흐바우어의 초상|구스타프 클림트|wp:Portrait of Adele Bloch-Bauer I
생명의 나무|구스타프 클림트|wp:The Tree of Life (Klimt)
야경|렘브란트|wp:The Night Watch
시녀들|디에고 벨라스케스|wp:Las Meninas
카드놀이 하는 사람들|폴 세잔|wp:The Card Players
사과 바구니|폴 세잔|wp:The Basket of Apples
발레 수업|에드가 드가|wp:The Ballet Class (Degas, Musée d'Orsay)
아테네 학당|라파엘로|wp:The School of Athens
전함 테메레르|윌리엄 터너|wp:The Fighting Temeraire
비, 증기, 속도|윌리엄 터너|wp:Rain, Steam and Speed – The Great Western Railway
건초 마차|존 컨스터블|wp:The Hay Wain
안개 바다 위의 방랑자|카스파르 다비트 프리드리히|wp:Wanderer above the Sea of Fog
아타케의 소나기|우타가와 히로시게|wp:Sudden Shower over Shin-Ōhashi bridge and Atake
베르툼누스 (과일 얼굴)|주세페 아르침볼도|wp:Vertumnus (painting)
여름|주세페 아르침볼도|wp:Summer (Arcimboldo)
바벨탑|피터르 브뤼헐|wp:The Tower of Babel (Bruegel)
아이들의 놀이|피터르 브뤼헐|wp:Children's Games (Bruegel)
잠자는 집시|앙리 루소|wp:The Sleeping Gypsy
열대 폭풍 속의 호랑이|앙리 루소|wp:Tiger in a Tropical Storm
구성 7|바실리 칸딘스키|wp:Composition VII
빨강, 파랑, 노랑의 구성|피트 몬드리안|file:Piet_Mondriaan,_1930_-_Mondrian_Composition_II_in_Red,_Blue,_and_Yellow.jpg
피리 부는 소년|에두아르 마네|wp:The Fifer
몽마르트르 대로의 밤|카미유 피사로|wp:The Boulevard Montmartre at Night
그네|장 오노레 프라고나르|-
""".strip().splitlines()

def build():
    rows = []
    for line in WORKS:
        t, a, ref = line.split("|")
        if ref == "-":
            continue
        rows.append({"t": t, "a": a, "ref": ref})
    titles = [r["t"] for r in rows]
    artists = sorted(set(r["a"] for r in rows))
    out = []
    n = 0
    for i, r in enumerate(rows):
        R = random.Random(i)
        local = f"assets/art/art-{i:02d}.jpg"
        im = img(r["ref"], "🖼️", local=local)
        pw = who(i, 31)
        tp = [x for x in titles if x != r["t"]]
        ap = [x for x in artists if x != r["a"]]
        n += 1
        out.append(Q(f"art-{n:03d}", "미술", f"{pw['가']} 미술관에서 이 그림을 봤어요. 그림의 제목은?" if i % 2 == 0 else "이 그림의 제목은 무엇일까요?",
                     [r["t"]] + R.sample(tp, 2), 0, level=2, image=im, pool=tp, group="art-title", explain=f"〈{r['t']}〉 — {r['a']}"))
        n += 1
        out.append(Q(f"art-{n:03d}", "미술", "이 그림을 그린 화가는 누구일까요?", [r["a"]] + R.sample(ap, 2), 0, level=2,
                     image=im, pool=ap, group="art-artist", explain=f"〈{r['t']}〉 — {r['a']}"))
        n += 1
        z = {"scale": 2.6, "x": R.choice([25, 50, 75]), "y": R.choice([30, 50, 70])}
        out.append(Q(f"art-{n:03d}", "미술", "그림의 한 부분을 크게 보여 줄게요. 어떤 그림일까요?", [r["t"]] + R.sample(tp, 2), 0, level=3,
                     image=dict(im, zoom=z), pool=tp, group="art-zoom", explain=f"〈{r['t']}〉 — {r['a']}"))
    # 이 화가의 그림은? (보기가 그림)
    by = {}
    for i, r in enumerate(rows):
        by.setdefault(r["a"], []).append((i, r))
    for a, lst in by.items():
        for k, (i, r) in enumerate(lst[:3]):
            n += 1
            others = [(j, x) for j, x in enumerate(rows) if x["a"] != a]
            R = random.Random(i * 7 + k)
            o = R.sample(others, 2)
            mk = lambda j, x: img(x["ref"], "🖼️", local=f"assets/art/art-{j:02d}.jpg", label=x["t"])
            pw = who(i, 32 + k)
            out.append(Q(f"art-{n:03d}", "미술", f"{pw['가']} {a}의 그림을 찾고 있어요. 어느 것일까요?" if k % 2 == 0 else f"{a}의 그림은 어느 것일까요?",
                         [mk(i, r)] + [mk(j, x) for j, x in o], 0, type="imageChoice", level=3,
                         poolImages=[mk(j, x) for j, x in others], group="art-byartist", explain=f"〈{r['t']}〉 — {a}"))
    return out, rows
