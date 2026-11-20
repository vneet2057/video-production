# Nexcium Explains: video production

First time on a new Mac: `./setup.sh`. New video: `./new-video.sh topic-slug`.

- `MASTER-PROMPT.md`: the full workflow and rules. Read this first.
- `kit/`: reusable scripts (`template/`), past videos to copy from (`examples/`), Unsplash tools (`stock/`), `export-1080p.sh`.
- `tts/`: Kokoro voice model, shared by all videos.
- `geo/wgj/`: country outlines for map hooks.
- `.venv/`: Python environment; run scripts with `../../.venv/bin/python`.
- `videos/YYYY-MM-DD-topic/`: one folder per video. Created by `new-video.sh`.
- `_originals/`: the zips this came from.

Each video folder:
```
videos/YYYY-MM-DD-topic/
├── exported/   ← post these: NAME-1080p.mp4 (upload), NAME-720p.mp4 (preview), NAME-cover.jpg, posting-pack.md
├── work/       ← voice, timing, frames, draft videos
├── in/         ← your photos / clips
├── chk/        ← check frames
└── slides.html + scripts
```
