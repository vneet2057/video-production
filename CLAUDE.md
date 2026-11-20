# Nexcium Explains: news video production

This folder makes short vertical news explainer videos (1080x1920, 61–66 s, AI male voice-over, animated slides) for the **Nexcium Explains** channel: Facebook Reels (main earner), YouTube Shorts (@nexcium_explains), TikTok.

**Before any video work, read `MASTER-PROMPT.md` in full.** It is the source of truth for the workflow, editorial rules, voice settings, slide style, render scripts, upload export and posting pack. Follow it exactly; when it conflicts with this file, this file wins only on the "Running on this Mac" notes below.

## Layout
- `MASTER-PROMPT.md`: workflow + rules (read first).
- `kit/template/`: the **fast template** (default since 20 Nov 2026, MASTER-PROMPT §7c): narrate.py, make_slides.py (timed reveals, Ken Burns photos, 1/4 tracker), render.py, photos.py (optional), finish.py (captions + SFX), peek.py. `base-slides.html` is only for the older map examples.
- `kit/examples/`: past videos to copy from (maps, hemicycle, freezer diagram, clip hook, etc.). See `kit/README.md`.
- `kit/stock/`: Unsplash fetch/build scripts (needs `UNSPLASH_KEY`).
- `kit/export-1080p.sh work/NAME-final.mp4 NAME [cover-s]`: makes `-1080p` (~8 Mbps, the upload file), `-720p` (~5 Mbps, previews) and the cover; audio −14 LUFS stereo.
- `tts/`: shared Kokoro voice model (`narrate.py` searches parent folders for it).
- `videos/YYYY-MM-DD-topic-slug/`: one folder per video (`./new-video.sh slug`). Inside: scripts + slides.html at top, `in/` (user's files), `work/` (voice, timing, frames, drafts), `exported/` (ONLY deliverables: `NAME-1080p.mp4`, `NAME-720p.mp4`, `NAME-cover.jpg`, `posting-pack.md`), `chk/` (check frames). Delete `work/frames/` after a final render.
- `_originals/`: original zips, don't modify.

## Starting a session
- "Today's topic is X" → research (search first, 2–3 sources), then follow MASTER-PROMPT §2 in order.
- "Find topics" → rank 10 stories from the last 24 h (MASTER-PROMPT §2 step 1). Check `videos/` to skip topics already covered.

## Non-negotiables (summary; details in MASTER-PROMPT)
- Hook line under 2 s, motion and headline visible at frame 0. Key fact in first 10 s.
- Neutral on politics/wars; explain the basics; never invent numbers or quotes.
- Label every image honestly. No graphic violence.
- No "Part N". End with "Let's see what happens. Follow for more."
- Narration: no dotted abbreviations ("United States", not "U.S."), numbers as words.
- Fast style: ~10 scenes, reveals timed to the voice, motion everywhere, burned-in captions, SFX (MASTER-PROMPT §7c).
- Deliver: `-1080p` + `-720p` (report sizes + bitrates), cover JPG, `posting-pack.md`; open the 1080p in QuickTime Player. Recommend uploading the 1080p.
- Posting text in chat: per platform, each field in its own code block (copyable). Remind: fill the Facebook **Title** field too.
- Schedule: user schedules every Reel for **18:00–03:00 Nepal time** (US daytime), max 1–2/day, 4–6 h apart; tell them the next slot (`date` = Nepal time).
- Topics: prefer a clear US/Trump angle (US/Western viewers earn most); Asia-only stories rank lower (MASTER-PROMPT §1c).

## Running on this Mac (set up and tested 19 Nov 2026)
- Setup is done; `./setup.sh` re-checks/repairs it (Homebrew ffmpeg + espeak-ng + font-inter, `.venv/`, Kokoro model in `tts/`, country outlines in `geo/wgj/`).
- New video: `./new-video.sh topic-slug` → `videos/YYYY-MM-DD-topic-slug/` (template copied in, plus `in/` for the user's files and `chk/` for check frames).
- Always run Python with the venv, from inside the video folder: `../../.venv/bin/python narrate.py` (system python has no numpy/playwright).
- Pipeline: `narrate.py` → (`build_map.py`) → `make_slides.py` → `render.py` → (`photos.py`) → `finish.py` → `../../kit/export-1080p.sh work/NAME-final.mp4 NAME 3`. NAME = folder name without the date. Set `ANIMS` only in narrate.py (render.py reads work/anims.json).
- Export: real ~8 Mbps CBR (`nal-hrd=cbr`), ~60 MB/min, plus a 720p copy. Report the paths, sizes and bitrates it prints.
- Files stay local, so there is no chat size limit: never shrink the upload file.
- Mac espeak-ng (1.52) can phonemize differently from the old Linux build; if a `FIX` entry stops working, compare `espeak-ng -q --ipa -v en-us WORD`.
