import streamlit as st
import os
import toml
import tempfile
from huggingface_hub import hf_hub_download
from transformers import pipeline


def load_api_key() -> str:
    config = toml.load("config.toml")
    HUGGING_FACE_API_KEY = config["api"]["HUGGING_FACE_API_KEY"]
    return HUGGING_FACE_API_KEY

@st.cache_resource
def load_model_resnetinception(API_KEY: str):
    model_id = "SivaResearch/Fake_Detection"
    filenames = [
        "config.json",
        "deepfakeconfig.py",
        "deepfakemodel.py",
        "model.safetensors",
        "pipeline.py",
        "pytorch_model.bin",
        "requirements.txt",
    ]
    for filename in filenames:
        downloaded_model_path = hf_hub_download(
            repo_id=model_id,
            filename=filename,
            token=API_KEY
        )
    return pipeline(model="not-lain/deepfake", trust_remote_code=True)

def temp_path(image_file):
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, image_file.name)
    with open(temp_path, "wb") as f:
        f.write(image_file.getvalue())
    return temp_path, temp_dir

def main() -> None:
    # page title
    st.title("Detect deepfake in Image")

    # initialize cache
    if "image" not in st.session_state:
        st.session_state.image = None
    if "result" not in st.session_state:
        st.session_state.result = None
    # store in image object
    image_file = st.file_uploader("Browse Files", type=["jpeg", "jpg", "png", "webp"])

    # grab token
    token = load_api_key()

    # cache image
    if image_file:
        st.session_state.image = image_file
        # display image
        st.image(st.session_state.image)
        path, dir = temp_path(st.session_state.image)
        pipe = load_model_resnetinception(token)
        result = pipe.predict(path)
        st.write(result["confidences"])
        st.session_state.result = result["confidences"]

    # pull image from cache
    if not image_file and st.session_state.image:
        st.image(st.session_state.image)
        st.write(st.session_state.result)

main()