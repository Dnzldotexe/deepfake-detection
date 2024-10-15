import streamlit as st
import os
import toml
import tempfile
from huggingface_hub import hf_hub_download
from transformers import pipeline


config = toml.load("config.toml")
HUGGING_FACE_API_KEY = config["api"]["HUGGING_FACE_API_KEY"]

model_id = "dima806/deepfake_vs_real_image_detection"
filenames = [
    "config.json",
    "model.safetensors",
    "preprocessor_config.json",
    "pytorch_model.bin",
    "training_args.bin",
]

for filename in filenames:
    downloaded_model_path = hf_hub_download(
        repo_id=model_id,
        filename=filename,
        token=HUGGING_FACE_API_KEY
    )

pipe = pipeline("image-classification", model=model_id, device=-1)


st.title("Detect deepfake in Image")

if "image" not in st.session_state:
    st.session_state.image = None

image_file = st.file_uploader("Browse Files", type=["jpeg", "jpg", "png", "webp"])

if image_file:
    st.session_state.image = image_file

if st.session_state.image:
    st.image(st.session_state.image)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = os.path.join(temp_dir, image_file.name)
        with open(temp_path, "wb") as f:
            f.write(image_file.getvalue())
        st.write(pipe(temp_path))