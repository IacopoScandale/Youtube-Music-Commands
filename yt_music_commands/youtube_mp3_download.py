from .data.utils import download_as_mp3
from pytubefix import YouTube
# from pytube import YouTube
from argparse import ArgumentParser, Namespace


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description=(
      "Takes in input a youtube video url and downloads its mp3 audio "
      "in the current folder. NB: due to a strange error caused by "
      "mutagen I prefer to reprocess mp3 files with ffmpeg. This "
      "permits to use mp3 file in other programs e.g. audacity, that "
      "otherwise will not recognize this mp3 file"
    )
  )
  parser.add_argument("youtube_video_link")
  parser.add_argument(
    "-ss", 
    "--start",
    metavar="time",
    type=str, 
    help="where the video starts e.g. '07:12'",
    default=None,
  )
  parser.add_argument(
    "-to", 
    "--end",
    metavar="time",
    type=str, 
    help="where the video ends e.g. '12:31'",
    default=None,
  )

  args: Namespace = parser.parse_args()
  return args


def main() -> None:
  args: Namespace = get_arguments()
  video: YouTube = YouTube(args.youtube_video_link)

  print(f"  Downloading '{video.title}'")

  download_as_mp3(video, start=args.start, end=args.end)