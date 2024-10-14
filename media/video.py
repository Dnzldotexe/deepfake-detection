import streamlit as st

st.title("Detect deepfake in Video")

video_file = st.file_uploader("Browse Files", type=["mp4", "mkv"])

if video_file:
    st.image(video_file)