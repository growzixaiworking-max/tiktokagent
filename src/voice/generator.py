import os
import requests
from dotenv import load_dotenv

load_dotenv()

class VoiceGenerator:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.url = "https://api.elevenlabs.io/v1/text-to-speech/CwhRBWXzGAHq8TQ4Fs17" # Valid Voice ID

    def generate_voice(self, text, output_filename):
        if not self.api_key:
            print("Error: ELEVENLABS_API_KEY not found.")
            return None

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        print(f"🎙️ Generating AI Voice for: {text[:50]}...")
        response = requests.post(self.url, json=data, headers=headers)

        if response.status_code == 200:
            with open(output_filename, "wb") as f:
                f.write(response.content)
            return output_filename
        else:
            print(f"Failed to generate voice: {response.text}")
            return None

if __name__ == "__main__":
    # Test
    gen = VoiceGenerator()
    # gen.generate_voice("Hello, this is a test for Growzix Estimating.", "assets/audio/test.mp3")
