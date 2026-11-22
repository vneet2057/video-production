# Burn in keyword captions (sound-off viewers) + whoosh on every cut + hit on stamps -> work/NAME-final.mp4
# Input: work/NAME-photos.mp4 if photos.py was run, else work/NAME-vertical-narrated.mp4. Edit DISPLAY to show digits in captions.
import json, re, subprocess
from pathlib import Path
V = Path(__file__).parent; W = V / "work"
NAME = V.name[11:] if V.name[:4].isdigit() else V.name
SRC = W / f"{NAME}-photos.mp4"                      # photos.py output, if you used it
if not SRC.exists():
    SRC = W / f"{NAME}-vertical-narrated.mp4"
# stamps that get a low "hit" sound: (slide, sentence, extra seconds), 1-based slide, 0-based sentence, matching at() in make_slides.py
MUSIC = None   # e.g. "musics/track.mp3" (path from project root): plays under the voice, ducked while the narrator speaks
MUSIC_VOL = 0.10   # light: ~-20 dB under the voice, ducked further while speaking
STAMPS = [(2, 0, 1.8), (8, 2, 0), (10, 3, 0)]
sent = json.load(open(W / "sentences.json"))
starts = json.load(open(W / "timing.json"))["starts"]
ns = {}; exec(re.search(r"NARRATION = \[.*?\n\]", (V / "narrate.py").read_text(), re.S).group(0), ns)
DISPLAY = {"forty minutes": "40 minutes", "Number one": "Number 1", "Number two": "Number 2", "Number three": "Number 3", "Number four": "Number 4"}

def ts(t):
    h, r = divmod(max(t, 0), 3600); m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

ev = []
for text, marks in zip(ns["NARRATION"], sent):
    for s_txt, (a, b) in zip(re.findall(r"[^.!?]+[.!?]", text), marks):
        s_txt = s_txt.strip()
        for k, v in DISPLAY.items(): s_txt = s_txt.replace(k, v)
        words = s_txt.split()
        chunks = [words[i:i + 3] for i in range(0, len(words), 3)]
        total = sum(len(" ".join(c)) for c in chunks)
        t = a
        for c in chunks:
            d = (b - a) * len(" ".join(c)) / total
            ev.append((t, t + d, " ".join(c).rstrip(",")))
            t += d
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Cap,Inter,64,&H00FFFFFF,&H00FFFFFF,&H28101418,&H00000000,-1,0,0,0,100,100,0,0,3,16,0,5,60,60,0,1", "",
       "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for a, b, txt in ev:
    ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{{\\pos(540,1470)\\fad(40,40)}}{txt}")
(W / "captions.ass").write_text("\n".join(ass), encoding="utf-8")

# synth SFX once: soft whoosh (filtered pink noise) and a low hit
def ff(*a): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)
ff("-f", "lavfi", "-i", "anoisesrc=d=0.45:c=pink:a=0.6", "-af",
   "highpass=f=300,lowpass=f=4000,afade=t=in:d=0.22:curve=exp,afade=t=out:st=0.22:d=0.23,volume=0.55", "-ar", "48000", "-ac", "2", str(W / "whoosh.wav"))
ff("-f", "lavfi", "-i", "sine=f=70:d=0.35", "-af", "afade=t=out:st=0.03:d=0.32,volume=1.3", "-ar", "48000", "-ac", "2", str(W / "hit.wav"))
cuts = [round(s - 0.25, 2) for s in starts[1:]]                      # whoosh just before each transition lands
stamps = [round(starts[s - 1] + sent[s - 1][k][0] - sent[s - 1][0][0] + 0.3 + x, 2) for s, k, x in STAMPS]
inputs, fc, labels = [], [], []
for i, t in enumerate(cuts):
    inputs += ["-i", str(W / "whoosh.wav")]; fc.append(f"[{i+1}:a]adelay={int(t*1000)}|{int(t*1000)}[w{i}]"); labels.append(f"[w{i}]")
for j, t in enumerate(stamps):
    k = len(cuts) + j + 1
    inputs += ["-i", str(W / "hit.wav")]; fc.append(f"[{k}:a]adelay={int(t*1000)}|{int(t*1000)}[h{j}]"); labels.append(f"[h{j}]")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(SRC)], capture_output=True, text=True).stdout)
fc.append("[0:a]aformat=channel_layouts=stereo,aresample=48000[voice]")
mix_in = ["[voice]"]
if MUSIC:
    mpath = next(q / MUSIC for q in [V, *V.parents] if (q / MUSIC).exists())
    k = len(cuts) + len(stamps) + 1
    inputs += ["-stream_loop", "-1", "-i", str(mpath)]
    fc.append("[voice]asplit=2[voice1][vkey]")
    fc.append(f"[{k}:a]aformat=channel_layouts=stereo,aresample=48000,atrim=0:{dur:.2f},volume={MUSIC_VOL},"
              f"afade=t=in:d=0.4,afade=t=out:st={dur-2.0:.2f}:d=2.0[mus]")
    fc.append("[mus][vkey]sidechaincompress=threshold=0.02:ratio=6:attack=40:release=400[mduck]")
    mix_in = ["[voice1]", "[mduck]"]
fc.append(f"{''.join(mix_in)}{''.join(labels)}amix=inputs={len(mix_in)+len(labels)}:normalize=0:duration=first[aout]")
fc.append(f"[0:v]ass={W/'captions.ass'}:fontsdir={Path.home()/'Library/Fonts'}[vout]")
ff("-i", str(SRC), *inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
   "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(W / f"{NAME}-final.mp4"))
print("captions:", len(ev), "whooshes:", len(cuts), "hits:", stamps)
