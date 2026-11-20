import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
D = Path(__file__).parent
shots = [(1, 0.0), (1, 2.9), (1, 3.5), (1, 6.5), (2, 3.1), (3, 3.1), (4, 3.1), (5, 3.1)]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto(f"file://{D}/slides.html")
    for i, t in shots:
        pg.evaluate("i => { document.querySelectorAll('.s').forEach(e => e.classList.remove('on')); document.getElementById('s'+i).classList.add('on'); }", i)
        pg.wait_for_timeout(100)
        print(i, "overflow", pg.evaluate("i => { const e=document.getElementById('s'+i); return e.scrollHeight-e.clientHeight }", i))
        pg.evaluate("t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t })", t * 1000)
        pg.screenshot(path=str(D / "chk" / f"p{i}_{t}.jpg"), type="jpeg", quality=85)
    b.close()
