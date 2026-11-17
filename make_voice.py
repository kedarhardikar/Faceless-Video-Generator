import edge_tts, asyncio, json

data = json.load(open("script.json", encoding="utf-8"))
text = data["hook"] + " " + " ".join(s["voiceover"] for s in data["scenes"]) + " " + data["cta"]

async def main():
    communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural", rate="+8%")
    await communicate.save("voice.mp3")
    print(f"voice.mp3 created ({len(text)} chars)")

asyncio.run(main())