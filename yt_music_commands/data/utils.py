from pytubefix import YouTube
import subprocess
import os


def get_video_output_name(video: YouTube, mp3_ext: bool = False) -> str:
  """
  Removes title problematic characters and returns output filename
  WITOUT .mp3 extension
  """
  video_title: str = video.title.replace("\\"," ").replace("/"," ")
  if mp3_ext is True:
    return f"{video_title}.mp3"
  return video_title


def download_as_mp3(video: YouTube) -> None:
  """
  Download video as mp3 and reformat using ffmpeg
  """
  to_download = video.streams.filter(only_audio=True,file_extension='mp4')
  # print(to_download)

  # Select best quality audio stream
  best_audio = to_download.order_by('abr').desc().first()
  # TODO add possibility to select audio quality

  # manually set video title for reuse file with EasyMP3
  video_title: str = get_video_output_name(video)

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