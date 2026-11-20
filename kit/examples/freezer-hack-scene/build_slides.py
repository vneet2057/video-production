from pathlib import Path

V = Path(__file__).parent
DARK, LIGHT, RED, RED2, CYAN = "#0B1020", "#EEF1F6", "#C8323A", "#FF6B70", "#3DD6F5"

# ---------- hook: freezer heating up ----------
temps = [("-18", 0.0, 0.9, CYAN), ("-6", 0.9, 1.25, CYAN), ("9", 1.25, 1.6, "#F2B04E"),
         ("24", 1.6, 1.95, "#F2B04E"), ("37", 1.95, 2.3, RED2), ("50", 2.3, None, RED2)]
nums = []
for t, a, b, c in temps:
    if a == 0:
        cls, st = "hide", f"--d:{b}s"
    elif b is None:
        cls, st = "appear", f"--d:{a}s"
    else:
        cls, st = "blink", f"--d:{a}s;--len:{b - a:.2f}s"
    nums.append(f'<text class="{cls}" style="{st};font:900 120px Inter;fill:{c}" x="444" y="150" text-anchor="middle">{t}°C</text>')

items = []
cols = ["#E8EEF6", "#9CC8E8", "#F2B04E", "#C8D6E6", "#7FB0D8", "#E6A0A0"]
for door in range(3):
    x0 = 88 + door * 240
    for row in range(4):
        for k in range(3):
            items.append(f'<rect x="{x0 + 22 + k * 66}" y="{300 + row * 110}" width="54" height="80" rx="8" fill="{cols[(door + row + k) % 6]}" opacity=".9"/>')

hook_svg = f'''<svg viewBox="0 0 888 840" width="888" height="840" aria-label="Illustration of a freezer heating up">
<rect x="244" y="20" width="400" height="170" rx="22" fill="#05070D" stroke="#2A3550" stroke-width="4"/>
<text x="444" y="56" text-anchor="middle" style="font:700 22px Inter;letter-spacing:5px;fill:#6E7A94">FREEZER TEMP</text>
{''.join(nums)}
<rect x="70" y="230" width="748" height="560" rx="26" fill="#1A2238" stroke="#3A4766" stroke-width="6"/>
<rect class="inside" x="88" y="248" width="712" height="524" rx="14"/>
{''.join(items)}
<line x1="328" y1="248" x2="328" y2="772" stroke="#3A4766" stroke-width="8"/>
<line x1="568" y1="248" x2="568" y2="772" stroke="#3A4766" stroke-width="8"/>
<rect class="frost" x="88" y="248" width="712" height="524" rx="14" fill="url(#fr)"/>
<defs><linearGradient id="fr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#DDF6FF" stop-opacity=".55"/><stop offset=".5" stop-color="#DDF6FF" stop-opacity=".1"/><stop offset="1" stop-color="#DDF6FF" stop-opacity=".45"/></linearGradient></defs>
<g class="heat" style="--d:2.2s" stroke="{RED2}" stroke-width="7" fill="none" stroke-linecap="round">
<path d="M250 300 q20 30 0 60 q-20 30 0 60"/><path d="M444 280 q20 30 0 60 q-20 30 0 60"/><path d="M638 300 q20 30 0 60 q-20 30 0 60"/></g>
<g class="stampg" style="--d:2.6s"><rect x="264" y="440" width="360" height="110" rx="16" fill="{DARK}" stroke="{RED2}" stroke-width="8"/>
<text x="444" y="518" text-anchor="middle" style="font:900 72px Inter;letter-spacing:10px;fill:{RED2}">HACKED</text></g>
<text x="444" y="830" text-anchor="middle" style="font:600 22px Inter;fill:#6E7A94">Illustration</text>
</svg>'''

# ---------- how: control panel diagram ----------
fr = "".join(f'<g><rect x="20" y="{30 + i * 110}" width="120" height="90" rx="12" fill="#1A2238" stroke="{CYAN}" stroke-width="4"/>'
             f'<text x="80" y="{84 + i * 110}" text-anchor="middle" style="font:700 22px Inter;fill:{LIGHT}">Fridge</text>'
             f'<line class="wire" pathLength="1" x1="140" y1="{75 + i * 110}" x2="300" y2="185" stroke="{CYAN}" stroke-width="4" style="--d:{.5 + i * .15}s"/></g>'
             for i in range(3))
how_svg = f'''<svg viewBox="0 0 888 380" width="888" height="380" aria-label="Diagram of how supermarket fridges connect to the internet">
{fr}
<g class="pop" style="--d:.9s"><rect x="300" y="125" width="200" height="120" rx="16" fill="#1A2238" stroke="#F2B04E" stroke-width="5"/>
<text x="400" y="178" text-anchor="middle" style="font:800 26px Inter;fill:{LIGHT}">Control</text><text x="400" y="212" text-anchor="middle" style="font:800 26px Inter;fill:{LIGHT}">panel</text></g>
<line class="wire" pathLength="1" x1="500" y1="185" x2="610" y2="185" stroke="#F2B04E" stroke-width="5" style="--d:1.2s"/>
<g class="pop" style="--d:1.4s"><path d="M625 215 q-30 0 -30 -30 q0 -30 32 -30 q10 -32 48 -28 q30 -26 62 0 q40 -4 44 32 q30 6 26 32 q-2 26 -32 24 z" fill="#1A2238" stroke="{LIGHT}" stroke-width="4"/>
<text x="690" y="198" text-anchor="middle" style="font:800 26px Inter;fill:{LIGHT}">Internet</text></g>
<line class="wire" pathLength="1" x1="690" y1="230" x2="600" y2="300" stroke="#5BD69A" stroke-width="4" style="--d:1.7s"/>
<g class="pop" style="--d:1.8s"><rect x="470" y="300" width="230" height="66" rx="12" fill="#12301F" stroke="#5BD69A" stroke-width="4"/><text x="585" y="342" text-anchor="middle" style="font:700 24px Inter;fill:#5BD69A">Repair company</text></g>
<line class="wire dash" pathLength="1" x1="720" y1="230" x2="790" y2="300" stroke="{RED2}" stroke-width="5" style="--d:2.4s"/>
<g class="pop" style="--d:2.6s"><rect x="720" y="300" width="160" height="66" rx="12" fill="#3A1218" stroke="{RED2}" stroke-width="5"/><text x="800" y="342" text-anchor="middle" style="font:800 26px Inter;fill:{RED2}">Hacker</text></g>
</svg>'''

# ---------- trick: defrost bars ----------
trick_svg = f'''<svg viewBox="0 0 888 330" width="888" height="330" aria-label="Normal defrost cycle versus hacked defrost cycle">
<text x="0" y="40" style="font:800 30px Inter;letter-spacing:2px;fill:#4E5868">NORMAL DEFROST</text>
<rect class="bar" x="0" y="60" width="110" height="64" rx="10" fill="#2AA9C9" style="--d:.5s"/>
<text x="130" y="104" style="font:800 36px Inter;fill:#0B1020">short, overnight</text>
<text x="0" y="200" style="font:800 30px Inter;letter-spacing:2px;fill:{RED}">HACKED</text>
<rect class="bar" x="0" y="220" width="888" height="64" rx="10" fill="{RED}" style="--d:1.0s;animation-duration:1.4s"/>
<text class="pop" x="440" y="264" text-anchor="middle" style="--d:2.2s;font:900 36px Inter;fill:#fff">stretched by hours · no alarm</text>
<text x="0" y="322" style="font:600 22px Inter;fill:#6E7A94">Illustration · early findings, not yet confirmed</text>
</svg>'''

css = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#000;font-family:'Inter',Arial,sans-serif;width:1080px;height:1920px;overflow:hidden}}
.s{{display:none;width:1080px;height:1920px;padding:130px 96px 120px;flex-direction:column;justify-content:flex-start;gap:64px;overflow:hidden;position:relative}}
.s.on{{display:flex}}
.dark{{background:{DARK};color:{LIGHT}}}
.light{{background:{LIGHT};color:{DARK}}}
.redbg{{background:{RED};color:#fff}}
.eyebrow{{font-size:28px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{RED}}}
.dark .eyebrow{{color:{CYAN}}}.redbg .eyebrow{{color:#FFD9DB}}
.part{{display:inline-block;font-size:30px;font-weight:800;letter-spacing:3px;text-transform:uppercase;background:{RED};color:#fff;padding:12px 22px;border-radius:10px}}
h1{{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:108px;line-height:1.02;letter-spacing:-2px}}
h2{{font-family:'Inter Display','Inter',sans-serif;font-weight:700;font-size:80px;line-height:1.08;letter-spacing:-1px}}
p{{font-size:38px;line-height:1.38}}
.lead{{font-size:50px;line-height:1.3}}
.soft{{color:#4E5868}}.dark .soft{{color:#AEB8CC}}.redbg .soft{{color:#FFE3E4}}
.small{{font-size:27px}}
.hl{{color:{RED2}}}.light .hl{{color:{RED}}}
.head{{display:flex;flex-direction:column;gap:24px}}
.stack{{display:flex;flex-direction:column;gap:24px}}
.vs{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}
.card{{background:#161E33;border-radius:20px;padding:34px 38px;display:flex;flex-direction:column;gap:12px;border-left:6px solid {CYAN}}}
.light .card{{background:#FFFFFF;border-left-color:{RED}}}
.redbg .card{{background:#A8262D;border-left-color:#fff}}
.flag{{font-size:28px;font-weight:800;letter-spacing:2px;text-transform:uppercase}}
.stats{{display:grid;grid-template-columns:1fr 1fr;gap:40px}}
.stat .n{{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:120px;line-height:1;letter-spacing:-3px;color:{RED}}}
.dark .stat .n{{color:{RED2}}}
.stat .l{{font-size:32px;line-height:1.3}}
.a{{animation:rise .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}}
.x{{animation:slide .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}}
.stamp{{animation:stamp .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:var(--d,1s)}}
.hide{{animation:hide .01s steps(1) forwards;animation-delay:var(--d)}}
.blink{{opacity:0;animation:blink var(--len) steps(1,end) forwards;animation-delay:var(--d)}}
.appear{{opacity:0;animation:appear .01s forwards;animation-delay:var(--d)}}
.inside{{fill:#16324A;animation:hot 1.6s ease-in both;animation-delay:.8s}}
.frost{{animation:fade 1.2s ease both;animation-delay:.9s}}
.heat{{opacity:0;animation:heat .9s ease-in-out both;animation-delay:var(--d)}}
.stampg,.pop{{animation:pop .45s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:var(--d);transform-box:fill-box;transform-origin:center}}
.wire{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw .5s ease-out both;animation-delay:var(--d)}}
.bar{{transform-box:fill-box;transform-origin:left;animation:barg .7s cubic-bezier(.3,.6,.2,1) both;animation-delay:var(--d)}}
@keyframes hide{{to{{opacity:0}}}}
@keyframes blink{{0%{{opacity:1}}100%{{opacity:0}}}}
@keyframes appear{{to{{opacity:1}}}}
@keyframes hot{{to{{fill:#7A2A1C}}}}
@keyframes fade{{to{{opacity:0}}}}
@keyframes heat{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:none}}}}
@keyframes pop{{from{{opacity:0;transform:scale(1.6) rotate(-6deg)}}to{{opacity:1;transform:rotate(0)}}}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes barg{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
@keyframes slide{{from{{opacity:0;transform:translateX(-60px)}}to{{opacity:1;transform:none}}}}
@keyframes stamp{{from{{opacity:0;transform:scale(1.8) rotate(-8deg)}}to{{opacity:1;transform:rotate(-4deg)}}}}
"""

body = f"""
<div class="s dark" id="s1" style="gap:40px">
<div><p class="part">Cyber attack</p></div>
<h1>Hackers turned freezers <span class="hl">into ovens.</span></h1>
{hook_svg}
</div>

<div class="s light" id="s2">
<div class="head"><p class="eyebrow a" style="--d:.2s">France · October</p><h2 class="a" style="--d:.3s">Hundreds of supermarkets hit</h2></div>
<div class="stats">
<div class="stat a" style="--d:.5s"><p class="n">50°C</p><p class="l soft">freezers heated overnight. Some stores reported hotter</p></div>
<div class="stat a" style="--d:.8s"><p class="n">€€€</p><p class="l soft">millions of euros of food thrown away</p></div>
</div>
<div class="card x" style="--d:1.1s"><p class="flag">Chains hit</p><p class="soft">Carrefour, Intermarché, E.Leclerc, Monoprix, Coopérative U. Some stores caught fire.</p></div>
<p class="small soft a" style="--d:1.4s">Sources differ on the exact number of stores</p>
</div>

<div class="s dark" id="s3" style="gap:56px">
<div class="head"><p class="eyebrow a" style="--d:.2s">How it happened</p><h2 class="a" style="--d:.3s">One panel, online</h2></div>
{how_svg}
<div class="vs">
<div class="card x" style="--d:2.0s;border-left-color:{RED2}"><p class="flag">Old software</p><p class="soft">Known flaws, not updated</p></div>
<div class="card x" style="--d:2.3s;border-left-color:{RED2}"><p class="flag">Default password</p><p class="soft">Some never changed it</p></div>
</div>
</div>

<div class="s light" id="s4">
<div class="head"><p class="eyebrow a" style="--d:.2s">The trick</p><h2 class="a" style="--d:.3s">Defrost mode, no alarm</h2></div>
{trick_svg}
<div class="card x" style="--d:2.4s"><p class="flag">Found in the morning</p><p class="soft">Staff only noticed when they came in to restock</p></div>
</div>

<div class="s dark" id="s5">
<div class="head"><p class="eyebrow a" style="--d:.2s">United States · August</p><h2 class="a" style="--d:.3s">Military base stores too</h2></div>
<div class="card x" style="--d:.5s"><p class="flag">Several base stores</p><p class="soft">Freezers went into defrost mode overnight. Food spoiled.</p></div>
<div class="card x" style="--d:.8s"><p class="flag">The Pentagon</p><p class="soft">Treating it as a suspected hack. Working with France.</p></div>
</div>

<div class="s light" id="s6">
<div class="head"><p class="eyebrow a" style="--d:.2s">Who did it?</p><h2 class="a" style="--d:.3s">Nobody has said yet</h2></div>
<div class="vs">
<div class="card x" style="--d:.5s"><p class="flag">Theory 1</p><p class="soft">Young hackers showing off</p></div>
<div class="card x" style="--d:.8s"><p class="flag">Theory 2</p><p class="soft">State sabotage</p></div>
</div>
<div class="card x" style="--d:1.1s;border-left-color:#2AA9C9"><p class="flag">France's advice</p><p class="soft">Disconnect affected freezers from the internet and update them</p></div>
</div>

<div class="s redbg" id="s7">
<div class="head"><p class="eyebrow a" style="--d:.2s">The lesson</p><h2 class="a" style="--d:.3s">If it's online, it can be hacked</h2></div>
<p class="lead a" style="--d:.6s">Even a fridge.</p>
<div><p class="part stamp" style="--d:1.0s;background:{DARK};color:#fff;font-size:40px">Follow for more</p></div>
<p class="small soft a" style="--d:1.4s">Sources: Reuters, Al Jazeera, AFP, Le Monde, Bloomberg, SBS</p>
</div>
"""
(V / "slides.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>', encoding="utf-8")
print("ok")
