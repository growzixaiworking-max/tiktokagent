# Growzix TikTok Automation - Project Guidelines

## Tech Stack
- Python 3.10+
- Gemini API for LLM tasks.
- MoviePy for video editing.

## Structure
- `/src`: Source code
  - `/scripts`: Script generation logic
  - `/voice`: Audio generation logic
  - `/video`: Video assembly logic
- `/assets`: Stock clips, audio, fonts
- `/output`: Final rendered videos
- `/data`: SQLite database

## Standards
- Use environment variables for API keys.
- Log all AI generation steps.
- Ensure captions are high-contrast and centered for TikTok.
