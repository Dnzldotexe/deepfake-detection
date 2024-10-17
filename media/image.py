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

def temp_path(image_file: str) -> str:
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, image_file.name)
    with open(temp_path, "wb") as f:
        f.write(image_file.getvalue())
    return temp_path, temp_dir

@st.cache_resource
def load_model(API_KEY: str, option: str):
    if option == "dima806/deepfake_vs_real_image_detection":
        model_id = option
        filenames = [
            "config.json",
            "model.safetensors",
            "preprocessor_config.json",
            "pytorch_model.bin",
            "training_args.bin",
        ]
        pipe = pipeline("image-classification", model=model_id, device=-1)
    if option == "Wvolf/ViT_Deepfake_Detection":
        model_id = option
        filenames = [
            "config.json",
            "preprocessor_config.json",
            "pytorch_model.bin",
            "training_args.bin",
        ]
        pipe = pipeline("image-classification", model=model_id, device=-1)
    if option == "prithivMLmods/Deep-Fake-Detector-Model":
        model_id = option
        filenames = [
            "config.json",
            "model.safetensors",
            "preprocessor_config.json",
            "pytorch_model.bin",
            "training_args.bin",
        ]
        pipe = pipeline("image-classification", model=model_id, device=-1)
    if option == "not-lain/deepfake" or option == "SivaResearch/Fake_Detection":
        model_id = option
        filenames = [
            "config.json",
            "deepfakeconfig.py",
            "deepfakemodel.py",
            "model.safetensors",
            "pipeline.py",
            "pytorch_model.bin",
            "requirements.txt",
        ]
        pipe = pipeline(model="not-lain/deepfake", trust_remote_code=True)
    for filename in filenames:
        downloaded_model_path = hf_hub_download(
            repo_id=model_id,
            filename=filename,
            token=API_KEY
        )
    return pipe

def display_result(token: str, option: str) -> str:
    path, dir = temp_path(st.session_state.image)
    pipe = load_model(token, option)
    if option == "not-lain/deepfake" or option == "SivaResearch/Fake_Detection":
        result = pipe.predict(path)
        st.session_state.result = result["confidences"]
        return result["confidences"]
    else:
        result = pipe(path)
        st.session_state.result = result
        return result

def main() -> None:
    # page title
    st.title("Detect deepfake in Image")

    # initialize cache
    if "image" not in st.session_state:
        st.session_state.image = None
    if "result" not in st.session_state:
        st.session_state.result = None

    # model choice
    option = st.selectbox(
        "Select Model",
        (
            "not-lain/deepfake",
            "SivaResearch/Fake_Detection",
            "dima806/deepfake_vs_real_image_detection", 
            "Wvolf/ViT_Deepfake_Detection", 
            "prithivMLmods/Deep-Fake-Detector-Model",
        ),
    )
    
    # store in image object
    image_file = st.file_uploader("Browse Files", type=["jpeg", "jpg", "png", "webp"])

    # grab token
    token = load_api_key()

    # cache image
    if image_file:
        st.session_state.image = image_file
        # display image
        st.image(st.session_state.image)
        # show result
        result = display_result(token, option)
        st.write(result)

    # pull image from cache
    elif st.session_state.image:
        st.image(st.session_state.image)
        st.write(st.session_state.result)
        st.session_state.image = None
        st.session_state.result = None

main()