"""칭찬·격려 문장을 AI 목소리(MeloTTS 한국어, MIT 라이선스)로 녹음해 assets/voice/ 에 mp3로 만든다.
준비:  pip install torch torchaudio  (CPU 버전이면 충분)
       pip install git+https://github.com/myshell-ai/MeloTTS.git
       python -m unidic download   (필요할 때)
실행:  python3 tools/make_voice.py
"""
import json, os, re, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "voice")

def phrases():
    src = open(os.path.join(ROOT, "js", "app.js"), encoding="utf-8").read()
    out = []
    for name in ("PRAISE", "RETRY", "SHOW", "DONE"):
        arr = re.search(r"const %s = \[(.*?)\];" % name, src).group(1)
        out += re.findall(r"'([^']*)'", arr)
    return out

def clean(t):  # app.js 의 cleanForSpeech 와 같은 규칙(이모지 제거)
    t = re.sub("[\U0001F000-\U0001FAFF☀-➿️‍]", "", t)
    return t.strip()

def main():
    from melo.api import TTS
    tts = TTS(language="KR", device="cpu")
    spk = tts.hps.data.spk2id["KR"]
    os.makedirs(OUT, exist_ok=True)
    table = {}
    for i, p in enumerate(phrases()):
        text = clean(p)
        wav = os.path.join(tempfile.gettempdir(), f"v{i}.wav")
        tts.tts_to_file(text, spk, wav, speed=1.05)
        mp3 = os.path.join(OUT, f"v{i:02d}.mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", "loudnorm=I=-16:TP=-1.5", "-ac", "1", "-b:a", "64k", mp3], check=True)
        table[text] = f"assets/voice/v{i:02d}.mp3"
        print("녹음", text)
    json.dump(table, open(os.path.join(OUT, "voice.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
