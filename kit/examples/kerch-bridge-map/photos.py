# The user's two bridge photos as panels under the slide text (slide 2 and slide 3), slow zoom, honest label.
import json, subprocess
from pathlib import Path
V = Path(__file__).parent
FONT = str(Path.home() / "Library/Fonts/Inter-SemiBold.otf")
st = json.load(open(V / "work" / "timing.json"))["starts"]
SRC = V / "work" / "kerch-bridge-vertical-narrated.mp4"
END = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(SRC)],
                           capture_output=True, text=True).stdout)
LABEL = "Unverified photo · date not confirmed"
#        file                     start          end            (x,   y,   w,   h)
PLAN = [("in/bridge-span.png",  st[1] + 1.4, st[2] + 0.05, (96, 640, 888, 444)),
        ("in/bridge-smoke.png", st[2] + 1.6, st[3] + 0.05, (96, 840, 888, 512))]
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(SRC)]
fc, prev = [], "[0:v]"
(V / "work" / "plabel.txt").write_text(LABEL, encoding="utf-8")
for i, (f, t0, t1, (x, y, w, h)) in enumerate(PLAN, 1):
    d = round(t1 - t0, 2); n = int(d * 30) + 2
    cmd += ["-loop", "1", "-i", str(V / f)]
    fc.append(f"[{i}:v]scale={6*w}:{6*h}:force_original_aspect_ratio=increase:flags=lanczos,crop={6*w}:{6*h},"
              f"zoompan=z='1+0.06*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s={w}x{h}:fps=30,trim=duration={d},"
              f"setsar=1,format=yuv420p,drawbox=x=0:y=0:w=iw:h=ih:color=0xE25D4B:t=6,"
              f"drawtext=fontfile={FONT}:textfile={V/'work'/'plabel.txt'}:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=12:x=22:y=22,"
              f"format=yuva420p,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={d-0.3}:d=0.3:alpha=1,setpts=PTS-STARTPTS+{t0}/TB[p{i}]")
    fc.append(f"{prev}[p{i}]overlay={x}:{y}:enable='between(t,{t0},{t1})':eof_action=pass[v{i}]")
    prev = f"[v{i}]"
out = V / "work" / "kerch-bridge-final.mp4"
cmd += ["-filter_complex", ";".join(fc), "-map", prev, "-map", "0:a", "-c:v", "libx264", "-crf", "19",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-t", str(END), str(out)]
subprocess.run(cmd, check=True)
print("panels:", [(round(p[1], 2), round(p[2], 2)) for p in PLAN], "END", END)
