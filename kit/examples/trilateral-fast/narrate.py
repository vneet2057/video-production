import json, re, shutil, subprocess, wave, sys
from pathlib import Path
import numpy as np
import onnxruntime as ort

V = Path(__file__).parent
(V / "work").mkdir(exist_ok=True)   # outputs: voice, drafts, frames, timing
T = next(p / "tts" for p in V.parents if (p / "tts").is_dir())   # finds the shared tts/ folder
ESPEAK = shutil.which("espeak-ng") or "/opt/homebrew/bin/espeak-ng"   # macOS: brew install espeak-ng
SR, F = 24000, 0.4   # shorter transitions = faster cuts
ANIMS = [4.5, 3.2, 7.2, 3.2, 5.0, 7.4, 5.5, 3.4, 5.6, 6.0]   # seconds of captured animation per slide
SPEED = float(sys.argv[2]) if len(sys.argv) > 2 else 1.32
VOICE = sys.argv[1] if len(sys.argv) > 1 else "am_fenrir"

NARRATION = [
    "Trump, Xi and Putin agreed on four things. But the biggest war wasn't one of them.",
    "On Thursday in Shenzhen, China, the leaders of the world's three biggest nuclear powers met for the first time.",
    "Number one, nuclear weapons. They agreed no one can win a nuclear war, and they'll talk about reducing the risks. But no limits on their weapons.",
    "Trump told reporters, quote, it's very hard to give them up.",
    "Number two, oil. They promised to produce more petroleum products. Some analysts call that a big win for Russia.",
    "Number three, the United Nations. All three hold permanent seats on its Security Council, and they want it reformed. A surprise from Trump, a longtime critic.",
    "Number four, a warning to the International Criminal Court, not to abuse its powers. It's the court that issued an arrest warrant for Putin.",
    "So what was missing? Ukraine. The war wasn't even mentioned in their declaration.",
    "Trump and Putin did talk alone, for about forty minutes. No result was announced. And Ukraine wasn't in the room.",
    "A step toward peace, or just a photo op? Comment below. Let's see what happens. Follow for more.",
]

vocab = json.load(open(T / "config.json"))["vocab"]
voices = np.load(T / "voices-v1.0.bin")
sess = ort.InferenceSession(str(T / "kokoro-v1.0.onnx"))

def ipa(chunk):
    out = subprocess.run([ESPEAK, "-q", "--ipa", "-v", "en-us", chunk], capture_output=True, text=True).stdout
    return " ".join(out.split())

def phonemize(sentence):
    ph = ""
    for p in re.split(r"([,.;:!?])", sentence):
        if not p.strip():
            continue
        ph = (ph.rstrip() + p + " ") if p in ",.;:!?" else (ph + ipa(p.strip()) + " ")
    for a, b in FIX:
        ph = ph.replace(a, b)
    return ph.strip()

FIX = [("ɪɹˈænz", "aɪɹˈɑːnz"), ("ɪɹˈæn", "aɪɹˈɑːn"), ("ɪɹˈeɪnɪən", "aɪɹˈeɪniən"), ("hˈoːɹmʌz", "hɔːɹmˈuːz"), ("hˈɔːɹmʌz", "hɔːɹmˈuːz"), ("hˈaʊθaɪz", "hˈuːθiːz"), ("tænjˈʊɹɹə", "tɑːnˈʊɹə"), ("ɹˈɪjæd", "ɹiːjˈɑːd"), ("bjʊlˈɑːvə", "bʊlˈɑːvə"), ("dʒˈɑːŋ ˈʌn", "dʒˈʌŋ ˈʊn"), ("baɪnˈæns", "bˈaɪnæns"), ("kˈæɾɑːɹ", "kˈʌtɑːɹ"), ("wˈʌnsən", "wˈɑːnsɑːn")]

def synth(sentence):
    toks = [vocab[c] for c in phonemize(sentence) if c in vocab][:508]
    audio = sess.run(None, {"tokens": np.array([[0, *toks, 0]], dtype=np.int64),
                            "style": voices[VOICE][len(toks)].astype(np.float32),
                            "speed": np.array([SPEED], dtype=np.float32)})[0]
    return np.asarray(audio).reshape(-1)

gap = np.zeros(int(0.09 * SR), dtype=np.float32)
clips, sent_marks = [], []
for text in NARRATION:
    segs, marks, pos = [], [], 0
    for s in re.findall(r"[^.!?]+[.!?]", text):
        a = synth(s.strip())
        marks.append([pos / SR, (pos + len(a)) / SR])
        pos += len(a) + len(gap)
        segs += [a, gap]
    sent_marks.append(marks)
    clips.append(np.concatenate(segs[:-1]))

holds, starts, t = [], [], 0.0
n = len(clips)
for i, c in enumerate(clips):
    a = len(c) / SR
    lead = 0.25 if i == 0 else F - 0.1
    tail = F if i < n - 1 else 0.8
    hold = max(0.5, lead + a + 0.15 + tail - ANIMS[i])
    holds.append(round(hold, 3))
    starts.append(t + lead)
    t += ANIMS[i] + holds[-1] - (F if i < n - 1 else 0)

track = np.zeros(int(t * SR) + SR, dtype=np.float32)
for s, c in zip(starts, clips):
    k = int(s * SR)
    track[k:k + len(c)] += c
track = track[: int(t * SR)]
track = track / max(1e-6, np.abs(track).max()) * 0.89
with wave.open(str(V / "work" / "narration.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track * 32767).astype(np.int16).tobytes())
json.dump(holds, open(V / "work" / "holds.json", "w"))
sent_abs = [[[round(s + a, 2), round(s + b, 2)] for a, b in m] for s, m in zip(starts, sent_marks)]
json.dump(sent_abs, open(V / "work" / "sentences.json", "w"))
for i, m in enumerate(sent_abs, 1):
    print(i, m)
print("clip seconds:", [round(len(c) / SR, 1) for c in clips], "total", round(t, 1))
