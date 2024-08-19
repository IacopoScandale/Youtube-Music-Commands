from pytubefix import YouTube
# from pytube import YouTube
from argparse import ArgumentParser, Namespace


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description=(
      "Takes in input a youtube video url and downloads its mp3 audio "
      "in the current folder."
    )
  )
  parser.add_argument("youtube_video_link")

  args: Namespace = parser.parse_args()
  return args


def main() -> None:
  args: Namespace = get_arguments()

  video = YouTube(args.youtube_video_link)

  print(f"  Downloading '{video.title}'")
  to_download = video.streams.filter(only_audio=True,file_extension='mp4')
  # print(to_download)

  # Select best quality audio stream
  best_audio = to_download.order_by('abr').desc().first()
  # TODO add possibility to select audio quality

  # Download selected audio stream
  best_audio.download(
    output_path='.', 
    filename=video.title, 
    mp3=True,
    remove_problematic_character="\\"
  )