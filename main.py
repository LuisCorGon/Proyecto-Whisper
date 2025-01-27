import os
import whisper
import streamlit as st
import tempfile
import logging
import deepl
import json
import subprocess
from pathlib import Path


with open("config.json", "r") as file:
    config = json.load(file)
auth_key = config["deepl_auth_key"]
translator = deepl.Translator(auth_key, server_url="https://api-free.deepl.com")
logging.info(f"DeepL auth key: {auth_key}")

def generate_translated_srt(video_path, output_srt_path, actual_language="EN", target_language_input="ES", model="large"):
    # Comprueba si el archivo existe
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Archivo no encontrado: {video_path}")
    # Carga el modelo de Whisper
    model = whisper.load_model(model)  # Usa "large" para mejores traducciones

    # Procesa el video y transcribe/traduce
    print("Procesando el video...")
    result = model.transcribe(video_path, task="translate" , language=actual_language.lower())

    # Genera el archivo SRT
    print("Generando el archivo SRT...")
    current_directory = os.getcwd()  
    output_srt_path = os.path.join(current_directory, os.path.basename(video_path) + ".srt")
    with open(output_srt_path, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(result['segments']):
            start = format_time(segment['start'])   
            end = format_time(segment['end'])
            text = segment['text']
            print("Lenguaje actual:", actual_language, "Lenguaje destino:", target_language_input)
            translated_text = translator.translate_text(text,source_lang=actual_language,target_lang=target_language_input).text
            logging.info(f"Text: {translated_text}")

            # Escribe en formato SRT
            srt_file.write(f"{i + 1}\n")
            srt_file.write(f"{start} --> {end}\n")
            srt_file.write(f"{translated_text.strip()}\n\n")

    print(f"Archivo SRT generado en: {output_srt_path}")

def format_time(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hrs, secs = divmod(seconds, 3600)
    mins, secs = divmod(secs, 60)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

def embed_subtitles(video_path, subtitles_path, output_path):
    try:

        # Obtén las rutas completas
        video_path = Path(video_path).resolve()
        subtitles_path = Path(subtitles_path).resolve()
        output_path = Path(output_path).resolve()

        print("Ruta completa del video:", video_path)
        print("Ruta completa de los subtítulos:", subtitles_path)
        print("Ruta completa de salida:", output_path)

        command = [
            "ffmpeg", "-i", video_path,
            "-vf", f"subtitles={subtitles_path}",
            "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental",
            output_path
        ]
        print("Ejecutando comando FFmpeg:", " ".join(command))
        subprocess.run(command, check=True)
        print("Subtítulos incrustados correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False




logging.basicConfig(level=logging.DEBUG) 

st.set_page_config(
    page_title="Subtitles Generator",
    page_icon="🎥",
    layout="wide",  # "centered" o "wide"
    initial_sidebar_state="expanded"  # "collapsed" o "expanded"
)

st.title("Subtitles Generator")
st.header("Welcome to the Subtitles Generator!")
st.subheader("This app allows you to generate translated subtitles for your videos.")

try:
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mkv", "mov", "flv", "wmv", "webm", "ogg", "mp3", "wav", "flac", "aac", "m4a", "3gp", "3g2", "mj2", "wma", "wmv", "asf", "amv"])
    if uploaded_file is not None:
        
        st.success(f"File uploaded successfully!")
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            video_path = tmp_file.name
            st.info(f"Video path: {video_path}")

    else:
        st.error("No file uploaded yet. ")
except Exception as e:
    st.error(f"An error occurred:")



translation_source_lenguages = ["AR", "BG", "CS", "DA","DE","EL","EN","ES","ET","FI","FR","HU","ID","IT","JA","KO","LT","LV","NB","NL","PL","PT","RO","RU","SK","SL","SV","TR","UK","ZH"]
translation_target_lenguages = ["AR", "BG", "CS","DA" ,"DE" ,"EL" ,"EN","EN-GB","ES","ET","FI","FR","HU","ID","IT","JA","KO","LT","LV","NB","NL","PL","PT","RO","RU","SK","SL","SV","TR","UK","ZH"]

actual_language = st.selectbox("Actual language", translation_source_lenguages)
target_language_input = st.selectbox("Target language", translation_target_lenguages)

model = st.selectbox("Model", ["small", "medium", "large", "tiny"])

if st.button("Generate subtitles"):
    if uploaded_file is None:
        st.error("Please upload a video or audio file first!")
    else:
        if model in ["tiny", "small", "medium"] and actual_language != "EN":
            st.warning("The selected model is not suitable for the selected language. Switching to 'large' model.")
            model = "large"
        output_srt_path = f"{os.path.splitext(video_path)[0]}.srt"
        with st.spinner("Generating subtitles..."):
            try:
                generate_translated_srt(
                    video_path, output_srt_path,
                    actual_language=actual_language,
                    target_language_input=target_language_input,
                    model=model
                )
                output_video_path = f"{os.path.splitext(video_path)[0]}_with_subtitles.mp4"
                success = embed_subtitles(video_path, output_srt_path, output_video_path)
                if success:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success("Subtitles generated successfully!")
                        with open(output_srt_path, "rb") as file:
                            st.download_button("Download SRT", file, f"{uploaded_file.name}.srt", "text/srt")
                    with col2:
                        st.success("Video with subtitles generated successfully!")
                        with open(output_video_path, "rb") as file:
                            st.download_button("Download Video", file, f"{uploaded_file.name}_with_subtitles.mp4", "video/mp4")
                else:
                    st.error("Error generating subtitles")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                if os.path.exists(video_path):
                    os.remove(video_path)
                    st.info(f"Temporary file deleted: {video_path}")


    




