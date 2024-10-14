import streamlit as st

st.title("Detect deepfake in Audio")

audio_file = st.file_uploader("Browse Files", type=["mp3"])