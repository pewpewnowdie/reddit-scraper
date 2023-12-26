
# Import everything needed to edit video clips 
from moviepy.editor import *
import requests
import tempfile

def download_video(url):
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    else:
        return None

# loading video file
video_url = 'https://v.redd.it/makrvr18628c1/DASH_720.mp4?source=fallback'
video_name = download_video(video_url)
video_clip = VideoFileClip(video_name)
  
# loading audio file 
audio_url = 'https://v.redd.it/makrvr18628c1/DASH_AUDIO_64.mp4'
audio_name = download_video(audio_url)
audio_clip = AudioFileClip(audio_name)
  
# adding audio to the video clip 
clip = video_clip.set_audio(audio_clip) 

clip.write_videofile('final.mp4', audio = True)
clip.preview()
    