import streamlit as st
import tempfile
from huggingface_hub import hf_hub_download
from transformers import pipeline
import soundfile as sf
from pydub import AudioSegment


# Convert the audio to a format that soundfile can read (like WAV)
def convert_audio_to_wav(audio_file):
    # Create a temporary .wav file
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    # If the input is not a .wav, convert it to .wav
    if audio_file.name[-3:] != "wav":
        audio = AudioSegment.from_file(audio_file)  # Automatically detects the format
    else:
        # If already a .wav, copy it to the temporary file
        audio = AudioSegment.from_wav(audio_file)  # Load the .wav file directly
    # Convert the (now .wav) file to mono
    audio = audio.set_channels(1)
    audio.export(temp_wav.name, format="wav")  # Overwrite with mono .wav
    return temp_wav.name

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
        pipe = pipeline("audio-classification", model=model_id)
    if option == "MelodyMachine/Deepfake-audio-detection-V2":
        model_id = option
        filenames = [
            "config.json",
            "model.safetensors",
            "preprocessor_config.json",
            "training_args.bin",
        ]
        pipe = pipeline("audio-classification", model=model_id)
    for filename in filenames:
        downloaded_model_path = hf_hub_download(
            repo_id=model_id,
            filename=filename,
            token=API_KEY
        )
    return pipe

def display_result(token: str, option: str) -> str:
    # Convert the audio to WAV before using it
    wav_path = convert_audio_to_wav(st.session_state.audio)
    pipe = load_model(token, option)
    # Read the audio data and sample rate using soundfile
    data, samplerate = sf.read(wav_path)  # Read the WAV file into data
    # Run the audio data through the model
    result = pipe(data)
    st.session_state.result = result
    return result

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
        st.write(result)

    # pull audio from cache
    elif st.session_state.audio:
        st.audio(st.session_state.audio)
        st.write(st.session_state.result)
        st.session_state.audio = None
        st.session_state.result = None

main()
