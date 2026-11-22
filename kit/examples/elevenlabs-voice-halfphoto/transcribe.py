import json, wave, numpy as np
from faster_whisper import WhisperModel
w = wave.open("work/voice16.wav"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, word_timestamps=True, beam_size=5)
words = [[x.word.strip(), round(x.start, 3), round(x.end, 3)] for s in segs for x in s.words]
json.dump(words, open("work/words.json", "w"))
print(" ".join(x[0] for x in words))
