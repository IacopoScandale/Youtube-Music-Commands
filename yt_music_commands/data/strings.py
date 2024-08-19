import os

PACKAGE_NAME: str = "yt_music_commands"

INFO_FOLDER: str = f"{PACKAGE_NAME}.egg-info"

VENV_FOLDER: str = "venv"

VENV_SCRIPTS_WIN: str = os.path.join(VENV_FOLDER, "Scripts")


COMMAND_LINK_FOLDER: str = "Commands"

# DATA_FOLDER: str = "data"


# command names
YT_MP3: str = "ytmp3"
YT_MP3_PLAYLIST: str = "ytmp3_playlist"



COMMANDS: dict[str,str] = {
  YT_MP3: "youtube_mp3_download",
  YT_MP3_PLAYLIST: "youtube_mp3_playlist_download",
}
"""
Maps each command name to the filename to call (without .py ext)
"""