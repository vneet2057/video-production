"""World map hook: camera on Russia (Bulava arc across Russia) -> Korea (about ten launches) ->
wide view adding France (Atlantic arc) and South Korea. Times come from sentences.json."""
import json
from pathlib import Path

V = Path(__file__).parent
S1 = json.load(open(V / "work" / "sentences.json"))[0]
r0, k0, f0, q0 = S1[0][0], S1[1][0], S1[2][0], S1[3][0]
A = round(S1[-1][1] + 0.5, 2)
G = json.load(open(next(p / "geo/wgj/countries.geo.json" for p in [V, *V.parents] if (p / "geo/wgj").is_dir())))   # shared geo/ at project root
W, LAT_T, LAT_B = 888, 85, -60
H = round((LAT_T - LAT_B) / 360 * W * 2)
VW, VH = 888, 760

def xy(lon, lat):
    return ((lon + 180) / 360 * W, (LAT_T - lat) / (LAT_T - LAT_B) * H)

def ring(r):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in (xy(lo, la) for lo, la in r)) + " Z"

LIT = {"RUS": r0 + 0.2, "PRK": k0 + 0.15, "FRA": f0 + 0.6, "KOR": f0 + 1.6}
paths = []
for f in G["features"]:
    iso = f["id"]
    if iso == "ATA":
        continue
    g = f["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    d = " ".join(ring(p[0]) for p in polys)
    cls = "lit" if iso in LIT else "land"
    st = f' style="--d:{LIT[iso]:.2f}s"' if iso in LIT else ""
    paths.append(f'<path class="{cls}" d="{d}"{st}/>')

def arc(a, b, lift, width, delay, dur, cls="trk"):
    (x1, y1), (x2, y2) = xy(*a), xy(*b)
    cx, cy = (x1 + x2) / 2, min(y1, y2) - lift
    d = f"M{x1:.2f} {y1:.2f} Q{cx:.2f} {cy:.2f} {x2:.2f} {y2:.2f}"
    return d, (f'<path class="{cls}" d="{d}" pathLength="1" fill="none" stroke="#FF5A47" stroke-width="{width}" '
               f'stroke-linecap="round" style="--d:{delay:.2f}s;--t:{dur}s"/>')

arcs = []
# Russia: Bulava from the Sea of Okhotsk westward (target range estimated by analysts: Kanin Peninsula)
rus_d, a1 = arc((146, 53.5), (45, 67.5), 40, 2.4, r0 + 0.5, 2.4)
arcs.append(a1)
arcs.append(f'<circle class="mhead" r="4" fill="#FFE1D6" style="offset-path:path(\'{rus_d}\');--d:{r0+0.5:.2f}s;--t:2.4s"/>')
# North Korea: about ten short-range missiles from the Wonsan area into the sea off the east coast
for i in range(10):
    end = (131.4 + (i % 4) * 0.8, 41.2 - i * 0.38)
    arcs.append(arc((127.45, 39.15), end, 1.4 + (i % 3) * 0.5, 0.5, k0 + 0.45 + i * 0.13, 0.7)[1])
# France: M51.3 from off Brittany into the North Atlantic
arcs.append(arc((-4.8, 48.2), (-24, 46.5), 10, 2.2, f0 + 0.8, 1.4)[1])
kx, ky = xy(127.8, 36.4)
rings = (f'<circle class="ring" cx="{kx:.1f}" cy="{ky:.1f}" r="3.2" fill="none" stroke="#F2B04E" stroke-width=".8" '
         f'style="--d:{f0+1.6:.2f}s;transform-origin:{kx:.1f}px {ky:.1f}px"/>')

def cam(lon, lat, s):
    x, y = xy(lon, lat)
    return (VW / 2 - s * x, VH / 2 - s * y, s)

def tf(c):
    return f"translate({c[0]:.1f}px,{c[1]:.1f}px) scale({c[2]})"

RU, KO, WIDE, END = cam(95, 60, 1.75), cam(129, 39, 8), cam(55, 47, 1.6), cam(60, 45, 1.45)
pc = lambda t: f"{100 * max(0, min(t, A)) / A:.2f}%"
css = f"""
.cam{{transform-origin:0 0;animation:cam {A}s cubic-bezier(.45,0,.3,1) both}}
@keyframes cam{{0%{{transform:{tf(RU)}}}{pc(k0-0.45)}{{transform:{tf(RU)}}}{pc(k0+0.35)}{{transform:{tf(KO)}}}{pc(f0-0.3)}{{transform:{tf(KO)}}}{pc(f0+0.5)}{{transform:{tf(WIDE)}}}100%{{transform:{tf(END)}}}}}
.land{{fill:#2C3340;stroke:#11151B;stroke-width:.35}}
.lit{{fill:#2C3340;stroke:#11151B;stroke-width:.35;animation:lit .45s ease both;animation-delay:var(--d)}}
@keyframes lit{{to{{fill:#8E3B33}}}}
.trk{{stroke-dasharray:1;stroke-dashoffset:1;animation:trk var(--t) cubic-bezier(.4,0,.6,1) both;animation-delay:var(--d)}}
@keyframes trk{{to{{stroke-dashoffset:0}}}}
.mhead{{offset-distance:0%;opacity:0;animation:head var(--t) cubic-bezier(.4,0,.6,1) both;animation-delay:var(--d)}}
@keyframes head{{0%{{opacity:1;offset-distance:0%}}96%{{opacity:1}}100%{{opacity:0;offset-distance:100%}}}}
.ring{{opacity:0;animation:ring 1.2s ease-out 3 both;animation-delay:var(--d)}}
@keyframes ring{{0%{{opacity:0;transform:scale(.6)}}10%{{opacity:1;transform:scale(.8)}}100%{{opacity:0;transform:scale(2.6)}}}}
"""

# screen-space badges (outside the camera so they stay the same size)
def badge(i, x, y, text, t_in, t_out, color="#FF5A47", size=30):
    w = size * 0.62 * len(text) + 36
    hh = size + 24
    k = f"b{i}"
    fade = 0.25
    frames = (f"0%{{opacity:0;transform:scale(.6)}}{pc(t_in)}{{opacity:0;transform:scale(.6)}}"
              f"{pc(t_in+fade)}{{opacity:1;transform:scale(1)}}")
    frames += (f"{pc(t_out-fade)}{{opacity:1;transform:scale(1)}}{pc(t_out)}{{opacity:0;transform:scale(1)}}100%{{opacity:0}}"
               if t_out < A else "100%{opacity:1;transform:scale(1)}")
    global css
    css += f".{k}{{animation:{k} {A}s linear both;transform-box:fill-box;transform-origin:center}}@keyframes {k}{{{frames}}}\n"
    return (f'<g class="{k}"><rect x="{x-w/2:.0f}" y="{y-hh/2:.0f}" width="{w:.0f}" height="{hh}" rx="10" fill="#11151B" '
            f'stroke="{color}" stroke-width="3"/><text x="{x:.0f}" y="{y+size*0.36:.0f}" text-anchor="middle" '
            f'style="font:800 {size}px Inter,Arial;letter-spacing:1px;fill:{color}">{text}</text></g>')

def scr(c, lon, lat):
    x, y = xy(lon, lat)
    return c[0] + c[2] * x, c[1] + c[2] * y

bd = [badge(1, 444, 92, "RUSSIA · NUCLEAR-CAPABLE BULAVA", r0 + 0.4, k0 - 0.3, size=32),
      badge(2, 444, 92, "NORTH KOREA · ~10 MISSILES TODAY", k0 + 0.4, f0 - 0.2, size=32)]
labels = [("RUSSIA", 95, 63, -4, k0 - 0.3), ("N. KOREA", 127, 40, 22, f0 + 0.5), ("FRANCE", -2, 46.5, 34, f0 + 0.8),
          ("S. KOREA", 128, 36, 50, f0 + 1.6)]
for j, (t, lo, la, dy, tin) in enumerate(labels, 3):
    x, y = scr(END, lo, la)
    if t == "RUSSIA":
        tin = f0 + 0.5
    bd.append(badge(j, x, y + dy, t, tin, A + 1, color="#F2B04E", size=22))
svg = (f'<svg viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}" aria-label="World map: missile tests by Russia, North Korea, France and South Korea" '
       f'style="border-radius:20px;background:#0E2A3E;overflow:hidden"><g class="cam">{"".join(paths)}{"".join(arcs)}{rings}</g>{"".join(bd)}</svg>')
(V / "map.svg").write_text(svg, encoding="utf-8")
(V / "map.css").write_text(css, encoding="utf-8")
print(A, r0, k0, f0, q0, [round(v, 1) for v in scr(END, 128, 36)], [round(v, 1) for v in scr(END, -2, 46.5)])
