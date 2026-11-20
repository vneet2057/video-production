from pathlib import Path

V = Path(__file__).parent
DARK, LIGHT, AMB, AMB2, ADK, RED = "#11151B", "#F2EEE6", "#E39B2D", "#F2B04E", "#A8620C", "#E25D4B"

base_css = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#000;font-family:'Inter',Arial,sans-serif;width:1080px;height:1920px;overflow:hidden}}
.s{{display:none;width:1080px;height:1920px;padding:130px 96px 120px;flex-direction:column;justify-content:flex-start;gap:60px;overflow:hidden;position:relative}}
.s.on{{display:flex}}
.dark{{background:{DARK};color:{LIGHT}}}
.light{{background:{LIGHT};color:{DARK}}}
.amber{{background:{AMB};color:{DARK}}}
.eyebrow{{font-size:28px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{ADK}}}
.dark .eyebrow{{color:{AMB2}}}.amber .eyebrow{{color:{DARK}}}
.part{{display:inline-block;font-size:30px;font-weight:800;letter-spacing:3px;text-transform:uppercase;background:{AMB2};color:{DARK};padding:12px 22px;border-radius:10px}}
h1{{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:96px;line-height:1.03;letter-spacing:-2px}}
h2{{font-family:'Inter Display','Inter',sans-serif;font-weight:700;font-size:80px;line-height:1.08;letter-spacing:-1px}}
p{{font-size:38px;line-height:1.36}}
.lead{{font-size:50px;line-height:1.3}}
.soft{{color:#505866}}.dark .soft{{color:#B5BDC9}}.amber .soft{{color:#3A3020}}
.small{{font-size:27px}}
.hl{{color:{AMB2}}}.light .hl{{color:{ADK}}}
.head{{display:flex;flex-direction:column;gap:24px}}
.stack{{display:flex;flex-direction:column;gap:22px}}
.vs{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}
.card{{background:#1C222B;border-radius:20px;padding:32px 36px;display:flex;flex-direction:column;gap:10px;border-left:6px solid {AMB2}}}
.light .card{{background:#FFFFFF;border-left-color:{ADK}}}
.amber .card{{background:#F4C981;border-left-color:{DARK}}}
.flag{{font-size:28px;font-weight:800;letter-spacing:2px;text-transform:uppercase}}
.q{{font-family:'Charter','Bitstream Charter',Georgia,serif;font-size:42px;line-height:1.25}}
.a{{animation:rise .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}}
.x{{animation:slide .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}}
.stamp{{animation:stamp .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:var(--d,1s)}}
@keyframes rise{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
@keyframes slide{{from{{opacity:0;transform:translateX(-60px)}}to{{opacity:1;transform:none}}}}
@keyframes stamp{{from{{opacity:0;transform:scale(1.8) rotate(-8deg)}}to{{opacity:1;transform:rotate(-4deg)}}}}
"""

body = f"""
<div class="s dark" id="s1">
<div class="head"><p class="eyebrow a" style="--d:.2s">4 November · after the vote</p><h2 class="a" style="--d:.3s">His own VP blamed the war</h2></div>
<div class="vs">
<div class="card x" style="--d:.5s"><p class="flag">JD Vance</p><p class="q">"The reason we lost is the war."</p></div>
<div class="card x" style="--d:.8s"><p class="flag">Trump</p><p class="q">"Largely true"</p><p class="soft small">It pushed up gas prices</p></div>
</div>
</div>

<div class="s light" id="s2">
<div class="head"><p class="eyebrow a" style="--d:.2s">Trump's side</p><h2 class="a" style="--d:.3s">No regrets</h2></div>
<div class="vs">
<div class="card x" style="--d:.5s"><p class="flag">His reason</p><p class="soft">"You can't let Iran have a nuclear weapon"</p></div>
<div class="card x" style="--d:.8s"><p class="flag">When will it end?</p><p class="q">"Whenever I want it to"</p></div>
</div>
</div>

<div class="s dark" id="s3">
<div class="head"><p class="eyebrow a" style="--d:.2s">Congress</p><h2 class="a" style="--d:.3s">Democrats want it ended</h2></div>
<div class="vs">
<div class="card x" style="--d:.5s"><p class="flag">From January</p><p class="soft">Hearings, and efforts to limit the war</p></div>
<div class="card x" style="--d:.8s;border-left-color:{RED}"><p class="flag">But</p><p class="soft">Trump can veto</p></div>
</div>
</div>

<div class="s light" id="s4">
<div class="head"><p class="eyebrow a" style="--d:.2s">Iran reacts</p><h2 class="a" style="--d:.3s">Celebration, and a warning</h2></div>
<div class="vs">
<div class="card x" style="--d:.5s"><p class="flag">Parliament speaker</p><p class="q">"Americans said no to war"</p></div>
<div class="card x" style="--d:.8s"><p class="flag">Supreme leader</p><p class="soft">US hostility "will persist"</p></div>
</div>
</div>

<div class="s amber" id="s5">
<div class="head"><p class="eyebrow a" style="--d:.2s">What's next</p><h2 class="a" style="--d:.3s">The war ends, or gets bigger?</h2></div>
<div class="stack" style="align-items:flex-start;gap:30px"><p class="part stamp" style="--d:.7s;background:{DARK};color:{AMB2}">Let's see what happens</p><p class="part stamp" style="--d:1.1s;background:{DARK};color:{AMB2};font-size:40px">Follow for more</p></div>
<p class="small soft a" style="--d:1.4s">Sources: HuffPost, Yahoo News, ABC/TNND, Al Jazeera, SBS, Times of Israel</p>
</div>
"""
(V / "slides.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{base_css}</style></head><body>{body}</body></html>', encoding="utf-8")

# hook overlay (transparent), sits over Trump's clip
hook = f"""<!doctype html><html><head><meta charset="utf-8"><style>{base_css}
body{{background:transparent}}
.ov{{position:absolute;inset:0;width:1080px;height:1920px}}
.top{{position:absolute;left:0;right:0;top:0;height:400px;background:linear-gradient({DARK} 78%,rgba(17,21,27,0));padding:110px 70px 0}}
.qc{{position:absolute;left:60px;right:60px;top:1210px;background:rgba(17,21,27,.86);border-left:8px solid {AMB2};border-radius:18px;padding:26px 34px}}
.lab{{position:absolute;left:60px;top:1140px;font:600 26px Inter;color:#fff;background:rgba(0,0,0,.65);padding:10px 16px;border-radius:6px}}
</style></head><body><div class="ov">
<div class="top"><p class="part" style="font-size:26px;padding:8px 18px">Iran War · Part 8</p>
<h1 style="color:{LIGHT};font-size:84px;margin-top:22px">Trump admits: <span class="hl">war cost him Congress</span></h1></div>
<p class="lab">Video: Trump speaking to reporters · 4 Nov 2026</p>
<div class="qc"><p class="q" style="color:{LIGHT};font-size:46px">"If I had to do it again, I'd have to do it again."</p><p class="small" style="color:{AMB2};margin-top:8px;font-weight:700">Donald Trump</p></div>
</div></body></html>"""
(V / "hook.html").write_text(hook, encoding="utf-8")
print("ok")
