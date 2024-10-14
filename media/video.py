import streamlit as st

st.title("Detect deepfake in Video")

if "video" not in st.session_state:
    st.session_state.video = None

video_file = st.file_uploader("Browse Files", type=["mp4", "mkv"])

if video_file:
    st.session_state.video = video_file

if st.session_state.video:
    st.image(st.session_state.video)