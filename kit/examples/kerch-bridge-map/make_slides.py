from pathlib import Path
V = Path(__file__).parent
MAP_SVG = (V / "map.svg").read_text(encoding="utf-8")
MAP_CSS = (V / "map.css").read_text(encoding="utf-8")

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#000;font-family:'Inter',Arial,sans-serif;width:1080px;height:1920px;overflow:hidden}
.s{display:none;width:1080px;height:1920px;padding:130px 96px 120px;flex-direction:column;justify-content:flex-start;gap:70px;overflow:hidden;position:relative}
.s.on{display:flex}
.dark{background:#11151B;color:#F2EEE6}
.light{background:#F2EEE6;color:#11151B}
.amber{background:#E39B2D;color:#11151B}
.eyebrow{font-size:28px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:#A8620C}
.dark .eyebrow{color:#F2B04E}.amber .eyebrow{color:#11151B}
.part{display:inline-block;font-size:30px;font-weight:800;letter-spacing:3px;text-transform:uppercase;background:#F2B04E;color:#11151B;padding:12px 22px;border-radius:10px}
h1{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:108px;line-height:1.02;letter-spacing:-2px}
h2{font-family:'Inter Display','Inter',sans-serif;font-weight:700;font-size:80px;line-height:1.08;letter-spacing:-1px}
h3{font-size:42px;font-weight:700;line-height:1.2}
p{font-size:40px;line-height:1.4}
.lead{font-size:50px;line-height:1.3}
.soft{color:#505866}.dark .soft{color:#B5BDC9}.amber .soft{color:#3A3020}
.small{font-size:28px}
.hl{color:#F2B04E}.light .hl{color:#A8620C}
.red{color:#E25D4B}.light .red{color:#C2412F}
.head{display:flex;flex-direction:column;gap:26px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.card{background:#1C222B;border-radius:20px;padding:36px 40px;display:flex;flex-direction:column;gap:14px;border-left:6px solid #F2B04E}
.light .card{background:#FFFFFF;border-left-color:#A8620C}
.amber .card{background:#F4C981;border-left-color:#11151B}
.card.ru{border-left-color:#C2412F}
.flag{font-size:30px;font-weight:800;letter-spacing:2px;text-transform:uppercase}
.stats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:28px}
.stat .n{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:92px;line-height:1;color:#A8620C;letter-spacing:-2px}
.dark .stat .n{color:#F2B04E}
.stat .l{font-size:30px;line-height:1.3;margin-top:10px}
.tl{position:relative;display:flex;flex-direction:column;gap:44px;padding-left:64px}
.tl .line{position:absolute;left:11px;top:14px;bottom:14px;width:4px;background:#F2B04E;transform-origin:top;animation:grow 1.6s cubic-bezier(.3,.6,.2,1) both;animation-delay:.4s}
.ev{position:relative;display:flex;flex-direction:column;gap:6px}
.ev::before{content:"";position:absolute;left:-64px;top:8px;width:26px;height:26px;border-radius:50%;background:#F2B04E}
.ev b{font-size:34px;font-weight:700;letter-spacing:1px;color:#F2B04E}
.ev span{font-size:42px;line-height:1.3}
.list{display:flex;flex-direction:column;gap:26px}
.a{animation:rise .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}
.z{animation:zoom .6s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,.3s)}
.x{animation:slide .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}
.stamp{animation:stamp .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:var(--d,1s)}
@keyframes rise{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
@keyframes zoom{from{opacity:0;transform:scale(.8)}to{opacity:1;transform:none}}
@keyframes slide{from{opacity:0;transform:translateX(-60px)}to{opacity:1;transform:none}}
@keyframes stamp{from{opacity:0;transform:scale(1.8) rotate(-8deg)}to{opacity:1;transform:rotate(-4deg)}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
"""

BODY = f"""
<!-- 1 HOOK: headline + badge + map visible at frame 0, camera already moving -->
<div class="s dark" id="s1" style="gap:44px">
<div><p class="part">Ukraine war</p></div>
<h1>Ukraine just broke <span class="hl">Putin's bridge</span></h1>
<div style="position:relative">{MAP_SVG}<p class="stopped">TRAINS STOPPED</p>
<p class="small soft" style="margin-top:14px">Map simplified</p></div>
</div>

<!-- 2 BASICS (photo panel under the stats) -->
<div class="s light" id="s2">
<div class="head"><p class="eyebrow a" style="--d:.2s">The basics</p><h2 class="a" style="--d:.3s">Russia's link to Crimea</h2></div>
<div class="stats">
<div class="stat a" style="--d:.5s"><p class="n">19 km</p><p class="l soft">long, over the Kerch Strait</p></div>
<div class="stat a" style="--d:.75s"><p class="n">2018</p><p class="l soft">opened by Putin himself</p></div>
<div class="stat a" style="--d:1s"><p class="n">2014</p><p class="l soft">Russia took Crimea from Ukraine</p></div>
</div>
</div>

<!-- 3 TIMELINE (photo panel under it) -->
<div class="s dark" id="s3">
<div class="head"><p class="eyebrow a" style="--d:.2s">Three attacks in a week</p><h2 class="a" style="--d:.3s">What happened</h2></div>
<div class="tl"><div class="line"></div>
<div class="ev x" style="--d:.55s"><b>16–17 November</b><span>Road section hit; Ukraine says a span was destroyed</span></div>
<div class="ev x" style="--d:.85s"><b>19 November</b><span>Railway hit; Russia suspends trains</span></div>
</div>
<p class="small soft a" style="--d:1.3s">Sources differ on how bad the damage is</p>
</div>

<!-- 4 BOTH SIDES -->
<div class="s light" id="s4">
<div class="head"><p class="eyebrow a" style="--d:.2s">Both sides</p><h2 class="a" style="--d:.3s">Two very different views</h2></div>
<div class="vs">
<div class="card x" style="--d:.5s"><p class="flag">Ukraine says</p><p class="soft">It's a "war conveyor belt" for fuel and ammunition. A response to Russian attacks on Ukraine's infrastructure.</p></div>
<div class="card ru x" style="--d:.8s"><p class="flag">Russia says</p><p class="soft">Confirms damage, but gives few details. Says trains should run again soon.</p></div>
</div>
</div>

<!-- 5 WHY IT MATTERS -->
<div class="s dark" id="s5">
<div class="head"><p class="eyebrow a" style="--d:.2s">Why it matters</p><h2 class="a" style="--d:.3s">The fastest supply route</h2></div>
<div class="list">
<div class="card x" style="--d:.5s"><h3>Russia → Crimea</h3><p class="soft">Road and rail, straight across the strait</p></div>
<div class="card ru x" style="--d:.8s"><h3>Without it</h3><p class="soft">Ferries and longer, slower routes</p></div>
</div>
</div>

<!-- 6 CTA -->
<div class="s amber" id="s6">
<div class="head"><p class="eyebrow a" style="--d:.2s">What's next</p><h2 class="a" style="--d:.3s">Can Russia keep Crimea supplied?</h2></div>
<p class="lead a" style="--d:.8s"><b>Tell us what you think in the comments.</b></p>
<div><p class="part stamp" style="--d:1.2s;background:#11151B;color:#F2B04E">Follow for more</p></div>
<p class="small soft a" style="--d:1.4s">Sources: Washington Post, NBC News, CNN, Ukrainska Pravda, Interfax-Ukraine, Bloomberg</p>
</div>
"""

(V / "slides.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{MAP_CSS}</style></head><body>{BODY}</body></html>", encoding="utf-8")
print("slides.html written")
