import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class ScriptGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_scripts(self, count=5):
        print(f"🧠 Brainstorming {count} new viral TikTok scripts for Growzix...")
        
        prompt = f"""
        You are an expert TikTok Content Strategist for the USA Construction Estimation market.
        Generate {count} high-engagement, short-form video scripts.
        
        Target Audience: General Contractors, Subcontractors, and Estimators in the USA.
        Goal: Position 'Growzix' as the solution for accurate material takeoffs and estimation.
        
        Each script MUST follow this exact JSON format:
        {{
            "id": "unique_id_here",
            "topic": "Short Topic Name",
            "visual_query": "Specific Pexels search term for a unique background clip",
            "hook": "Strong 3-second hook to stop the scroll",
            "body": "Concise, value-driven explanation (max 3 sentences)",
            "cta": "Clear Call to Action (e.g., 'Link in bio for a free quote')"
        }}
        
        Topics should cover:
        - Common estimation mistakes.
        - How to increase profit margins.
        - The pain of manual takeoffs.
        - The benefit of professional estimation.
        - Market trends in US construction.
        
        Return ONLY a JSON list of scripts. No markdown, no preamble.
        """
        
        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            
            # Remove potential markdown code blocks if AI includes them
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            scripts = json.loads(content)
            return scripts
        except Exception as e:
            print(f"❌ Error generating scripts: {e}")
            return []

    def update_script_file(self, script_file="data/initial_scripts.json"):
        # 1. Load existing scripts
        if os.path.exists(script_file):
            with open(script_file, "r") as f:
                try:
                    current_scripts = json.load(f)
                except json.JSONDecodeError:
                    current_scripts = []
        else:
            current_scripts = []

        # 2. Generate new scripts
        new_scripts = self.generate_scripts(count=5)
        
        if not new_scripts:
            print("⚠️ No new scripts generated.")
            return False

        # 3. Assign unique IDs to avoid duplicates
        existing_ids = {s["id"] for s in current_scripts}
        final_scripts = current_scripts.copy()
        
        for i, s in enumerate(new_scripts):
            # Create a unique ID based on current count and index
            s["id"] = str(len(current_scripts) + i + 1)
            final_scripts.append(s)

        # 4. Save back to file
        with open(script_file, "w") as f:
            json.dump(final_scripts, f, indent=4)
        
        print(f"✅ Successfully added {len(new_scripts)} new scripts to {script_file}!")
        return True

if __name__ == "__main__":
    gen = ScriptGenerator()
    gen.update_script_file()
