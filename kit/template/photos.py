# OPTIONAL: photos/clips as panels under the slide text or full-screen cutaways, over the narrated video.
# Output: work/NAME-photos.mp4 (finish.py picks it up automatically). Simpler alternative: put photos straight into
# slides.html with a Ken Burns CSS animation (see make_slides.py: .hookimg / .himg / .qimg) and skip this script.
# Labels must be honest: "File photo · Name", "Illustrative photo · ...", "Unverified photo · date not confirmed" (red border).
import json, subprocess
from pathlib import Path
V = Path(__file__).parent; W = V / "work"
NAME = V.name[11:] if V.name[:4].isdigit() else V.name
FONT = str(Path.home() / "Library/Fonts/Inter-SemiBold.otf")
st = json.load(open(W / "timing.json"))["starts"]          # when each slide starts
SRC = W / f"{NAME}-vertical-narrated.mp4"
END = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(SRC)],
                           capture_output=True, text=True).stdout)   # never cut the video short
GOLD, RED = "0xF2B04E", "0xE25D4B"
# file in in/, start, end, (x, y, w, h) panel (keep y+h <= ~1380 so captions at y~1470 stay clear) or None = full screen, label, border
PLAN = [
    # ("in/photo1.jpg", st[1] + 1.4, st[2] + 0.05, (96, 700, 888, 500), "File photo · Name", GOLD),
    # ("in/photo2.jpg", 31.2, 34.0, None, "Unverified photo · date not confirmed", RED),
]
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(SRC)]
fc, prev = [], "[0:v]"
for i, (f, t0, t1, box, label, color) in enumerate(PLAN, 1):
    (W / f"plabel{i}.txt").write_text(label, encoding="utf-8")
    d = round(t1 - t0, 2); n = int(d * 30) + 2
    w, h = (box[2], box[3]) if box else (1080, 1920)
    x, y = (box[0], box[1]) if box else (0, 0)
    cmd += ["-loop", "1", "-i", str(V / f)]
    if box:   # smooth slow zoom on a 6x upscale (sub-pixel steps)
        move = (f"[{i}:v]scale={6*w}:{6*h}:force_original_aspect_ratio=increase:flags=lanczos,crop={6*w}:{6*h},"
                f"zoompan=z='1+0.06*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s={w}x{h}:fps=30,trim=duration={d},"
                f"setsar=1,format=yuv420p,drawbox=x=0:y=0:w=iw:h=ih:color={color}:t=6,")
    else:     # full screen: slow left->right pan (max 180 px), worked at 2x
        move = (f"[{i}:v]fps=30,trim=duration={d},scale=-2:{2*h*1.12:.0f}:flags=lanczos,"
                f"crop={2*w}:{2*h}:x='(iw-{2*w})/2-min((iw-{2*w})/2\\,180)+min(iw-{2*w}\\,360)*t/{d}':y='(ih-{2*h})/2',scale={w}:{h}:flags=bicubic,setsar=1,format=yuv420p,")
    fs, pad = (26, 22) if box else (32, 64)
    fc.append(move + f"drawtext=fontfile={FONT}:textfile={W/f'plabel{i}.txt'}:fontsize={fs}:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=12:x={pad}:y={pad},"
              f"format=yuva420p,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={d-0.3}:d=0.3:alpha=1,setpts=PTS-STARTPTS+{t0}/TB[p{i}]")
    fc.append(f"{prev}[p{i}]overlay={x}:{y}:enable='between(t,{t0},{t1})':eof_action=pass[v{i}]")
    prev = f"[v{i}]"
if PLAN:
    cmd += ["-filter_complex", ";".join(fc), "-map", prev, "-map", "0:a", "-c:v", "libx264", "-crf", "19",
            "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-t", str(END), str(W / f"{NAME}-photos.mp4")]
    subprocess.run(cmd, check=True)
    print("panels:", [(p[0], round(p[1], 2), round(p[2], 2)) for p in PLAN])
else:
    print("PLAN is empty: nothing to do (finish.py will use the narrated video)")
