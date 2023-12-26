
# Import everything needed to edit video clips 
from moviepy.editor import *
import requests

# loading video file
response  = requests.get('https://v.redd.it/makrvr18628c1/DASH_720.mp4?source=fallback')
with open('video.mp4', 'wb') as f:
    f.write(response.content)
clip = VideoFileClip('video.mp4')
  
# loading audio file 
response = requests.get('https://v.redd.it/makrvr18628c1/DASH_AUDIO_64.mp4')
with open('audio.mp4', 'wb') as f:
    f.write(response.content)
audioclip = AudioFileClip('audio.mp4')
  
# adding audio to the video clip 
videoclip = clip.set_audio(audioclip) 
  
videoclip.preview()