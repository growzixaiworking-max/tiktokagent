import os
import platform
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, ColorClip
import json

def _find_font():
    system = platform.system()
    if system == "Windows":
        candidates = [
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\calibri.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
        ]
    elif system == "Darwin":
        candidates = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Arial.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
        ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

class VideoAssembler:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.font_path = _find_font()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def create_tiktok_video(self, video_path, script_data, audio_path=None):
        clip = VideoFileClip(video_path).resized(height=1920).without_audio()
        w, h = clip.size
        target_w = h * 9 / 16
        clip = clip.cropped(x_center=w/2, width=target_w)

        common_args = {
            "font": self.font_path,
            "method": "caption",
            "size": (int(target_w*0.8), None),
        }

        hook_txt = TextClip(
            text=script_data['hook'],
            font_size=70,
            color='yellow',
            **common_args
        ).with_duration(3).with_position('center')

        body_txt = TextClip(
            text=script_data['body'],
            font_size=50,
            color='white',
            **common_args
        ).with_start(3).with_duration(clip.duration - 6).with_position('center')

        cta_txt = TextClip(
            text=script_data['cta'],
            font_size=60,
            color='green',
            **common_args
        ).with_start(clip.duration - 3).with_duration(3).with_position(('center', int(h*0.8)))

        # Combine
        final = CompositeVideoClip([clip, hook_txt, body_txt, cta_txt])

        if audio_path and os.path.exists(audio_path):
            voice_audio = AudioFileClip(audio_path)
            final = final.with_audio(voice_audio)
            final = final.with_duration(voice_audio.duration)
        
        import time
        output_filename = f"Growzix_Video_{script_data['id']}.mp4"
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Universal Mode: Best for all Mobiles, PCs, and Social Media
        try:
            final.write_videofile(
                output_path, 
                fps=24, 
                codec="libx264", 
                audio_codec="libmp3lame", 
                audio_bitrate="192k",
                ffmpeg_params=[
                    "-pix_fmt", "yuv420p",
                    "-profile:v", "main",
                    "-level", "3.0",
                    "-movflags", "+faststart"
                ],
                threads=4,
                logger=None
            )
            time.sleep(2) 
        finally:
            final.close()
            clip.close()
            if audio_path: voice_audio.close()
            
        return output_path

if __name__ == "__main__":
    print("VideoAssembler ready.")
