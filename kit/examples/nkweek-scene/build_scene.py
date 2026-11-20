"""Hook scene for 'North Korea's week'. Frame 0 already shows a lit map (good automatic cover).
s0 "Ten ballistic missiles in one day."        -> ten arcs fly from Wonsan into the sea, counter 1..10
s1 "Suicide drones diving onto mock tanks."   -> illustration: drones dive onto a mock tank target, blasts
s2 "This was North Korea's week."             -> stamp"""
import json, math
from pathlib import Path

V = Path(__file__).parent
S1 = json.load(open(V / "work" / "sentences.json"))[0]
s0, s1, s2 = S1[0][0], S1[1][0], S1[2][0]
A = round(S1[-1][1] + 0.5, 2)
G = json.load(open(next(p / "geo/wgj/countries.geo.json" for p in [V, *V.parents] if (p / "geo/wgj").is_dir())))   # shared geo/ at project root
RED, AMB, INK, TXT, SOFT = "#FF5A47", "#F2B04E", "#11151B", "#F2EEE6", "#B5BDC9"
VW, VH = 888, 760
LON0, LON1, LAT1 = 121.0, 136.0, 43.6
K = VW / ((LON1 - LON0) * math.cos(math.radians(38)))

def xy(lon, lat):
    return ((lon - LON0) * math.cos(math.radians(38)) * K, (LAT1 - lat) * K)

def ring(r):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in (xy(lo, la) for lo, la in r)) + " Z"

css, el = [], []
# ---------- scene 1: map ----------
el.append('<g class="sc1">')
for f in G["features"]:
    iso = f["id"]
    if iso not in ("PRK", "KOR", "CHN", "JPN", "RUS"):
        continue
    g = f["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    d = " ".join(ring(p[0]) for p in polys)
    fill = "#8E3B33" if iso == "PRK" else "#2C3340"
    el.append(f'<path d="{d}" fill="{fill}" stroke="#11151B" stroke-width="1.5"/>')

def lab(lon, lat, t, size=26, col=TXT, italic=False):
    x, y = xy(lon, lat)
    st = "font-style:italic;" if italic else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" style="font:800 {size}px Inter,Arial;letter-spacing:3px;fill:{col};{st}'
            f'paint-order:stroke;stroke:#0E2A3E;stroke-width:6px">{t}</text>')

el.append(lab(126.6, 40.3, "NORTH KOREA", 28))
el.append(lab(127.9, 36.2, "SOUTH KOREA", 22, SOFT))
el.append(lab(132.3, 38.0, "Sea of Japan / East Sea", 20, "#9FC4DA", True))
wx, wy = xy(127.45, 39.15)
el.append(f'<circle cx="{wx:.0f}" cy="{wy:.0f}" r="9" fill="{TXT}"/>')
el.append(f'<text x="{wx-14:.0f}" y="{wy+34:.0f}" text-anchor="end" style="font:800 20px Inter,Arial;fill:{TXT};paint-order:stroke;stroke:#0E2A3E;stroke-width:5px">Wonsan</text>')
t_arc = []
for i in range(10):
    ex, ey = xy(130.2 + (i % 4) * 0.75, 41.4 - i * 0.42)
    lift = 70 + (i % 3) * 30
    d = f"M{wx:.0f} {wy:.0f} Q{(wx+ex)/2:.0f} {min(wy, ey)-lift:.0f} {ex:.0f} {ey:.0f}"
    t = round(s0 + 0.05 + i * 0.12, 2)
    t_arc.append(t)
    el.append(f'<path class="arc" d="{d}" pathLength="1" fill="none" stroke="{RED}" stroke-width="4.5" stroke-linecap="round" style="animation-delay:{t}s"/>')
    el.append(f'<circle class="spl" cx="{ex:.0f}" cy="{ey:.0f}" r="8" fill="none" stroke="{RED}" stroke-width="3" '
              f'style="animation-delay:{t+0.55:.2f}s;transform-origin:{ex:.0f}px {ey:.0f}px"/>')
css.append(".arc{stroke-dasharray:1;stroke-dashoffset:1;animation:dr .6s cubic-bezier(.4,0,.6,1) both}@keyframes dr{to{stroke-dashoffset:0}}"
           ".spl{opacity:0;animation:spl .6s ease-out forwards}@keyframes spl{0%{opacity:1;transform:scale(.4)}100%{opacity:0;transform:scale(2.4)}}")
# counter badge 1..10
el.append(f'<rect x="24" y="24" width="330" height="92" rx="14" fill="{INK}" stroke="{RED}" stroke-width="3"/>')
el.append(f'<text x="210" y="62" style="font:800 20px Inter,Arial;letter-spacing:2px;fill:{SOFT}">BALLISTIC</text>'
          f'<text x="210" y="92" style="font:800 20px Inter,Arial;letter-spacing:2px;fill:{SOFT}">MISSILES</text>')
el.append(f'<text class="c0" x="190" y="96" text-anchor="end" style="font:900 72px Inter,Arial;fill:{RED}">~10</text>')
for i, t in enumerate(t_arc, 1):
    nxt = t_arc[i] if i < 10 else None
    cls = "cnt last" if i == 10 else "cnt"
    dur = f"{nxt - t:.2f}" if nxt else ".1"
    el.append(f'<text class="{cls}" x="190" y="96" text-anchor="end" style="font:900 72px Inter,Arial;fill:{RED};animation-delay:{t+0.4:.2f}s;animation-duration:{dur}s">{"~10" if i == 10 else i}</text>')
css.append(f".c0{{animation:hide .01s both;animation-delay:{t_arc[0]+0.4:.2f}s}}@keyframes hide{{to{{opacity:0}}}}"
           ".cnt{opacity:0;animation-name:cnt;animation-timing-function:steps(1);animation-fill-mode:none}"
           "@keyframes cnt{0%,100%{opacity:1}}.cnt.last{animation-fill-mode:forwards}")
el.append("</g>")
css.append(f".sc1{{animation:out .35s ease both;animation-delay:{s1+0.1:.2f}s}}@keyframes out{{to{{opacity:0}}}}")

# ---------- scene 2: drone dive illustration ----------
el.append('<g class="sc2">')
el.append(f'<rect width="{VW}" height="{VH}" fill="#151B26"/>')
el.append(f'<rect y="600" width="{VW}" height="160" fill="#232B36"/>')
TX, TY = 444, 600
tank = (f'<g><rect x="{TX-150}" y="{TY-78}" width="300" height="58" rx="10" fill="#4B5563"/>'
        f'<rect x="{TX-70}" y="{TY-118}" width="140" height="46" rx="12" fill="#5B6573"/>'
        f'<rect x="{TX+60}" y="{TY-104}" width="170" height="14" rx="6" fill="#5B6573"/>'
        f'<rect x="{TX-165}" y="{TY-26}" width="330" height="30" rx="15" fill="#2F3640"/></g>')
el.append(tank)
el.append(f'<text x="{TX}" y="{TY+70}" text-anchor="middle" style="font:800 26px Inter,Arial;letter-spacing:4px;fill:{AMB}">MOCK TARGET</text>')
drone = '<path d="M-34 0 L0 -12 L34 0 L8 4 L0 18 L-8 4 Z" fill="#E5E7EB" stroke="#11151B" stroke-width="2"/>'
starts = [(-60, 60), (444, -60), (950, 90)]
for k, (x0, y0) in enumerate(starts):
    d = f"M{x0} {y0} Q{(x0+TX)/2:.0f} {y0+40} {TX + (k-1)*60} {TY-90}"
    t = round(s1 + 0.35 + k * 0.4, 2)
    el.append(f'<g class="dr" style="offset-path:path(\'{d}\');offset-rotate:auto 90deg;scale:2.2;animation-delay:{t}s">{drone}</g>')
    bx = TX + (k - 1) * 60
    el.append(f'<g class="bl" style="animation-delay:{t+0.95:.2f}s;transform-origin:{bx}px {TY-90}px">'
              f'<circle cx="{bx}" cy="{TY-90}" r="60" fill="{AMB}" opacity=".9"/><circle cx="{bx}" cy="{TY-90}" r="34" fill="#FFF3D6"/></g>')
el.append(f'<text x="{VW/2}" y="70" text-anchor="middle" style="font:900 40px Inter,Arial;letter-spacing:3px;fill:{TXT}">SUICIDE DRONES</text>')
el.append(f'<text x="{VW/2}" y="735" text-anchor="middle" style="font:500 20px Inter,Arial;fill:{SOFT}">Illustration · based on North Korean state media reports</text>')
css.append(".dr{offset-distance:0%;opacity:0;animation:dive 1s cubic-bezier(.5,0,.8,.6) both}"
           "@keyframes dive{0%{offset-distance:0%;opacity:1}95%{opacity:1}100%{offset-distance:100%;opacity:0}}"
           ".bl{opacity:0;animation:bl .7s ease-out forwards}@keyframes bl{0%{opacity:1;transform:scale(.2)}60%{opacity:1}100%{opacity:0;transform:scale(1.8)}}")
el.append("</g>")
css.append(f".sc2{{opacity:0;animation:fin .3s ease both;animation-delay:{s1+0.2:.2f}s}}@keyframes fin{{to{{opacity:1}}}}")
# stamp
el.append(f'<g class="stp" style="transform-origin:444px 330px"><rect x="84" y="270" width="720" height="120" rx="16" fill="{INK}" stroke="{RED}" stroke-width="8"/>'
          f'<text x="444" y="352" text-anchor="middle" style="font:900 54px Inter,Arial;letter-spacing:3px;fill:{RED}">NORTH KOREA\'S WEEK</text></g>')
css.append(f".stp{{opacity:0;animation:st .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:{s2+0.15:.2f}s}}"
           "@keyframes st{from{opacity:0;transform:scale(1.8) rotate(-8deg)}to{opacity:1;transform:rotate(-4deg)}}")

svg = (f'<svg viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}" aria-label="Map of North Korea missile launches and a drone strike illustration" '
       f'style="border-radius:20px;background:#0E2A3E;overflow:hidden">{"".join(el)}</svg>')
(V / "scene.svg").write_text(svg, encoding="utf-8")
(V / "scene.css").write_text("\n".join(css), encoding="utf-8")
print("A", A, s0, s1, s2)
