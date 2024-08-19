# Youtube Music Commands
Simple terminal line commands




# Download
Recommended install is by executing install files respectively .bat for windows and ??? for linux. 

This will install this package and dependencies in a virtual environment. Then all commands will be put in Commands folder that will automaticly added to path variable. In this way commands will always loaded on terminal. All this is done in the scrypt `post_install.py`. 

If you only want to install the package, just use this command inside the package folder: 
``` 
pip install -e .
```

## Windows
Just double click on `setup.bat` file. If you want to uninstall just double click on `uninstall.bat` file. Easy peasy.

## Linux
work in progress


# Commands:
|command|description|
|-|-|
|`ytmp3`|downloads the mp3 audio from a youtube video link|
|`ytmp3_playlist`|downloads all the mp3 audio from a youtube playlist. Then (optional) it asks to insert some fields like album, artist, cover etc.|