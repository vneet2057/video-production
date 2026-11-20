"""Animated hook scene (888x760 SVG + CSS) timed to the hook sentences:
s0 "Six billion dollars, gone in minutes"  -> coins stream from Binance hot wallets to attacker wallets, counter to $6.3B
s1 "Hackers just hit Binance..."           -> HACKED stamp, WITHDRAWALS PAUSED badge
s2 "...largest crypto theft in history"    -> scene switches to a bar chart of the biggest crypto hacks"""
import json
from pathlib import Path

V = Path(__file__).parent
S1 = json.load(open(V / "work" / "sentences.json"))[0]
s0, s1, s2 = S1[0][0], S1[1][0], S1[2][0]
A = round(S1[-1][1] + 0.5, 2)
RED, AMB, INK, CARD, TXT, SOFT = "#FF5A47", "#F2B04E", "#11151B", "#1C222B", "#F2EEE6", "#8B95A5"

css, el = [], []
# --- scene 1: wallets ---
L, R, TOP, BOT = (60, 320), (568, 828), 250, 610
el.append('<g class="sc1">')
for (x0, x1), name, cls in [(L, "BINANCE HOT WALLETS", "drain"), (R, "ATTACKER WALLETS", "fill")]:
    el.append(f'<text x="{(x0+x1)/2}" y="{TOP-22}" text-anchor="middle" style="font:800 22px Inter,Arial;letter-spacing:2px;fill:{SOFT}">{name}</text>')
    el.append(f'<rect x="{x0}" y="{TOP}" width="{x1-x0}" height="{BOT-TOP}" rx="22" fill="{CARD}" stroke="#2C3340" stroke-width="3"/>')
    col = AMB if cls == "drain" else RED
    el.append(f'<rect class="{cls}" x="{x0+14}" y="{TOP+14}" width="{x1-x0-28}" height="{BOT-TOP-28}" rx="14" fill="{col}" '
              f'style="transform-origin:{(x0+x1)/2}px {BOT-14}px"/>')
el.append(f'<text x="{(L[0]+L[1])/2}" y="{TOP+70}" text-anchor="middle" style="font:900 40px Inter,Arial;fill:{TXT};paint-order:stroke;stroke:{INK};stroke-width:6px">BINANCE</text>')
el.append(f'<text class="qm" x="{(R[0]+R[1])/2}" y="{(TOP+BOT)/2+30}" text-anchor="middle" style="font:900 110px Inter,Arial;fill:{INK}">?</text>')
css.append(f".drain{{animation:drain {2.2}s cubic-bezier(.3,0,.4,1) both;animation-delay:{s0+0.1}s}}@keyframes drain{{to{{transform:scaleY(.08)}}}}")
css.append(f".fill{{transform:scaleY(0);animation:fillb {2.2}s cubic-bezier(.3,0,.4,1) both;animation-delay:{s0+0.4}s}}@keyframes fillb{{from{{transform:scaleY(0)}}to{{transform:scaleY(.92)}}}}")
css.append(f".qm{{opacity:0;animation:fadein .4s ease both;animation-delay:{s0+1.6}s}}")
# coin stream
path = f"M{L[1]-10} {TOP+120} C {L[1]+70} {TOP-90}, {R[0]-70} {TOP-90}, {R[0]+10} {TOP+120}"
syms = ["₿", "Ξ", "$", "Ξ", "$", "₿"]
end = s2 - 0.4
n = 26
for i in range(n):
    d = round(s0 + 0.15 + i * (end - 0.9 - s0) / n, 2)
    el.append(f'<g class="coin" style="offset-path:path(\'{path}\');animation-delay:{d}s"><circle r="24" fill="{AMB}" stroke="{INK}" stroke-width="3"/>'
              f'<text y="9" text-anchor="middle" style="font:900 26px Inter,Arial;fill:{INK}">{syms[i % 6]}</text></g>')
css.append(".coin{offset-distance:0%;offset-rotate:0deg;opacity:0;animation:coin .9s cubic-bezier(.4,0,.6,1) both}"
           "@keyframes coin{0%{offset-distance:0%;opacity:0}10%{opacity:1}90%{opacity:1}100%{offset-distance:100%;opacity:0}}")
# counter 0.0 -> 6.3 with ease-out timing
cx = 444
el.append(f'<text x="{cx}" y="70" text-anchor="middle" style="font:800 24px Inter,Arial;letter-spacing:4px;fill:{SOFT}">DRAINED</text>')
c0, c1 = s0 + 0.15, s0 + 2.1
vals = [i / 10 for i in range(64)]
for i, v in enumerate(vals):
    t = c0 + (c1 - c0) * (1 - (1 - i / 63) ** 2)
    t2 = c0 + (c1 - c0) * (1 - (1 - (i + 1) / 63) ** 2) if i < 63 else None
    last = i == 63
    dur = round((t2 - t), 3) if not last else 0.1
    el.append(f'<text class="cnt{" last" if last else ""}" x="{cx}" y="150" text-anchor="middle" '
              f'style="font:900 92px Inter,Arial;fill:{RED};animation-delay:{t:.3f}s;animation-duration:{max(dur, .001)}s">${v:.1f}B</text>')
css.append(".cnt{opacity:0;animation-name:cnt;animation-timing-function:steps(1);animation-fill-mode:none}"
           "@keyframes cnt{0%,100%{opacity:1}}.cnt.last{animation-fill-mode:forwards}")
# HACKED stamp + paused badge
hx, hy = (L[0] + L[1]) / 2, (TOP + BOT) / 2
el.append(f'<g class="hk" style="transform-origin:{hx}px {hy}px"><rect x="{hx-150}" y="{hy-48}" width="300" height="96" rx="12" fill="{INK}" '
          f'stroke="{RED}" stroke-width="7"/><text x="{hx}" y="{hy+22}" text-anchor="middle" style="font:900 60px Inter,Arial;letter-spacing:6px;fill:{RED}">HACKED</text></g>')
css.append(f".hk{{opacity:0;animation:stmp .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:{s1+0.25}s}}"
           "@keyframes stmp{from{opacity:0;transform:scale(1.9) rotate(-10deg)}to{opacity:1;transform:rotate(-6deg)}}")
el.append(f'<g class="pz"><rect x="{444-230}" y="{BOT+40}" width="460" height="64" rx="32" fill="{RED}"/>'
          f'<text x="444" y="{BOT+82}" text-anchor="middle" style="font:900 30px Inter,Arial;letter-spacing:3px;fill:{INK}">WITHDRAWALS PAUSED</text></g>')
css.append(f".pz{{opacity:0;animation:rise2 .45s cubic-bezier(.2,.7,.2,1) both;animation-delay:{s1+1.6}s}}"
           "@keyframes rise2{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:none}}")
el.append("</g>")
css.append(f".sc1{{animation:out .35s ease both;animation-delay:{s2-0.25}s}}@keyframes out{{to{{opacity:0}}}}")

# --- scene 2: biggest crypto hacks ---
rows = [("Ronin · 2022", 0.6, SOFT, "$0.6B"), ("Bybit · 2025", 1.4, SOFT, "$1.4B"), ("Binance · 2026", 6.3, RED, "~$6.3B*")]
el.append('<g class="sc2">')
el.append(f'<text x="60" y="110" style="font:800 30px Inter,Arial;letter-spacing:4px;fill:{AMB}">BIGGEST CRYPTO HACKS</text>')
for i, (lab, v, col, txt) in enumerate(rows):
    y = 200 + i * 170
    w = 480 * v / 6.3
    dl = s2 + 0.35 + i * 0.35
    el.append(f'<text x="60" y="{y}" style="font:700 34px Inter,Arial;fill:{TXT}">{lab}</text>')
    el.append(f'<rect class="bar" x="60" y="{y+22}" width="{w:.0f}" height="72" rx="10" fill="{col}" style="animation-delay:{dl:.2f}s"/>')
    el.append(f'<text class="bv" x="{60+w+18:.0f}" y="{y+72}" style="font:900 44px Inter,Arial;fill:{col};animation-delay:{dl+0.5:.2f}s">{txt}</text>')
el.append(f'<text x="60" y="720" style="font:500 22px Inter,Arial;fill:{SOFT}">*Binance estimate, not final · Ronin and Bybit hacks blamed on North Korea</text>')
el.append(f'<g class="rec" style="transform-origin:700px 98px"><rect x="575" y="60" width="250" height="78" rx="12" fill="{INK}" stroke="{AMB}" stroke-width="6"/>'
          f'<text x="700" y="114" text-anchor="middle" style="font:900 44px Inter,Arial;letter-spacing:4px;fill:{AMB}">RECORD?</text></g>')
el.append("</g>")
css.append(f".sc2{{opacity:0;animation:fadein .35s ease both;animation-delay:{s2-0.1}s}}@keyframes fadein{{to{{opacity:1}}}}")
css.append(".bar{transform:scaleX(0);transform-box:fill-box;transform-origin:left;animation:barg .7s cubic-bezier(.2,.7,.2,1) both}"
           "@keyframes barg{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
           ".bv{opacity:0;animation:fadein .3s ease both}")
css.append(f".rec{{opacity:0;animation:stmp .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:{s2+1.7:.2f}s}}")

svg = (f'<svg viewBox="0 0 888 760" width="888" height="760" aria-label="Animation: billions drained from Binance; biggest crypto hacks compared" '
       f'style="border-radius:20px;background:#0B0F15;overflow:hidden">{"".join(el)}</svg>')
(V / "scene.svg").write_text(svg, encoding="utf-8")
(V / "scene.css").write_text("\n".join(css), encoding="utf-8")
print("A", A, s0, s1, s2)
