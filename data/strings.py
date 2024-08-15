import os

DATA_FOLDER: str = "data"

PIP_VENV_WIN: str = "venv\\Scripts\\pip3.exe"
# PIP_VENV_LINUX: str = "venv/bin/"

PYTHON_VENV_WIN: str = "venv\\Scripts\\python.exe"
# PYTHON_VENV_LINUX: str = "venv/bin/python3"

COMMANDS_BAT: str = os.path.join(DATA_FOLDER, "commands.bat")
COMMANDS_SH: str = os.path.join(DATA_FOLDER, "commands.sh")