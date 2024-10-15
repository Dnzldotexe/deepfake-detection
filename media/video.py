import streamlit as st
import toml


config = toml.load("config.toml")
HUGGING_FACE_API_KEY = config["api"]["HUGGING_FACE_API_KEY"]

st.title("Detect deepfake in Image")

if "video" not in st.session_state:
    st.session_state.video = None

video_file = st.file_uploader("Browse Files", type=["mp4", "mkv"])

if video_file:
    st.session_state.video = video_file

if st.session_state.video:
    st.image(st.session_state.video)