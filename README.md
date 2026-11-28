# 박시은의 매일매일 공부방

7살 시은이가 휴대폰으로 혼자 푸는 학습 웹앱입니다. 과목마다 하루 10문제씩 나오고, 문제 문장은 소리로 읽어 줍니다.

- 과목: 국어, 영어, 연산, 창의 수학, 시간, 한자, 미술, 세계, 자연, 가게, 사람, 사회, 전래동화, 관용구·속담, 운동, 악기, 환경, 그림 + 오답노트
- 직접 만든 문제 3,600개 이상. 수학·가게·한자 숫자 문제는 생성기가 매번 새 숫자로 만듭니다.
- 사진은 위키미디어 커먼즈의 자유 이용 사진(퍼블릭 도메인, CC0, CC BY, CC BY-SA, 공공누리 1유형)만 씁니다. 출처는 앱 안 「사진·소리 출처」 화면에 모아 두었습니다.

## 휴대폰에서 쓰기

정적 파일만 있으면 되므로 GitHub Pages 같은 곳에 올리면 됩니다.

1. GitHub 저장소 → Settings → Pages → Branch를 이 브랜치(또는 main)의 `/ (root)`로 지정합니다.
2. 휴대폰 크롬에서 주소를 열고 메뉴 → **홈 화면에 추가**를 누르면 「시은이 공부방」 아이콘이 생깁니다.
3. 처음 한 번 화면을 터치해야 음성이 나옵니다(브라우저 정책). 음성이 안 나오면 「부모님 메뉴 → 음성 테스트」를 눌러 보세요. 안드로이드 설정 → 텍스트 음성 변환에서 Google 음성(한국어·영어)이 설치되어 있어야 합니다.

컴퓨터에서 확인하려면 `python3 -m http.server`를 실행한 뒤 `http://localhost:8000`을 엽니다. `file://`로 직접 열면 문제 파일을 불러오지 못합니다.

## 출제 방식

- **안 푼 문제 먼저**: 과목마다 푼 문제를 기억하고(localStorage), 다 풀면 다시 섞어서 처음부터 냅니다.
- **복습**: 틀린 문제는 2일 뒤, 두 번째에 맞힌 문제는 4일 뒤 다시 나옵니다(하루 최대 3개). 복습에서 맞히면 목록에서 빠집니다.
- **보기 섞기**: 보기 순서는 매번 섞고, 오답 보기도 같은 종류의 낱말 중에서 매번 다시 고릅니다.
- **레벨**: 그 과목에서 푼 문제가 30개 미만이면 레벨 1, 90개 미만이면 레벨 2까지, 그 뒤로는 레벨 3까지 나옵니다.
- **정답·오답**: 맞히면 별 1개와 칭찬. 틀리면 한 번 더 기회를 주고, 두 번째도 틀리면 정답을 보여 주고 넘어갑니다.

## 오답노트

한 번이라도 틀린 문제는 홈 화면 맨 아래 「📒 오답노트」에 모입니다. 과목별로 볼 수 있고, 「오답노트 풀기」로 다시 풀 수 있어요. 다시 맞히면 ✅ 표시가 붙고, 또 틀리면 틀린 횟수가 늘어요. 기록은 그 폰의 브라우저에 저장됩니다.

## 기록 옮기기 (폰 여러 대)

기록은 폰마다 따로 저장돼요. 「부모님 메뉴 → 📤 기록 내보내기」로 만든 글자(또는 파일)를 카톡 등으로 보내고, 다른 폰의 「📥 기록 가져오기」에 붙여 넣으면 두 폰의 기록(별·푼 문제·복습·오답노트)이 합쳐집니다. 여러 번 가져와도 같은 기록이 두 번 더해지지 않아요.

## 문제 고치기·추가하기

문제는 `data/과목.json`에 있습니다. 바로 고쳐도 되고, 많이 바꿀 때는 원본 목록을 고친 뒤 다시 만드는 편이 편합니다.

| 파일 | 내용 |
|---|---|
| `tools/content/korean.py` | 국어 낱말(정답·오답·사진)과 빈칸 문장 |
| `tools/content/english.py` | 영단어 |
| `tools/content/mathq.py` | 수학 문장제 템플릿과 생성기 목록 |
| `tools/content/timeq.py` | 시간: 시계·달력 지식 문제와 생성기 목록 (시계 읽기·달력 문제는 `js/gen.js`가 매번 새로 만듦) |
| `tools/content/folktale.py` | 전래동화 퀴즈 (이야기마다 등장하는 것·줄거리·내용 문제) |
| `tools/content/hanja.py` | 한자, 훈음, 낱말 |
| `tools/content/art.py` | 명화(제목·화가·사진) |
| `tools/content/world.py` | 국기, 명소, 음식, 동물, 인사말 |
| `tools/content/nature.py` | 동물·식물·공룡·계절·날씨 |
| `tools/content/store.py` | 가게 물건 가격, 가게 종류, 상황 문제 |
| `tools/content/sports.py`, `music.py`, `env.py`, `people.py` | 나머지 과목 |

```bash
python3 tools/build.py --fetch   # 새 사진을 위키미디어에서 찾아 data/*.json을 다시 만듦
python3 tools/check_links.py     # 모든 사진·소리 링크가 열리는지 검사 (결과: tools/link_report.json)
python3 tools/fetch_sounds.py    # 악기·동물 소리를 받아 assets/sounds/에 mp3로 만듦
python3 tools/fetch_local.py     # 명화·한자 옛 글자 이미지를 앱(assets/)에 내려받음
sh tools/fetch_all.sh            # 위 작업을 순서대로 한 번에 (요청 제한을 지키며 천천히)
```

- 사진이 마음에 들지 않으면 `tools/image_overrides.json`에 `"wp:문서이름": "file:커먼즈_파일명.jpg"`처럼 바꿀 사진을 적습니다. `null`로 적으면 사진 대신 이모지가 나옵니다.
- JSON 문제 형식(예):

```json
{
  "id": "kor-001",
  "subject": "국어",
  "type": "choice",
  "prompt": "그림에 맞는 바른 글자를 골라요.",
  "image": { "url": "https://upload.wikimedia.org/...", "credit": "작가, CC BY-SA 4.0, Wikimedia Commons", "fallbackEmoji": "🍎" },
  "choices": ["사과", "사가"],
  "answer": 0,
  "speakChoices": false,
  "level": 1
}
```

  - `type`: `choice`(글자 보기), `imageChoice`(사진 보기), `sort`(분리수거 통에 끌어다 놓기), `word`(수학 문장제 템플릿), `shop`(가게 상황 템플릿), `clockInput`(시계 보고 시·분 버튼을 직접 골라 확인)
  - `pool` / `poolImages`: 오답 후보. 있으면 매번 여기서 오답을 새로 뽑습니다.
  - `speakChoices: false`: 보기를 읽지 않습니다(국어 맞춤법).
  - `sound`: 들려줄 소리 파일, `sayWord`: 음성으로 읽어 줄 단어(`lang`: `en-US` 등)

## 사진·소리 출처

- 사진: [Wikimedia Commons](https://commons.wikimedia.org/). 각 사진의 작가와 라이선스는 `data/*.json`의 `credit`, `source`에 있고 앱의 「사진·소리 출처」 화면에서 볼 수 있습니다.
- 한국 동전·지폐 사진: 한국은행 「화폐 도안 이용 기준」에 따라 쓸 수 있는 커먼즈 이미지(`South Korean currency` 표시)입니다.
- 악기 소리: [tonejs-instruments](https://github.com/nbrosowsky/tonejs-instruments) 실제 악기 녹음 샘플(CC BY 3.0)과 위키미디어 커먼즈 녹음
- 동물 소리: 위키미디어 커먼즈 녹음 (CC BY / CC BY-SA / CC0)
- 칭찬·격려 목소리: 오픈소스 AI 음성 [MeloTTS](https://github.com/myshell-ai/MeloTTS)(MIT 라이선스) 한국어 모델로 만든 녹음 (`tools/make_voice.py`)
