import math
from pathlib import Path

V = Path(__file__).parent
BLUE, RED, GOLD = "#4C8DF6", "#E25D4B", "#E0A546"


def hemicycle(cx, cy, r_in, r_out, rows, total, dot, k0, k1, t0, t1):
    """Seats ordered left (Democrats) to right. Seats < k0 start blue, k0..k1 flip to blue, rest stay red."""
    radii = [r_in + (r_out - r_in) * i / (rows - 1) for i in range(rows)]
    raw = [r / sum(radii) * total for r in radii]
    counts = [int(x) for x in raw]
    for i in sorted(range(rows), key=lambda i: raw[i] - counts[i], reverse=True)[: total - sum(counts)]:
        counts[i] += 1
    seats = []
    for r, n in zip(radii, counts):
        for j in range(n):
            a = math.pi - math.pi * (j + 0.5) / n
            seats.append((a, cx + r * math.cos(a), cy - r * math.sin(a)))
    seats.sort(key=lambda s: -s[0])
    out = []
    for i, (_, x, y) in enumerate(seats):
        if i < k0:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{dot}" fill="{BLUE}"/>')
        elif i < k1:
            d = t0 + (t1 - t0) * (i - k0) / max(1, k1 - k0 - 1)
            out.append(f'<circle class="flip" cx="{x:.1f}" cy="{y:.1f}" r="{dot}" style="--d:{d:.2f}s"/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{dot}" fill="{RED}"/>')
    tick = f'<line x1="{cx}" y1="{cy - r_out - 14}" x2="{cx}" y2="{cy - r_in + 18}" stroke="{GOLD}" stroke-width="4" stroke-dasharray="10 8"/>'
    return "".join(out) + tick


house = hemicycle(444, 450, 175, 420, 11, 435, 9.5, 212, 232, 0.8, 2.2)
senate = hemicycle(444, 790, 150, 255, 5, 100, 11, 47, 53, 1.4, 2.4)
svg = f'''<svg viewBox="0 0 888 840" width="888" height="840" aria-label="Illustration of House and Senate seats flipping">
{house}
<text x="444" y="380" text-anchor="middle" style="font:800 40px Inter;letter-spacing:6px;fill:#F3ECDD">HOUSE</text>
<text x="444" y="425" text-anchor="middle" style="font:600 26px Inter;fill:#B5BDC9">218 to control</text>
{senate}
<text x="444" y="742" text-anchor="middle" style="font:800 32px Inter;letter-spacing:5px;fill:#F3ECDD">SENATE</text>
<text x="444" y="775" text-anchor="middle" style="font:600 24px Inter;fill:#B5BDC9">51 to control</text>
<g class="flipstamp" style="--d:2.55s"><rect x="339" y="466" width="210" height="58" rx="10" fill="#0F1B2D" stroke="{BLUE}" stroke-width="5"/><text x="444" y="506" text-anchor="middle" style="font:900 34px Inter;letter-spacing:4px;fill:{BLUE}">FLIPPED</text></g>
<g class="flipstamp" style="--d:2.8s"><rect x="706" y="734" width="176" height="52" rx="10" fill="#0F1B2D" stroke="{BLUE}" stroke-width="5"/><text x="794" y="770" text-anchor="middle" style="font:900 29px Inter;letter-spacing:4px;fill:{BLUE}">FLIPPED</text></g>
<g style="font:700 24px Inter"><circle cx="40" cy="826" r="10" fill="{BLUE}"/><text x="58" y="834" style="fill:#F3ECDD">Democrats</text><circle cx="230" cy="826" r="10" fill="{RED}"/><text x="248" y="834" style="fill:#F3ECDD">Republicans</text></g>
</svg>'''

css = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#000;font-family:'Inter',Arial,sans-serif;width:1080px;height:1920px;overflow:hidden}}
.s{{display:none;width:1080px;height:1920px;padding:130px 96px 120px;flex-direction:column;justify-content:flex-start;gap:70px;overflow:hidden;position:relative}}
.s.on{{display:flex}}
.dark{{background:#0F1B2D;color:#F3ECDD}}
.light{{background:#F3ECDD;color:#0F1B2D}}
.gold{{background:{GOLD};color:#0F1B2D}}
.eyebrow{{font-size:28px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:#9A6418}}
.dark .eyebrow{{color:{GOLD}}}.gold .eyebrow{{color:#0F1B2D}}
.part{{display:inline-block;font-size:30px;font-weight:800;letter-spacing:3px;text-transform:uppercase;background:{GOLD};color:#0F1B2D;padding:12px 22px;border-radius:10px}}
h1{{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:104px;line-height:1.02;letter-spacing:-2px}}
h2{{font-family:'Inter Display','Inter',sans-serif;font-weight:700;font-size:80px;line-height:1.08;letter-spacing:-1px}}
h3{{font-size:40px;font-weight:700;line-height:1.2}}
p{{font-size:38px;line-height:1.38}}
.lead{{font-size:50px;line-height:1.3}}
.soft{{color:#4E5868}}.dark .soft{{color:#B5BDC9}}.gold .soft{{color:#3A3020}}
.small{{font-size:27px}}
.hl{{color:{GOLD}}}.light .hl{{color:#9A6418}}
.head{{display:flex;flex-direction:column;gap:24px}}
.stack{{display:flex;flex-direction:column;gap:24px}}
.vs{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}
.card{{background:#1A2940;border-radius:20px;padding:34px 38px;display:flex;flex-direction:column;gap:12px;border-left:6px solid {GOLD}}}
.light .card{{background:#FFFFFF;border-left-color:#9A6418}}
.gold .card{{background:#F1C982;border-left-color:#0F1B2D}}
.flag{{font-size:28px;font-weight:800;letter-spacing:2px;text-transform:uppercase}}
.stats{{display:grid;grid-template-columns:1fr 1fr;gap:40px}}
.stat .n{{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:140px;line-height:1;letter-spacing:-3px;color:#9A6418}}
.stat .l{{font-size:32px;line-height:1.3}}
.dark .stat .n{{color:{GOLD}}}
.light .card .flag{{color:#0F1B2D}}
.tl{{position:relative;display:flex;flex-direction:column;gap:40px;padding-left:64px}}
.tl .line{{position:absolute;left:11px;top:14px;bottom:14px;width:4px;background:{GOLD};transform-origin:top;animation:grow 2s cubic-bezier(.3,.6,.2,1) both;animation-delay:.4s}}
.ev{{position:relative;display:flex;flex-direction:column;gap:6px}}
.ev::before{{content:"";position:absolute;left:-64px;top:8px;width:26px;height:26px;border-radius:50%;background:{GOLD}}}
.ev b{{font-size:32px;font-weight:700;letter-spacing:1px;color:{GOLD}}}
.light .ev b{{color:#9A6418}}.light .ev::before{{background:#9A6418}}.light .tl .line{{background:#9A6418}}
.ev span{{font-size:38px;line-height:1.3}}
.a{{animation:rise .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}}
.z{{animation:zoom .6s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,.3s)}}
.x{{animation:slide .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}}
.stamp{{animation:stamp .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:var(--d,1s)}}
.flip{{fill:{RED};animation:flip .35s ease both;animation-delay:var(--d)}}
.flipstamp{{animation:pop .45s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:var(--d);transform-box:fill-box;transform-origin:center}}
@keyframes flip{{to{{fill:{BLUE}}}}}
@keyframes pop{{from{{opacity:0;transform:scale(1.8) rotate(-8deg)}}to{{opacity:1;transform:rotate(-4deg)}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
@keyframes zoom{{from{{opacity:0;transform:scale(.8)}}to{{opacity:1;transform:none}}}}
@keyframes slide{{from{{opacity:0;transform:translateX(-60px)}}to{{opacity:1;transform:none}}}}
@keyframes stamp{{from{{opacity:0;transform:scale(1.8) rotate(-8deg)}}to{{opacity:1;transform:rotate(-4deg)}}}}
@keyframes grow{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
"""

body = f"""
<div class="s dark" id="s1" style="gap:34px">
<div><p class="part">US Vote · 2026</p></div>
<h1>Trump's party just <span class="hl">lost Congress.</span></h1>
{svg}
<p class="small soft">Illustration · final seat counts still coming · 4 November 2026</p>
</div>

<div class="s light" id="s2">
<div class="head"><p class="eyebrow a" style="--d:.2s">Who's who</p><h2 class="a" style="--d:.3s">Congress makes the laws</h2></div>
<div class="card x" style="--d:.5s"><p class="flag">Congress</p><p class="soft">America's lawmaking body. Writes the laws and controls the budget.</p></div>
<div class="vs">
<div class="card x" style="--d:.8s;border-left-color:{RED}"><p class="flag" style="color:#C2412F">Republicans</p><p class="soft">Trump's party. Usually more conservative.</p></div>
<div class="card x" style="--d:1.1s;border-left-color:{BLUE}"><p class="flag" style="color:#2F6FD8">Democrats</p><p class="soft">The other side. Usually more liberal.</p></div>
</div>
</div>

<div class="s dark" id="s3">
<div class="head"><p class="eyebrow a" style="--d:.2s">Explainer</p><h2 class="a" style="--d:.3s">Congress has two houses</h2></div>
<div class="stats">
<div class="stat a" style="--d:.5s"><p class="n">435</p><p class="l"><b>House</b> seats</p><p class="l soft">218 to control</p></div>
<div class="stat a" style="--d:.8s"><p class="n">100</p><p class="l"><b>Senate</b> seats</p><p class="l soft">51 to control</p></div>
</div>
<p class="small soft a" style="--d:1.1s">On the ballot: all 435 House seats and 35 Senate seats</p>
</div>

<div class="s light" id="s4">
<div class="head"><p class="eyebrow a" style="--d:.2s">What changed</p><h2 class="a" style="--d:.3s">Both houses flip</h2></div>
<div class="tl"><div class="line"></div>
<div class="ev x" style="--d:.5s"><b>Before the vote</b><span>Republicans held both, narrowly</span></div>
<div class="ev x" style="--d:.8s"><b>3 November</b><span>Democrats win both, networks project</span></div>
<div class="ev x" style="--d:1.1s"><b>3 January</b><span>The new Congress takes over</span></div>
</div>
</div>

<div class="s dark" id="s5">
<div class="head"><p class="eyebrow a" style="--d:.2s">What it means for Trump</p><h2 class="a" style="--d:.3s">Congress holds the money</h2></div>
<div class="vs">
<div class="card x" style="--d:.5s"><p class="flag">Block</p><p class="soft">Budget plans and new laws</p></div>
<div class="card x" style="--d:.7s"><p class="flag">Investigate</p><p class="soft">Hearings into his government</p></div>
<div class="card x" style="--d:.9s"><p class="flag">Iran war</p><p class="soft">Can try to limit it</p></div>
<div class="card x" style="--d:1.1s;border-left-color:#C2412F"><p class="flag">But</p><p class="soft">Trump can veto. Override needs two-thirds</p></div>
</div>
</div>

<div class="s light" id="s6">
<div class="head"><p class="eyebrow a" style="--d:.2s">The world reacts</p><h2 class="a" style="--d:.3s">All eyes on Washington</h2></div>
<div class="vs">
<div class="card x" style="--d:.5s"><p class="flag">Iran's speaker</p><p class="soft">"Americans said no to war"</p></div>
<div class="card x" style="--d:.8s"><p class="flag">Iran's leader</p><p class="soft">Hopes of a US shift are "mistaken"</p></div>
</div>
<div class="card x" style="--d:1.1s"><p class="flag">Poland's Tusk</p><p class="soft">"Democracy won in America"</p></div>
</div>

<div class="s gold" id="s7">
<div class="head"><p class="eyebrow a" style="--d:.2s">What's next</p><h2 class="a" style="--d:.3s">Two years of split power</h2></div>
<p class="lead a" style="--d:.6s">Some races are still being counted. A Republican president, a Democratic Congress.</p>
<div class="stack" style="gap:30px;align-items:flex-start"><p class="part stamp" style="--d:1.1s;background:#0F1B2D;color:{GOLD}">Let's see what happens</p><p class="part stamp" style="--d:1.5s;background:#0F1B2D;color:{GOLD};font-size:40px">Follow for more</p></div>
<p class="small soft a" style="--d:1.8s">Sources: NPR, CNN, NBC News via Sky, Al Jazeera, ABC News, Reuters, Euronews</p>
</div>
"""
(V / "slides.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>', encoding="utf-8")
print("ok")
