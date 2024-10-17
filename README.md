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
venv python -m venv deepfake
```
## Activating the virtual environment
- Powershell: `.\deepfake\Scripts\activate`
- Bash: `source ./deepfake/bin/activate`
## Installing dependencies (this takes time)
```
pip install -r requirements.txt
```
##  Adding your config file
```
cp config.toml.example config.toml
```
## Adding your Huggingface API key
- Create your Huggingface account and go to [Settings > Tokens](https://huggingface.co/settings/tokens)
- Create a READ type token and give it a name
- Copy the token and paste it to `config.toml`
- Your `config.toml` should look like below
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