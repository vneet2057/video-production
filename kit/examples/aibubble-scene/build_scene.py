"""Hook scene: China's AI bubble swells and POPS ($480B counter), America's bubble wobbles and cracks ("?").
Timed to the hook sentences in sentences.json."""
import json, math
from pathlib import Path

V = Path(__file__).parent
S1 = json.load(open(V / "work" / "sentences.json"))[0]
s0, s1, s2 = S1[0][0], S1[1][0], S1[2][0]
A = round(S1[-1][1] + 0.5, 2)
RED, AMB, INK, TXT, SOFT, CYAN = "#FF5A47", "#F2B04E", "#0B0F15", "#F2EEE6", "#8B95A5", "#7FE3FF"
css, el = [], []

el.append('<defs><radialGradient id="bg1" cx="38%" cy="32%" r="70%"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".55"/>'
          f'<stop offset=".35" stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="#3B7BFF" stop-opacity=".35"/></radialGradient></defs>')

def bubble(cls, cx, cy, r, label, sub):
    return (f'<g class="{cls}" style="transform-origin:{cx}px {cy}px">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#bg1)" stroke="{CYAN}" stroke-width="4"/>'
            f'<ellipse cx="{cx-r*.38}" cy="{cy-r*.42}" rx="{r*.22}" ry="{r*.12}" fill="#FFFFFF" opacity=".55" transform="rotate(-35 {cx-r*.38} {cy-r*.42})"/>'
            f'<text x="{cx}" y="{cy+28}" text-anchor="middle" style="font:900 {int(r*.62)}px Inter,Arial;fill:{TXT};opacity:.92">AI</text></g>'
            f'<text x="{cx}" y="{cy+r+70}" text-anchor="middle" style="font:800 28px Inter,Arial;letter-spacing:3px;fill:{SOFT}">{label}</text>'
            f'<text x="{cx}" y="{cy+r+104}" text-anchor="middle" style="font:600 22px Inter,Arial;fill:#5D6675">{sub}</text>')

CX, CY, CR = 235, 400, 165
UX, UY, UR = 655, 400, 150
pop = s0 + 1.75
el.append(bubble("cn", CX, CY, CR, "CHINA", "STAR 50 index"))
css.append(f".cn{{animation:swell 1.6s cubic-bezier(.3,.8,.3,1) both,popb .18s ease-in both;animation-delay:{s0}s,{pop}s}}"
           "@keyframes swell{from{transform:scale(.25)}to{transform:scale(1)}}"
           "@keyframes popb{from{transform:scale(1);opacity:1}to{transform:scale(1.25);opacity:0}}")
# burst shards and droplets
for i in range(12):
    a = i * math.tau / 12 + .13
    x1, y1 = CX + math.cos(a) * CR * .9, CY + math.sin(a) * CR * .9
    x2, y2 = CX + math.cos(a) * CR * 1.35, CY + math.sin(a) * CR * 1.35
    el.append(f'<line class="sh" x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{CYAN}" stroke-width="6" stroke-linecap="round" '
              f'style="transform-origin:{CX}px {CY}px"/>')
    dx, dy = CX + math.cos(a + .26) * CR * 1.2, CY + math.sin(a + .26) * CR * 1.2
    el.append(f'<circle class="sh" cx="{dx:.0f}" cy="{dy:.0f}" r="7" fill="{CYAN}" style="transform-origin:{CX}px {CY}px"/>')
css.append(f".sh{{opacity:0;animation:shard .7s cubic-bezier(.2,.7,.3,1) forwards;animation-delay:{pop}s}}"
           "@keyframes shard{0%{opacity:1;transform:scale(.7)}100%{opacity:0;transform:scale(1.45)}}")
el.append(f'<text class="popt" x="{CX}" y="{CY+30}" text-anchor="middle" style="font:900 96px Inter,Arial;letter-spacing:2px;fill:{RED};transform-origin:{CX}px {CY}px">POP!</text>')
css.append(f".popt{{opacity:0;animation:popt .45s cubic-bezier(.2,.9,.3,1.4) both;animation-delay:{pop+0.05}s}}"
           "@keyframes popt{from{opacity:0;transform:scale(.3) rotate(-12deg)}to{opacity:1;transform:rotate(-6deg)}}")

# US bubble: grows early, wobbles + cracks on "Is America next?"
el.append(bubble("us", UX, UY, UR, "UNITED STATES", "Nasdaq, AI giants"))
css.append(f".us{{animation:swell 1.8s cubic-bezier(.3,.8,.3,1) both,wob 1.3s ease-in-out both;animation-delay:{s0+0.3}s,{s2}s}}"
           "@keyframes wob{0%,100%{transform:scale(1)}20%{transform:scale(1.05,.96)}45%{transform:scale(.96,1.04)}70%{transform:scale(1.03,.98)}}")
cracks = [f"M{UX-20} {UY-UR+6} L{UX-6} {UY-80} L{UX-40} {UY-40} L{UX-12} {UY+10}",
          f"M{UX+UR-8} {UY-30} L{UX+90} {UY-18} L{UX+70} {UY+28} L{UX+30} {UY+40}",
          f"M{UX-UR+14} {UY+60} L{UX-90} {UY+52} L{UX-70} {UY+96}"]
for k, d in enumerate(cracks):
    el.append(f'<path class="ck" d="{d}" pathLength="1" fill="none" stroke="{TXT}" stroke-width="5" stroke-linejoin="round" '
              f'style="animation-delay:{s2+0.15+k*0.18:.2f}s"/>')
css.append(".ck{stroke-dasharray:1;stroke-dashoffset:1;animation:ck .35s ease-out both}@keyframes ck{to{stroke-dashoffset:0}}")
el.append(f'<g class="qm" style="transform-origin:{UX}px {UY-UR-10}px"><circle cx="{UX+UR*.75}" cy="{UY-UR*.8}" r="48" fill="{AMB}" stroke="{INK}" stroke-width="5"/>'
          f'<text x="{UX+UR*.75}" y="{UY-UR*.8+24}" text-anchor="middle" style="font:900 68px Inter,Arial;fill:{INK}">?</text></g>')
css.append(f".qm{{opacity:0;animation:popt .45s cubic-bezier(.2,.9,.3,1.4) both;animation-delay:{s2+0.6:.2f}s}}")

# counter -$0B -> -$480B on "Four hundred and eighty billion dollars, gone"
el.append(f'<text class="lab" x="444" y="62" text-anchor="middle" style="font:800 24px Inter,Arial;letter-spacing:4px;fill:{SOFT}">WIPED OUT · CHINA AI STOCKS</text>')
css.append(f".lab{{opacity:0;animation:fadein .3s ease both;animation-delay:{s1:.2f}s}}@keyframes fadein{{to{{opacity:1}}}}")
c0, c1 = s1 + 0.05, s1 + 1.7
vals = list(range(0, 481, 10))
N = len(vals) - 1
for i, v in enumerate(vals):
    t = c0 + (c1 - c0) * (1 - (1 - i / N) ** 2)
    nxt = c0 + (c1 - c0) * (1 - (1 - (i + 1) / N) ** 2) if i < N else t + .1
    last = i == N
    el.append(f'<text class="cnt{" last" if last else ""}" x="444" y="150" text-anchor="middle" '
              f'style="font:900 96px Inter,Arial;fill:{RED};animation-delay:{t:.3f}s;animation-duration:{max(nxt - t, .001):.3f}s">−${v}B</text>')
css.append(".cnt{opacity:0;animation-name:cnt;animation-timing-function:steps(1);animation-fill-mode:none}"
           "@keyframes cnt{0%,100%{opacity:1}}.cnt.last{animation-fill-mode:forwards}")

svg = (f'<svg viewBox="0 0 888 760" width="888" height="760" aria-label="Animation: China\'s AI bubble pops; America\'s bubble wobbles" '
       f'style="border-radius:20px;background:radial-gradient(circle at 50% 55%,#16233A,#0B0F15 70%);overflow:hidden">{"".join(el)}</svg>')
(V / "scene.svg").write_text(svg, encoding="utf-8")
(V / "scene.css").write_text("\n".join(css), encoding="utf-8")
print("A", A, s0, s1, s2, "pop", pop)
