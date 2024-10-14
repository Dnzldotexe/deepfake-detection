import streamlit as st

st.title("Detect deepfake in Audio")

if "item" not in st.session_state:
    st.session_state.item = None

audio_file = st.file_uploader("Browse Files", type=["mp3"])

if audio_file:
    st.session_state.item = audio_file

if st.session_state.item:
    st.image(st.session_state.item)