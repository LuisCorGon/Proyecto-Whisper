import whisper
import os

def generate_translated_srt(video_path, output_srt_path, target_language="es", model="large"):
    # Comprueba si el archivo existe
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Archivo no encontrado: {video_path}")
    # Carga el modelo de Whisper
    model = whisper.load_model(model)  # Usa "large" para mejores traducciones

    # Procesa el video y transcribe/traduce
    print("Procesando el video...")
    result = model.transcribe(video_path, task="translate", language=target_language)

    # Genera el archivo SRT
    print("Generando el archivo SRT...")
    with open(output_srt_path, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(result['segments']):
            start = format_time(segment['start'])   
            end = format_time(segment['end'])
            text = segment['text']

            # Escribe en formato SRT
            srt_file.write(f"{i + 1}\n")
            srt_file.write(f"{start} --> {end}\n")
            srt_file.write(f"{text.strip()}\n\n")

    print(f"Archivo SRT generado en: {output_srt_path}")

def format_time(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hrs, secs = divmod(seconds, 3600)
    mins, secs = divmod(secs, 60)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

# Ruta del video MP4 y salida SRT
video_path = "video.mp4"
output_srt_path = "subtitles.srt"

generate_translated_srt(video_path, output_srt_path)
