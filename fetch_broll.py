import requests, json, os
from dotenv import load_dotenv
load_dotenv()
PEXELS_KEY = os.getenv("PEXELS_API_KEY")
if not PEXELS_KEY:
    raise SystemExit("Set $env:PEXELS_API_KEY first")

os.makedirs("clips", exist_ok=True)
# Clean old clips
for f in os.listdir("clips"):
    os.remove(os.path.join("clips", f))

data = json.load(open("script.json", encoding="utf-8"))

for i, scene in enumerate(data["scenes"]):
    q = scene["broll_query"]
    r = requests.get(
        "https://api.pexels.com/videos/search",
        headers={"Authorization": PEXELS_KEY},
        params={"query": q, "orientation": "portrait", "per_page": 5}
    ).json()

    videos = r.get("videos", [])
    if not videos:
        print(f"[{i}] NO RESULTS for '{q}' — trying landscape fallback")
        r = requests.get(
            "https://api.pexels.com/videos/search",
            headers={"Authorization": PEXELS_KEY},
            params={"query": q, "per_page": 5}
        ).json()
        videos = r.get("videos", [])
        if not videos:
            print(f"[{i}] STILL NO RESULTS — skipping. Manually add clips/{i:02d}.mp4")
            continue

    video = videos[0]
    # Pick HD-ish file, prefer ≤1080p to save bandwidth
    files_sorted = sorted(video["video_files"], key=lambda f: abs(f.get("width", 9999) - 1080))
    file = files_sorted[0]

    print(f"[{i}] {q} → downloading...")
    with open(f"clips/{i:02d}.mp4", "wb") as out:
        out.write(requests.get(file["link"]).content)

print("Done.")