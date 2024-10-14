import streamlit as st

st.title("Detect deepfake in Audio")

if "audio" not in st.session_state:
    st.session_state.audio = None

audio_file = st.file_uploader("Browse Files", type=["mp3"])

if audio_file:
    st.session_state.audio = audio_file

if st.session_state.audio:
    st.image(st.session_state.audio)