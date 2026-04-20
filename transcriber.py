
import whisper
import imageio_ffmpeg
import subprocess
import numpy as np
import wave
import warnings
import tempfile
import sys
import os
from pathlib import Path
from tqdm import tqdm

warnings.filterwarnings("ignore")

VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
AUDIO_EXTENSIONS = ['.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg']

BASE_DIR = Path(__file__).parent
VIDEOS_DIR = BASE_DIR / "videos"
OUTPUT_DIR = BASE_DIR / "output"
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def is_video(file_path):
    return Path(file_path).suffix.lower() in VIDEO_EXTENSIONS

def is_audio(file_path):
    return Path(file_path).suffix.lower() in AUDIO_EXTENSIONS

def extract_audio(input_path, output_wav):
    subprocess.run(
        [FFMPEG_EXE, "-y", "-i", input_path,
         "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", output_wav],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

def load_wav_as_array(wav_path):
    with wave.open(wav_path, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
    return np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0

def transcribe_file(file_path, model):
    print(f"\n🎬 Transcribing: {Path(file_path).name}")

    file_name = Path(file_path).stem
    output_txt = OUTPUT_DIR / f"{file_name}.txt"

    try:
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        audio_temp = tmp.name
        tmp.close()

        print("🎵 Extracting audio...")
        extract_audio(file_path, audio_temp)

        print("🤖 Transcribing (this may take a few minutes)...")
        audio_array = load_wav_as_array(audio_temp)

        CHUNK = whisper.audio.CHUNK_LENGTH * whisper.audio.SAMPLE_RATE
        chunks = [audio_array[i:i+CHUNK] for i in range(0, len(audio_array), CHUNK)]
        texts = []
        for chunk in tqdm(chunks, desc="Progress", unit="chunk", file=sys.stdout, dynamic_ncols=False):
            padded = whisper.audio.pad_or_trim(chunk)
            mel = whisper.audio.log_mel_spectrogram(padded).to(model.device)
            opts = whisper.DecodingOptions(language="en", without_timestamps=True)
            texts.append(model.decode(mel, opts).text)
        result = {"text": " ".join(texts)}

        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write(result['text'])

        print(f"✅ Done: {output_txt}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if os.path.exists(audio_temp):
            os.unlink(audio_temp)

if __name__ == "__main__":
    VIDEOS_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    files = [f for f in VIDEOS_DIR.iterdir() if f.is_file() and (is_video(str(f)) or is_audio(str(f)))]

    if not files:
        print("⚠️  No video or audio files found in the 'videos' folder.")
    else:
        to_process = []
        for file_path in files:
            output_txt = OUTPUT_DIR / f"{file_path.stem}.txt"
            if output_txt.exists():
                print(f"⏭️  Skipping '{file_path.name}' — already transcribed.")
            else:
                to_process.append(file_path)

        if not to_process:
            print("✅ All files already transcribed. Nothing to do.")
        else:
            print("🤖 Loading Whisper model...")
            model = whisper.load_model("small")
            for file_path in to_process:
                transcribe_file(str(file_path), model)

# python transcriber.py
