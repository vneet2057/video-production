# News video kit

1. Runs locally on the Mac with Claude Code in ~/Desktop/video production (see ../CLAUDE.md and ../MASTER-PROMPT.md).
   Say "Today's topic is: ___" or "find today's hot topics". Setup: ../setup.sh. New video: ../new-video.sh topic-slug
2. Voice: Kokoro am_fenrir, speed 1.32 (models in ../tts/), country outlines in ../geo/wgj/.
3. template/      FAST TEMPLATE (default since 20 Nov 2026, master prompt section 7c):
                  narrate.py (voice + sentence timings; the only place to set ANIMS), make_slides.py (~10 scenes, reveals
                  timed to the voice with at(), Ken Burns photos, 1/4 tracker), render.py (slides -> video), photos.py
                  (optional panels/cutaways), finish.py (burned-in captions + whoosh/hit SFX), peek.py (check frames)
                  Run: narrate -> make_slides -> render -> (photos) -> finish -> ../export-1080p.sh (1080p + 720p + cover)
   examples/      trilateral-fast (the fast-style reference: "Trump, Xi and Putin agreed on 4 things"),
                  kerch-bridge-map (zooming Kerch Strait map, train + strike + TRAINS STOPPED, user photos as panels),
                  nkweek-scene (old default make_slides.py), animated hooks: Gulf map (Iran Part 5), Korea missiles + drone dive, world map camera, Binance drain, AI bubble pop,
                  us-vote-explainer (House/Senate hemicycle + my photos as panels; best video, ~12k FB views),
                  freezer-hack-scene (freezer temp counter, how-it-works diagram, comparison bars),
                  clip-hook-part8 (real Trump clip as the hook + headline/quote overlay, joined to narrated slides;
                  last numbered part, so swap its 'Iran War · Part 8' badge for a topic badge when reusing)
   stock/         Unsplash fetch + panels/pans (needs UNSPLASH_KEY in the environment; paste your Access Key in chat)
4. Rules: 61-66 s, first line under 2 s with motion at frame 0 (biggest drop-off is 0:02), headline visible on frame 0,
   divisive topic + neutral delivery, explain the basics, end with a question + 'Follow for more', cover JPG,
   1080x1920 ~8 Mbps -1080p export (the upload file) + a 720p copy, burned-in captions (keep platform auto-captions off), AI label on. Facebook audience is 84% aged 55+: test voice speed 1.2 there.
5. Platforms: Facebook Reels (main earner), YouTube Shorts @nexcium_explains (since 5 Nov 2026), TikTok (keep posting, same style for now).
   No more numbered parts: Iran War Part 8 was the last. Topic badge on the hook, every video ends "Let's see what happens. Follow for more."
   Each video ships with a posting pack: TikTok caption, Facebook title + description, YouTube title + description + tags (master prompt section 10).
   Why: audience is older (84% of FB viewers 55+) and likes calm, clear explainers; TikTok style changes only later, when we decide.
