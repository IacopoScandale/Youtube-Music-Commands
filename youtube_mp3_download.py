from dataaa.constants import help_and_error
from pytubefix import YouTube
# from pytube import YouTube
import os
import sys


help_message = """
Takes in input a youtube video url and downloads its mp3 audio in the
current folder.

Usage: ytmp3 <youtube_video_url>
"""

help_and_error(help_message, sys.argv, 1)

yt_video_link = sys.argv[1]
video = YouTube(yt_video_link)

print(f"  Downloading '{video.title}'")
to_download = video.streams.filter(only_audio=True,file_extension='mp4')
# print(to_download)    

# Seleziona il flusso audio con la migliore qualità
best_audio = to_download.order_by('abr').desc().first()
video_name = ""

# Controlla se il nome contiene caratteri particolari
for ch in video.title:
  if ch in "/\\":
    video_name += "-"
  else:
    video_name += ch

# Scarica il flusso audio selezionato
best_audio.download(output_path='.', filename=f"tmp_{video_name}.mp3")

# Cambia la codifica in mp3
os.system(
  f'ffmpeg -i "tmp_{video_name}.mp3" -c:a mp3 -hide_banner "{video_name}.mp3"'
)

# Cancella il file temporaneo sperando che lo faccia dopo che il comando
# precedente sia terminato
os.remove(f"tmp_{video_name}.mp3")