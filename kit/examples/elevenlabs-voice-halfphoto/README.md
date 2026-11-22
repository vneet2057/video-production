# ElevenLabs voice + half-photo layout (22 Nov 2026, "Trump wants a permanent Iran deal")

Use when the user supplies their own voice file (e.g. ElevenLabs mp3) instead of Kokoro.

1. Put the mp3 in `in/voice-elevenlabs.mp3`.
2. `ffmpeg -i in/voice-elevenlabs.mp3 -ar 16000 -ac 1 work/voice16.wav`, then `../../.venv/bin/python transcribe.py`
   (faster-whisper `small.en` word timestamps -> work/words.json; `pip install faster-whisper` into .venv once).
3. Edit the `ANCH` list in align.py (first two words of every sentence) -> work/src_sentences.json.
4. narrate.py: NARRATION must match the voice sentence-for-sentence. It shortens pauses over 0.24 s and applies
   a light atempo (max 1.18) to hit TARGET (64 s), then writes narration.wav / holds / anims / sentences as usual.
5. make_slides.py: text top half, photo bottom half on every slide, calm motion, real-outline Hormuz map with sailing tankers.
6. finish.py: soft "swish" on reveals (REVEALS list), no heavy hits, light music.

Known issue: captions at y=1470 landed ON the photos. The user dislikes that. Next time keep a plain band for captions
(move the photo lower/shorter or move the caption y into the text half).
