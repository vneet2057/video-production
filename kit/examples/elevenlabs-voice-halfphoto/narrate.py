# EXTERNAL VOICE version (ElevenLabs mp3 in in/), instead of Kokoro.
# Needs work/src_sentences.json from work/align.py (faster-whisper word timestamps -> sentence spans).
# Shortens long pauses, applies a light atempo to land on TARGET seconds, then lays the slides out like narrate.py.
import json, re, subprocess, wave
from pathlib import Path
import numpy as np

V = Path(__file__).parent
W = V / "work"
SRC = V / "in" / "voice-elevenlabs.mp3"
SR, F = 44100, 0.4
TARGET = 64.0      # seconds, final video length
MAXPAUSE = 0.24    # any pause inside a sentence longer than this is cut down to it
SENT_GAP = 0.16    # gap between sentences on the same slide

NARRATION = [  # one string per slide; must match the voice file sentence-for-sentence (captions come from here)
    "Trump wants a permanent Iran deal. But Iran is still firing at American bases.",
    "Speaking to Fox News on Saturday, the president said no future president should be able to let Iran get a nuclear weapon.",
    "His reason: \"We make a deal, and then they break the deal the next day\".",
    "A normal deal can be cancelled by the next president. In twenty eighteen, Trump himself pulled America out of the Obama-era nuclear deal.",
    "Now Iran has its own terms. Its foreign minister says reopening the Strait of Hormuz is \"not difficult\".",
    "But first, America must end its naval blockade, lift sanctions, and free Iran's frozen money. Then, Iran says, the strait could reopen the next day.",
    "About one fifth of the world's oil normally sails through it.",
    "Meanwhile, the fighting hasn't stopped. On Wednesday, Iran fired at a United States air base in Kuwait, and at targets in Bahrain. Kuwait says its air defenses stopped the drones.",
    "And on Saturday, Iran's military said a ship hit a mine in the strait and caught fire.",
    "Trump's envoys Steve Witkoff and Jared Kushner met officials from Qatar to push talks.",
    "So, a deal that lasts forever, or more strikes first? Let's see what happens. Follow for more.",
]

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(SRC), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
audio = np.frombuffer(raw, np.float32)
log = subprocess.run(["ffmpeg", "-i", str(SRC), "-af", "silencedetect=noise=-35dB:d=0.2", "-f", "null", "-"], capture_output=True, text=True).stderr
ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
sil = list(zip(ss, se))

src = json.load(open(W / "src_sentences.json"))
counts = [len(re.findall(r"[^.!?]+[.!?]", t)) for t in NARRATION]
assert sum(counts) == len(src), (counts, len(src))

def cut(a, b):
    """Audio a..b (s) with every inner silence longer than MAXPAUSE shortened to MAXPAUSE."""
    out, t = [], a
    for s0, s1 in sil:
        if s0 > a and s1 < b and s1 - s0 > MAXPAUSE:
            keep = MAXPAUSE / 2
            out.append(audio[int(t * SR):int((s0 + keep) * SR)])
            t = s1 - keep
    out.append(audio[int(t * SR):int(b * SR)])
    return np.concatenate(out)

clips0, marks0, k = [], [], 0
for n in counts:
    segs, marks, pos = [], [], 0
    for j in range(n):
        a, b, _ = src[k]
        nxt = src[k + 1][0] if k + 1 < len(src) else len(audio) / SR
        c = cut(max(0, a - 0.05), min(nxt - 0.02, b + 0.14))
        marks.append([pos / SR, (pos + len(c)) / SR])
        segs += [c, np.zeros(int(SENT_GAP * SR), np.float32)]
        pos += len(c) + int(SENT_GAP * SR)
        k += 1
    clips0.append(np.concatenate(segs[:-1])); marks0.append(marks)

N = len(clips0)
overhead = 0.25 + sum(0.15 + F - 0.1 for _ in range(N)) - 0.1 + 0.8 + (N - 1) * (F - F)  # lead/tail per slide minus xfade overlap
speech = sum(len(c) for c in clips0) / SR
TEMPO = min(1.18, max(1.0, speech / (TARGET - overhead)))

def tempo(c):
    if TEMPO == 1.0: return c
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={TEMPO:.4f}",
                        "-f", "f32le", "-"], input=c.tobytes(), capture_output=True).stdout
    return np.frombuffer(r, np.float32)

clips = [tempo(c) for c in clips0]
sent_marks = [[[a / TEMPO, b / TEMPO] for a, b in m] for m in marks0]

ANIMS, holds, starts, t = [], [], [], 0.0
for i, c in enumerate(clips):
    a = len(c) / SR
    lead = 0.25 if i == 0 else F - 0.1
    tail = F if i < N - 1 else 1.0
    need = lead + a + 0.15 + tail
    ANIMS.append(round(max(2.5, need - 0.5), 2))   # animate (Ken Burns etc.) through almost the whole slide
    holds.append(round(max(0.5, need - ANIMS[-1]), 3))
    starts.append(t + lead)
    t += ANIMS[i] + holds[-1] - (F if i < N - 1 else 0)

track = np.zeros(int(t * SR) + SR, dtype=np.float32)
for s, c in zip(starts, clips):
    q = int(s * SR); track[q:q + len(c)] += c
track = track[: int(t * SR)]
track = track / max(1e-6, np.abs(track).max()) * 0.89
with wave.open(str(W / "narration.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track * 32767).astype(np.int16).tobytes())
json.dump(holds, open(W / "holds.json", "w"))
json.dump(ANIMS, open(W / "anims.json", "w"))
sent_abs = [[[round(s + a, 2), round(s + b, 2)] for a, b in m] for s, m in zip(starts, sent_marks)]
json.dump(sent_abs, open(W / "sentences.json", "w"))
for i, m in enumerate(sent_abs, 1):
    print(i, m)
print(f"tempo {TEMPO:.3f}  speech {speech:.1f}s -> {speech/TEMPO:.1f}s  ANIMS {ANIMS}  total {t:.1f}s")
