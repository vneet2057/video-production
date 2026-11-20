# Kerch Strait hook map: region view -> camera zooms to the bridge, a train crosses, strike flash, X, "TRAINS STOPPED".
import json, math
from pathlib import Path

V = Path(__file__).parent
G = json.load(open(next(p / "geo/wgj/countries.geo.json" for p in [V, *V.parents] if (p / "geo/wgj").is_dir())))
LON0, LON1, LAT_T = 32.2, 39.4, 47.65
VW, VH = 888, 700
C = math.cos(math.radians(45.8))
K = VW / ((LON1 - LON0) * C)


def xy(lon, lat):
    return ((lon - LON0) * C * K, (LAT_T - lat) * K)


def ring(r):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in (xy(lo, la) for lo, la in r)) + " Z"


def rings(iso):
    g = next(f for f in G["features"] if f["id"] == iso)["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    return [p[0] for p in polys]


ukr = rings("UKR")
rus = rings("RUS")
main = max(ukr, key=len)
# Crimea = the run of UKR points south of the Perekop isthmus (from Henichesk/Arabat round to Perekop)
i0 = next(i for i, p in enumerate(main) if abs(p[0] - 34.962342) < 1e-4)
i1 = next(i for i, p in enumerate(main) if abs(p[0] - 33.298567) < 1e-4)
crimea = main[i0:i1 + 1]

A = (36.44, 45.30)   # Crimea end of the bridge (Kerch side)
B = (36.672, 45.248)  # Russia end (Taman)
ax, ay = xy(*A); bx, by = xy(*B)
mx, my = (ax + bx) / 2, (ay + by) / 2
rail = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in (xy(*q) for q in [(37.6, 45.05), (37.0, 45.2), B, A, (36.1, 45.33)]))

S = 2.2   # zoom on the bridge


def cam(s, x, y):
    return f"translate({VW/2 - s*x:.1f}px,{VH/2 - s*y:.1f}px) scale({s})"


css = f"""
.cam{{transform-origin:0 0;animation:cam 2.4s cubic-bezier(.45,0,.25,1) both}}
@keyframes cam{{0%{{transform:{cam(1.0, VW/2, VH/2)}}}100%{{transform:{cam(S, mx, my - 12)}}}}}
.land{{fill:#2C3340;stroke:#11151B;stroke-width:1}}
.ru{{fill:#353C4A;stroke:#11151B;stroke-width:1}}
.cr{{fill:#6A3A2C;stroke:#E39B2D;stroke-width:1.2;stroke-dasharray:4 3}}
.train{{offset-path:path('{rail}');offset-rotate:auto;animation:train 2.6s cubic-bezier(.3,.5,.4,1) both}}
@keyframes train{{from{{offset-distance:0%}}to{{offset-distance:56%}}}}
.flash{{transform-box:fill-box;transform-origin:center;animation:flash .7s ease-out both;animation-delay:2.55s}}
@keyframes flash{{0%{{opacity:0;transform:scale(.2)}}30%{{opacity:1}}100%{{opacity:0;transform:scale(2.4)}}}}
.xm{{transform-box:fill-box;transform-origin:center;animation:xm .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:2.75s}}
@keyframes xm{{from{{opacity:0;transform:scale(.2)}}to{{opacity:1;transform:scale(1)}}}}
.lbl2{{animation:fadein .4s ease both;animation-delay:1.9s}}
.reg{{animation:fadeout .5s ease both;animation-delay:1.1s}}
@keyframes fadeout{{to{{opacity:0}}}}
@keyframes fadein{{from{{opacity:0}}to{{opacity:1}}}}
.stopped{{position:absolute;left:50%;top:470px;transform:translateX(-50%) rotate(-4deg);font:900 58px Inter,Arial;letter-spacing:6px;color:#E25D4B;border:6px solid #E25D4B;padding:6px 24px;border-radius:12px;background:rgba(17,21,27,.88);white-space:nowrap;animation:stamp2 .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:3.05s}}
@keyframes stamp2{{from{{opacity:0;transform:translateX(-50%) scale(1.8) rotate(-8deg)}}to{{opacity:1;transform:translateX(-50%) rotate(-4deg)}}}}
"""


def label(lon, lat, text, size, color="#F3ECDD", weight=800, spacing=3, italic=False, cls=""):
    x, y = xy(lon, lat)
    st = "font-style:italic;" if italic else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<text{c} x="{x:.0f}" y="{y:.0f}" text-anchor="middle" style="font:{weight} {size}px Inter,Arial;'
            f'letter-spacing:{spacing}px;fill:{color};{st}">{text}</text>')


land = "".join(f'<path class="land" d="{ring(r)}"/>' for r in ukr)
land += "".join(f'<path class="ru" d="{ring(r)}"/>' for r in rus)
land += f'<path class="cr" d="{ring(crimea)}"/>'
s = 1 / S  # sizes for labels that must read well after the zoom
svg = f'''<svg viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}" aria-label="Map of the Kerch Strait and the Crimean Bridge" style="border-radius:20px;background:#0E2A3E;overflow:hidden;display:block"><g class="cam">
{land}
{label(34.2, 46.95, "UKRAINE", 34, cls="reg")}
{label(38.6, 45.0, "RUSSIA", 34, cls="reg")}
{label(34.4, 45.35, "CRIMEA", 34, "#F2B04E", cls="reg")}
{label(34.4, 45.12, "Held by Russia since 2014", 17, "#E8C9A0", 600, 1, cls="reg")}
{label(36.75, 46.05, "Sea of Azov", 20, "#9FC4DA", 500, 1, True, cls="reg")}
{label(34.6, 44.05, "Black Sea", 24, "#9FC4DA", 500, 1, True, cls="reg")}
<path d="{rail}" fill="none" stroke="#7FB8D8" stroke-width="1.6" stroke-dasharray="3 3" opacity=".8"/>
<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#F2B04E" stroke-width="5" stroke-linecap="round"/>
<g class="train"><rect x="-7" y="-3" width="14" height="6" rx="2" fill="#FFFFFF"/></g>
<circle class="flash" cx="{mx:.1f}" cy="{my:.1f}" r="16" fill="#FF8A3D"/>
<g class="xm"><circle cx="{mx:.1f}" cy="{my:.1f}" r="11" fill="#11151B" stroke="#E25D4B" stroke-width="3"/>
<path d="M{mx-5:.1f} {my-5:.1f} L{mx+5:.1f} {my+5:.1f} M{mx+5:.1f} {my-5:.1f} L{mx-5:.1f} {my+5:.1f}" stroke="#E25D4B" stroke-width="3" stroke-linecap="round"/></g>
<g class="lbl2">{label(36.555, 45.40, "Crimean Bridge · 19 km", 12, "#F2B04E", 800, 1)}{label(36.3, 45.24, "Kerch", 10, "#F3ECDD", 700, 1)}{label(36.84, 45.33, "Taman", 10, "#F3ECDD", 700, 1)}{label(35.85, 45.18, "CRIMEA", 16, "#F2B04E", 800, 2)}{label(37.3, 45.13, "RUSSIA", 16, "#F3ECDD", 800, 2)}{label(36.6, 45.62, "Sea of Azov", 11, "#9FC4DA", 500, 1, True)}{label(36.35, 44.95, "Black Sea", 11, "#9FC4DA", 500, 1, True)}</g>
</g></svg>'''
(V / "map.svg").write_text(svg, encoding="utf-8")
(V / "map.css").write_text(css, encoding="utf-8")
print("bridge mid", round(mx), round(my), "crimea pts", len(crimea))
