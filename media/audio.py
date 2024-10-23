import streamlit as st
import os
import tempfile
from huggingface_hub import hf_hub_download
from transformers import pipeline
import soundfile as sf
from pydub import AudioSegment
import numpy as np

def convert_audio_to_wav(audio_file):
    try:
        # Create a temporary .wav file
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        
        # Save uploaded file to a temporary location
        temp_input = tempfile.NamedTemporaryFile(delete=False)
        temp_input.write(audio_file.read())
        temp_input.close()
        
        # Check if the input is already a WAV file (case-insensitive)
        if not audio_file.name.lower().endswith('.wav'):
            # Convert non-WAV file to WAV
            audio = AudioSegment.from_file(temp_input.name)
        else:
            # Load existing WAV file
            audio = AudioSegment.from_wav(temp_input.name)
        
        # Convert to mono and set sample rate to 16000 Hz (common for speech models)
        audio = audio.set_channels(1).set_frame_rate(16000)
        
        # Export to temporary WAV file
        audio.export(temp_wav.name, format="wav", parameters=["-ar", "16000"])
        
        # Clean up the input temporary file
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
    if option == "HyperMoon/wav2vec2-base-960h-finetuned-deepfake":
        model_id = option
        filenames = [
            "config.json",
            "preprocessor_config.json",
            "pytorch_model.bin",
            "training_args.bin",
        ]
    elif option == "MelodyMachine/Deepfake-audio-detection-V2":
        model_id = option
        filenames = [
            "config.json",
            "model.safetensors",
            "preprocessor_config.json",
            "training_args.bin",
        ]
    
    for filename in filenames:
        downloaded_model_path = hf_hub_download(
            repo_id=model_id,
            filename=filename,
            token=API_KEY
        )
    
    pipe = pipeline("audio-classification", model=model_id)
    return pipe

def display_result(token: str, option: str) -> str:
    try:
        # Convert the audio to WAV before using it
        wav_path = convert_audio_to_wav(st.session_state.audio)
        
        # Load the model
        pipe = load_model(token, option)
        
        # Read the audio data and sample rate using soundfile
        data, samplerate = sf.read(wav_path)
        
        # Ensure the data is float32
        data = data.astype(np.float32)
        
        # Run the audio data through the model
        result = pipe({"raw": data, "sampling_rate": samplerate})
        
        # Clean up temporary file
        os.unlink(wav_path)
        
        st.session_state.result = result
        return result
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        return None

def main() -> None:
    # page title
    st.title("Detect deepfake in Audio")

    # initialize cache
    if "audio" not in st.session_state:
        st.session_state.audio = None
    if "result" not in st.session_state:
        st.session_state.result = None

    # model choice
    option = st.selectbox(
        "Select Model",
        (
            "MelodyMachine/Deepfake-audio-detection-V2",
            "HyperMoon/wav2vec2-base-960h-finetuned-deepfake",
        ),
    )
    
    # store in audio object
    audio_file = st.file_uploader("Browse Files", type=["mp3", "m4a", "wav"])

    # grab token
    token = st.secrets["api"]["HUGGING_FACE_API_KEY"]

    # cache audio
    if audio_file:
        st.session_state.audio = audio_file
        # display audio
        st.audio(st.session_state.audio)
        # show result
        result = display_result(token, option)
        if result:
            st.write(result)

    # pull audio from cache
    elif st.session_state.audio:
        st.audio(st.session_state.audio)
        if st.session_state.result:
            st.write(st.session_state.result)
        st.session_state.audio = None
        st.session_state.result = None

main()
