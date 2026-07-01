import os
import json
import sqlite3
from src.video.downloader import VideoDownloader
from src.video.assembler import VideoAssembler
from src.voice.generator import VoiceGenerator
from src.utils.notifier import EmailNotifier
from src.scripts.generate_initial_scripts import ScriptGenerator
from dotenv import load_dotenv

load_dotenv()

load_dotenv()

def log_to_db(script_id, topic, video_path):
    conn = sqlite3.connect('data/growzix.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO videos (script_id, topic, video_path, status) VALUES (?, ?, ?, ?)", 
              (script_id, topic, video_path, 'Generated'))
    conn.commit()
    conn.close()

def get_generated_script_ids():
    conn = sqlite3.connect('data/growzix.db')
    c = conn.cursor()
    c.execute("SELECT script_id FROM videos WHERE status = 'Generated'")
    ids = [row[0] for row in c.fetchall()]
    conn.close()
    return ids

def generate_metadata(script):
    description = script.get('description', 'No description provided.')
    hashtags = script.get('seo_hashtags', '#construction #estimation #builder')
    return f"{description}\n\n{hashtags}"

def main():
    print("🚀 Starting Growzix TikTok Automation System...")
    
    # 1. Load Scripts
    script_file = "data/initial_scripts.json"
    if not os.path.exists(script_file):
        print("Error: Scripts not found. Generating initial set...")
        ScriptGenerator().update_script_file()

    with open(script_file, "r") as f:
        scripts = json.load(f)

    # 2. Initialize Modules
    downloader = VideoDownloader()
    assembler = VideoAssembler()
    voice_gen = VoiceGenerator()
    notifier = EmailNotifier()
    script_gen = ScriptGenerator()

    # 3. Get already generated IDs to avoid duplication
    generated_ids = get_generated_script_ids()
    print(f"ℹ️ Already generated Script IDs: {generated_ids}")

    # Check if we have any scripts left to process
    scripts_to_process = [s for s in scripts if s["id"] not in generated_ids]
    
    if not scripts_to_process:
        print("\n♻️ No new scripts available. Generating fresh content...")
        script_gen.update_script_file()
        # Reload scripts after generation
        with open(script_file, "r") as f:
            scripts = json.load(f)
        scripts_to_process = [s for s in scripts if s["id"] not in generated_ids]

    if not scripts_to_process:
        print("❌ Failed to generate new scripts. Exiting.")
        return

    # Map topics to relevant high-quality stock video search queries
    search_queries = {
        "Estimation Mistake": "construction site",
        "Material Takeoff": "house blueprints",
        "Profit Margins": "roof construction",
        "Lumber Prices": "concrete pouring",
        "Concrete Estimation": "excavator digging"
    }

    # Generate up to 5 fresh videos in this run
    videos_to_generate = 5
    generated_count = 0

    for script in scripts_to_process:
        if generated_count >= videos_to_generate:
            break
            
        script_id = script["id"]
        # No need to check generated_ids here as we filtered scripts_to_process already


        print(f"\n🎬 Processing NEW Video {script_id}: {script['topic']}")
        
        # A. Download Footage based on AI suggested visual query
        query = script.get('visual_query', 'construction worker')
        clips = downloader.search_and_download(query, count=1)
        if not clips: 
            print(f"⚠️ Could not download clips for query: {query}. Skipping.")
            continue
        video_path = clips[0]

        # B. Generate Voice 
        full_text = f"{script['hook']} {script['body']} {script['cta']}"
        audio_filename = f"assets/audio/voice_{script_id}.mp3"
        audio_path = voice_gen.generate_voice(full_text, audio_filename)
        
        # C. Assemble Video
        print(f"🔨 Assembling Professional Video {generated_count+1}/{videos_to_generate}...")
        try:
            output_file = assembler.create_tiktok_video(video_path, script, audio_path=audio_path)
            
            # D. Metadata & Database
            caption = generate_metadata(script)
            log_to_db(script_id, script['topic'], output_file)
            
            # E. Email Notification (If credentials exist)
            notifier.send_video_email(output_file, caption)
            
            # Save metadata to text file
            meta_file = output_file.replace(".mp4", "_metadata.txt")
            with open(meta_file, "w", encoding="utf-8") as meta_f:
                meta_f.write(caption)

            print(f"✅ Success! Saved and Logged: {output_file}")
            generated_count += 1
        except Exception as e:
            print(f"❌ Error during assembly: {e}")

    if generated_count == 0:
        print("\n🎉 All 20 scripts have already been generated! Database is fully complete.")
    else:
        print(f"\n✨ Batch processing complete. Generated {generated_count} new unique videos.")

if __name__ == "__main__":
    main()
