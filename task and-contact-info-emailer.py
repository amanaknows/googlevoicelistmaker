import openai_secret_manager
import json
import io
import re
import smtplib
import nltk
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from nltk.tokenize import word_tokenize

#get api credentials
secrets = openai_secret_manager.get_secrets("google")

# Build the Google Voice API service
service = build('voice', 'v1', credentials=Credentials.from_authorized_user_info(info=secrets))

# Get the voicemail list
results = service.voicemails().list(phoneNumber='<YOUR_PHONE_NUMBER>').execute()

# Use Google Cloud Speech-to-Text API to transcribe the audio
def transcribe_audio(audio_file_path):
    """
    Transcribe audio file using Google Cloud Speech-to-Text API
    """

    client = speech_v1.SpeechClient()

    # The language of the supplied audio
    language_code = "en-US"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
    }
    with open(audio_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        return alternative.transcript

# A list to store the customer's needs and wants
needs_and_wants = []

# A dictionary to store the customer's contact information
contact_info = {}

# download the Punkt tokenizer
nltk.download('punkt')

for voicemail in results.get('voicemails', []):
    # Get the voicemail audio file
    audio_file = service.voicemails().get(phoneNumber='<YOUR_PHONE_NUMBER>', id=voicemail['id']).execute()

    # Transcribe the audio to text
    text = transcribe_audio(audio_file)
    # Extract the customer's information
    # Extract the customer's name
    name = ""
    # Extract the customer's phone number
    phone_number = ""
    # Extract the customer's needs and wants
    needs_and_wants = []
   
    contact_info = {"name":name, "phone_number":phone_number}

# Email credentials
email_address 
