
import mlx_whisper
import ffmpeg
import os
from pathlib import Path

# CAMBIA ESTA RUTA CADA VEZ QUE USES EL SCRIPT
FILE_PATH = "/Users/josemiguelrozobaez/documents/develop/transcrypt/bitcoin.mp3"

# Extensiones de video y audio soportadas
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
AUDIO_EXTENSIONS = ['.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg']

def is_video(file_path):
    """Verifica si el archivo es un video basado en su extensión."""
    return Path(file_path).suffix.lower() in VIDEO_EXTENSIONS

def is_audio(file_path):
    """Verifica si el archivo es un audio basado en su extensión."""
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

def transcribe_file(file_path):
    print("\n🎬 Iniciando transcripción...")
    
    if not os.path.exists(file_path):
        print(f"❌ No existe el archivo: {file_path}")
        return
    
    file_name = Path(file_path).stem
    output_txt = f"/Users/josemiguelrozobaez/documents/develop/transcrypt/{file_name}.txt"
    
    if is_video(file_path):
        print("🎵 Extrayendo audio del video...")
        audio_temp = f"/Users/josemiguelrozobaez/documents/develop/transcrypt/temp_{file_name}.wav"
        if not extract_audio(file_path, audio_temp):
            print("❌ Error al extraer audio")
            return
        audio_to_transcribe = audio_temp
    elif is_audio(file_path):
        print("🎵 Procesando archivo de audio...")
        audio_to_transcribe = file_path
    else:
        print("❌ Tipo de archivo no soportado. Solo videos o audios.")
        return
    
    try:
        print("🤖 Transcribiendo (puede tardar varios minutos)...")
        result = mlx_whisper.transcribe(
            audio_to_transcribe,
            path_or_hf_repo="mlx-community/whisper-small-mlx-4bit",
            language="en",
            verbose=False
        )
        
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write(result['text'])
        
        if is_video(file_path) and os.path.exists(audio_to_transcribe):
            os.unlink(audio_to_transcribe)
        
        print(f"✅ Transcripción lista: {output_txt}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if is_video(file_path) and os.path.exists(audio_to_transcribe):
            os.unlink(audio_to_transcribe)

if __name__ == "__main__":
    transcribe_file(FILE_PATH)


# python transcriber.py
# ./venv/bin/python transcriber.py