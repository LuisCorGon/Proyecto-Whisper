import streamlit as st
from communicator import Communicator
import tempfile
import os

comm = Communicator()


st.set_page_config(
    page_title="Subtitles Generator",
    page_icon="🎥",
    layout="wide",  # "centered" o "wide"
    initial_sidebar_state="expanded"  # "collapsed" o "expanded"
)

st.title("Subtitles Generator")
st.header("Welcome to the Subtitles Generator!")
st.subheader("This app allows you to generate translated subtitles for your videos.")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mkv", "mov", "flv", "wmv", "webm", "ogg", "mp3", "wav", "flac", "aac", "m4a", "3gp", "3g2", "mj2", "wma", "wmv", "asf", "amv"])
try:
    if uploaded_file is not None:
        st.write("Uploaded file:", uploaded_file)
        st.write("Filename:", uploaded_file.name)
        st.write("Type:", uploaded_file.type)
        st.write("Size:", uploaded_file.size)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            video_path = tmp_file.name
            st.success(f"File saved to temporary path: {video_path}")
except:
    st.error(f"An error occurred while saving the file: {uploaded_file.name}")

lenguages = ["es", "en", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko", "ar", "hi", "bn", "fa", "pl", "tr", "nl", "sv", "he", "da", "fi", "hu", "no", "ro", "uk", "vi", "ca", "el", "id", "ms", "th", "ur", "bg", "hr", "sr", "sk", "sl", "et", "lt", "lv", "mt", "eu", "gl", "cy", "sq", "be", "kk", "hy", "az", "ka", "mk", "mn", "nn", "ps", "tl", "pa", "so", "st", "ts", "sw", "uz", "af", "kab", "co", "haw", "yo", "is", "sw", "tl", "tg", "ta", "tt", "te", "ug", "uz", "ur", "yi", "zu"]
target_language = st.selectbox("Target language", lenguages)

model = st.selectbox("Model", ["small", "medium", "large", "tiny"])

if st.button("Generate subtitles"):
    st.text("Generating subtitles...")
    output_srt_path = f"{video_path}.srt"
    comm.send_initiator(True)


# comprobar que se ha generado el archivo y luego ejecutar este codigo
#st.download_button("Download SRT", output_srt_path)
    




