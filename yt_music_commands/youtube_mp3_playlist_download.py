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
from mutagen import File
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TRCK  
from argparse import ArgumentParser, Namespace
import subprocess
import os


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description=(
      "Downloads all videos in a youtube playlist converting them to "
      "mp3 audio. Optional: it also asks to insert album name, artist, "
      "date, and asks if you want to enumerate them in the shown "
      "order. NB: due to a strange error caused by mutagen I prefer "
      "to reprocess mp3 files with ffmpeg. This only for adding "
      "album metadata as cover, artist etc..."
    )
  )
  parser.add_argument("youtube_playlist_link")
  args: Namespace = parser.parse_args()
  return args


def get_optional_choices() -> tuple[str]:
  # optional: add album name, artist and year to every file
  album: str = input("\n 1/5: Insert album name or leave it blank:\n      ")
  artist: str = input("\n 2/5: Insert artist or leave it blank:\n      ")
  year: str = input("\n 3/5: Insert album date or leave it blank:\n      ")
  # optional: enumerate music files
  enumerate_choice: str = input(
    (
      "\n 4/5: Do you want to enumerate them in the shown order?"
      "\n      [Y,n]: "
    )
  )
  # optional: cover
  cover_choice: str = input(
    (
      "\n 5/5: Use the only image in the folder as album cover for each file?"
      "\n      (if not present drag it in the folder now)"
      "\n      [Y,n]: "
    )
  )
  print()
  return (album, artist, year, enumerate_choice, cover_choice)


def find_cover() -> str:
  """
  Finds in the current folder a file ending in:
  - ".jpg"
  - ".jpeg"
  - ".png"

  and returns its filename. If not found returns empty string "". 
  
  TLDR: Returns the first image name found in a folder. So if we are
  used to put in an album folder the cover file, then it will be used
  as cover.
  """
  cover_extensions: list[str] = (".jpg",".jpeg",".png")
  
  for filename in os.listdir():
    if filename.endswith(cover_extensions):
      return filename
    
  return ""


def get_mime_type(cover: str) -> str:
  """
  Returns image mime type e.g. "cover.jpg" has mime type "image/jpg"
  """
  _, extension = os.path.splitext(cover)
  
  return f"image/{extension[1:]}"


def main():
  args: Namespace = get_arguments()

  playlist: Playlist = Playlist(args.youtube_playlist_link)

  # show playlist content
  for i, video in enumerate(playlist.videos, 1):
    print(f"{i:>4}.  {video.title}")

  # optional choiches: add album name, artist and year to every file and
  # choose whether to enumerate files or apply cover in the folder
  album, artist, year, enumerate_choice, cover_choice = get_optional_choices()
  
  # find cover and mime type for later
  cover: str = find_cover()
  mime_type: str = get_mime_type(cover)

  # start to download
  for i, video in enumerate(playlist.videos, 1):
    print(f"{i:>4}) Downloading '{video.title}'")
    to_download = video.streams.filter(only_audio=True, file_extension='mp4')    

    # Select best quality audio stream
    best_audio = to_download.order_by('abr').desc().first()
    # TODO add possibility to select audio quality

    # manually set video title for reuse file with EasyMP3
    video_title: str = video.title.replace("\\"," ").replace("/"," ")

    # Download selected audio stream
    best_audio.download(
      output_path='.', 
      filename=f"tmp_{video_title}",
      mp3=True
    )
    
    tmp_filename: str = f"tmp_{video_title}.mp3"
    filename: str = f"{video_title}.mp3"

    subprocess.run(
      ["ffmpeg", "-i", tmp_filename, filename],
      stdout=subprocess.DEVNULL,  # suppress standard output
      stderr=subprocess.DEVNULL,  # out error and progress information
      stdin=subprocess.DEVNULL,  # suppress any standard input requests
    )

    os.remove(tmp_filename)

    audio = ID3(filename)
    audio["TIT2"] = TIT2(encoding=3, text=video.title)

    # optional choiches:
    if album != "":
      audio["TALB"] = TALB(encoding=3, text=album)
    if artist != "":
      audio["TPE1"] = TPE1(encoding=3, text=artist)
    if year != "" and year.isnumeric():
      audio["TDRC"] = TDRC(encoding=3, text=year)
    if enumerate_choice in "yYsS":
      audio["TRCK"] = TRCK(encoding=3, text=str(i))
      # audio.add(TRCK(encoding=3, text=str(i)))
      # pass

    if cover_choice in "yYsS" and cover != "":
      with open(cover, "rb") as image:
        albumart: bytes = image.read()
      
      # set album cover
      audio["APIC"] = APIC(
        encoding=3,
        mime=mime_type,
        type=3, # type "front cover" 
        desc="Front Cover",
        data=albumart
      )
      audio.save()