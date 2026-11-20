import json, subprocess
from pathlib import Path
V = Path(__file__).parent
FONT = str(Path.home() / "Library/Fonts/Inter-SemiBold.otf")   # macOS: brew install --cask font-inter
st = json.load(open(V / "work" / "timing.json"))["starts"]
END = 82.7
def ff(*a): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)
# pre-crop to panel ratio (Trump: keep the top so the cap isn't cut)
ff("-i", "voter.jpg", "-vf", "crop=iw:iw*520/888:0:(ih-iw*520/888)/2", "p_voter.png")
ff("-i", "rally.jpg", "-vf", "crop=iw:iw*600/888", "p_rally.png")
ff("-i", "trump.jpg", "-vf", "crop=iw:iw*480/888:0:8", "p_trump.png")
PLAN = [("p_voter.png", st[2] + 1.5, st[3] + 0.05, (96, 880, 888, 520), "Illustrative photo · Voting booth"),
        ("p_rally.png", st[3] + 1.6, st[4] + 0.05, (96, 800, 888, 600), "Illustrative photo · Democratic supporters"),
        ("p_trump.png", st[4] + 1.6, st[5] + 0.05, (96, 1030, 888, 480), "File photo · Donald Trump")]
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(V / "work" / "us-vote-2026-vertical-narrated.mp4")]
fc, prev = [], "[0:v]"
for i, (f, t0, t1, (x, y, w, h), label) in enumerate(PLAN, 1):
    (V / f"l{i}.txt").write_text(label, encoding="utf-8")
    d = round(t1 - t0, 2); n = int(d * 30) + 2
    cmd += ["-loop", "1", "-i", str(V / f)]
    fc.append(f"[{i}:v]scale={6*w}:{6*h}:force_original_aspect_ratio=increase:flags=lanczos,crop={6*w}:{6*h},"
              f"zoompan=z='1+0.06*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s={w}x{h}:fps=30,trim=duration={d},"
              f"setsar=1,format=yuv420p,drawbox=x=0:y=0:w=iw:h=ih:color=0xE0A546:t=6,"
              f"drawtext=fontfile={FONT}:textfile={V/f'l{i}.txt'}:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.65:boxborderw=12:x=22:y=22,"
              f"format=yuva420p,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={d-0.3}:d=0.3:alpha=1,setpts=PTS-STARTPTS+{t0}/TB[p{i}]")
    fc.append(f"{prev}[p{i}]overlay={x}:{y}:enable='between(t,{t0},{t1})':eof_action=pass[v{i}]")
    prev = f"[v{i}]"
out = V / "work" / "us-vote-2026-final.mp4"
cmd += ["-filter_complex", ";".join(fc), "-map", prev, "-map", "0:a", "-c:v", "libx264", "-crf", "19",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-t", str(END), str(out)]
subprocess.run(cmd, check=True)
print([(round(p[1], 2), round(p[2], 2)) for p in PLAN])
