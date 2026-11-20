from pathlib import Path
V = Path(__file__).parent
src = next(q for q in [V / "base-slides.html", *(p / "kit/template/base-slides.html" for p in V.parents)] if q.exists()).read_text(encoding="utf-8")
head = src[:src.index("<style>") + 7]
css = src[src.index("<style>") + 7:src.index(".cam{")]
css += (V / "map.css").read_text(encoding="utf-8")
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
<div class="s dark" id="s1" style="gap:36px;justify-content:flex-start">
<div><p class="part a" style="--d:.1s">Iran War · Part 5</p></div>
<h1 class="z" style="--d:.2s;font-size:88px">Strikes <span class="hl">after the election?</span></h1>
{(V / "map.svg").read_text(encoding="utf-8")}
<p class="small soft a" style="--d:.6s">Map simplified · arrows illustrative, based on reports</p>
</div>

<div class="s dark" id="s2" style="justify-content:flex-start;gap:60px">
<div class="head"><p class="eyebrow a" style="--d:.2s">The war signal · Wall Street Journal</p><h2 class="a" style="--d:.3s">"Get ready" for a short, intense campaign</h2></div>
<div class="stack" style="gap:20px">
<div class="card x" style="--d:.5s"><h3>Carrier group + Marines</h3><p class="soft">Joining about 20 US warships already in the region</p></div>
<div class="card x" style="--d:.75s"><h3>Patriot: Texas → Israel</h3><p class="soft">Air-defence system on the move; munitions restocked</p></div>
</div>
<p class="quote a" style="--d:1.1s;font-size:60px">"We may do another little Epic Fury." <span class="soft" style="font-size:32px;font-family:Inter">– Trump</span></p>
</div>

<div class="s light" id="s3" style="justify-content:flex-start;gap:60px">
<div class="head"><p class="eyebrow a" style="--d:.2s">Talks at the same time</p><h2 class="a" style="--d:.3s">A door still open?</h2></div>
<div class="vs">
<div class="card x" style="--d:.5s"><p class="flag">Vance</p><p class="soft">Reportedly wrote to a top Iranian security official to restart talks</p></div>
<div class="card x" style="--d:.75s"><p class="flag">Qatar</p><p class="soft">UN inspectors in, some sanctions eased</p></div>
</div>
<div><p class="part stamp" style="--d:1.2s;background:#E25D4B;color:#11151B;font-size:40px">Iran: "unacceptable"</p></div>
</div>

<div class="s dark" id="s4" style="justify-content:flex-start;gap:60px">
<div class="head"><p class="eyebrow a" style="--d:.2s">Iran's side</p><h2 class="a" style="--d:.3s">Attacks on ships doubled</h2></div>
<div class="stats">
<div class="stat a" style="--d:.5s"><p class="n" style="font-size:120px;color:#E25D4B">26</p><p class="l soft">ship attacks, 1–19 October</p></div>
<div class="stat a" style="--d:.75s"><p class="n" style="font-size:120px">13</p><p class="l soft">in all of September</p></div>
</div>
<div class="card x" style="--d:1.1s"><h3>Iran's warning</h3><p class="soft">"Devastating impact on int'l markets" of any new attack – Foreign Minister Araghchi</p></div>
</div>

<div class="s amber" id="s5" style="justify-content:flex-start;gap:60px">
<div class="head"><p class="eyebrow a" style="--d:.2s">What to watch</p><h2 class="a" style="--d:.3s">November 3</h2></div>
<div class="stack" style="gap:20px">
<div class="card x" style="--d:.5s"><h3>Before</h3><p class="soft">Trump promised no strikes before the midterms</p></div>
<div class="card x" style="--d:.8s"><h3>After</h3><p class="soft">"Anything's possible."</p></div>
</div>
<div><p class="part stamp" style="--d:1.1s;background:#11151B;color:#F2B04E">Follow for Part 6</p></div>
<p class="small soft a" style="--d:1.3s">Sources: Wall Street Journal via Middle East Eye, Fox News, CBS News, Axios, JINSA, Gulf News</p>
</body></html>"""
(V / "slides.html").write_text(head + css + "</style></head><body>" + body, encoding="utf-8")
