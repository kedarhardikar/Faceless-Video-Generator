# Faceless Video Generator

A Python-based workflow for turning a short-form video script into a vertical, narrated video with stock B-roll and word-level captions. The included example project creates a short explainer about how airplanes fly.

## Features

- **Script-driven workflow:** video title, hook, scene voiceovers, B-roll search terms, call to action, description, and hashtags are stored in `script.json`.
- **Automated B-roll retrieval:** searches the Pexels video API for clips matching each scene.
- **Text-to-speech narration:** generates an English voiceover with Edge TTS.
- **Automatic captions:** uses Faster-Whisper word timestamps to create an `.ass` subtitle file.
- **Video assembly:** uses FFmpeg to normalize portrait clips, combine them, add narration, and burn in captions.

## Pipeline

```text
script.json
    |
    +--> make_voice.py ------> voice.mp3
    |
    +--> fetch_broll.py -----> clips/*.mp4
    |
    +--> make_captions.py ---> captions.ass
                                  |
clips/*.mp4 + voice.mp3 + captions.ass
                                  |
                             assemble.py
                                  |
                              final.mp4
```

## Tech Stack

- Python
- Pexels API
- Edge TTS
- Faster-Whisper
- FFmpeg / FFprobe
- ASS subtitles

## Requirements

- Python 3.10+
- FFmpeg and FFprobe installed and available on your `PATH`
- A Pexels API key
- Internet access for Pexels downloads and the initial Whisper model download

Install Python dependencies:

```bash
pip install -r req.txt
```

Set your Pexels API key as an environment variable:

```bash
# macOS / Linux
export PEXELS_API_KEY="your_pexels_api_key"

# Windows PowerShell
$env:PEXELS_API_KEY="your_pexels_api_key"
```

Get an API key from [Pexels](https://www.pexels.com/api/).

## Usage

Run the scripts from the project directory, in this order:

```bash
python make_voice.py
python fetch_broll.py
python make_captions.py
python assemble.py
```

The final rendered video is written to `final.mp4`.

### Customize the video

Edit `script.json` to change the content. Each scene contains:

- `voiceover`: narration for that scene
- `broll_query`: search phrase used to find a matching stock video

The file also contains the opening hook, title, call to action, video description, and hashtags. Keep the scene structure valid JSON.

## Project Structure

```text
.
├── script.json          # Video content and B-roll prompts
├── make_voice.py        # Generates voice.mp3
├── fetch_broll.py       # Downloads stock clips from Pexels
├── make_captions.py     # Transcribes narration into word-level captions
├── assemble.py          # Normalizes and assembles the final video
├── check_ffprobe.py     # FFprobe availability diagnostic
├── req.txt              # Python dependencies
└── clips/               # Downloaded and normalized video clips
```

## Notes

- `make_captions.py` uses the `base.en` Faster-Whisper model; the model is downloaded on first use.
- The video assembly script outputs a 1080 × 1920, 30 FPS portrait video.
- Pexels API availability, network access, and the installed FFmpeg build can affect execution.
- Review stock-media licensing and attribution requirements before publishing a generated video.
- The example `script.json` describes an aviation explainer; it is intended as sample content.

## Future Improvements

- Add command-line options for selecting scripts and output paths.
- Add retries and clearer handling for failed stock-video searches.
- Support multiple voices, languages, and caption styles.
- Add validation for script structure and missing scene clips.
- Separate generated media from source code and add a reproducible project setup.

## License

No license is currently specified. Add a license before redistributing or reusing this project.
