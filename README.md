# [https://deepfake-detection-artinte-infosec.streamlit.app/](https://deepfake-detection-artinte-infosec.streamlit.app/)
# Setting Up
## Clone the repository
```
git clone https://github.com/Dnzldotexe/deepfake-detection.git
```
## Go to project directory
```
cd deepfake-detection
```
## Creating a python virtual environment
```
python -m venv venv
```
## Activating the virtual environment
- Powershell: `.\venv\Scripts\activate`
- Bash: `source ./venv/bin/activate`
## Installing dependencies (this takes time)
```
pip install -r requirements.txt
```
## Install ffmpeg for audio detection
```
- Powershell: `winget install "FFmpeg (Essentials Build)"`
- Bash: `sudo apt-get install ffmpeg`
```
##  Adding your config file in .streamlit/ directory
```
cp secrets.toml.example secrets.toml
```
## Adding your Huggingface API key
- Create your Huggingface account and go to [Settings > Tokens](https://huggingface.co/settings/tokens)
- Create a READ type token and give it a name
- Copy the token and paste it to `secrets.toml`
- Your `secrets.toml` should look like below
```
[api]
HUGGING_FACE_API_KEY = "hf_iloveshrek"
```
## Running streamlit server
```
streamlit run .\app.py
```
## Stopping streamlit server
```
CTRL + C
```
## Deactivating the virtual environment
```
deactivate
```
