import random

def Q(id, subject, prompt, choices, answer=0, type="choice", level=1, **kw):
    d = {"id": id, "subject": subject, "type": type, "prompt": prompt,
         "choices": choices, "answer": answer, "level": level}
    for k, v in kw.items():
        if v is not None:
            d[k] = v
    return d

def img(ref=None, emoji="❓", **kw):
    d = {"ref": ref, "fallbackEmoji": emoji}
    d.update(kw)
    return d

# 시은이 등장 비율 ~50%: 문항 번호로 결정해 빌드마다 같은 결과
PEOPLE = ["친구", "엄마", "아빠", "동생", "언니", "할머니", "선생님", "짝꿍"]
def who(i, salt=0):
    """번갈아 가며 '시은' 또는 다른 사람. 반환: (이가/는/랑/의 형태를 담은 dict)"""
    r = random.Random(i * 31 + salt)
    if r.random() < 0.5:
        return {"가": "시은이가", "는": "시은이는", "랑": "시은이랑", "의": "시은이의", "를": "시은이를", "에게": "시은이에게", "name": "시은이"}
    p = r.choice(PEOPLE)
    last = p[-1]
    has_batchim = (ord(last) - 0xAC00) % 28 != 0
    return {"가": p + ("이" if has_batchim else "가"), "는": p + ("은" if has_batchim else "는"),
            "랑": p + ("이랑" if has_batchim else "랑"), "의": p + "의", "를": p + ("을" if has_batchim else "를"),
            "에게": p + "에게", "name": p}

def josa(word, a, b):
    """받침 있으면 a, 없으면 b  (예: josa('사과','을','를'))"""
    c = word[-1]
    if not ('가' <= c <= '힣'):
        return b
    return a if (ord(c) - 0xAC00) % 28 else b
