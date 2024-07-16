help_message = """
Questo comando prende in input il link di un video su youtube e
ne scarica l'audio in mp3 nella cartella corrente. 

Usage: mp3_download <url_video_youtube>
"""

from pytube import YouTube
from sys import argv
from os import system, remove
from Data.constants import help_and_error

help_and_error(help_message, argv, 1)

yt_video_link = argv[1]
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
system(f'ffmpeg -i "tmp_{video_name}.mp3" -c:a mp3 -hide_banner "{video_name}.mp3"')

# Cancella il file temporaneo sperando che lo faccia dopo che il comando precedente sia terminato
remove(f"tmp_{video_name}.mp3")