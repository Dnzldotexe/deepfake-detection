import streamlit as st

st.title("Detect deepfake in Audio")

audio_file = st.file_uploader("Browse Files", type=["mp3"])

if audio_file:
    st.image(audio_file)