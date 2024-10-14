import streamlit as st

st.title("Detect deepfake in Image")

if "image" not in st.session_state:
    st.session_state.image = None

image_file = st.file_uploader("Browse Files", type=["jpeg", "jpg", "png"])

if image_file:
    st.session_state.image = image_file

if st.session_state.image:
    st.image(st.session_state.image)