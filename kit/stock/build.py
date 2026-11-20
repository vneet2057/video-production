import json, subprocess
from pathlib import Path
V = Path(__file__).parent; S = V.parent
import os
K = os.environ["UNSPLASH_KEY"]
FONT = str(Path.home() / "Library/Fonts/Inter-SemiBold.otf")   # macOS: brew install --cask font-inter
meta = json.load(open(V / "meta.json"))
st = json.load(open(S / "work" / "timing.json"))["starts"]
END = 55.8
PLAN = [("jet0.jpg",  st[1] + 1.6, st[2] + 0.05, (96, 1060, 888, 460)),
        ("dr23.jpg",  st[2] + 1.6, st[3] + 0.05, (96, 1030, 888, 490)),
        ("pyl2.jpg",  st[3] + 1.3, st[4] + 0.05, (96, 760, 888, 620)),
        ("dmz0.jpg",  st[4] + 1.6, END,          (96, 1040, 888, 480)),
        ("dro2.jpg",  22.4,        25.15,        None)]
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(S / "work" / "north-korea-week-vertical-narrated.mp4")]
fc, prev = [], "[0:v]"
for i, (f, t0, t1, box) in enumerate(PLAN, 1):
    m = meta[f]
    subprocess.run(["curl", "-s", "-o", "/dev/null", "-H", f"Authorization: Client-ID {K}", m["dl"]])  # Unsplash download ping
    (V / f"l{i}.txt").write_text(f"Stock photo · {m['name']} / Unsplash", encoding="utf-8")
    d = round(t1 - t0, 2); n = int(d * 30) + 2
    w, h = (box[2], box[3]) if box else (1080, 1920)
    x, y = (box[0], box[1]) if box else (0, 0)
    fs, pad = (24, 18) if box else (32, 64)
    cmd += ["-loop", "1", "-i", str(V / f)]
    border = f"drawbox=x=0:y=0:w=iw:h=ih:color=0xF2B04E:t=5," if box else ""
    if box:   # smooth slow zoom: zoompan on a 6x image, so each integer step is sub-pixel at output size
        move = (f"[{i}:v]scale={6*w}:{6*h}:force_original_aspect_ratio=increase:flags=lanczos,crop={6*w}:{6*h},"
                f"zoompan=z='1+0.06*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s={w}x{h}:fps=30,trim=duration={d},")
    else:     # full screen: left-to-right pan, worked at 2x then scaled down for smooth motion
        move = (f"[{i}:v]fps=30,trim=duration={d},scale=-2:{2*h*1.12:.0f}:flags=lanczos,"
                f"crop={2*w}:{2*h}:x='(iw-{2*w})/2-min((iw-{2*w})/2\\,180)+min(iw-{2*w}\\,360)*t/{d}':y='(ih-{2*h})/2',scale={w}:{h}:flags=bicubic,")
    fc.append(move +
              f"setsar=1,format=yuv420p,{border}"
              f"drawtext=fontfile={FONT}:textfile={V/f'l{i}.txt'}:fontsize={fs}:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=10:x={pad}:y={pad if not box else 18},"
              f"format=yuva420p,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={d-0.3}:d=0.3:alpha=1,setpts=PTS-STARTPTS+{t0}/TB[p{i}]")
    fc.append(f"{prev}[p{i}]overlay={x}:{y}:enable='between(t,{t0},{t1})':eof_action=pass[v{i}]")
    prev = f"[v{i}]"
out = S / "work" / "north-korea-week-final.mp4"
cmd += ["-filter_complex", ";".join(fc), "-map", prev, "-map", "0:a", "-c:v", "libx264", "-crf", "19",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-t", str(END), str(out)]
subprocess.run(cmd, check=True)
for t0 in [p[1] + 1.0 for p in PLAN]:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t0:.2f}", "-i", str(out), "-frames:v", "1",
                    "-vf", "scale=270:-2", str(V / f"c{t0:.0f}.png")], check=True)
print([round(p[1], 2) for p in PLAN])
