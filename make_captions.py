from faster_whisper import WhisperModel

print("Loading model (first run downloads ~150MB)...")
model = WhisperModel("base.en", device="cpu", compute_type="int8")

print("Transcribing...")
segments, _ = model.transcribe("voice.mp3", word_timestamps=True)

ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginL, MarginR, MarginV
Style: Default,Impact,96,&H00FFFFFF,&H00000000,&H80000000,1,6,2,2,40,40,500

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def fmt(t):
    h, m, s = int(t // 3600), int((t % 3600) // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

lines = []
for seg in segments:
    for w in seg.words:
        word = w.word.strip().upper().replace(",", "").replace(".", "")
        if not word:
            continue
        lines.append(f"Dialogue: 0,{fmt(w.start)},{fmt(w.end)},Default,,0,0,0,,{word}")

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass_header + "\n".join(lines))

print(f"captions.ass created ({len(lines)} words)")