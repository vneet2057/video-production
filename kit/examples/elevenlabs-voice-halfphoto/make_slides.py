# Trump wants a permanent Iran deal (22 Nov 2026). Calm "half & half" layout: content on top, photo on the bottom half
# of every slide (captions sit over the photo). Subtle motion only: slow Ken Burns, rise/slide reveals timed to the voice.
import json, math
from pathlib import Path
V = Path(__file__).parent
S = json.load(open(V / "work" / "sentences.json"))
ANIMS = json.load(open(V / "work" / "anims.json"))


def at(slide, sent, frac=0.0):
    """Delay (s, from slide start) for sentence `sent` of slide `slide`, plus `frac` of that sentence's length."""
    m = S[slide - 1]
    a, b = m[sent]
    return round(a - m[0][0] + 0.3 + frac * (b - a), 2)


# ---------- Hormuz map (real outlines) for slide 7 ----------
G = json.load(open(next(p / "geo/wgj/countries.geo.json" for p in V.parents if (p / "geo/wgj").is_dir())))
LON0, LON1, LAT0, LAT1 = 47.0, 60.5, 20.6, 32.0
MW, MH = 1080, 1020
K = MW / ((LON1 - LON0) * math.cos(math.radians(26)))


def xy(lon, lat):
    return ((lon - LON0) * math.cos(math.radians(26)) * K, (LAT1 - lat) * K)


def ring(r):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in (xy(lo, la) for lo, la in r)) + " Z"


land = []
for f in G["features"]:
    g = f["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    d = " ".join(ring(p[0]) for p in polys)
    fill = "#3A2A22" if f["id"] == "IRN" else "#2A313B"
    land.append(f'<path d="{d}" fill="{fill}" stroke="#55606E" stroke-width="2"/>')
route = [(49.6, 28.6), (52.0, 27.0), (54.6, 26.3), (56.0, 26.55), (56.6, 26.3), (57.3, 25.5), (59.0, 24.6), (61.0, 23.8)]
rd = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in (xy(*p) for p in route))
hx, hy = xy(56.35, 26.45)
labs = [("IRAN", 53.2, 30.2, 46), ("SAUDI ARABIA", 48.6, 23.6, 30), ("UAE", 54.0, 23.4, 30), ("OMAN", 57.6, 22.4, 30), ("QATAR", 51.25, 24.6, 22), ("KUWAIT", 47.6, 29.5, 22)]
labels = "".join(f'<text x="{xy(lo, la)[0]:.0f}" y="{xy(lo, la)[1]:.0f}" font-size="{fs}" fill="#8B95A5" font-weight="800" letter-spacing="3" font-family="Inter">{t}</text>' for t, lo, la, fs in labs)
ships = "".join(f'<g class="ship" style="animation-delay:-{d}s"><rect x="-16" y="-7" width="32" height="14" rx="7" fill="#F2B04E"/></g>' for d in (0, 1.7, 3.4, 5.1))
MAP = f"""<svg viewBox="0 0 {MW} {MH}" width="{MW}" height="{MH}" style="background:#16314A">
{''.join(land)}{labels}
<path d="{rd}" fill="none" stroke="#F2B04E" stroke-width="4" stroke-dasharray="14 12" opacity=".7"/>
<circle cx="{hx:.0f}" cy="{hy:.0f}" r="60" fill="none" stroke="#F2B04E" stroke-width="5" class="pulse"/>
<text x="{hx - 340:.0f}" y="{hy - 95:.0f}" font-size="36" font-weight="900" fill="#F2EEE6" font-family="Inter" letter-spacing="2">STRAIT OF HORMUZ</text>
{ships}
</svg>"""
ROUTE_CSS = f".ship{{offset-path:path('{rd}');offset-rotate:auto;animation:sail 6.8s linear infinite}}"

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#000;font-family:'Inter',Arial,sans-serif;width:1080px;height:1920px;overflow:hidden}
.s{display:none;width:1080px;height:1920px;padding:110px 84px 1010px;flex-direction:column;justify-content:center;gap:36px;overflow:hidden;position:relative}
.s.on{display:flex}
.dark{background:#11151B;color:#F2EEE6;--bg:17,21,27}
.light{background:#F2EEE6;color:#11151B;--bg:242,238,230}
.amber{background:#E39B2D;color:#11151B;--bg:227,155,45}
.eyebrow{font-size:30px;font-weight:700;letter-spacing:4px;text-transform:uppercase;color:#A8620C}
.dark .eyebrow{color:#F2B04E}.amber .eyebrow{color:#11151B}
.part{display:inline-block;font-size:30px;font-weight:800;letter-spacing:3px;text-transform:uppercase;background:#F2B04E;color:#11151B;padding:12px 22px;border-radius:10px}
h1{font-weight:900;font-size:100px;line-height:1.02;letter-spacing:-2px}
h2{font-weight:900;font-size:88px;line-height:1.05;letter-spacing:-1.5px}
h3{font-size:46px;font-weight:800;line-height:1.2}
p{font-size:44px;line-height:1.3}
.lead{font-size:50px;line-height:1.2;font-weight:800}
.soft{color:#505866}.dark .soft{color:#B5BDC9}.amber .soft{color:#3A3020}
.hl{color:#F2B04E}.light .hl{color:#A8620C}
.red{color:#E25D4B}.light .red{color:#C2412F}
.head{display:flex;flex-direction:column;gap:18px}
.card{background:#1C222B;border-radius:18px;padding:26px 34px;display:flex;flex-direction:column;gap:8px;border-left:6px solid #F2B04E}
.light .card{background:#FFFFFF;border-left-color:#A8620C}
.card.ok{border-left-color:#6FCF8E}.card.no{border-left-color:#E25D4B}
/* photo half */
.ph{position:absolute;left:0;top:900px;width:1080px;height:1020px;overflow:hidden}
.ph img{width:100%;height:100%;object-fit:cover;animation:kb var(--kb,5s) linear both;transform-origin:var(--o,50% 30%)}
.ph::before{content:"";position:absolute;left:0;right:0;top:0;height:120px;z-index:1;background:linear-gradient(rgb(var(--bg)),rgba(var(--bg),0))}
.ph::after{content:"";position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.45))}
@keyframes kb{from{transform:scale(1.0)}to{transform:scale(1.08)}}
.ph.pan img{animation-name:pan}
@keyframes pan{from{transform:scale(1.1) translateX(-24px)}to{transform:scale(1.1) translateX(24px)}}
.label{position:absolute;left:24px;top:110px;z-index:2;font-size:24px;font-weight:600;color:#fff;background:rgba(0,0,0,.68);padding:8px 14px;border-radius:6px}
.name{position:absolute;z-index:2;font-size:30px;font-weight:800;color:#11151B;background:#F2B04E;padding:8px 16px;border-radius:8px}
/* rows */
.rows{display:flex;flex-direction:column;gap:20px}
.row{display:grid;grid-template-columns:72px 1fr;align-items:center;gap:22px;font-size:46px;font-weight:800;line-height:1.15}
.row b{display:flex;align-items:center;justify-content:center;width:72px;height:72px;border-radius:50%;font-size:36px;color:#11151B;background:#F2B04E}
.light .row b{background:#11151B;color:#F2B04E}
.row.no b{background:#E25D4B;color:#fff}.row.ok b{background:#6FCF8E}
/* timeline */
.tl{position:relative;display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding-top:44px}
.tl::before{content:"";position:absolute;left:40px;right:40px;top:18px;height:6px;background:#11151B;border-radius:3px;transform-origin:left;animation:grow 1.2s ease-out both;animation-delay:.4s}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.ev{position:relative;text-align:center}
.ev::before{content:"";position:absolute;left:50%;top:-38px;width:26px;height:26px;margin-left:-13px;border-radius:50%;background:#A8620C}
.ev.r::before{background:#C2412F}
.ev b{display:block;font-size:56px;font-weight:900;color:#A8620C}
.ev.r b{color:#C2412F}
.ev span{display:block;font-size:30px;font-weight:700;line-height:1.2}
/* quote */
.quote{font-family:'Charter','Bitstream Charter',Georgia,serif;font-size:78px;line-height:1.12}
/* counter */
.big{font-weight:900;font-size:190px;line-height:.9;letter-spacing:-6px;color:#F2B04E}
/* flags */
.qa{display:inline-block;width:120px;height:72px;border-radius:8px;vertical-align:middle;margin-right:18px;background:linear-gradient(90deg,#fff 0 30%,#8A1538 30%);position:relative;overflow:hidden}
.qa::before{content:"";position:absolute;left:24%;top:0;bottom:0;width:14px;background:repeating-linear-gradient(135deg,#fff 0 6px,#8A1538 6px 12px)}
/* split */
.split{position:absolute;left:0;top:900px;width:1080px;height:1020px;display:grid;grid-template-columns:1fr 1fr;gap:8px;overflow:hidden}
.split div{position:relative;overflow:hidden}
.split img{width:100%;height:100%;object-fit:cover;animation:kb 5.6s linear both}
.split .tag{position:absolute;left:0;right:0;top:120px;text-align:center;font-size:64px;font-weight:900;letter-spacing:2px;color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.8)}
/* map */
.pulse{transform-box:fill-box;transform-origin:center;animation:pl 1.6s ease-out infinite}
@keyframes pl{0%{opacity:1;transform:scale(.6)}100%{opacity:0;transform:scale(1.6)}}
@keyframes sail{from{offset-distance:0%}to{offset-distance:100%}}
/* reveals (gentle) */
.a{animation:rise .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}
.x{animation:slide .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}
.z{animation:zoom .5s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,.3s)}
@keyframes rise{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:none}}
@keyframes slide{from{opacity:0;transform:translateX(-50px)}to{opacity:1;transform:none}}
@keyframes zoom{from{opacity:0;transform:scale(.85)}to{opacity:1;transform:none}}
"""


def ph(img, label, i, o="50% 30%", pan=False, extra=""):
    return (f'<div class="ph{" pan" if pan else ""}" style="--kb:{ANIMS[i - 1] + 0.6}s;--o:{o}">'
            f'<img src="{img}" style="object-position:{o}"><span class="label">{label}</span>{extra}</div>')


BODY = f"""
<!-- 1 HOOK: headline + photo visible at frame 0 -->
<div class="s dark" id="s1">
<div><p class="part">Iran · United States</p></div>
<h1>Trump wants a <span class="hl">permanent</span> Iran deal</h1>
<p class="lead x" style="--d:{at(1,1)}s">But Iran is <span class="red">still firing</span> at American bases.</p>
{ph("in/trump-closeup.png", "Donald Trump · file photo", 1, "55% 30%")}
</div>

<!-- 2 FOX NEWS -->
<div class="s light" id="s2">
<div class="head"><p class="eyebrow a" style="--d:.1s">Fox News interview · Saturday</p><h2 class="a" style="--d:.2s">"No future president..."</h2></div>
<div class="card x" style="--d:{at(2,0,.45)}s"><h3>should be able to let Iran</h3><p class="soft" style="font-weight:700">get a nuclear weapon ☢</p></div>
{ph("in/trump-podium.png", "Donald Trump · file photo", 2, "40% 30%", pan=True)}
</div>

<!-- 3 QUOTE -->
<div class="s dark" id="s3">
<div class="head"><p class="eyebrow a" style="--d:.1s">His reason</p></div>
<p class="quote z" style="--d:.25s">"We make a deal, and then they <span class="hl">break the deal</span> the next day."</p>
<p class="soft a" style="--d:.6s;font-size:32px;font-weight:600">Donald Trump, to Fox News</p>
{ph("in/trump-closeup.png", "Donald Trump · file photo", 3, "50% 45%")}
</div>

<!-- 4 WHY PERMANENT -->
<div class="s light" id="s4">
<div class="head"><p class="eyebrow a" style="--d:.1s">Why "permanent"?</p><h2 class="a" style="--d:.2s">A deal can be cancelled</h2></div>
<p class="soft a" style="--d:{at(4,0,.4)}s;font-weight:700">...by the next president.</p>
<div class="tl">
<div class="ev a" style="--d:{at(4,1,.1)}s"><b>2015</b><span>Obama-era<br>nuclear deal</span></div>
<div class="ev r a" style="--d:{at(4,1,.35)}s"><b>2018</b><span>Trump pulls<br>America out</span></div>
<div class="ev a" style="--d:{at(4,1,.85)}s"><b>2026</b><span>"Permanent"<br>deal?</span></div>
</div>
{ph("in/trump-signing.png", "Trump signing orders · file photo", 4, "50% 25%")}
</div>

<!-- 5 IRAN'S SIDE -->
<div class="s dark" id="s5">
<div class="head"><p class="eyebrow a" style="--d:.1s">Iran's side</p><h2 class="a" style="--d:.2s">Iran has its own terms</h2></div>
<div class="card x" style="--d:{at(5,1)}s"><h3>Reopening Hormuz is</h3><p class="lead hl">"not difficult"</p></div>
{ph("in/araghchi.png", "Abbas Araghchi · Iran's foreign minister · file photo", 5, "45% 30%")}
</div>

<!-- 6 THE TERMS -->
<div class="s light" id="s6">
<div class="head"><p class="eyebrow a" style="--d:.1s">But first, America must:</p></div>
<div class="rows">
<div class="row x" style="--d:{at(6,0,.22)}s"><b>1</b>End the naval blockade</div>
<div class="row x" style="--d:{at(6,0,.52)}s"><b>2</b>Lift sanctions</div>
<div class="row x" style="--d:{at(6,0,.7)}s"><b>3</b>Free Iran's frozen money</div>
</div>
<div class="card z" style="--d:{at(6,1)}s"><h3>Then, Iran says:</h3><p class="soft" style="font-weight:700">the strait could reopen the next day</p></div>
{ph("in/tanker.png", "Oil tanker · illustrative", 6, "50% 50%")}
</div>

<!-- 7 WHY HORMUZ MATTERS -->
<div class="s dark" id="s7">
<div class="head"><p class="eyebrow a" style="--d:.1s">Why it matters</p></div>
<div style="display:flex;align-items:flex-end;gap:26px"><p class="big z" style="--d:.3s">1 in 5</p></div>
<p class="lead a" style="--d:.7s">barrels of the world's oil<br><span class="soft" style="font-size:38px;font-weight:600">normally sail through this strait</span></p>
<div class="ph" style="--bg:17,21,27">{MAP}<span class="label">Map · Strait of Hormuz</span></div>
</div>

<!-- 8 THE FIGHTING -->
<div class="s dark" id="s8">
<div class="head"><p class="eyebrow a" style="--d:.1s">Meanwhile</p><h2 class="a" style="--d:.2s">The fighting <span class="red">hasn't stopped</span></h2></div>
<div class="rows">
<div class="row no x" style="--d:{at(8,1,.2)}s"><b>!</b>Wednesday: US air base in Kuwait</div>
<div class="row no x" style="--d:{at(8,1,.78)}s"><b>!</b>Targets in Bahrain</div>
<div class="row ok x" style="--d:{at(8,2,.1)}s"><b>✓</b>Kuwait: drones stopped</div>
</div>
{ph("in/kuwait-satellite.png", "Satellite image · file", 8, "50% 50%", pan=True)}
</div>

<!-- 9 MINE -->
<div class="s light" id="s9">
<div class="head"><p class="eyebrow a" style="--d:.1s">Saturday · Strait of Hormuz</p><h2 class="a" style="--d:.2s">A ship hits a mine and <span class="red">catches fire</span></h2></div>
<p class="soft a" style="--d:{at(9,0,.3)}s;font-weight:700">According to Iran's military</p>
{ph("in/tanker-fire.png", "File photo · an earlier tanker attack, not this ship", 9, "35% 50%")}
</div>

<!-- 10 TALKS -->
<div class="s dark" id="s10">
<div class="head"><p class="eyebrow a" style="--d:.1s">The talks</p><h2 class="a" style="--d:.2s">Trump's envoys meet Qatar</h2></div>
<p class="lead x" style="--d:{at(10,0,.55)}s"><span class="qa"></span>Qatar is helping<br><span class="soft" style="font-size:38px;font-weight:600">push the talks with Iran</span></p>
{ph("in/kushner-witkoff.jpg", "File photo", 10, "50% 20%", extra='<span class="name" style="left:120px;top:660px">Jared Kushner</span><span class="name" style="right:190px;top:660px">Steve Witkoff</span>')}
</div>

<!-- 11 CTA -->
<div class="s amber" id="s11">
<div class="head"><p class="eyebrow a" style="--d:.1s">Your view</p><h2 class="a" style="--d:.2s">A deal that lasts forever, or more strikes first?</h2></div>
<div><p class="part z" style="--d:{at(11,2)}s;background:#11151B;color:#F2B04E">Follow for more</p></div>
<p class="soft a" style="--d:1.0s;font-size:24px">Sources: Fox News via Anadolu, AP, Al Jazeera, Dawn, A News, TRT World</p>
<div class="split"><div><img src="in/trump-closeup.png" style="object-position:55% 30%"><p class="tag">DEAL?</p></div><div><img src="in/araghchi.png" style="object-position:42% 30%"><p class="tag">STRIKES?</p></div></div>
</div>
"""
(V / "slides.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{ROUTE_CSS}</style></head><body>{BODY}</body></html>", encoding="utf-8")
print("slides.html written")
