# Project Plan: TikTok AI Content Automation System (Growzix Estimating)

## 1. Overview
Automated system to generate, edit, and manage TikTok content for the USA construction estimation market.

## 2. Tech Stack
- **Language:** Python (Best for AI, video processing, and automation)
- **AI Text (Scripts/Captions):** Gemini API (Google)
- **AI Voice:** ElevenLabs API or OpenAI Audio
- **Video Processing:** MoviePy (Python library)
- **Stock Footage:** Pexels API / Pixabay API
- **Database:** SQLite (Local storage for scripts and metadata)
- **Automation:** GitHub Actions or local CRON jobs for scheduling.

## 3. Implementation Phases

### Phase 1: Core Content Engine (The "What")
1.  **Script Generator:** Prompt engineering for construction estimation hooks, body, and CTAs.
2.  **Voice Generator:** Converting scripts to high-quality US-English audio.
3.  **Video Assembler:**
    - Download stock construction clips.
    - Overlay AI voice.
    - Burn captions (subtitles) onto the video.
    - Add background music.
4.  **Metadata Generator:** Generate captions and hashtags.

### Phase 2: Database & Dashboard
1.  **Storage:** Save every generated video with its script and status.
2.  **CLI/Web Interface:** A simple way to trigger generation and review content.

### Phase 3: Scheduling & Analytics
1.  **Auto-Post/Schedule:** Integration with TikTok Content Posting API (or manual queue system).
2.  **Analytics:** Track view/lead performance.

## 4. Immediate Next Steps (Today)
1.  Initialize Python environment.
2.  Create Script Generator Module.
3.  Source initial stock footage URLs or API integration.
4.  Generate first 20 scripts as requested.
