from pathlib import Path
V = Path(__file__).parent
src = next(q for q in [V / "base-slides.html", *(p / "kit/template/base-slides.html" for p in V.parents)] if q.exists()).read_text(encoding="utf-8")
head = src[:src.index("<style>") + 7]
css = src[src.index("<style>") + 7:src.index(".cam{")]
css += src[src.index(".chk{"):src.index("</style>")]
css += (V / "map.css").read_text(encoding="utf-8")
css += """
.dark .card{border-left-color:#FF5A47}
.red{color:#FF5A47}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.stat .l{font-size:32px;line-height:1.3}
.light .stat .n{color:#C2412F}
"""
body = f"""
<div class="s dark" id="s1" style="gap:36px;justify-content:flex-start">
<div><p class="part a" style="--d:.1s;background:#FF5A47">World · Missile tests</p></div>
<h1 class="z" style="--d:.2s;font-size:92px">A month of <span class="red">missile tests.</span></h1>
{(V / "map.svg").read_text(encoding="utf-8")}
<p class="small soft a" style="--d:.6s">Flight paths illustrative · Map simplified</p>
</div>

<div class="s dark" id="s2" style="justify-content:flex-start;gap:70px">
<div class="head"><p class="eyebrow a" style="--d:.2s;color:#FF5A47">Russia · This week</p><h2 class="a" style="--d:.3s">A nuclear sub fires a Bulava missile</h2></div>
<div class="stats">
<div class="stat a" style="--d:.5s"><p class="n" style="font-size:110px;color:#FF5A47">8,000+</p><p class="l soft">km range</p></div>
<div class="stat a" style="--d:.75s"><p class="n" style="font-size:110px;color:#FF5A47">Nuclear</p><p class="l soft">capable, built for warheads</p></div>
</div>
<div class="card x" style="--d:1.1s"><h3>Being watched</h3><p class="soft">The United States sent spy planes to observe the launch.</p></div>
</div>

<div class="s light" id="s3" style="justify-content:flex-start;gap:70px">
<div class="head"><p class="eyebrow a" style="--d:.2s;color:#C2412F">North Korea · Today</p><h2 class="a" style="--d:.3s">About 10 missiles in one day</h2></div>
<div class="stats">
<div class="stat a" style="--d:.5s"><p class="n" style="font-size:110px">~10</p><p class="l soft">short-range ballistic missiles, South Korea says</p></div>
<div class="stat a" style="--d:.75s"><p class="n" style="font-size:110px">900+</p><p class="l soft">km flown by one missile on 12 October</p></div>
</div>
<div class="card x" style="--d:1.1s;border-left-color:#C2412F"><h3>The timing</h3><p class="soft">Days after Kim Jong Un's visit to China.</p></div>
</div>

<div class="s dark" id="s4" style="justify-content:flex-start;gap:70px">
<div class="head"><p class="eyebrow a" style="--d:.2s;color:#FF5A47">Also this month</p><h2 class="a" style="--d:.3s">France and South Korea test too</h2></div>
<div class="stack">
<div class="card x" style="--d:.5s"><h3>France · 6 October</h3><p class="soft">New M51.3 nuclear-capable missile, first launch from a submarine. No warhead.</p></div>
<div class="card x" style="--d:.8s"><h3>South Korea · 8 October</h3><p class="soft">First homemade hypersonic missile, Mach 5+. "We must secure our security through our own strength."</p></div>
</div>
</div>

<div class="s amber" id="s5" style="justify-content:flex-start;gap:70px">
<div class="head"><p class="eyebrow a" style="--d:.2s">Why now?</p><h2 class="a" style="--d:.3s">No new war declared</h2></div>
<div class="stack" style="gap:20px">
<div class="card x" style="--d:.5s"><h3>On edge</h3><p class="soft">Ukraine, the Iran war and the Korean Peninsula</p></div>
<div class="card x" style="--d:.8s"><h3>The signal</h3><p class="soft">Countries are showing what they have</p></div>
</div>
<div><p class="part stamp" style="--d:1.1s;background:#11151B;color:#F2B04E">Follow for more</p></div>
<p class="small soft a" style="--d:1.3s">Sources: TASS, South Korea JCS, French Defence Ministry, NPR, Daily Maverick</p>
</div>
</body></html>"""
(V / "slides.html").write_text(head + css + "</style></head><body>" + body, encoding="utf-8")
