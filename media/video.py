import streamlit as st

st.title("Detect deepfake in Video")

if "item" not in st.session_state:
    st.session_state.item = None

video_file = st.file_uploader("Browse Files", type=["mp4", "mkv"])

if video_file:
    st.session_state.item = video_file

if st.session_state.item:
    st.image(st.session_state.item)