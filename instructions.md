# Transcryp

Converts videos and audios to text locally using OpenAI's Whisper. Nothing is uploaded to the internet.

---

## Setup

**Step 1 — Install Python** (skip if already installed)

Download and install from [https://www.python.org/downloads/](https://www.python.org/downloads/)
During installation, check **"Add Python to PATH"**.

**Step 2 — Run setup**

Open a terminal in the project folder (right-click → "Open in Terminal") and run:
```bash
.\setup.bat
```
This creates the virtual environment and installs all dependencies.

---
run
.venv\Scripts\activate

## Usage

Drop your video or audio file into the `videos/` folder, then run:

```bash
python transcriber.py
```

The transcription `.txt` will appear in `output/` with the same filename.

**Supported formats:** `.mp4` `.avi` `.mov` `.mkv` `.wmv` `.webm` `.mp3` `.wav` `.m4a` `.flac` `.aac` `.ogg`

> First run downloads the Whisper model (~460 MB). Subsequent runs are faster.
