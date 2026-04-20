
import whisper
import ffmpeg
import os
from pathlib import Path

VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
AUDIO_EXTENSIONS = ['.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg']

BASE_DIR = Path(__file__).parent
VIDEOS_DIR = BASE_DIR / "videos"
OUTPUT_DIR = BASE_DIR / "output"

def is_video(file_path):
    return Path(file_path).suffix.lower() in VIDEO_EXTENSIONS

def is_audio(file_path):
    return Path(file_path).suffix.lower() in AUDIO_EXTENSIONS

def extract_audio(video_path, audio_path):
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return True
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode()}")
        return False

def transcribe_file(file_path, model):
    print(f"\n🎬 Transcribing: {file_path}")

    file_name = Path(file_path).stem
    output_txt = OUTPUT_DIR / f"{file_name}.txt"
    audio_temp = OUTPUT_DIR / f"temp_{file_name}.wav"

    if is_video(file_path):
        print("🎵 Extracting audio from video...")
        if not extract_audio(file_path, str(audio_temp)):
            print("❌ Failed to extract audio")
            return
        audio_to_transcribe = str(audio_temp)
    elif is_audio(file_path):
        print("🎵 Processing audio file...")
        audio_to_transcribe = file_path
    else:
        print("❌ Unsupported file type.")
        return

    try:
        print("🤖 Transcribing (this may take a few minutes)...")
        result = model.transcribe(audio_to_transcribe, language="en")

        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write(result['text'])

        if is_video(file_path) and os.path.exists(audio_to_transcribe):
            os.unlink(audio_to_transcribe)

        print(f"✅ Done: {output_txt}")

    except Exception as e:
        print(f"❌ Error: {e}")
        if is_video(file_path) and os.path.exists(audio_to_transcribe):
            os.unlink(audio_to_transcribe)

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