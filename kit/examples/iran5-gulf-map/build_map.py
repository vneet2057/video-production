"""Part 5 hook map (real outlines from world.geo.json): Gulf allies light up ("get ready"), a carrier group sails in,
a Patriot arc flies in from the west (from Texas) to Israel, dashed "possible strike" arrows point at Iran, an
AFTER NOV 3 badge, then the PART 5 stamp. Timed to sentences.json."""
import json, math
from pathlib import Path

V = Path(__file__).parent
S1 = json.load(open(V / "work" / "sentences.json"))[0]
s0, s1, s2 = S1[0][0], S1[1][0], S1[2][0]
A = round(S1[-1][1] + 0.5, 2)
G = json.load(open(next(p / "geo/wgj/countries.geo.json" for p in [V, *V.parents] if (p / "geo/wgj").is_dir())))   # shared geo/ at project root
LON0, LON1, LAT0, LAT1 = 27.0, 66.0, 10.5, 40.0
W = 888
K = W / ((LON1 - LON0) * math.cos(math.radians(25)))
H = round((LAT1 - LAT0) * K)
RED, AMB, INK, TXT, SOFT = "#E25D4B", "#F2B04E", "#11151B", "#F2EEE6", "#B5BDC9"

def xy(lon, lat):
    return ((lon - LON0) * math.cos(math.radians(25)) * K, (LAT1 - lat) * K)

def ring(r):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in (xy(lo, la) for lo, la in r)) + " Z"

GULF = {"SAU": .3, "ARE": .5, "QAT": .6, "KWT": .7, "OMN": .8, "BHR": .6}
paths, css = [], []
for f in G["features"]:
    iso = f["id"]
    g = f["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    d = " ".join(ring(p[0]) for p in polys)
    if iso in GULF:
        paths.append(f'<path class="gulf" d="{d}" style="--d:{s0 + GULF[iso]:.2f}s"/>')
    elif iso == "IRN":
        paths.append(f'<path class="irn" d="{d}"/>')
    elif iso == "ISR":
        paths.append(f'<path class="isr" d="{d}"/>')
    else:
        paths.append(f'<path class="land" d="{d}"/>')

def label(lon, lat, t, size=24, col=SOFT, cls=""):
    x, y = xy(lon, lat)
    c = f' class="{cls}"' if cls else ""
    return (f'<text{c} x="{x:.0f}" y="{y:.0f}" text-anchor="middle" style="font:800 {size}px Inter,Arial;letter-spacing:3px;fill:{col};'
            f'paint-order:stroke;stroke:#0E2A3E;stroke-width:5px">{t}</text>')

el = []
el.append(label(54, 33.2, "IRAN", 40, TXT))
el.append(label(44.5, 23.5, "SAUDI ARABIA", 24, INK))
# carrier group sails from the Arabian Sea into the Gulf of Oman
c_path = "M{:.0f} {:.0f} Q{:.0f} {:.0f} {:.0f} {:.0f}".format(*xy(64.5, 14.0), *xy(62.5, 20.5), *xy(58.9, 23.9))
el.append(f'<g class="ship" style="offset-path:path(\'{c_path}\');offset-rotate:auto"><path d="M-30 -9 L22 -9 L34 0 L22 9 L-30 9 Z" fill="{TXT}" stroke="{INK}" stroke-width="3"/>'
          f'<rect x="-6" y="-16" width="14" height="10" fill="{TXT}" stroke="{INK}" stroke-width="2"/></g>')
cx, cy = xy(61.5, 21.6)
el.append(f'<g class="cg"><rect x="{cx-290}" y="{cy+60}" width="230" height="40" rx="8" fill="{INK}" stroke="{TXT}" stroke-width="2"/>'
          f'<text x="{cx-175}" y="{cy+87}" text-anchor="middle" style="font:800 20px Inter,Arial;letter-spacing:2px;fill:{TXT}">CARRIER GROUP</text></g>')
# Patriot: arc in from the west edge (from Texas) to Israel
ix, iy = xy(35.0, 31.6)
p_d = f"M-10 {iy-160:.0f} Q{ix*0.45:.0f} {iy-260:.0f} {ix:.0f} {iy:.0f}"
el.append(f'<path class="pat" d="{p_d}" pathLength="1" fill="none" stroke="{AMB}" stroke-width="5" stroke-linecap="round"/>')
el.append(f'<g class="pl"><rect x="12" y="100" width="250" height="40" rx="8" fill="{INK}" stroke="{AMB}" stroke-width="2"/>'
          f'<text x="137" y="127" text-anchor="middle" style="font:800 20px Inter,Arial;letter-spacing:2px;fill:{AMB}">PATRIOT FROM TEXAS</text></g>')
el.append(label(35.0, 33.4, "ISRAEL", 22, AMB, "isrl"))
# possible strike arrows (dashed) from the Gulf toward Iran
targets = [(51.4, 35.6), (51.7, 32.7), (50.9, 29.0), (56.3, 27.3)]
for k, (lo, la) in enumerate(targets):
    x0, y0 = xy(53.0 + k * 0.6, 24.6)
    x1, y1 = xy(lo, la)
    el.append(f'<path class="stk" d="M{x0:.0f} {y0:.0f} Q{(x0+x1)/2+30:.0f} {(y0+y1)/2:.0f} {x1:.0f} {y1:.0f}" pathLength="1" fill="none" '
              f'stroke="{RED}" stroke-width="5" stroke-linecap="round" style="animation-delay:{s1 + 1.7 + k * 0.18:.2f}s"/>')
    el.append(f'<circle class="tg" cx="{x1:.0f}" cy="{y1:.0f}" r="9" fill="{RED}" style="animation-delay:{s1 + 2.2 + k * 0.18:.2f}s;transform-origin:{x1:.0f}px {y1:.0f}px"/>')
el.append(f'<g class="ps"><rect x="{W-300}" y="{xy(0, 30.2)[1]:.0f}" width="270" height="44" rx="8" fill="{INK}" stroke="{RED}" stroke-width="2"/>'
          f'<text x="{W-165}" y="{xy(0, 30.2)[1]+30:.0f}" text-anchor="middle" style="font:800 20px Inter,Arial;letter-spacing:2px;fill:{RED}">POSSIBLE STRIKES</text></g>')
# top badges
el.append(f'<g class="b1"><rect x="214" y="22" width="460" height="64" rx="12" fill="{INK}" stroke="{AMB}" stroke-width="3"/>'
          f'<text x="444" y="65" text-anchor="middle" style="font:900 30px Inter,Arial;letter-spacing:2px;fill:{AMB}">GULF ALLIES: "GET READY"</text></g>')
el.append(f'<g class="b2"><rect x="264" y="22" width="360" height="64" rx="12" fill="{RED}"/>'
          f'<text x="444" y="66" text-anchor="middle" style="font:900 32px Inter,Arial;letter-spacing:3px;fill:{INK}">AFTER NOV 3?</text></g>')
el.append(f'<g class="p5" style="transform-origin:444px {H/2+40:.0f}px"><rect x="214" y="{H/2:.0f}" width="460" height="100" rx="14" fill="{INK}" stroke="{RED}" stroke-width="7"/>'
          f'<text x="444" y="{H/2+68:.0f}" text-anchor="middle" style="font:900 56px Inter,Arial;letter-spacing:5px;fill:{RED}">IRAN WAR · 5</text></g>')

css.append(f"""
.land{{fill:#2C3340;stroke:#11151B;stroke-width:1}}
.gulf{{fill:#2C3340;stroke:#11151B;stroke-width:1;animation:gl .5s ease both;animation-delay:var(--d)}}@keyframes gl{{to{{fill:#B98A3E}}}}
.irn{{fill:#2C3340;stroke:#11151B;stroke-width:1;animation:ir .6s ease both;animation-delay:{s1+1.5:.2f}s}}@keyframes ir{{to{{fill:#7A3029}}}}
.isr{{fill:#2C3340;stroke:#11151B;stroke-width:1;animation:gl .4s ease both;animation-delay:{s1+1.5:.2f}s}}
.ship{{offset-distance:0%;animation:sail 2.2s cubic-bezier(.3,.6,.3,1) both;animation-delay:{s1:.2f}s}}@keyframes sail{{to{{offset-distance:100%}}}}
.cg,.pl,.ps,.isrl{{opacity:0;animation:fi .35s ease both}}@keyframes fi{{to{{opacity:1}}}}
.cg{{animation-delay:{s1+0.6:.2f}s}}.pl{{animation-delay:{s1+0.4:.2f}s}}.ps{{animation-delay:{s1+2.0:.2f}s}}.isrl{{animation-delay:{s1+1.5:.2f}s}}
.pat{{stroke-dasharray:1;stroke-dashoffset:1;animation:dr 1.3s ease-in-out both;animation-delay:{s1+0.3:.2f}s}}@keyframes dr{{to{{stroke-dashoffset:0}}}}
.stk{{stroke-dasharray:.04 .03;stroke-dashoffset:0;opacity:0;animation:stk .6s ease-out both}}@keyframes stk{{from{{opacity:0;clip-path:inset(0 100% 0 0)}}to{{opacity:1;clip-path:inset(0 0 0 0)}}}}
.tg{{opacity:0;animation:tg .45s cubic-bezier(.2,.9,.3,1.4) both}}@keyframes tg{{from{{opacity:0;transform:scale(.2)}}to{{opacity:1;transform:scale(1)}}}}
.b1{{opacity:0;animation:bw {A}s linear both}}
@keyframes bw{{0%,{100*(s0+0.3)/A:.1f}%{{opacity:0}}{100*(s0+0.6)/A:.1f}%,{100*(s1+0.9)/A:.1f}%{{opacity:1}}{100*(s1+1.1)/A:.1f}%,100%{{opacity:0}}}}
.b2{{opacity:0;animation:b2 {A}s linear both}}
@keyframes b2{{0%,{100*(s1+1.1)/A:.1f}%{{opacity:0;transform:none}}{100*(s1+1.4)/A:.1f}%,100%{{opacity:1}}}}
.p5{{opacity:0;animation:st .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:{s2+0.2:.2f}s}}
@keyframes st{{from{{opacity:0;transform:scale(1.8) rotate(-8deg)}}to{{opacity:1;transform:rotate(-4deg)}}}}
""")
svg = (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" aria-label="Map: US forces move toward the Gulf; possible strikes on Iran" '
       f'style="border-radius:20px;background:#0E2A3E;overflow:hidden">{"".join(paths)}{"".join(el)}</svg>')
(V / "map.svg").write_text(svg, encoding="utf-8")
(V / "map.css").write_text("".join(css), encoding="utf-8")
print(W, H, A, s0, s1, s2)
