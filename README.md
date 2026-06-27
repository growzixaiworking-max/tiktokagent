# Growzix TikTok Automation - Final Instructions

## 1. Setup
- **Install Python 3.10+**
- **Install ImageMagick:** Required by MoviePy to write text on videos.
  - Download from: https://imagemagick.org/script/download.php
- **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

## 2. Configuration
- Open `.env` and add your API Keys:
  - `GEMINI_API_KEY`: For script generation.
  - `PEXELS_API_KEY`: For stock footage (Get it free at pexels.com/api).
  - `ELEVENLABS_API_KEY`: For premium AI voice (Optional, or use OpenAI).

## 3. Usage
- To generate 3 test videos, run:
  ```bash
  python main.py
  ```
- Check the `output/` folder for your `.mp4` files.

## 4. Posting Schedule (USA EST)
- 8:00 AM
- 12:00 PM
- 6:00 PM
- 9:00 PM

## 5. Next Steps for Scalability
- **Voiceover:** Currently, the system uses text overlays. To add voice, connect the `src/voice` module to ElevenLabs.
- **Lead Capture:** Once you have 1,000 followers, add your website link to the TikTok bio.
