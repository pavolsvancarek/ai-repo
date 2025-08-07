import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

def transcribe(filename):
    with open(filename, "rb") as f:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer " + API_KEY},
            files={"file": (filename, f, "audio/wav")},
            data={"model": "whisper-1"}
        )

    try:
        return response.json()["text"]
    except Exception as e:
        print("CHYBA v odpovedi Whisper API:", response.text)
        return ""
