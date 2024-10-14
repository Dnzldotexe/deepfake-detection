import streamlit as st

st.title("Detect deepfake in Image")

image_file = st.file_uploader("Browse Files", type=["jpeg", "jpg", "png"])

if image_file:
    st.image(image_file)