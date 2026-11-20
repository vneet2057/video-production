#!/bin/sh
# Real-clip hook (Iran War Part 8): clip of the leader speaking, blurred fill, headline + quote overlay (hook.html -> hook_ov.png)
# 1) render hook_ov.png from hook.html with Playwright: page.screenshot(path="hook_ov.png", omit_background=True)
# 2) cut the clip from where he starts answering (START) to a natural pause (END) and overlay
START=7.6; END=24.25
ffmpeg -y -ss $START -to $END -i in/clip.mp4 -i hook_ov.png -filter_complex \
"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30,eq=brightness=-0.35[bg];\
[b]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=0:420[v0];[v0][1:v]overlay=0:0,fps=30,format=yuv420p[v]" \
-map "[v]" -map 0:a -c:v libx264 -crf 18 -c:a aac -b:a 192k -ar 24000 -ac 1 hook.mp4
# 3) narrate.py + render.py + photos.py for the slides (p8-slides-final.mp4), then join with a 0.5 s slideup:
H=$(ffprobe -v error -show_entries format=duration -of csv=p=0 hook.mp4)
ffmpeg -y -i hook.mp4 -i work/p8-slides-final.mp4 -filter_complex \
"[0:v]fps=30,settb=AVTB[a];[1:v]fps=30,settb=AVTB[b];[a][b]xfade=transition=slideup:duration=0.5:offset=$(echo "$H - 0.5" | bc)[v];[0:a][1:a]acrossfade=d=0.5[au]" \
-map "[v]" -map "[au]" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart final.mp4
