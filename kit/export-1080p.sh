#!/bin/sh
# Usage: kit/export-1080p.sh work/NAME-final.mp4 [NAME] [COVER_SECONDS]
#   -> exported/NAME-1080p.mp4 (main upload file) + exported/NAME-720p.mp4 (720x1280, ~5 Mbps) + exported/NAME-cover.jpg
# Audio: normalised to -14 LUFS (Reels/Shorts/TikTok level), stereo 48 kHz.
# nal-hrd=cbr forces a real ~8 Mbps. Without it, x264 drops static slides to ~1.4 Mbps and Facebook flags them as low quality.
set -e
IN="$1"; [ -z "$IN" ] && { echo "usage: $0 work/NAME-final.mp4 [NAME] [COVER_SECONDS]"; exit 1; }
NAME="${2:-$(basename "$IN" .mp4 | sed 's/-final$//; s/-vertical-narrated$//')}"
COVER_T="${3:-3}"
D="$(cd "$(dirname "$IN")" && pwd)"; [ "$(basename "$D")" = work ] && D="$(dirname "$D")"
mkdir -p "$D/exported"
OUT="$D/exported/$NAME-1080p.mp4"
ffmpeg -y -loglevel error -i "$IN" -c:v libx264 -preset medium -profile:v high -level 4.2 -pix_fmt yuv420p -r 30 \
  -b:v 8M -minrate 8M -maxrate 8M -bufsize 16M -x264-params nal-hrd=cbr -g 60 \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -tag:v avc1 "$OUT"
OUT720="$D/exported/$NAME-720p.mp4"
ffmpeg -y -loglevel error -i "$IN" -vf "scale=720:1280:flags=lanczos" -c:v libx264 -preset medium -profile:v high -level 4.0 -pix_fmt yuv420p -r 30 \
  -b:v 5M -minrate 5M -maxrate 5M -bufsize 10M -x264-params nal-hrd=cbr -g 60 \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -tag:v avc1 "$OUT720"
ffmpeg -y -loglevel error -ss "$COVER_T" -i "$OUT" -frames:v 1 -q:v 2 "$D/exported/$NAME-cover.jpg"
for f in "$OUT" "$OUT720"; do echo "== $(basename "$f")"; ffprobe -v error -select_streams v -show_entries stream=width,height,r_frame_rate,bit_rate -of default=nw=1 "$f"; done
ls -lh "$OUT" "$OUT720" "$D/exported/$NAME-cover.jpg"
