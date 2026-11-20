# Trilateral outcome video: 10 fast scenes. Reveals inside a slide are timed to the narration (work/sentences.json).
import json
from pathlib import Path
V = Path(__file__).parent
S = json.load(open(V / "work" / "sentences.json"))


def at(slide, sent, extra=0.0):
    """Animation delay (s, from slide start) for the moment sentence `sent` of slide `slide` (1-based) starts."""
    m = S[slide - 1]
    return round(m[sent][0] - m[0][0] + 0.3 + extra, 2)


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#000;font-family:'Inter',Arial,sans-serif;width:1080px;height:1920px;overflow:hidden}
.s{display:none;width:1080px;height:1920px;padding:130px 96px 120px;flex-direction:column;justify-content:flex-start;gap:60px;overflow:hidden;position:relative}
.s.on{display:flex}
.dark{background:#11151B;color:#F2EEE6}
.light{background:#F2EEE6;color:#11151B}
.amber{background:#E39B2D;color:#11151B}
.eyebrow{font-size:28px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:#A8620C}
.dark .eyebrow{color:#F2B04E}.amber .eyebrow{color:#11151B}
.part{display:inline-block;font-size:30px;font-weight:800;letter-spacing:3px;text-transform:uppercase;background:#F2B04E;color:#11151B;padding:12px 22px;border-radius:10px}
h1{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:104px;line-height:1.02;letter-spacing:-2px}
h2{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:92px;line-height:1.04;letter-spacing:-1.5px}
h3{font-size:44px;font-weight:700;line-height:1.2}
p{font-size:40px;line-height:1.35}
.lead{font-size:54px;line-height:1.25;font-weight:700}
.soft{color:#505866}.dark .soft{color:#B5BDC9}.amber .soft{color:#3A3020}
.small{font-size:26px}
.hl{color:#F2B04E}.light .hl{color:#A8620C}
.red{color:#E25D4B}.light .red{color:#C2412F}
.head{display:flex;flex-direction:column;gap:22px}
.card{background:#1C222B;border-radius:20px;padding:34px 40px;display:flex;flex-direction:column;gap:12px;border-left:6px solid #F2B04E}
.light .card{background:#FFFFFF;border-left-color:#A8620C}
.card.no{border-left-color:#E25D4B}
.label{position:absolute;left:22px;top:22px;font-size:24px;font-weight:600;color:#fff;background:rgba(0,0,0,.7);padding:8px 14px;border-radius:6px}
/* progress tracker "1 / 4" */
.trk{position:absolute;right:96px;top:122px;display:flex;align-items:center;gap:12px;font-size:30px;font-weight:800;letter-spacing:2px}
.trk i{display:block;width:22px;height:22px;border-radius:50%;border:4px solid currentColor;opacity:.45}
.trk i.on{background:#F2B04E;border-color:#F2B04E;opacity:1}
.light .trk i.on{background:#A8620C;border-color:#A8620C}
.big{font-family:'Inter Display','Inter',sans-serif;font-weight:900;font-size:300px;line-height:.9;letter-spacing:-10px;color:#F2B04E}
.light .big{color:#A8620C}
/* check / cross rows */
.rows{display:flex;flex-direction:column;gap:26px}
.row{display:grid;grid-template-columns:84px 1fr;align-items:center;gap:26px;font-size:46px;font-weight:700;line-height:1.2}
.row b{display:flex;align-items:center;justify-content:center;width:84px;height:84px;border-radius:50%;font-size:50px;color:#11151B;background:#6FCF8E}
.row.no b{background:#E25D4B}
/* hook photo */
.hookimg{position:absolute;left:0;top:700px;width:1080px;height:720px;overflow:hidden}
.hookimg img{width:100%;height:100%;object-fit:cover;object-position:50% 30%;animation:kb 4.5s linear both;transform-origin:50% 35%}
.hookimg::after{content:"";position:absolute;inset:0;background:linear-gradient(#11151B 0%,rgba(17,21,27,0) 18%,rgba(17,21,27,0) 80%,#11151B 100%)}
@keyframes kb{from{transform:scale(1.0)}to{transform:scale(1.1)}}
/* scene 2: three flags converge */
.meet{position:relative;height:640px}
.fl{position:absolute;width:250px;text-align:center;font-size:32px;font-weight:800;letter-spacing:3px}
.fl .f{height:160px;border-radius:14px;overflow:hidden;margin-bottom:14px;box-shadow:0 8px 24px rgba(0,0,0,.4)}
.us .f{background:repeating-linear-gradient(#B22234 0 12.3px,#fff 12.3px 24.6px);position:relative}
.us .f::before{content:"";position:absolute;left:0;top:0;width:44%;height:53.8%;background:#3C3B6E}
.cn .f{background:#DE2910;position:relative}
.cn .f::before{content:"★";position:absolute;left:24px;top:6px;font-size:64px;color:#FFDE00}
.ru .f{background:linear-gradient(#fff 0 33.3%,#0039A6 33.3% 66.6%,#D52B1E 66.6%)}
.pin{position:absolute;left:0;right:0;top:420px;text-align:center}
.hub{transform-box:fill-box;transform-origin:center;animation:hub .45s cubic-bezier(.2,.9,.3,1.4) both;animation-delay:1.85s}
@keyframes hub{from{transform:scale(0)}to{transform:scale(1)}}
.ring{transform-box:fill-box;transform-origin:center;animation:ring 1s ease-out both;animation-delay:2.1s}
@keyframes ring{from{opacity:1;transform:scale(1)}to{opacity:0;transform:scale(3.2)}}
.pin .dot{width:40px;height:40px;border-radius:50%;background:#F2B04E;margin:0 auto 14px;box-shadow:0 0 0 0 rgba(242,176,78,.7);animation:ping 1.2s ease-out infinite}
@keyframes ping{to{box-shadow:0 0 0 46px rgba(242,176,78,0)}}
.pin p{font-size:40px;font-weight:900;letter-spacing:4px}
.us{left:0;top:0;animation:fromL .7s cubic-bezier(.2,.8,.2,1) both;animation-delay:.2s}
.cn{left:319px;top:0;animation:fromT .7s cubic-bezier(.2,.8,.2,1) both;animation-delay:.45s}
.ru{right:0;top:0;animation:fromR .7s cubic-bezier(.2,.8,.2,1) both;animation-delay:.7s}
@keyframes fromL{from{opacity:0;transform:translateX(-200px)}to{opacity:1;transform:none}}
@keyframes fromR{from{opacity:0;transform:translateX(200px)}to{opacity:1;transform:none}}
@keyframes fromT{from{opacity:0;transform:translateY(-160px)}to{opacity:1;transform:none}}
.wire{stroke:#F2B04E;stroke-width:5;fill:none;stroke-dasharray:1;stroke-dashoffset:1;animation:draw .8s ease-out both;animation-delay:1.1s}
@keyframes draw{to{stroke-dashoffset:0}}
/* oil bars */
.bars{display:flex;align-items:flex-end;gap:40px;height:330px;padding:0 20px}
.bar{flex:1;display:flex;flex-direction:column;align-items:center;gap:14px;font-size:30px;font-weight:800;letter-spacing:2px}
.bar i{display:block;width:100%;border-radius:14px 14px 4px 4px;background:linear-gradient(#F2B04E,#A8620C);transform-origin:bottom;animation:barup .9s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d)}
.bar i::after{content:"▲";display:block;text-align:center;color:#11151B;font-size:40px;padding-top:12px}
@keyframes barup{from{transform:scaleY(0)}to{transform:scaleY(1)}}
/* UN seats */
.seats{display:grid;grid-template-columns:repeat(5,1fr);gap:20px}
.seat{border-radius:18px;padding:26px 8px;text-align:center;font-size:30px;font-weight:800;letter-spacing:1px;background:#E6DCC8;color:#8A8274}
.seat.lit{background:#11151B;color:#F2B04E;animation:lit .5s ease both;animation-delay:var(--d)}
@keyframes lit{from{background:#E6DCC8;color:#8A8274;transform:scale(1)}50%{transform:scale(1.12)}to{background:#11151B;color:#F2B04E;transform:scale(1)}}
/* quote */
.quote{font-family:'Charter','Bitstream Charter',Georgia,serif;font-size:96px;line-height:1.1}
.qimg{position:relative;width:888px;height:500px;border-radius:18px;overflow:hidden;border:6px solid #F2B04E}
.qimg img{width:100%;height:100%;object-fit:cover;animation:kb 3.2s linear both}
/* twist */
.mega{font-family:'Inter Display','Inter',sans-serif;font-weight:900;font-size:200px;letter-spacing:-6px;line-height:1}
.stampx{display:inline-block;font:900 54px Inter,Arial;letter-spacing:5px;color:#E25D4B;border:7px solid #E25D4B;padding:10px 26px;border-radius:14px;transform:rotate(-5deg)}
/* 40 minutes counter */
@property --n{syntax:'<integer>';initial-value:0;inherits:false}
.count{font-family:'Inter Display','Inter',sans-serif;font-weight:900;font-size:220px;line-height:.9;letter-spacing:-6px;color:#F2B04E;counter-reset:n var(--n);animation:cnt 1.1s cubic-bezier(.2,.7,.2,1) both;animation-delay:.3s}
.count::after{content:counter(n)}
@keyframes cnt{from{--n:0}to{--n:40}}
.himg{position:relative;width:888px;height:520px;border-radius:18px;overflow:hidden;border:6px solid #F2B04E}
.himg img{width:100%;height:100%;object-fit:cover;object-position:50% 25%;animation:pan 5.6s linear both}
@keyframes pan{from{transform:scale(1.12) translateX(-30px)}to{transform:scale(1.12) translateX(30px)}}
/* generic */
.a{animation:rise .5s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}
.z{animation:zoom .5s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,.3s)}
.x{animation:slide .5s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}
.stamp{animation:stamp .45s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:var(--d,1s)}
@keyframes rise{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
@keyframes zoom{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:none}}
@keyframes slide{from{opacity:0;transform:translateX(-70px)}to{opacity:1;transform:none}}
@keyframes stamp{from{opacity:0;transform:scale(2) rotate(-10deg)}to{opacity:1;transform:rotate(-5deg)}}
"""


def trk(n):
    return '<div class="trk"><span>' + f"{n} / 4" + "</span>" + "".join(f'<i class="{"on" if k <= n else ""}"></i>' for k in range(1, 5)) + "</div>"


BODY = f"""
<!-- 1 HOOK: photo already zooming at frame 0, headline fully visible -->
<div class="s dark" id="s1" style="gap:36px">
<div><p class="part">World news</p></div>
<h1 style="font-size:98px">Trump, Xi and Putin agreed on <span class="hl">4 things</span></h1>
<p class="lead a" style="--d:{at(1,1)}s;font-size:40px;white-space:nowrap">But the biggest war <span class="red">wasn't one of them.</span></p>
<div class="hookimg"><img src="in/lineup-hires.png"><span class="label" style="top:auto;bottom:150px;z-index:2">File photo · Putin, Xi and Trump</span></div>
</div>

<!-- 2 FIRST TIME EVER -->
<div class="s light" id="s2">
<div class="head"><p class="eyebrow a" style="--d:.15s">19 November · Shenzhen, China</p><h2 class="a" style="--d:.25s">The world's 3 biggest nuclear powers</h2></div>
<div class="meet">
<svg width="888" height="640" style="position:absolute;left:0;top:0;overflow:visible"><path class="wire" pathLength="1" d="M125 228 C125 330 300 372 444 372"/><path class="wire" pathLength="1" d="M444 228 L444 372"/><path class="wire" pathLength="1" d="M763 228 C763 330 588 372 444 372"/><circle class="ring" cx="444" cy="372" r="22" fill="none" stroke="#F2B04E" stroke-width="4"/><circle class="hub" cx="444" cy="372" r="22" fill="#F2B04E" stroke="#11151B" stroke-width="5"/></svg>
<div class="fl us"><div class="f"></div>USA</div>
<div class="fl cn"><div class="f"></div>CHINA</div>
<div class="fl ru"><div class="f"></div>RUSSIA</div>
<div class="pin"><p class="a" style="--d:1.75s">SHENZHEN</p><p class="stamp" style="--d:2.1s;margin-top:22px;display:inline-block;background:#11151B;color:#F2B04E;font-size:34px;padding:10px 22px;border-radius:10px">FIRST TIME TOGETHER</p></div>
</div>
</div>

<!-- 3 #1 NUCLEAR -->
<div class="s dark" id="s3">
{trk(1)}
<div class="head"><p class="eyebrow a" style="--d:.1s">Number one</p><h2 class="a" style="--d:.2s">Nuclear weapons</h2></div>
<div class="rows">
<div class="row x" style="--d:{at(3,1)}s"><b>✓</b>No one can win a nuclear war</div>
<div class="row x" style="--d:{at(3,1,1.6)}s"><b>✓</b>Talks on reducing the risks</div>
<div class="row no x" style="--d:{at(3,2)}s"><b>✕</b>No limits on their weapons</div>
</div>
</div>

<!-- 4 QUOTE -->
<div class="s light" id="s4">
<div class="head"><p class="eyebrow a" style="--d:.1s">Trump, to reporters</p></div>
<p class="quote z" style="--d:.2s">"It's very hard to give them up."</p>
<div class="qimg a" style="--d:.5s"><img src="in/lineup-small.png"><span class="label">File photo · Putin, Xi and Trump</span></div>
</div>

<!-- 5 #2 OIL -->
<div class="s light" id="s5">
{trk(2)}
<div class="head"><p class="eyebrow a" style="--d:.1s">Number two</p><h2 class="a" style="--d:.2s">More oil products</h2></div>
<div class="bars">
<div class="bar"><i style="height:220px;--d:{at(5,1)}s"></i>USA</div>
<div class="bar"><i style="height:250px;--d:{at(5,1,.2)}s"></i>CHINA</div>
<div class="bar"><i style="height:280px;--d:{at(5,1,.4)}s"></i>RUSSIA</div>
</div>
<div class="card x" style="--d:{at(5,2)}s"><h3>Some analysts:</h3><p class="soft">A big win for Russia</p></div>
</div>

<!-- 6 #3 UN -->
<div class="s light" id="s6">
{trk(3)}
<div class="head"><p class="eyebrow a" style="--d:.1s">Number three</p><h2 class="a" style="--d:.2s">Reform the United Nations</h2></div>
<p class="small soft a" style="--d:{at(6,1)}s;font-size:32px;font-weight:600">UN Security Council · permanent seats</p>
<div class="seats">
<div class="seat lit" style="--d:{at(6,1,.4)}s">USA</div><div class="seat lit" style="--d:{at(6,1,.6)}s">CHINA</div><div class="seat lit" style="--d:{at(6,1,.8)}s">RUSSIA</div><div class="seat">UK</div><div class="seat">FRANCE</div>
</div>
<div class="card x" style="--d:{at(6,2)}s"><h3>A surprise</h3><p class="soft">Trump is a longtime critic of the UN</p></div>
</div>

<!-- 7 #4 ICC -->
<div class="s dark" id="s7">
{trk(4)}
<div class="head"><p class="eyebrow a" style="--d:.1s">Number four</p><h2 class="a" style="--d:.2s">A warning to a world court</h2></div>
<div class="card z" style="--d:.6s"><h3>International Criminal Court</h3><p class="soft">"Must not abuse" its powers</p></div>
<div class="card no x" style="--d:{at(7,1)}s"><h3>Same court that</h3><p class="soft">issued an arrest warrant for Putin in 2023</p></div>
</div>

<!-- 8 TWIST -->
<div class="s dark" id="s8" style="justify-content:flex-start;gap:50px">
<p class="lead a" style="--d:.15s">So what was missing?</p>
<p class="mega z" style="--d:{at(8,1)}s">UKRAINE</p>
<div><p class="stampx stamp" style="--d:{at(8,2)}s">NOT IN THE DECLARATION</p></div>
</div>

<!-- 9 40 MINUTES -->
<div class="s light" id="s9" style="gap:40px">
<div style="display:flex;align-items:flex-end;gap:24px"><p class="count"></p><p class="lead" style="padding-bottom:20px">minutes<br><span class="soft" style="font-size:38px;font-weight:600">Trump and Putin, alone</span></p></div>
<div class="himg a" style="--d:.2s"><img src="in/handshake.png"><span class="label">File photo · Trump, Xi and Putin</span></div>
<div style="display:flex;gap:20px">
<div class="card no x" style="--d:{at(9,1)}s;flex:1"><h3>Result</h3><p class="soft">None announced</p></div>
<div class="card no x" style="--d:{at(9,2)}s;flex:1"><h3>Ukraine</h3><p class="soft">Not in the room</p></div>
</div>
</div>

<!-- 10 CTA -->
<div class="s amber" id="s10">
<div class="head"><p class="eyebrow a" style="--d:.1s">Your view</p><h2 class="a" style="--d:.2s">A step toward peace, or just a photo op?</h2></div>
<p class="lead a" style="--d:{at(10,1)}s">Comment below.</p>
<div><p class="part stamp" style="--d:{at(10,3)}s;background:#11151B;color:#F2B04E">Follow for more</p></div>
<p class="small soft a" style="--d:1.2s">Sources: CNBC, NBC News, Al Jazeera, RFE/RL, France 24, The Hill, AFP</p>
</div>
"""
(V / "slides.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{BODY}</body></html>", encoding="utf-8")
print("slides.html written")
