from pathlib import Path
V = Path(__file__).parent
src = next(q for q in [V / "base-slides.html", *(p / "kit/template/base-slides.html" for p in V.parents)] if q.exists()).read_text(encoding="utf-8")
head = src[:src.index("<style>") + 7]
css = src[src.index("<style>") + 7:src.index(".cam{")]
css += (V / "scene.css").read_text(encoding="utf-8")
css += """
.dark .card{border-left-color:#FF5A47}
.red{color:#FF5A47}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.stat .l{font-size:32px;line-height:1.3}
.light .stat .n{color:#C2412F}
.bars{display:flex;flex-direction:column;gap:30px}
.br{display:grid;grid-template-columns:270px 1fr 150px;align-items:center;gap:20px}
.br span{font-size:40px;font-weight:700}.br small{display:block;font-size:24px;font-weight:500;color:#8B95A5}
.br i{display:block;height:54px;border-radius:10px;background:#FF5A47;width:calc(var(--w) * 4.5%);transform-origin:left;animation:barg .7s cubic-bezier(.2,.7,.2,1) both;animation-delay:calc(var(--d) + .15s)}
.br b{font-size:48px;font-weight:900;color:#FF5A47}
@keyframes barg{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.light .tl .line{background:#C2412F}.light .ev::before{background:#C2412F}.light .ev b{color:#C2412F}
"""
body = f"""
<div class="s dark" id="s1" style="gap:36px;justify-content:flex-start;background:#0B0F15">
<div><p class="part" style="background:#FF5A47">North Korea · This week</p></div>
<h1 style="font-size:92px">Missiles <span class="red">and suicide drones</span></h1>
{(V / "scene.svg").read_text(encoding="utf-8")}
<p class="small soft">Sources: South Korea JCS, North Korean state media (KCNA)</p>
</div>

<div class="s dark" id="s2" style="justify-content:flex-start;gap:60px">
<div class="head"><p class="eyebrow a" style="--d:.2s;color:#FF5A47">Thursday, 29 October</p><h2 class="a" style="--d:.3s">About 10 missiles in one launch</h2></div>
<div class="stats">
<div class="stat a" style="--d:.5s"><p class="n" style="font-size:120px;color:#FF5A47">~10</p><p class="l soft">short-range ballistic missiles, from near Wonsan</p></div>
<div class="stat a" style="--d:.75s"><p class="n" style="font-size:120px">12:30</p><p class="l soft">local time, into the Sea of Japan / East Sea</p></div>
</div>
<div class="card x" style="--d:1.1s"><h3>The timing</h3><p class="soft">During South Korea–US stealth jet drills, and a day after Trump said he might meet Kim.</p></div>
</div>

<div class="s light" id="s3" style="justify-content:flex-start;gap:60px">
<div class="head"><p class="eyebrow a" style="--d:.2s;color:#C2412F">The same day</p><h2 class="a" style="--d:.3s">Kim's drone show</h2></div>
<div class="stats">
<div class="stat a" style="--d:.5s"><p class="n" style="font-size:120px">30+</p><p class="l soft">types of drones on display, incl. a new stealth drone</p></div>
<div class="stat a" style="--d:.75s"><p class="n" style="font-size:120px">"100%"</p><p class="l soft">hit rate claimed by state media</p></div>
</div>
<div class="card x" style="--d:1.1s;border-left-color:#C2412F"><h3>Not verified</h3><p class="soft">Suicide drones dove onto mock targets, including a tank, state media images show. Claims can't be independently checked.</p></div>
</div>

<div class="s dark" id="s4" style="justify-content:flex-start;gap:60px">
<div class="head"><p class="eyebrow a" style="--d:.2s;color:#FF5A47">Kim's message</p><h2 class="a" style="--d:.3s">"Absolute superiority" in drones</h2></div>
<div class="card x" style="--d:.5s"><h3>600 mm rocket launcher</h3><p class="soft">Also on show. North Korea says it can carry nuclear warheads.</p></div>
</div>

<div class="s amber" id="s5" style="justify-content:flex-start;gap:60px">
<div class="head"><p class="eyebrow a" style="--d:.2s">Why now?</p><h2 class="a" style="--d:.3s">A border landmine row</h2></div>
<div class="vs">
<div class="card x" style="--d:.5s"><p class="flag">Seoul</p><p class="soft">North planted the mine that wounded 3 soldiers; wants an apology</p></div>
<div class="card x" style="--d:.75s"><p class="flag">Pyongyang</p><p class="soft">Denies it: "no limit" to its options</p></div>
</div>
<div><p class="part stamp" style="--d:1.1s;background:#11151B;color:#F2B04E">Follow for more</p></div>
<p class="small soft a" style="--d:1.3s">Sources: South Korea JCS, KCNA, Al Jazeera, NK News, SBS</p>
</body></html>"""
(V / "slides.html").write_text(head + css + "</style></head><body>" + body, encoding="utf-8")
