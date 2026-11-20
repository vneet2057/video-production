import json, subprocess
from pathlib import Path
V = Path(__file__).parent
FONT = str(Path.home() / "Library/Fonts/Inter-SemiBold.otf")   # macOS: brew install --cask font-inter
tm = json.load(open(V / "work" / "timing.json")); st = tm["starts"]
END = round(st[-1] + tm["durs"][-1], 2)
def ff(*a): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)
PLAN = [("in/rally.png",   st[0] + 1.4, st[1] + 0.05, (96, 730, 888, 592), "Illustrative photo · Election night supporters"),
        ("in/collage.png", st[1] + 1.4, st[2] + 0.05, (96, 700, 888, 500), "Illustration"),
        ("in/usiran.png",  st[3] + 1.4, st[4] + 0.05, (96, 770, 888, 566), "Illustration · AI-generated, not a real scene")]
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(V / "work" / "p8-vertical-narrated.mp4")]
fc, prev = [], "[0:v]"
for i, (f, t0, t1, (x, y, w, h), label) in enumerate(PLAN, 1):
    pre = V / f"pc{i}.png"
    ff("-i", f, "-vf", f"crop='min(iw,ih*{w}/{h})':'min(ih,iw*{h}/{w})'", str(pre))
    (V / f"l{i}.txt").write_text(label, encoding="utf-8")
    d = round(t1 - t0, 2); n = int(d * 30) + 2
    cmd += ["-loop", "1", "-i", str(pre)]
    fc.append(f"[{i}:v]scale={6*w}:{6*h}:force_original_aspect_ratio=increase:flags=lanczos,crop={6*w}:{6*h},"
              f"zoompan=z='1+0.06*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s={w}x{h}:fps=30,trim=duration={d},"
              f"setsar=1,format=yuv420p,drawbox=x=0:y=0:w=iw:h=ih:color=0xF2B04E:t=6,"
              f"drawtext=fontfile={FONT}:textfile={V/f'l{i}.txt'}:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.65:boxborderw=12:x=22:y=22,"
              f"format=yuva420p,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={d-0.3}:d=0.3:alpha=1,setpts=PTS-STARTPTS+{t0}/TB[p{i}]")
    fc.append(f"{prev}[p{i}]overlay={x}:{y}:enable='between(t,{t0},{t1})':eof_action=pass[v{i}]")
    prev = f"[v{i}]"
cmd += ["-filter_complex", ";".join(fc), "-map", prev, "-map", "0:a", "-c:v", "libx264", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "24000", "-ac", "1", "-movflags", "+faststart", "-t", str(END), str(V / "work" / "p8-slides-final.mp4")]
subprocess.run(cmd, check=True)
print(END)
