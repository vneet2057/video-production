# MASTER PROMPT: Vertical News Explainer Videos for TikTok

> **Runs locally on my Mac with Claude Code** in `~/Desktop/video production` (see `CLAUDE.md`). Open a session there and say:
> **"Today's topic is: ___"** (or "find today's hot topics first"). Tools are installed by `./setup.sh`; start each video with `./new-video.sh topic-slug`.
> Run every Python script with the project venv: `../../.venv/bin/python script.py` from inside the video folder.
> Everything below is the exact workflow, rules, voice setup and code we used to make the
> Irkutsk plague, Noah's Ark, October cyber-attacks, Korea bank hacks, Iran War Parts 1–4, and the
> "World stockpile" video (world map camera + Unsplash stock photos), the **US Vote 2026 explainer** (our best video so far:
> ~12k Facebook views in 12 hours) and the **"Hackers turned freezers into ovens"** cyber explainer.
> **Current focus: world affairs** (the Iran war and global news), plus **explainers of big, confusing news** on any topic
> (elections, cyber attacks, human stories). Wars stay on every topic list, but don't pick only wars.
> **My Unsplash Access Key** is in `.env` at the project root (not in git). Load it when running stock scripts: `set -a; . ../../.env; set +a`. Use it only for Unsplash.

---

## 1. Who I am and what we make

- My channel is **Nexcium Explains**: short **news explainer videos**, posted on three platforms:
  - **Facebook Reels** (Page "Nexcium Explains"): my main platform and earner right now.
  - **YouTube Shorts** (**@nexcium_explains**, started 5 November 2026): long-term growth, search traffic, monetization.
  - **TikTok** ("Nexcium Explains"): same videos, keep posting.
- Format: **vertical 1080×1920**, animated text slides, **male AI voice-over (am_fenrir, fast)**, animated SVG map hook, my own images/clips and **Unsplash stock photos** cut in, labelled honestly.
- Target length: **61–66 seconds** (one story, 6–7 slides). Must be OVER 1 minute: TikTok Creator Rewards only pays for videos longer than 1 minute. Our 82 s vote video lost most viewers in the middle, so trim before going past ~70 s. Longer explainers (2–3 min) only when I ask.
- **Cover / first frame:** Facebook and TikTok use the first frame as the default cover, so the hook slide's headline, badge and map must be fully visible at frame 0 (no fade-in on them). Also export a cover JPG (best hook frame) for me to set as the custom cover.
- **What gets views (my Facebook data):**
  - **Best so far: US Vote 2026 explainer, 11,947 views / 10,770 viewers in ~12 h** (previous best: Russia + North Korea missile tests 1.2k; stockpile 471). Money/tech stories (AI bubble, crypto) did worse.
  - Why it worked: huge news that people found confusing (who are Democrats/Republicans, what are the House and Senate), explained simply; a **divisive topic delivered neutrally**, so both sides could watch and share it safely (0.00% hide rate); posted while results were still breaking; hook named a person + result ("Trump's party just lost Congress").
  - Reach came from the algorithm, not followers: **99.8% non-followers, 99.6% from the Reels feed**. Facebook tested it for ~8 h, then it spiked. 17 new follows.
  - Engagement was modest: 84 reactions (4 angry), 8 comments, 7 shares, 0.70% like rate. It was NOT a comment war; Facebook spread it because people stopped to watch.
  - **My Facebook audience: 84% are 55+ (54.6% are 65+), mostly men.** Write for older men who follow world affairs: clear, calm, big text, plain words, explain the basics.
  - **Weak spot = the first 2 seconds:** Facebook's biggest drop-off was at **0:02**. Only 58% of views reached 3 s (6,964 of 11,947); average watch 16 s (19% of the video); 16.9% reached 20 s; 923 (8%) reached 1 minute.
  - Formula to repeat: big divisive or confusing story → neutral, both sides fairly → explain the basics → key fact in the first 10 s → end with a question that invites opinions + a share line.
- **Upload quality:** after the final render, re-export for upload at 1080×1920, 30 fps, ~8 Mbps so Facebook treats it as HD: run `kit/export-1080p.sh work/NAME-final.mp4 NAME` (output goes to `exported/`; same as `ffmpeg -i final.mp4 -c:v libx264 -preset medium -profile:v high -level 4.2 -pix_fmt yuv420p -r 30 -b:v 8M -minrate 8M -maxrate 8M -bufsize 16M -x264-params nal-hrd=cbr -g 60 -c:a aac -b:a 192k -ar 48000 -movflags +faststart -tag:v avc1 NAME-1080p.mp4`). The `nal-hrd=cbr` part is required: without it x264 drops static slides to ~1.4 Mbps even with `-b:v 8M` (tested on this Mac, 19 Nov 2026). (CRF output of static slides is only ~1 Mbps and Facebook flagged it as below 720p.) Expect ~60 MB per minute. The script also writes a **720p** copy (720×1280, ~5 Mbps CBR) for previews/quick sharing; **upload the 1080p** on all three platforms (sharper text after the platforms re-encode, and it is their recommended size). Resolution is not why views drop: when views fall, look at the 3-second hold, the first 2 seconds and the topic (ask me for analytics).
  - **ALWAYS do this, on every video, no exceptions.** Reason (from me): the US Vote 2026 video, our best ever, was exported as a heavy, high-quality file in an earlier session, and I believe that is part of why it went viral. A light, low-bitrate file looks soft and Facebook can flag it as low quality.
  - **The -1080p file is the file I get.** Never make only a smaller or compressed version (-small, ~3 Mbps) in its place. Make the -1080p with the script above (it runs `ffprobe` to confirm 1080x1920, 30 fps and the real video bitrate), and tell me the full path, size and bitrate.
  - Files are saved locally in the video's folder (`videos/YYYY-MM-DD-slug/`), so there is no size limit: never shrink the upload file. Give me the clickable path to the -1080p file and the cover JPG.
  - If I send you the settings or file of a past high-performing video, match them.
- Always turn on the **AI-generated** label (AI voice); self-labelling doesn't cut reach, not labelling risks penalties.
- **No more numbered series.** "Iran War · Part 8" (Trump admits the war cost him Congress, 5 Nov 2026) was the **last numbered part**. From now on every video is a standalone story: no "Part N" badge, no "Follow for part …". Use a topic badge instead ("Iran war", "US politics", "Cyber attack", "World news").
- **Every video ends with "Follow for more."** Default last line: "Let's see what happens. Follow for more." (a share line is fine too: "Share this with someone who needs it. Follow for more.").

## 1b. Decisions we made on 5 November 2026, and why
- **Why no more parts:** new viewers find us through the algorithm (99.8% non-followers on Facebook) and through YouTube search, not by following a series. "Part 8" tells a newcomer they missed seven videos; a standalone story with "Follow for more" works for everyone. Old parts stay in a YouTube playlist ("Iran War: the full series").
- **Why we keep the calm, explainer style:** our audience is older. On Facebook **84% of viewers are 55+** (54.6% are 65+), mostly men, and they like slower, clear content that explains the basics. That is what is working:

  | Video | Facebook | TikTok |
  |---|---|---|
  | US Vote 2026 explainer | 13k | 600 |
  | Hackers turned freezers into ovens | 8.9k | 481 |
  | Iran War Part 8 (Trump clip hook) | 5.1k (first hours) | 146 |
  | Iran War Part 7 / Part 6 | 308 / 321 | 407 / 388 |

- **TikTok:** it hasn't taken off like Facebook (every video stays at ~150–600 views, i.e. TikTok's first test batch). Its audience is younger and prefers fast cuts and faces. **We keep posting the same videos to TikTok and do NOT change the style for it now.** Later, when we decide it's needed (not today or tomorrow), we may make a separate faster "TikTok cut". Don't change the format for TikTok unless I ask.
- **YouTube:** added because its viewers skew older, news explainers do well in search, and videos keep getting views for months. Monetization: 1,000 subscribers + 4,000 watch hours (12 months) or 10M Shorts views (90 days); from 1 Feb 2027 new applicants need 8,000 hours or 20M Shorts views. A weekly longer video (8–10 min) built from our slides is the faster route to watch hours, when I ask for it.

## 2. The workflow (do it in this order)

1. **Find topics** (if I ask): search today's news (last 24 hrs), then rank **10 stories** by TikTok/Facebook potential: keep wars on the list, but include elections, cyber, tech/AI, human stories, disasters and other world news. For each: one-line summary, why it gets views, a hook idea. Recommend one or two. Flag sensitive or graphic ones, and ones only one source reports. Skip anything I've already covered.
2. **Research the chosen story**: search first, always. Read at least 2–3 sources. Build a dated timeline. Note where sources **disagree** (dates, numbers) and don't state a number that sources conflict on. Present unverified claims as claims ("Iran says…", "America says that's false").
3. **Write the narration**: one short paragraph per scene, ~10 scenes (see §4 and §7c). Start a folder with `./new-video.sh topic-slug`.
4. **Generate the voice** with Kokoro (§6): `narrate.py` times every sentence (`work/sentences.json`). Set `ANIMS` here only.
5. **Build the slides** with `make_slides.py` (fast template, §7c): reveals timed to the voice with `at(slide, sentence)`, my photos inside the slides with Ken Burns movement.
6. **Render** with `render.py` (Playwright frames + ffmpeg xfade + voice, §8).
7. **Optional inserts**: `photos.py` for panels/full-screen cutaways (§9), a GIF/video I send plays **inside the slide as a panel** (§9b), Unsplash stock (§9c).
8. **Finish** with `finish.py`: burned-in 3-word captions + whoosh on every cut + a hit on stamps (§7c).
9. **Check** a contact sheet of frames (hook at 0 s, every reveal, every insert): no text overflow, labels visible, captions readable, content above y≈1400.
10. **Export** with `../../kit/export-1080p.sh work/NAME-final.mp4 NAME [cover-seconds]` → `exported/NAME-1080p.mp4` (the upload file), `NAME-720p.mp4`, `NAME-cover.jpg`. **Open the 1080p in QuickTime Player** (`open -a "QuickTime Player" file`) when done.
11. **Report**: what's on screen with timestamps, image labels, anything uncertain, sources.
    When I paste analytics, compare them with the numbers in §1 and suggest what to change; update §1 when I ask.
12. **Posting pack** (§10): save `exported/posting-pack.md` and, when I ask, paste it in chat **per platform, each field in its own code block** (so I can copy it): TikTok caption, Facebook title + description, YouTube title + description + tags, pinned comment. **Comment replies** when I paste comments (§11).

## 3. Editorial rules (non-negotiable)

- **Hook first, always, and win the first 2 seconds** (our biggest drop-off is at 0:02):
  - First spoken line **under 2 seconds**, 4–7 words, naming a person/place + result: "Trump just lost Congress." / "Hackers turned freezers into ovens."
  - **Something is already moving at frame 0** (counter ticking, map moving, dots flipping). A busy still chart at frame 0 loses people.
  - The on-screen headline matches the hook word for word and is fully visible at frame 0 (many people scroll with the sound off).
  - The key fact lands in the **first 10 seconds**; then explain.
- **Neutral on politics and wars.** Show each side's position side by side. No winners, no opinions, no loaded words. Quote leaders accurately and attribute ("the president said, quote…").
- **Divisive topic, neutral delivery.** Pick stories people already argue about (elections, Trump, Israel/Iran, Russia/Ukraine), but never take a side: neutral is what lets both sides share it. Let the debate happen in the comments, not in the video. Use party colours (blue/red) only in data graphics; keep the slide palette neutral.
- **Explain the basics** for a general, older audience: who the sides are, what the institution is, how it works, before what changed (e.g. "Congress is America's lawmaking body… Republicans are Trump's party…").
- **Don't invent anything.** No made-up numbers or quotes. If sources conflict, leave the number out or say "sources differ".
- **Label every image honestly** in a small box top-left: `file photo`, `Illustration` (AI/edited art), `Illustrative photo` (real photo, unverified place/date), `Stock footage`, `Stock photo · Photographer / Unsplash`, `Unverified footage: date and place not confirmed` (viral clips), or a real caption like "Strait of Hormuz from space". AI-made images that look real must say they're not real. Stock images must never look like footage of the actual event (use generic places/things: a city, Mount Fuji, power lines, a pantry).
- **No graphic violence** (TikTok limits reach). No content that targets private people.
- End with sources on the last slide (small text) and list them in chat.

## 4. Narration writing rules (these fixed real problems)

- **Never use abbreviations with full stops.** "U.S." made the voice say "U … S" because the script splits sentences at every full stop. Write **"United States"** or **"American"**. Same for "Dr.", "St.", "a.m.", etc.
- Write numbers and dates **as words**: "February twenty-eighth", "a hundred and eighteen dollars", "November third".
- Spell out acronyms the voice should say letter by letter with spaces: "P H P", "N S A", "Node J S". Respell tricky names phonetically: "e Mudra" (eMudhra), "Light L L M" (LiteLLM), "Eerkootsk" (Irkutsk).
- Short, punchy sentences. One idea per sentence. ~185–200 words for a 61–70 second video.
- **Ending for every video:** "Let's see what happens. Follow for more." (or a share line: "Share this with someone who needs it. Follow for more."). Never "Follow for part …". Shares count more than likes, so ask for them.
- If a word is mispronounced, fix it in the `FIX` list in narrate.py (IPA override), e.g. "Iran" was heard as "ran", so we force `aɪɹˈɑːn`.

## 5. Visual style

- Canvas 1080×1920, padding `130px 96px 120px`. Fonts (macOS): **Inter / Inter Display** (headings 800 weight; `brew install --cask font-inter`, files in `~/Library/Fonts`), **Charter** for quotes (built into macOS). ffmpeg labels use `FONT = str(Path.home() / "Library/Fonts/Inter-SemiBold.otf")`.
- Palette per topic (pick one; dark/light/accent alternate slide to slide):
  - Iran/oil: dark `#11151B`, light `#F2EEE6`, amber `#E39B2D`/`#F2B04E`, accent dark-amber `#A8620C`, danger red `#E25D4B`
  - Cyber: dark `#0B1020`, light `#EEF1F6`, red `#C8323A`/`#FF6B70`, glitch cyan `#3DD6F5`
  - History/ark: navy `#0F1B2D`, cream `#F3ECDD`, gold `#C9892B`/`#E0A546`
- Slide types we reuse: **hook** (big headline + topic badge, e.g. "Iran war", + optional animated SVG map), **timeline** (vertical line that grows, dots, dated events), **vs cards** ("Iran says" / "The United States says"), **stat grid** (big numbers), **quote** (serif), **three outcomes** (cards), **CTA** ("Let's see what happens" + "Follow for more" stamps).
- **Layout rule: keep content in the top ~70% of every content slide.** Use `justify-content:flex-start;gap:90px` on content slides (cards, stats, timelines) so they sit under the heading. Leave the bottom ~25% clear for burned-in captions and TikTok's caption/buttons. Don't push cards to the bottom with `space-between`.
- **Panel area:** the empty space between the last card and y≈1550 is where embedded clips/stock photos go (x=96, width 888, height 400–530 depending on the slide), with a 5–6 px amber (or red for unverified footage) border and a small label top-left inside the panel.
- Transitions between slides (ffmpeg xfade): `slideup`, `smoothleft`, `circleopen`, `smoothup`, `pixelize` (cyber), `fade`.

## 6. Voice setup (Kokoro TTS, male voice)

- Model: **Kokoro v1.0 ONNX**. Voice: **`am_fenrir`** (deep male, current default). Alternatives: `am_michael` (used for Iran Part 1), `am_puck` (younger), `bm_george` (British). Female `af_heart` was used early on and I didn't want it.
- Speed: **1.32** (fast, punchy) for TikTok. Gap between sentences: 0.09 s.
- **A/B test speed 1.2 on Facebook:** 84% of my Facebook viewers are 55+, and 1.32 may be too fast for them. Run `../../.venv/bin/python narrate.py am_fenrir 1.2` for a Facebook version and compare retention.
- Setup on this Mac is done by `./setup.sh` (safe to re-run): Homebrew `ffmpeg` + `espeak-ng` (gives the IPA phonemes Kokoro needs) + `font-inter`, a Python venv at `.venv/` (numpy, onnxruntime, playwright + Chromium), the Kokoro ONNX model files in `tts/` (kokoro-v1.0.onnx, voices-v1.0.bin, config.json, from github.com/thewh1teagle/kokoro-onnx), and country outlines in `geo/wgj/`. We run the ONNX model directly (no kokoro-onnx package needed).
- Speed on this Mac (Apple Silicon): voice for a ~55 s video ≈ 40 s, frame render ≈ 55 s.

Folder layout: `tts/` and `geo/` at the project root (scripts search parent folders for them), one folder per video in `videos/YYYY-MM-DD-slug/` holding `slides.html`, `narrate.py`, `render.py`, `photos.py`.

Video folder layout (made by new-video.sh): scripts + `slides.html` at the top; `in/` my photos/clips; `work/` voice, timing JSON, frames and draft MP4s (scripts write here); `exported/` only the deliverables: `NAME-1080p.mp4` (upload file), `NAME-cover.jpg`, `posting-pack.md`; `chk/` check frames.

## 7. Slide template (slides.html)

Each slide is `<div class="s dark|light|amber" id="sN">`. Only the slide with class `on` shows (render.py toggles it). Animate children with classes `.a` (rise), `.z` (zoom), `.x` (slide in), `.stamp`, and stagger with `style="--d:.5s"`. Keep all animations inside the first ~2.5 s (3.2 s is captured; the last frame is then held while the voice continues). **Long animations** (e.g. a map that moves with the narration for the whole hook) get a longer capture: set that slide's entry in `ANIMS` (e.g. `ANIMS = [10.8, 3.2, 3.2, 3.2, 3.2, 3.2]`) in both narrate.py and render.py.

```html
<!doctype html>
<html><head><meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#000;font-family:'Inter',Arial,sans-serif;width:1080px;height:1920px;overflow:hidden}
.s{display:none;width:1080px;height:1920px;padding:130px 96px 120px;flex-direction:column;justify-content:space-between;gap:56px;overflow:hidden;position:relative}
.s.on{display:flex}
.dark{background:#11151B;color:#F2EEE6}
.light{background:#F2EEE6;color:#11151B}
.amber{background:#E39B2D;color:#11151B}
.eyebrow{font-size:28px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:#A8620C}
.dark .eyebrow{color:#F2B04E}.amber .eyebrow{color:#11151B}
.part{display:inline-block;font-size:30px;font-weight:800;letter-spacing:3px;text-transform:uppercase;background:#F2B04E;color:#11151B;padding:12px 22px;border-radius:10px}
h1{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:124px;line-height:1.02;letter-spacing:-2px}
h2{font-family:'Inter Display','Inter',sans-serif;font-weight:700;font-size:82px;line-height:1.08;letter-spacing:-1px}
h3{font-size:44px;font-weight:700;line-height:1.2}
p,li{font-size:40px;line-height:1.4}
.lead{font-size:52px;line-height:1.3}
.soft{color:#505866}.dark .soft{color:#B5BDC9}.amber .soft{color:#3A3020}
.small{font-size:28px}
.hl{color:#F2B04E}.light .hl{color:#A8620C}
.head{display:flex;flex-direction:column;gap:28px}
.stack{display:flex;flex-direction:column;gap:30px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.card{background:#1C222B;border-radius:20px;padding:40px 44px;display:flex;flex-direction:column;gap:14px;border-left:6px solid #F2B04E}
.light .card{background:#FFFFFF;border-left-color:#A8620C}
.amber .card{background:#F4C981;border-left-color:#11151B}
.flag{font-size:30px;font-weight:800;letter-spacing:2px;text-transform:uppercase}
/* timeline */
.tl{position:relative;display:flex;flex-direction:column;gap:46px;padding-left:64px}
.tl .line{position:absolute;left:11px;top:14px;bottom:14px;width:4px;background:#A8620C;transform-origin:top;animation:grow 2.2s cubic-bezier(.3,.6,.2,1) both;animation-delay:.4s}
.dark .tl .line{background:#F2B04E}
.ev{position:relative;display:flex;flex-direction:column;gap:6px}
.ev::before{content:"";position:absolute;left:-64px;top:8px;width:26px;height:26px;border-radius:50%;background:#A8620C}
.dark .ev::before{background:#F2B04E}.amber .ev::before{background:#11151B}
.ev b{font-size:34px;font-weight:700;letter-spacing:1px;color:#A8620C}
.dark .ev b{color:#F2B04E}
.ev span{font-size:40px;line-height:1.32}
/* stats */
.stats{display:grid;grid-template-columns:1fr 1fr;gap:56px 40px}
.stat .n{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:116px;line-height:1;color:#A8620C;letter-spacing:-2px}
.dark .stat .n{color:#F2B04E}
.stat .l{font-size:32px;line-height:1.3}
.quote{font-family:'Charter','Bitstream Charter',Georgia,serif;font-size:76px;line-height:1.15}
/* animations */
.a{animation:rise .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}
.z{animation:zoom .6s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,.3s)}
.x{animation:slide .55s cubic-bezier(.2,.7,.2,1) both;animation-delay:var(--d,.3s)}
.stamp{animation:stamp .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:var(--d,1s)}
.draw{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.8s ease-in-out both;animation-delay:var(--d,.4s)}
@keyframes rise{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
@keyframes zoom{from{opacity:0;transform:scale(.8)}to{opacity:1;transform:none}}
@keyframes slide{from{opacity:0;transform:translateX(-60px)}to{opacity:1;transform:none}}
@keyframes stamp{from{opacity:0;transform:scale(1.8) rotate(-8deg)}to{opacity:1;transform:rotate(-4deg)}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes draw{to{stroke-dashoffset:0}}
</style></head><body>

<!-- HOOK -->
<div class="s dark" id="s1">
<div><p class="part a" style="--d:.15s">Iran war</p></div>
<div class="stack" style="gap:44px">
<h1 class="z" style="--d:.3s">Iran: Hormuz is <span class="hl">"completely closed."</span></h1>
<h1 class="z" style="--d:1.2s;font-size:96px">America: <span class="hl">not true.</span></h1>
</div>
<p class="small soft a" style="--d:1.6s">27 October 2026</p>
</div>

<!-- VS CARDS -->
<div class="s light" id="s2">
<div class="head"><p class="eyebrow a" style="--d:.2s">The claim</p><h2 class="a" style="--d:.3s">Who controls the strait?</h2></div>
<div class="vs">
<div class="card x" style="--d:.5s"><p class="flag">Iran says</p><p class="soft">Its forces fully control the strait</p></div>
<div class="card x" style="--d:.8s"><p class="flag">The United States says</p><p class="soft">The claim is false</p></div>
</div>
<p class="lead a" style="--d:1.3s">Traffic is <span class="hl">way down</span>, but not zero.</p>
</div>

<!-- TIMELINE -->
<div class="s light" id="s3">
<div class="head"><p class="eyebrow a" style="--d:.2s">Timeline</p><h2 class="a" style="--d:.35s">Truces that didn't hold</h2></div>
<div class="tl"><div class="line"></div>
<div class="ev x" style="--d:.55s"><b>March</b><span>Iran closes the Strait of Hormuz</span></div>
<div class="ev x" style="--d:.8s"><b>April</b><span>Ceasefire agreed; blockade begins</span></div>
</div>
<p class="small soft a" style="--d:1.8s">Sources differ by a few days on some dates</p>
</div>

<!-- CTA -->
<div class="s dark" id="s4">
<div class="head"><p class="eyebrow a" style="--d:.2s">Today</p><h2 class="a" style="--d:.3s">Israel votes</h2></div>
<p class="lead a" style="--d:1.1s">This week matters.</p>
<div><p class="part stamp" style="--d:1.5s">Follow for more</p></div>
<p class="small soft a" style="--d:1.7s">Sources: …</p>
</div>
</body></html>
```

### Animated SVG map (used for the Hormuz hook)
`build_map.py` draws real coastlines from (longitude, latitude) points with an equirectangular projection, then animates: shipping lane draws in → tankers sail along the lane (CSS `offset-path` + `offset-distance`) and queue → red barrier line draws across the narrowest point → ✕ pops → "BLOCKED" stamp. Label it "Map simplified". Insert the generated `map.svg` into the hook slide inside `<div style="position:relative">` with `<p class="blocked" style="top:560px">BLOCKED</p>`. Extra CSS needed:

```css
.ship{offset-distance:0%;animation:sail 2.2s cubic-bezier(.3,.6,.3,1) both;animation-delay:var(--d,.2s)}
@keyframes sail{from{offset-distance:0%}to{offset-distance:var(--end)}}
.lane{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1s ease-out both;animation-delay:.1s}
.barrier{stroke-dasharray:1;stroke-dashoffset:1;animation:draw .5s ease-out both;animation-delay:1.6s}
.xmark{animation:pulse .7s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:2s}
@keyframes pulse{0%{opacity:0;transform:scale(.2)}70%{opacity:1;transform:scale(1.2)}100%{opacity:1;transform:scale(1)}}
.blocked{position:absolute;left:50%;transform:translateX(-50%);font:900 64px Inter,Arial;letter-spacing:8px;color:#E25D4B;border:6px solid #E25D4B;padding:6px 26px;border-radius:12px;background:rgba(17,21,27,.85);animation:stamp2 .5s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:2.3s}
@keyframes stamp2{from{opacity:0;transform:translateX(-50%) scale(1.8) rotate(-8deg)}to{opacity:1;transform:translateX(-50%) rotate(-4deg)}}
```

```python
# build_map.py — Strait of Hormuz map from approximate real coastline coordinates (lon, lat)
import math
from pathlib import Path

LON0, LON1, LAT0, LAT1 = 54.3, 58.3, 23.9, 27.7
W = 888
KX = W / ((LON1 - LON0) * math.cos(math.radians(26)))
H = round((LAT1 - LAT0) * KX)

def xy(lon, lat):
    return ((lon - LON0) * math.cos(math.radians(26)) * KX, (LAT1 - lat) * KX)

def path(pts, close=True):
    p = [xy(*q) for q in pts]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in p)
    return d + (" Z" if close else "")

IRAN = [(54.0, 26.62), (54.6, 26.5), (54.9, 26.55), (55.2, 26.62), (55.6, 26.86), (55.95, 27.02),
        (56.27, 27.19), (56.55, 27.13), (56.85, 27.0), (57.05, 26.7), (57.2, 26.2), (57.35, 25.85),
        (57.77, 25.65), (58.2, 25.58), (58.6, 25.58), (58.6, 28.0), (54.0, 28.0)]
QESHM = [(55.3, 26.66), (55.6, 26.76), (55.95, 26.88), (56.28, 26.98), (56.24, 26.86), (55.95, 26.74),
         (55.6, 26.62), (55.35, 26.58)]
HORMUZ_IS = [(56.43, 27.09), (56.5, 27.1), (56.5, 27.03), (56.43, 27.03)]
LARAK = [(56.33, 26.88), (56.39, 26.89), (56.39, 26.83), (56.33, 26.83)]
ARABIA = [(54.0, 24.15), (54.37, 24.47), (54.7, 24.75), (55.0, 24.98), (55.27, 25.27), (55.45, 25.38),
          (55.75, 25.6), (55.95, 25.8), (56.08, 26.05), (56.2, 26.22), (56.35, 26.38), (56.42, 26.35),
          (56.48, 26.2), (56.42, 26.0), (56.33, 25.8), (56.27, 25.62), (56.35, 25.33), (56.36, 25.05),
          (56.5, 24.75), (56.75, 24.4), (57.1, 24.1), (57.6, 23.85), (58.3, 23.65), (58.6, 23.6),
          (58.6, 23.0), (54.0, 23.0)]

LAND, STROKE = "#3A3226", "#C9A66B"
lane = path([(58.3, 24.85), (57.4, 25.3), (56.75, 26.25), (56.55, 26.55), (56.2, 26.6), (55.6, 26.25),
             (54.8, 25.7), (54.3, 25.4)], close=False)
bx1, by1 = xy(56.42, 26.36)
bx2, by2 = xy(56.6, 27.0)
cx, cy = (bx1 + bx2) / 2, (by1 + by2) / 2

def label(lon, lat, text, size=30, color="#F2EEE6", weight=700, spacing=4, italic=False):
    x, y = xy(lon, lat)
    st = "font-style:italic;" if italic else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" style="font:{weight} {size}px Inter,Arial;'
            f'letter-spacing:{spacing}px;fill:{color};{st}">{text}</text>')

ships = []
for end, delay in [(0.47, 0.2), (0.41, 0.45), (0.35, 0.7)]:
    ships.append(f'<path class="ship" style="offset-path:path(\'{lane}\');offset-rotate:auto 180deg;--end:{end*100:.0f}%;--d:{delay}s" '
                 f'd="M-16 -7 L12 -7 L20 0 L12 7 L-16 7 Z" fill="#F2B04E"/>')

svg = f'''<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" aria-label="Map of the Strait of Hormuz, shown blocked" style="border-radius:20px;background:#0E2A3E">
<path d="{path(IRAN)}" fill="{LAND}" stroke="{STROKE}" stroke-width="2"/>
<path d="{path(ARABIA)}" fill="{LAND}" stroke="{STROKE}" stroke-width="2"/>
<path d="{path(QESHM)}" fill="{LAND}" stroke="{STROKE}" stroke-width="1.5"/>
<path d="{path(HORMUZ_IS)}" fill="{LAND}" stroke="{STROKE}" stroke-width="1.5"/>
<path d="{path(LARAK)}" fill="{LAND}" stroke="{STROKE}" stroke-width="1.5"/>
<path class="lane" d="{lane}" pathLength="1" fill="none" stroke="#7FB8D8" stroke-width="4" stroke-linecap="round"/>
{''.join(ships)}
<line class="barrier" pathLength="1" x1="{bx1:.1f}" y1="{by1:.1f}" x2="{bx2:.1f}" y2="{by2:.1f}" stroke="#E25D4B" stroke-width="12" stroke-linecap="round"/>
<g class="xmark" style="transform-origin:{cx:.1f}px {cy:.1f}px"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="40" fill="#11151B" stroke="#E25D4B" stroke-width="7"/>
<path d="M{cx-18:.1f} {cy-18:.1f} L{cx+18:.1f} {cy+18:.1f} M{cx+18:.1f} {cy-18:.1f} L{cx-18:.1f} {cy+18:.1f}" stroke="#E25D4B" stroke-width="7" stroke-linecap="round"/></g>
{label(55.6, 27.4, "IRAN", 40)}
{label(55.4, 24.6, "UAE", 34)}
{label(57.6, 23.95, "OMAN", 34)}
{label(56.75, 25.75, "Musandam", 22, "#C9A66B", 600, 1)}
{label(55.0, 26.05, "Persian Gulf", 28, "#9FC4DA", 500, 1, True)}
{label(57.75, 24.75, "Gulf of Oman", 28, "#9FC4DA", 500, 1, True)}
</svg>'''
Path(__file__).with_name("map.svg").write_text(svg, encoding="utf-8")
```

### Other map types we've made (same projection idea)
- **Israel seat-meter map (Part 3):** country outline filled bottom-to-top in proportion to seats won (scanline area fill), with a "61 = majority" line.
- **Gulf missile map (Part 4):** Arabian Peninsula, Yemen, Iran outlines; curved missile tracks (`<path pathLength="1">` drawn with `.trk`), a missile dot moving with `offset-path`, a pin + pulsing rings on Ras Tanura (claimed hit), an amber ✕ on Riyadh (intercepted).
- **World map with moving camera (stockpile video):** real country outlines, camera zooms Europe → Japan → USA → whole world **timed to the narration**. See below.

### World map with a camera synced to the voice — build_map.py
Country outlines come from `git clone --depth 1 https://github.com/johan/world.geo.json geo/wgj` (works even when other downloads are blocked). Run **narrate.py first** (it writes `sentences.json`), then build_map.py, then splice `map.svg` into slide 1 and `map.css` into the `<style>`, then render. Each country lights up and its badge pops when the narrator says it; the camera moves on the same sentence times, so the picture always matches the voice. Set slide 1's `ANIMS` to the hook narration length (~11 s).

```python
import json
from pathlib import Path

V = Path(__file__).parent
S1 = json.load(open(V / "sentences.json"))[0]           # hook slide sentence times
(e1, j1, u1, w1) = (S1[0][1], S1[1][0], S1[2][0], S1[3][0])   # end of Europe sentence, start of Japan / US / "why now"
A = round(S1[-1][1] + 0.5, 2)                           # animation length = hook narration + 0.5 s
G = json.load(open(V / "geo/wgj/countries.geo.json"))
W, LAT_T, LAT_B = 888, 85, -60
H = round((LAT_T - LAT_B) / 360 * W * 2)
VW, VH = 888, 760                                       # viewport on the slide

def xy(lon, lat):
    return ((lon + 180) / 360 * W, (LAT_T - lat) / (LAT_T - LAT_B) * H)

def ring(r):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in (xy(lo, la) for lo, la in r)) + " Z"

EU = set("AUT BEL BGR HRV CYP CZE DNK EST FIN FRA DEU GRC HUN IRL ITA LVA LTU LUX MLT NLD POL PRT ROU SVK SVN ESP SWE".split())
KEY = {"GBR": 0.4, "SWE": 1.2, "FRA": 1.9, "IRL": 1.9, "NLD": 1.9, "JPN": round(j1 + 0.35, 2), "USA": round(u1 + 0.5, 2)}  # ISO3 → light-up time
paths = []
for f in G["features"]:
    iso = f["id"]
    if iso == "ATA":
        continue
    g = f["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    d = " ".join(ring(p[0]) for p in polys)
    if iso in KEY:
        paths.append(f'<path class="lit" d="{d}" style="--d:{KEY[iso]}s"/>')
    elif iso in EU:
        paths.append(f'<path class="eu" d="{d}" style="--d:1.9s"/>')
    else:
        paths.append(f'<path class="land" d="{d}"/>')

def badge(lon, lat, text, delay, dx=0, dy=0):
    x, y = xy(lon, lat)
    w = 9.2 * len(text) + 18
    return (f'<g class="bdg" style="--d:{delay}s"><rect x="{x+dx-w/2:.1f}" y="{y+dy-15:.1f}" width="{w:.1f}" height="26" rx="6" '
            f'fill="#11151B" stroke="#F2B04E" stroke-width="2"/><text x="{x+dx:.1f}" y="{y+dy+4:.1f}" text-anchor="middle" '
            f'style="font:800 15px Inter,Arial;fill:#F2B04E">{text}</text></g>')

badges = [badge(-2, 53, "UK 3 DAYS", 0.4, -38, 0), badge(16, 63, "SWEDEN 7 DAYS", 1.2, 6, -22),
          badge(10, 47, "EU 3 DAYS", 1.9, 26, 14), badge(138.5, 37, "JAPAN 3-7 DAYS", KEY["JPN"], -6, -40),
          badge(-98, 39, "US BASES 90 DAYS", KEY["USA"], 0, 0)]

def cam(lon, lat, s):            # camera centred on lon/lat at zoom s
    x, y = xy(lon, lat)
    return f"translate({VW/2 - s*x:.1f}px,{VH/2 - s*y:.1f}px) scale({s})"

over = f"translate(0px,{(VH - H)/2:.1f}px) scale(1)"
eu, jp, us = cam(10, 54, 3.4), cam(137, 38, 3.4), cam(-98, 40, 2.3)
pc = lambda t: f"{100 * t / A:.1f}%"
css = f"""
.cam{{transform-origin:0 0;animation:cam {A}s cubic-bezier(.45,0,.3,1) both}}
@keyframes cam{{0%{{transform:{eu}}}{pc(e1 - 0.35)}{{transform:{eu}}}{pc(j1 + 0.25)}{{transform:{jp}}}{pc(u1)}{{transform:{jp}}}{pc(u1 + 0.45)}{{transform:{us}}}{pc(w1)}{{transform:{us}}}{pc(min(A - 0.1, w1 + 0.8))},100%{{transform:{over}}}}}
.land{{fill:#2C3340;stroke:#11151B;stroke-width:.35}}
.eu{{fill:#2C3340;stroke:#11151B;stroke-width:.35;animation:eu .5s ease both;animation-delay:var(--d)}}
@keyframes eu{{to{{fill:#8A6A33}}}}
.lit{{fill:#2C3340;stroke:#11151B;stroke-width:.35;animation:lit .45s ease both;animation-delay:var(--d)}}
@keyframes lit{{to{{fill:#F2B04E}}}}
.bdg{{animation:bdg .4s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:var(--d);transform-box:fill-box;transform-origin:center}}
@keyframes bdg{{from{{opacity:0;transform:scale(.4)}}to{{opacity:1;transform:scale(1)}}}}
"""
svg = (f'<svg viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}" aria-label="World map" '
       f'style="border-radius:20px;background:#0E2A3E;overflow:hidden"><g class="cam">{"".join(paths)}{"".join(badges)}</g></svg>')
(V / "map.svg").write_text(svg, encoding="utf-8")
(V / "map.css").write_text(css, encoding="utf-8")
```
Check frames at the moment each country is named (e.g. 2 s, 5.3 s, 8 s, end) to confirm the camera is on the right place.

## 7c. Fast retention style (DEFAULT since 20 Nov 2026)

I asked for "much more cuts and movement" to hold viewers longer. Every video now uses the fast template (`kit/template/`, built from `kit/examples/trilateral-fast/`, our "Trump, Xi and Putin agreed on 4 things" video):

- **~10 scenes of 4–8 s** (not 5–6 long slides), transitions `F = 0.4` s (narrate.py and render.py). One idea per scene; the picture changes every ~5 s.
- **Motion at frame 0**: the hook is a full-width photo with a slow Ken Burns zoom (`.hookimg`) or an animated map; headline + topic badge fully visible on frame 0.
- **Open loop / list structure**: "X agreed on 4 things… but the biggest one wasn't on the list". A **"1 / 4" progress tracker** (`trk(n)`) top-right on the list scenes; the payoff/twist comes near the end.
- **Reveals timed to the voice**: in make_slides.py use `at(slide, sentence, extra)` (1-based slide, 0-based sentence from `work/sentences.json`) as the animation delay, so each card/✓/✕/stamp appears exactly when it is said. Then set that slide's `ANIMS` (in narrate.py only) to cover its last reveal + ~0.6 s, and re-run narrate.py.
- **My photos inside the slides** with movement: hook (`.hookimg`), quote + photo (`.qimg`), photo pan (`.himg`). Label honestly ("File photo · Names", or "Unverified photo · date not confirmed").
- **Reusable components** in make_slides.py: flags converging on a pin (wires meet exactly on an SVG hub dot), check/cross rows, rising bars, Security-Council seats lighting up, serif quote, mega word + ✕ stamp ("NOT IN THE DECLARATION"), ticking counter (`@property --n`).
- **Captions burned in** by finish.py: 3-word chunks timed within each sentence, white Inter on a dark box (ASS `BorderStyle 3`), centred at y≈1470, `fontsdir=~/Library/Fonts`. Use `DISPLAY` to show digits ("forty minutes" → "40 minutes"). Tell me to keep platform auto-captions OFF (no double captions).
- **SFX** by finish.py: synthesized soft whoosh just before every cut, low hit on stamps (`STAMPS = [(slide, sentence, extra)]`, same timing as `at()`).
- Keep content above y≈1400 (captions sit at ~1420–1520; platform buttons below).
- Still 61–66 s, first spoken line under 2 s (4–7 words: our last hooks ran 2.1–2.4 s, so write shorter).

## 8. Voice + timing + render scripts

### narrate.py — makes `narration.wav`, `holds.json` (how long each slide stays) and `sentences.json` (start/end of every sentence, used to place images)

```python
import json, re, subprocess, wave, sys
from pathlib import Path
import numpy as np
import onnxruntime as ort

V = Path(__file__).parent
T = next(p / "tts" for p in V.parents if (p / "tts").is_dir())   # shared tts/ at project root
SR, F = 24000, 0.6
ANIMS = [3.2, 3.2, 3.2, 3.2, 3.2]   # captured animation seconds per slide (e.g. 10.8 for a narrated map hook)
SPEED = float(sys.argv[2]) if len(sys.argv) > 2 else 1.32
VOICE = sys.argv[1] if len(sys.argv) > 1 else "am_fenrir"

NARRATION = [  # one string per slide, hook first
    "The world could be heading for another oil crisis. Iran now says it has shut the Strait of Hormuz completely. America says that's not true. So who's right?",
    "...",
]

vocab = json.load(open(T / "config.json"))["vocab"]
voices = np.load(T / "voices-v1.0.bin")
sess = ort.InferenceSession(str(T / "kokoro-v1.0.onnx"))

def ipa(chunk):
    out = subprocess.run([ESPEAK, "-q", "--ipa", "-v", "en-us", chunk], capture_output=True, text=True).stdout   # ESPEAK = shutil.which("espeak-ng")
    return " ".join(out.split())

# Pronunciation fixes: (espeak IPA, replacement IPA). Add more when a word sounds wrong.
FIX = [("ɪɹˈænz", "aɪɹˈɑːnz"), ("ɪɹˈæn", "aɪɹˈɑːn"), ("ɪɹˈeɪnɪən", "aɪɹˈeɪniən"), ("hˈoːɹmʌz", "hɔːɹmˈuːz"), ("hˈɔːɹmʌz", "hɔːɹmˈuːz"),
       ("hˈaʊθaɪz", "hˈuːθiːz"), ("tænjˈʊɹɹə", "tɑːnˈʊɹə"), ("ɹˈɪjæd", "ɹiːjˈɑːd")]   # Iran, Hormuz, Houthis, Tanura, Riyadh

def phonemize(sentence):
    ph = ""
    for p in re.split(r"([,.;:!?])", sentence):
        if not p.strip():
            continue
        ph = (ph.rstrip() + p + " ") if p in ",.;:!?" else (ph + ipa(p.strip()) + " ")
    for a, b in FIX:
        ph = ph.replace(a, b)
    return ph.strip()

def synth(sentence):
    toks = [vocab[c] for c in phonemize(sentence) if c in vocab][:508]
    audio = sess.run(None, {"tokens": np.array([[0, *toks, 0]], dtype=np.int64),
                            "style": voices[VOICE][len(toks)].astype(np.float32),
                            "speed": np.array([SPEED], dtype=np.float32)})[0]
    return np.asarray(audio).reshape(-1)

gap = np.zeros(int(0.09 * SR), dtype=np.float32)
clips, sent_marks = [], []
for text in NARRATION:
    segs, marks, pos = [], [], 0
    for s in re.findall(r"[^.!?]+[.!?]", text):
        a = synth(s.strip())
        marks.append([pos / SR, (pos + len(a)) / SR])
        pos += len(a) + len(gap)
        segs += [a, gap]
    sent_marks.append(marks)
    clips.append(np.concatenate(segs[:-1]))

holds, starts, t = [], [], 0.0
n = len(clips)
for i, c in enumerate(clips):
    a = len(c) / SR
    lead = 0.25 if i == 0 else F - 0.1
    tail = F if i < n - 1 else 0.8
    hold = max(0.5, lead + a + 0.15 + tail - ANIMS[i])
    holds.append(round(hold, 3))
    starts.append(t + lead)
    t += ANIMS[i] + holds[-1] - (F if i < n - 1 else 0)

track = np.zeros(int(t * SR) + SR, dtype=np.float32)
for s, c in zip(starts, clips):
    k = int(s * SR)
    track[k:k + len(c)] += c
track = track[: int(t * SR)]
track = track / max(1e-6, np.abs(track).max()) * 0.89
with wave.open(str(V / "narration.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track * 32767).astype(np.int16).tobytes())
json.dump(holds, open(V / "holds.json", "w"))
sent_abs = [[[round(s + a, 2), round(s + b, 2)] for a, b in m] for s, m in zip(starts, sent_marks)]
json.dump(sent_abs, open(V / "sentences.json", "w"))
for i, m in enumerate(sent_abs, 1):
    print(i, m)
print("clip seconds:", [round(len(c) / SR, 1) for c in clips], "total", round(t, 1))
```

### render.py — captures each slide's animation (ANIMS seconds at 30 fps) with Playwright, holds the last frame for the narration, joins slides with xfade transitions, adds the voice

```python
import json, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

D = Path(__file__).parent
NAME = "iran-war-part-2"        # change per video
FPS, F = 30, 0.6
ANIMS = [3.2, 3.2, 3.2, 3.2, 3.2]   # must match narrate.py
N = 5                           # number of slides
holds = json.load(open(D / "holds.json")) if (D / "holds.json").exists() else [3.0] * N
TRANS = ["slideup", "smoothleft", "circleopen", "slideup"]   # N-1 transitions

if "--skip-frames" not in sys.argv:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(f"file://{D}/slides.html")
        for i in range(1, N + 1):
            fd = D / "frames" / f"s{i}"
            fd.mkdir(parents=True, exist_ok=True)
            pg.evaluate("i => { document.querySelectorAll('.s').forEach(e => e.classList.remove('on'));"
                        "document.getElementById('s'+i).classList.add('on'); }", i)
            pg.wait_for_timeout(120)
            print(f"s{i} overflow px:", pg.evaluate("i => { const e = document.getElementById('s'+i); return e.scrollHeight - e.clientHeight }", i))
            for k in range(int(ANIMS[i - 1] * FPS)):
                pg.evaluate("t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t })", k * 1000 / FPS)
                pg.screenshot(path=str(fd / f"{k:03d}.jpg"), type="jpeg", quality=95)
        b.close()

cmd = ["ffmpeg", "-y", "-loglevel", "error"]
for i in range(1, N + 1):
    cmd += ["-framerate", str(FPS), "-i", str(D / "frames" / f"s{i}" / "%03d.jpg")]
durs = [ANIMS[i] + h for i, h in enumerate(holds)]
fc = [f"[{i}:v]tpad=stop_mode=clone:stop_duration={holds[i]},format=yuv420p[c{i}]" for i in range(N)]
prev, off = "[c0]", 0.0
for i in range(1, N):
    off += durs[i - 1] - F
    fc.append(f"{prev}[c{i}]xfade=transition={TRANS[i-1]}:duration={F}:offset={off:.3f}[v{i}]")
    prev = f"[v{i}]"
nar = D / "narration.wav"
out = D / (f"{NAME}-vertical-narrated.mp4" if nar.exists() else f"{NAME}-vertical-slides.mp4")
amap = []
if nar.exists():
    cmd += ["-i", str(nar)]
    amap = ["-map", f"{N}:a", "-c:a", "aac", "-b:a", "160k"]
cmd += ["-filter_complex", ";".join(fc), "-map", prev, *amap, "-r", str(FPS), "-c:v", "libx264", "-crf", "19",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
subprocess.run(cmd, check=True)
starts, t = [], 0.0          # when each slide starts in the video (used by panels and stock inserts)
for d in durs:
    starts.append(round(t, 2)); t += d - F
json.dump({"starts": starts, "durs": durs}, open(D / "timing.json", "w"))
print("done", starts)
```

Run order (inside the video folder, `P=../../.venv/bin/python`): `$P narrate.py` (writes work/sentences.json, holds.json, anims.json) → (`$P build_map.py` if a map is synced to the voice) → `$P make_slides.py` → `$P render.py` → (`$P photos.py` optional) → `$P finish.py` (captions + SFX → work/NAME-final.mp4) → `../../kit/export-1080p.sh work/NAME-final.mp4 NAME [cover-seconds]`. NAME comes from the folder name automatically. Check every slide prints `overflow px: 0`. `--skip-frames` only works while `work/frames/` still exists (it is deleted after the final export).

## 8b. When stock photos are blocked: draw it
If Unsplash is blocked (curl gets `CONNECT tunnel failed, response 403`), don't stall: build animated SVG illustrations in the slides instead and label them `Illustration`. Examples in the kit:
- `examples/us-vote-explainer/build_slides.py`: House/Senate **hemicycle** (435 + 100 seat dots) with dots flipping colour and "FLIPPED" stamps; majority line marked.
- `examples/freezer-hack-scene/build_slides.py`: **freezer display counting -18°C → 50°C** (stacked text with stepped opacity), freezer interior heating, "HACKED" stamp; a **how-it-works diagram** (fridges → control panel → internet → repair company / hacker, wires drawn with `pathLength="1"`); and **comparison bars** (normal vs hacked defrost).
Use these as starting points for elections, cyber attacks and "how it works" slides.

## 9. Image inserts — images.py

Each image appears at the **start of the sentence that mentions it**, ~3.5–5 s, with an 8% slow zoom, 0.3 s fade in/out, and a label box top-left. Framing: portrait photos → `COVER` (fill), wide images → centred over a blurred, darkened copy (`BLUR`), maps/satellite → crop to the area that matters.

```python
import json, subprocess
from pathlib import Path

V = Path(__file__).parent
M = V / "in"                                  # my images/clips go in the video folder's in/
NAME = "iran-war-part-2"
FONT = str(Path.home() / "Library/Fonts/Inter-SemiBold.otf")
FD, FPS = 0.3, 30
S = json.load(open(V / "sentences.json"))
IMG = {"sat": M / "satellite.jpg", "flags": M / "flags.jpg"}   # short names → files

def ff(*a):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)

BLUR = ("[0]split[a][b];[a]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,boxblur=40,"
        "eq=brightness=-0.3[bg];[b]scale=2160:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2")
COVER = "scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840"
ff("-i", str(IMG["sat"]), "-vf", "scale=-2:3840:flags=lanczos,crop=2160:3840:1650:0", str(V / "st_sat.png"))
ff("-i", str(IMG["flags"]), "-filter_complex", BLUR, str(V / "st_flags.png"))

# image, (slide index from 0, sentence index from 0), max seconds, label
PLAN = [
    ("sat",   (1, 1), 4.6, "Strait of Hormuz from space"),
    ("flags", (2, 1), 3.4, "Illustration"),
]
starts = [S[a][b][0] - 0.15 for _, (a, b), _, _ in PLAN]
INS = []
for i, (k, _, mx, label) in enumerate(PLAN):
    t0 = round(starts[i], 2)
    d = mx if i == len(PLAN) - 1 else min(mx, starts[i + 1] - t0 - 0.1)
    INS.append((k, t0, round(d, 2), label))

cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(V / f"{NAME}-vertical-narrated.mp4")]
fc, prev = [], "[0:v]"
for i, (k, t0, d, label) in enumerate(INS, 1):
    cmd += ["-i", str(V / f"st_{k}.png")]
    (V / f"label{i}.txt").write_text(label, encoding="utf-8")
    n = int(d * FPS)
    fc.append(
        f"[{i}:v]zoompan=z='1+0.08*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps={FPS},"
        f"setsar=1,format=yuv420p,drawtext=fontfile={FONT}:textfile={V / f'label{i}.txt'}:fontsize=32:fontcolor=white:"
        f"box=1:boxcolor=black@0.65:boxborderw=18:x=64:y=96,format=yuva420p,"
        f"fade=t=in:st=0:d={FD}:alpha=1,fade=t=out:st={d-FD}:d={FD}:alpha=1,setpts=PTS-STARTPTS+{t0}/TB[b{i}]")
    fc.append(f"{prev}[b{i}]overlay=enable='between(t,{t0},{t0+d})':eof_action=pass[v{i}]")
    prev = f"[v{i}]"
out = V / f"{NAME}-final.mp4"
cmd += ["-filter_complex", ";".join(fc), "-map", prev, "-map", "0:a", "-c:v", "libx264", "-crf", "19",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(out)]
subprocess.run(cmd, check=True)
print("done", INS)
```

B-roll video clips (silent stock footage) work the same way: `-ss START -t LEN -i clip.mp4`, scale/crop to 1080×1920, label "Stock footage", fade in/out, overlay at the sentence time. Never use footage that could be mistaken for the real event without a label.

### 9a. My photos as panels under the slide text — template/photos.py
When I send photos (e.g. a rally, a voter, a leader), show each one as a **panel** under the slide's cards with a smooth slow zoom, gold/amber border and an honest label (`Illustrative photo · …` if place/date are unknown, `File photo · Name` for a known person). Pre-crop each photo to the panel's ratio first (crop by width: `crop=iw:iw*H/W`, never by height, or small photos fail). Set the panel `y` just below the slide's content bottom (peek.py prints it) and end above y≈1550. **Set `END` to the narrated video's full length**, or the video gets cut short.

### 9a2. A real clip of the leader as the HOOK (best hook we have) — examples/clip-hook-part8/
When I send a clip of a leader saying the key line (e.g. Trump: "If I had to do it again, I'd have to do it again"), open the video with it:
- Start the clip **exactly where he starts answering** (skip the reporter's question), end at a natural pause; ~12–17 s.
- Fit the clip full-width over a blurred, darkened copy of itself; overlay (transparent PNG from `hook.html`): topic badge + headline at top (visible at frame 0), label `Video: [who] speaking to reporters · [date]`, and a quote box with his line for sound-off viewers.
- Quote only words that reputable outlets report verbatim. If you can't transcribe the clip (speech-to-text model downloads are blocked here), show the verified quote as a box, not word-timed captions, and ask me to confirm it matches.
- Then the narrated slides; join with a 0.5 s xfade + `acrossfade`. Keep the total over 60 s (extend the clip to the next pause if needed).

### 9b. A clip I send plays inside the slide — panel.py
When I send a GIF or video for a slide, it plays **inside that slide** in the panel area (under the cards), looping, for the whole time the slide is on screen. If a GIF arrives as a single still, ask me to send it as an MP4.

```python
import json, subprocess
from pathlib import Path
V = Path(__file__).parent
SRC = V / "in/my-clip.mp4"
FONT = str(Path.home() / "Library/Fonts/Inter-SemiBold.otf")
tm = json.load(open(V / "timing.json"))
t0 = tm["starts"][1] + 0.45            # slide 2: after the transition lands
t1 = tm["starts"][2] + 0.05            # until the next transition
d = round(t1 - t0, 2)
PW, PH, X, Y = 888, 496, 96, 850       # panel under the cards
(V / "plabel.txt").write_text("Unverified footage: date and place not confirmed", encoding="utf-8")
fc = (f"[1:v]trim=duration={d},fps=30,scale={PW}:{PH}:force_original_aspect_ratio=increase:flags=lanczos,crop={PW}:{PH},"
      f"setsar=1,format=yuv420p,drawbox=x=0:y=0:w=iw:h=ih:color=0xE25D4B:t=6,"
      f"drawtext=fontfile={FONT}:textfile={V/'plabel.txt'}:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=12:x=22:y=22,"
      f"format=yuva420p,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={d-0.3}:d=0.3:alpha=1,setpts=PTS-STARTPTS+{t0}/TB[p];"
      f"[0:v][p]overlay={X}:{Y}:enable='between(t,{t0},{t1})':eof_action=pass[v]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(V / "NAME-vertical-narrated.mp4"),
                "-stream_loop", "-1", "-i", str(SRC), "-filter_complex", fc, "-map", "[v]", "-map", "0:a",
                "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
                str(V / "NAME-final.mp4")], check=True)
```

### 9c. Unsplash stock photos — fetch.py + stock.py
**Setup:** on this Mac there is no domain allow-list; load `UNSPLASH_KEY` from `.env` (my **Access Key**, never the Secret Key) when running the stock scripts. Test with one search first. Unsplash's API has **photos only, no video**.

**Video clips (not set up yet):** Pexels — needs `api.pexels.com`, `images.pexels.com`, `videos.pexels.com` allowed plus a free Pexels API key. Until that works, use Unsplash photos, or I download clips and attach them.

**Rules:**
- One photo per content slide at most; the opening map slide gets none.
- Search words = the place/thing in the narration ("Mount Fuji", "Stockholm winter", "power lines sunset", "storm clouds city", "canned food pantry"). `orientation=landscape` for panels, `portrait` for full-screen cutaways. Add `content_filter=high`.
- Download 4 candidates per query, show a **contact sheet**, pick the clearest one; re-crop a photo if the subject sits off-centre (crop to the part that matters first).
- **Panel** (slide text stays visible): under the cards, 888 wide × 400–530 high, ending above y≈1550, amber border, **smooth slow zoom** (zoompan on a 6× upscaled image, zoom 6%). Shows from slide start + ~1.5 s (after cards animate in) to the next transition.
- **Full-screen cutaway** (2.5–3 s): on the sentence that names the place, **slow left→right pan**: travel capped at 180 px on screen over the whole cutaway (~2 px per frame), centred on the photo, done at 2× size then scaled down. Wide photos must NOT sweep the full width (too fast).
- Label each: `Stock photo · Photographer / Unsplash`. Ping each photo's `download_location` (Unsplash API rule). Put a credit line in the Facebook description: "Stock photos: Name, Name (Unsplash)".

```python
# fetch.py — search Unsplash and download 4 candidates per slide.  Run: UNSPLASH_KEY=... ../../.venv/bin/python fetch.py
import json, os, subprocess, urllib.parse
K = os.environ["UNSPLASH_KEY"]
Q = {"jp": ("Mount Fuji", "portrait"), "eu": ("Stockholm winter", "landscape"),
     "us": ("power lines sunset", "landscape"), "why": ("storm clouds city", "portrait")}
meta = {}
for k, (q, o) in Q.items():
    u = f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(q)}&orientation={o}&per_page=4&content_filter=high"
    r = json.loads(subprocess.run(["curl", "-sS", "--max-time", "20", "-H", f"Authorization: Client-ID {K}", u],
                                  capture_output=True, text=True).stdout)
    for i, p in enumerate(r["results"]):
        f = f"{k}{i}.jpg"
        subprocess.run(["curl", "-sS", "--max-time", "30", "-o", f, p["urls"]["regular"].replace("w=1080", "w=1600")], check=True)
        meta[f] = {"name": p["user"]["name"], "dl": p["links"]["download_location"], "alt": p.get("alt_description")}
json.dump(meta, open("meta.json", "w"), indent=1)
for f, m in meta.items(): print(f, m["name"], "|", m["alt"])
# contact sheet per query: ffmpeg -i jp0.jpg -i jp1.jpg -i jp2.jpg -i jp3.jpg -filter_complex
#   "[0]scale=400:400:force_original_aspect_ratio=increase,crop=400:400[a];...;[a][b][c][d]hstack=4" row_jp.jpg
```

```python
# stock.py — panels (smooth zoom) and full-screen cutaways (left→right pan) over the narrated video
import json, os, subprocess
from pathlib import Path
V = Path(__file__).parent; S = V.parent          # stock/ subfolder inside the video folder
K = os.environ["UNSPLASH_KEY"]
FONT = str(Path.home() / "Library/Fonts/Inter-SemiBold.otf")
meta = json.load(open(V / "meta.json"))
st = json.load(open(S / "timing.json"))["starts"]
END = 60.7                                       # video length
# file, start, end, panel (x, y, w, h) or None = full screen
PLAN = [("uk_crop.jpg", st[1] + 1.6, st[2] + 0.05, (96, 1110, 888, 440)),
        ("jp0.jpg",     28.9,        31.65,        None),          # on "Mount Fuji eruption"
        ("eu0.jpg",     st[3] + 1.3, st[4] + 0.05, (96, 1020, 888, 530)),
        ("us1.jpg",     st[4] + 1.8, st[5] + 0.05, (96, 1140, 888, 410)),
        ("why2.jpg",    51.3,        53.9,         None)]          # on "storms, earthquakes…"
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(S / "NAME-vertical-narrated.mp4")]
fc, prev = [], "[0:v]"
for i, (f, t0, t1, box) in enumerate(PLAN, 1):
    m = meta[f]
    subprocess.run(["curl", "-s", "-o", "/dev/null", "-H", f"Authorization: Client-ID {K}", m["dl"]])  # Unsplash download ping
    (V / f"l{i}.txt").write_text(f"Stock photo · {m['name']} / Unsplash", encoding="utf-8")
    d = round(t1 - t0, 2); n = int(d * 30) + 2
    w, h = (box[2], box[3]) if box else (1080, 1920)
    x, y = (box[0], box[1]) if box else (0, 0)
    fs, pad = (24, 18) if box else (32, 64)
    cmd += ["-loop", "1", "-i", str(V / f)]
    border = "drawbox=x=0:y=0:w=iw:h=ih:color=0xF2B04E:t=5," if box else ""
    if box:   # smooth slow zoom: zoompan on a 6x image, so each integer step is sub-pixel at output size
        move = (f"[{i}:v]scale={6*w}:{6*h}:force_original_aspect_ratio=increase:flags=lanczos,crop={6*w}:{6*h},"
                f"zoompan=z='1+0.06*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s={w}x{h}:fps=30,trim=duration={d},")
    else:     # full screen: left-to-right pan, worked at 2x then scaled down for smooth motion
        move = (f"[{i}:v]fps=30,trim=duration={d},scale=-2:{2*h*1.12:.0f}:flags=lanczos,"
                f"crop={2*w}:{2*h}:x='(iw-{2*w})/2-min((iw-{2*w})/2\\,180)+min(iw-{2*w}\\,360)*t/{d}':y='(ih-{2*h})/2',scale={w}:{h}:flags=bicubic,")
    fc.append(move + f"setsar=1,format=yuv420p,{border}"
              f"drawtext=fontfile={FONT}:textfile={V/f'l{i}.txt'}:fontsize={fs}:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=10:x={pad}:y={pad},"
              f"format=yuva420p,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={d-0.3}:d=0.3:alpha=1,setpts=PTS-STARTPTS+{t0}/TB[p{i}]")
    fc.append(f"{prev}[p{i}]overlay={x}:{y}:enable='between(t,{t0},{t1})':eof_action=pass[v{i}]")
    prev = f"[v{i}]"
cmd += ["-filter_complex", ";".join(fc), "-map", prev, "-map", "0:a", "-c:v", "libx264", "-crf", "19",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-t", str(END), str(S / "NAME-final.mp4")]
subprocess.run(cmd, check=True)
```
Avoid zoompan on a small image (shaky). Avoid zooming full-screen photos; pan them instead.

## 10. TikTok caption, hashtags and posting rules

- Caption **starts with the main keyword + the hook** (first ~2 lines show before "more"). Same keyword is spoken in the first sentence and shown on screen.
- **3–5 specific hashtags**, no #fyp / #viral. Example: `#IranWar #StraitOfHormuz #OilCrisis #IranNews #WorldNews` (swap #WorldNews for #PetrolPrice for a South Asian audience).
- End the caption with a question to invite comments ("What happens next? 👇").
- Rename the file to keywords before uploading, e.g. `iran-war-oil-crisis-strait-of-hormuz.mp4`.
- Pick a striking cover frame (e.g. the map with the BLOCKED stamp).
- Turn on TikTok's **AI-generated content** label (synthetic voice + AI images).
- Pin a comment linking a related video (e.g. the background explainer).
- Post first, then reply to comments on the older video pointing to the new one; reply fast in the first hour.

Caption template:
```
[Hook question or claim with keyword] 🛢️ [2-sentence summary with names] 👇 [Question]?

#Keyword1 #Keyword2 #Keyword3 #Keyword4 #Keyword5
```

### Facebook (Page, Reels)
- Post the **same clean MP4** (no TikTok watermark) as a Reel on the **Page** the same day.
- Facebook asks for a **title + description**: title = keyword + hook (under ~60 characters); description = 2–3 sentence summary, a question, the sources, the stock-photo credit line, then 3–5 hashtags.
- Turn on Facebook's **AI-generated** label too.
- What all platforms push: completion rate (aim 75%+), rewatches, shares and saves; hook in the first 3 s; keyword spoken + on screen + in the caption.

### YouTube Shorts (@nexcium_explains)
- **Adding a sound from YouTube's library only works in the YouTube mobile app** (Upload → Add sound → Volume: keep original voice high, added sound ~10–20%). Studio on PC can't do it. AirDrop the -1080p file to the phone (not WhatsApp, it compresses). Tags and "Altered content" still get set in Studio afterwards. A sound is optional for narrated explainers; never let it bury the voice.
- Upload the same clean **-1080p** file (never the TikTok download with the watermark). Vertical and under 3 minutes = a Short.
- **Title** (under ~70 characters): keyword first + hook + `#shorts`, e.g. `Trump Admits the Iran War Cost Him Congress #shorts`.
- **Description:** first line = the hook with the keyword; then a 2–3 sentence summary (with the date the news is from, e.g. "On 4 November…"); 2–3 "What happens now?" bullets; a question for comments; sources; the AI line ("Voice-over is AI-generated. Some images are illustrations or AI-generated and are labelled on screen."); the stock-photo credit line if any; 3–5 hashtags.
- **Tags:** 10–13 search phrases (topic, names, "explained", "world news").
- Settings: **Altered or synthetic content = Yes** (AI voice + realistic AI images), **Made for kids = No**, add to a topic **playlist** (e.g. "Iran War", "US Politics", "Cyber Attacks"; old numbered parts go in "Iran War: the full series").
- Pin a comment with the question + a link to a related video. Post 1–3 Shorts a day rather than dumping many at once.
- For older videos re-uploaded to YouTube, start the description with the date they cover ("As of 27 October 2026…") so old news doesn't mislead.

## 11. Comment replies

- Thank them, stay neutral and factual, point to a related video. Reply in the commenter's language when they don't write in English (translate their comment for me first).
- Don't argue opinions or unverifiable claims. Don't like/pin comments that hint at violence ("by fair means or foul") — reply neutrally or restrict/delete if threads turn abusive.

## 12. Known issues and their fixes

| Problem | Fix |
|---|---|
| Voice says "U … S" | Write "United States"; no dotted abbreviations |
| "Iran" heard as "ran" | IPA override in `FIX` → `aɪɹˈɑːn` |
| Voice too slow | `SPEED` 1.28–1.35, gap 0.09 s |
| Text cut off | render.py prints `overflow px`; must be 0 for every slide |
| Image hides key slide text | place image on a sentence after the slide's key fact, or shorten it |
| Video length | ~185–200 words / 5–6 slides ≈ 61–70 s at speed 1.32; check total > 60 s |
| pip install blocked / "externally managed" | use the project venv: `./setup.sh`, then `.venv/bin/python` |
| Hormuz not fixed by FIX on Mac | Homebrew espeak-ng 1.52 gives `hˈɔːɹmʌz`; FIX now covers both spellings. If a FIX stops working, compare `espeak-ng -q --ipa -v en-us WORD` |
| -1080p file only ~1.4 Mbps | needs `-x264-params nal-hrd=cbr` (in kit/export-1080p.sh) |
| Label font not found in ffmpeg | `brew install --cask font-inter`; FONT points to `~/Library/Fonts/Inter-SemiBold.otf` |
| Stock sites blocked | check internet/VPN; otherwise I download photos into the video's `in/` folder |
| Unsplash search works but images fail | `images.unsplash.com` not allowed yet |
| Stock photo zoom shaky | zoompan on a 6× upscaled image; pan full-screen photos instead |
| Map shows a country before the voice names it | build camera/lights from `sentences.json` (§7 world map) |
| GIF arrives as one still frame | ask for the MP4 version, embed as a panel (§9b) |
| Cards too low / hidden by captions | `justify-content:flex-start`; nothing below y≈1550 |
| Nepali voice | tested (Kokoro hm_psi/hm_omega, espeak) — not good enough; English only |
| Big drop-off at 0:02 | First line under 2 s, motion at frame 0, headline = hook (§3) |
| Viewers leave in the middle | Keep to 61–66 s; key fact in first 10 s |
| Unsplash 403 / blocked | Draw animated SVG illustrations instead (§8b) |
| Final video cut short after adding photos | `END` in photos.py/stock.py must equal the narrated video length |
| ffmpeg "Invalid too big" crop error on small photos | Crop by width (`crop=iw:iw*H/W`), not height |
| Speech-to-text (faster-whisper / Hugging Face) blocked | Use verified quotes from news sources in a quote box; ask me to confirm the clip matches |
| Picture drifts out of sync with the voice | ANIMS set in two places; now narrate.py writes work/anims.json and render.py reads it. Set ANIMS only in narrate.py |
| A timed element never appears (e.g. "Follow for more" chip) | its `at()` delay is later than that slide's ANIMS, or the wrong sentence index (0-based). Raise ANIMS or fix the index, re-run narrate.py |
| Burned-in captions look cramped / wrong font | ASS style `Inter`, bold, BorderStyle 3 (box), and pass `fontsdir=~/Library/Fonts` to the ass filter |
| Lines meant to meet at a point miss it | draw the hub dot inside the same SVG as the lines and end every path at the dot's exact coordinates |
| Light-coloured dates hard to read on light slides | Add `.light` colour overrides (darker accent) for timeline dates and dots |
