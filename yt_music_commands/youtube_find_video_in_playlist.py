# from pytube import Playlist
from pytubefix import Playlist, YouTube
from argparse import ArgumentParser, Namespace
import sys


def get_arguments() -> None:
  parser: ArgumentParser = ArgumentParser (
    description="Finds a query in each video of a youtube playlist"
  )
  parser.add_argument(
    "query",
    type=str,
    help="substring we want to find inside video titles in a playlist",
  )
  parser.add_argument("playlist_link")
  args: Namespace = parser.parse_args()
  return args


def main() -> None:
  args: Namespace = get_arguments()
  playlist: Playlist = Playlist(args.playlist_link)

  print(f"Searching '{args.query}' in the playlist\n")

  # find videos
  try:
    found_videos: list[YouTube] = []
    for video in playlist.videos:
      if args.query.lower() in video.title.lower():
        found_videos.append(video)
        print(f"{len(found_videos):>4}. Title: {video.title}")
        print(f"      URL:   {video.watch_url}\n")
  except Exception as e:
    print(e)
    sys.exit()

  # Display found videos
  if found_videos:
    print(f"Found {len(found_videos)} videos containing '{args.query}':\n")
  else:
    print(f"No videos found containing '{args.query}'.")