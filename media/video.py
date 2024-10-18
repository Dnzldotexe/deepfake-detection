import streamlit as st


HUGGING_FACE_API_KEY = st.secrets["api"]["HUGGING_FACE_API_KEY"]

st.title("Detect deepfake in Video")
st.warning("If you are seeing this, it means that there currently is no model loaded for this medium.", icon="⚠️")

if "video" not in st.session_state:
    st.session_state.video = None

video_file = st.file_uploader("Browse Files", type=["mp4", "mkv"])

if video_file:
    st.session_state.video = video_file
    st.balloons()

if st.session_state.video:
    st.video(st.session_state.video)