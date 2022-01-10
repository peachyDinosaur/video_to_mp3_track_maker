import os
from moviepy.editor import *
video = AudioFileClip(os.path.join("./art_rally.mp4"))
video.write_audiofile(os.path.join("./rally_audio.mp3"))