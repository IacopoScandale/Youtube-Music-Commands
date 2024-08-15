help_message = """
Questo comando prende in input il link di una playlist di video
su youtube e ne scarica gli l'audio in mp3 nella cartella corrente.

Inoltre chiederà anche di inserire la data dell'album, e di scegliere
se numerarli nell'ordine della playlist con una scelta [s,n]

Usage: ytmp3pl <youtube_playlist_url>

OSS: A causa della codifica "strana" di download ho dovuto riprocessare
     ogni singolo file scaricato con ffmpeg. Infatti scarico l'audio con
     un nome temporaneo, poi lo codifico con ffmpeg e cancello il file 
     originale.

NOTA: da terminare migliorando la visualizzazione che a causa di ffmpeg
      è un casino. Sarebbe carino fare una sorta di interfaccia grafica
      carina. 
"""

from pytubefix import Playlist
# from pytube import Playlist
import os, sys
from mutagen.mp3 import EasyMP3
from data.utils import help_and_error

help_and_error(help_message, sys.argv, 1)

# p = Playlist(input("link of the playlist: "))
# p = Playlist("https://www.youtube.com/playlist?list=PL7tpv_Zf76aUbf5Qz5TzAHwfO6CZrzZMz")
p = Playlist(sys.argv[1])

for i, video in enumerate(p.videos):
    print(f"  {i+1}) {video.title}")


choice =  input(f"\n Vuoi convertire questi video in mp3?\n  [s,n]: ")

# Aggiungi data se vuoi
date = input("\n Inserisci la data dell'album o lascia vuoto: ")

# Aggiungi numerazione se vuoi
num_choice = input("\n Vuoi numerarli nell'ordine della playlist?\n  [s,n]: ")



if choice == "s":
  for i, video in enumerate(p.videos):
    print(f"  {i+1}) Downloading '{video.title}'")
    to_download = video.streams.filter(only_audio=True, 
                                        file_extension='mp4')    

    # Seleziona il flusso audio con la migliore qualità
    best_audio = to_download.order_by('abr').desc().first()

    video_name = ""
    for ch in video.title:
      if ch in "/\\|":
        video_name += "-"
      else:
        video_name += ch

    # Scarica il flusso audio selezionato
    best_audio.download(
        output_path='.', filename=f"tmp_{video_name}.mp3"
    )

    # Cambia la codifica in mp3
    os.system(
      f'ffmpeg -i "tmp_{video_name}.mp3" -c:a mp3 -hide_banner "{video_name}.mp3"'
    )

    # Cancella il file temporaneo sperando che lo faccia dopo che il
    # comando precedente sia terminato
    os.remove(f"tmp_{video_name}.mp3")


    audio = EasyMP3(f"{video_name}.mp3")

    if date != "" and date.isnumeric():
      audio["date"] = date

    if num_choice == "s":
      audio["tracknumber"] = str(i+1)

    audio.save()