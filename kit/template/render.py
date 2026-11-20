import json, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

D = Path(__file__).parent
(D / "work").mkdir(exist_ok=True)
NAME = D.name[11:] if D.name[:4].isdigit() else D.name   # videos/2026-11-20-my-topic -> "my-topic"
FPS, F = 30, 0.4
ANIMS = json.load(open(D / "work" / "anims.json"))   # written by narrate.py: set ANIMS there, not here
N = len(ANIMS)
holds_file = D / "work" / "holds.json"
holds = json.load(open(holds_file)) if holds_file.exists() else [3.0]*N
TRANS = (["slideup", "smoothleft"] * N)[:N - 2] + ["circleopen"]   # N-1 transitions; override for a custom mix

if "--skip-frames" not in sys.argv:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(f"file://{D}/slides.html")
        for i in range(1, N + 1):
            fd = D / "work" / "frames" / f"s{i}"
            fd.mkdir(parents=True, exist_ok=True)
            pg.evaluate("i => { document.querySelectorAll('.s').forEach(e => e.classList.remove('on'));"
                        "document.getElementById('s'+i).classList.add('on'); }", i)
            pg.wait_for_timeout(120)
            print(f"s{i} overflow px:", pg.evaluate("i => { const e = document.getElementById('s'+i); return e.scrollHeight - e.clientHeight }", i))
            for k in range(int(ANIMS[i - 1] * FPS)):
                pg.evaluate("t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t })", k * 1000 / FPS)
                pg.screenshot(path=str(fd / f"{k:03d}.jpg"), type="jpeg", quality=95)
        b.close()

cmd = ["ffmpeg", "-y", "-loglevel", "error"]
for i in range(1, N + 1):
    cmd += ["-framerate", str(FPS), "-i", str(D / "work" / "frames" / f"s{i}" / "%03d.jpg")]
durs = [ANIMS[i] + h for i, h in enumerate(holds)]
fc = [f"[{i}:v]tpad=stop_mode=clone:stop_duration={holds[i]},format=yuv420p[c{i}]" for i in range(N)]
prev, off = "[c0]", 0.0
for i in range(1, N):
    off += durs[i - 1] - F
    fc.append(f"{prev}[c{i}]xfade=transition={TRANS[i-1]}:duration={F}:offset={off:.3f}[v{i}]")
    prev = f"[v{i}]"
nar = D / "work" / "narration.wav"
out = D / "work" / (f"{NAME}-vertical-narrated.mp4" if nar.exists() else f"{NAME}-vertical-slides.mp4")
amap = []
if nar.exists():
    cmd += ["-i", str(nar)]
    amap = ["-map", f"{N}:a", "-c:a", "aac", "-b:a", "160k"]
cmd += ["-filter_complex", ";".join(fc), "-map", prev, *amap, "-r", str(FPS), "-c:v", "libx264", "-crf", "19",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
subprocess.run(cmd, check=True)
starts, t = [], 0.0
for d in durs:
    starts.append(round(t, 2)); t += d - F
json.dump({"starts": starts, "durs": durs}, open(D / "work" / "timing.json", "w"))
print("done", starts)
