import streamlit as st
import os
import tempfile
from huggingface_hub import hf_hub_download
from transformers import pipeline
import soundfile as sf
from pydub import AudioSegment
import numpy as np
import torch

def convert_audio_to_wav(audio_file):
    try:
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        
        temp_input = tempfile.NamedTemporaryFile(delete=False)
        temp_input.write(audio_file.read())
        temp_input.close()
        
        if not audio_file.name.lower().endswith('.wav'):
            audio = AudioSegment.from_file(temp_input.name)
        else:
            audio = AudioSegment.from_wav(temp_input.name)
        
        # Standardize audio format
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        # Normalize audio
        audio = audio.normalize()
        
        # Export with specific parameters
        audio.export(
            temp_wav.name,
            format="wav",
            parameters=[
                "-ar", "16000",  # Sample rate
                "-ac", "1",      # Channels
                "-acodec", "pcm_s16le"  # 16-bit PCM encoding
            ]
        )
        
        os.unlink(temp_input.name)
        return temp_wav.name
    except Exception as e:
        if 'temp_input' in locals():
            os.unlink(temp_input.name)
        if 'temp_wav' in locals():
            os.unlink(temp_wav.name)
        raise Exception(f"Error converting audio: {str(e)}")

@st.cache_resource
def load_model(API_KEY: str, option: str):
    model_configs = {
        "HyperMoon/wav2vec2-base-960h-finetuned-deepfake": {
            "filenames": [
                "config.json",
                "preprocessor_config.json",
                "pytorch_model.bin",
                "training_args.bin",
            ]
        },
        "MelodyMachine/Deepfake-audio-detection-V2": {
            "filenames": [
                "config.json",
                "model.safetensors",
                "preprocessor_config.json",
                "training_args.bin",
            ]
        }
    }
    
    if option not in model_configs:
        raise ValueError(f"Unknown model option: {option}")
        
    model_id = option
    filenames = model_configs[option]["filenames"]
    
    for filename in filenames:
        downloaded_model_path = hf_hub_download(
            repo_id=model_id,
            filename=filename,
            token=API_KEY
        )
    
    pipe = pipeline("audio-classification", model=model_id, token=API_KEY)
    return pipe

def process_audio(data, samplerate):
    # Ensure the audio is the right length (5 seconds)
    target_length = 5 * samplerate
    if len(data) > target_length:
        # Take the middle 5 seconds
        start = (len(data) - target_length) // 2
        data = data[start:start + target_length]
    elif len(data) < target_length:
        # Pad with zeros
        padding = np.zeros(target_length - len(data))
        data = np.concatenate([data, padding])
    
    # Normalize the audio
    data = data / np.max(np.abs(data))
    return data

def display_result(token: str, option: str) -> str:
    try:
        wav_path = convert_audio_to_wav(st.session_state.audio)
        pipe = load_model(token, option)
        
        # Read and process audio
        data, samplerate = sf.read(wav_path)
        data = process_audio(data, samplerate)
        
        # Run inference
        result = pipe(
            {"raw": data, "sampling_rate": samplerate},
            top_k=None  # Get all class probabilities
        )
        
        os.unlink(wav_path)
        
        # Format results for display
        formatted_results = []
        for r in result:
            formatted_results.append({
                "label": r["label"],
                "confidence": f"{r['score']*100:.2f}%"
            })
        
        st.session_state.result = formatted_results
        return formatted_results
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        return None

def main() -> None:
    st.title("Detect deepfake in Audio")
    
    if "audio" not in st.session_state:
        st.session_state.audio = None
    if "result" not in st.session_state:
        st.session_state.result = None

    option = st.selectbox(
        "Select Model",
        (
            "MelodyMachine/Deepfake-audio-detection-V2",
            "HyperMoon/wav2vec2-base-960h-finetuned-deepfake",
        ),
    )
    
    audio_file = st.file_uploader("Browse Files", type=["mp3", "m4a", "wav"])
    token = st.secrets["api"]["HUGGING_FACE_API_KEY"]

    if audio_file:
        st.session_state.audio = audio_file
        st.audio(st.session_state.audio)
        
        with st.spinner('Processing audio...'):
            result = display_result(token, option)
            
        if result:
            st.subheader("Analysis Results:")
            for r in result:
                st.write(f"**{r['label']}:** {r['confidence']}")

    elif st.session_state.audio:
        st.audio(st.session_state.audio)
        if st.session_state.result:
            st.subheader("Previous Results:")
            for r in st.session_state.result:
                st.write(f"**{r['label']}:** {r['confidence']}")
        st.session_state.audio = None
        st.session_state.result = None

main()
