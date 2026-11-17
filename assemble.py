import json, subprocess, os, glob

data = json.load(open("script.json", encoding="utf-8"))
clips = sorted(glob.glob("clips/[0-9]*.mp4"))

if not clips:
    raise SystemExit("No clips found in clips/")

# Get total audio duration
audio_dur = float(subprocess.check_output([
    "ffprobe", "-i", "voice.mp3",
    "-show_entries", "format=duration",
    "-v", "quiet", "-of", "csv=p=0"
]).strip())

per_scene = audio_dur / len(clips)
print(f"Audio: {audio_dur:.1f}s across {len(clips)} clips = {per_scene:.1f}s each")

# Normalize each clip to 1080x1920, 30fps, trim to per_scene length
for i, c in enumerate(clips):
    out = f"clips/_v{i:02d}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", c,
        "-t", str(per_scene),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30",
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        out
    ], check=True, stderr=subprocess.DEVNULL)
    print(f"  normalized {i}")

# Build concat list (must be relative to file location)
with open("clips/concat.txt", "w") as f:
    for i in range(len(clips)):
        f.write(f"file '_v{i:02d}.mp4'\n")

# Final assembly: concat + audio + burned captions
subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", "clips/concat.txt",
    "-i", "voice.mp3",
    "-vf", "ass=captions.ass",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20",
    "-c:a", "aac", "-b:a", "192k",
    "-pix_fmt", "yuv420p",
    "-shortest", "final.mp4"
], check=True)

print("\n final.mp4 ready")