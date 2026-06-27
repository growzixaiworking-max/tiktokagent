import os
import requests
from dotenv import load_dotenv

load_dotenv()

class VideoDownloader:
    def __init__(self):
        self.api_key = os.getenv("PEXELS_API_KEY")
        self.base_url = "https://api.pexels.com/videos/search"
        self.headers = {"Authorization": self.api_key}

    def search_and_download(self, query, count=1):
        if not self.api_key:
            print("Error: PEXELS_API_KEY not found in .env")
            return []

        params = {
            "query": query,
            "per_page": count,
            "orientation": "portrait"
        }
        
        response = requests.get(self.base_url, headers=self.headers, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch videos: {response.status_code}")
            return []

        data = response.json()
        downloaded_paths = []

        for i, video in enumerate(data.get("videos", [])):
            # Prioritize HD quality above 1080p if available
            video_files = video.get("video_files", [])
            video_url = None
            
            # Sort by width descending to get best quality
            sorted_files = sorted(video_files, key=lambda x: x.get('width', 0), reverse=True)
            if sorted_files:
                video_url = sorted_files[0].get("link")
            
            if not video_url:
                continue

            filename = f"assets/clips/{query.replace(' ', '_')}_{i}.mp4"
            print(f"📥 Downloading High-Quality {query} clip...")
            
            v_res = requests.get(video_url)
            with open(filename, "wb") as f:
                f.write(v_res.content)
            
            downloaded_paths.append(filename)
        
        return downloaded_paths

if __name__ == "__main__":
    # Test downloader
    downloader = VideoDownloader()
    # downloader.search_and_download("construction site", 1)
