# Transcryp

Converts videos and audios to text locally using OpenAI's Whisper. Nothing is uploaded to the internet.

---

## Setup

1. Open a terminal in the project folder (`cmd` or PowerShell — right-click the folder → "Open in Terminal")
2. Run:
```bash
setup.bat
```
3. Wait for it to finish, then **restart your terminal** so the new PATH entries take effect.

---

## Usage

Drop your video or audio file into the `videos/` folder, then run:

```bash
python transcriber.py
```

The transcription `.txt` will appear in `output/` with the same filename.

**Supported formats:** `.mp4` `.avi` `.mov` `.mkv` `.wmv` `.webm` `.mp3` `.wav` `.m4a` `.flac` `.aac` `.ogg`

> First run downloads the Whisper model (~460 MB). Subsequent runs are faster.
