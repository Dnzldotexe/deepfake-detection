import streamlit as st

st.title("Detect deepfake in Image")

if "item" not in st.session_state:
    st.session_state.item = None

image_file = st.file_uploader("Browse Files", type=["jpeg", "jpg", "png"])

if image_file:
    st.session_state.item = image_file

if st.session_state.item:
    st.image(st.session_state.item)