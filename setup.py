from data import strings
from data.utils import regedit_windows_setup
import os
import sys
import json

# title
print("================================")
print("||   YOUTUBE MUSIC COMMANDS   ||")
print("================================",end="\n\n")

# project folder full path
here: str = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)

# create virtual environment
if not os.path.exists("venv"):
  print("Creating Virtual Environment 'venv'")
  os.system(f"{sys.executable} -m venv venv")  
  print("Done!\n")

# install from requirements.txt
print("Installing dependencies:")
if os.name == "nt":  # windows
  os.system(f"{strings.PIP_VENV_WIN} install -r requirements.txt")
  print("Done!\n")
elif os.name == "posix":  # linux TODO
  os.system("")
  print("Done!\n")
else: # other os
  raise OSError(f"Your os {os.name} not supported")


# WINDOWS SETUP: create 'commands.bat' file, write all commands, add to
# regedit autorun (requires administrator)
if os.name == "nt": 
  print("Windows setup: setting up all commands...")
  python_venv_full_path = os.path.join(os.getcwd(), strings.PYTHON_VENV_WIN)


  def windows_alias_command_line(
    command_name: str,
    filename_py: str,
    args: str = ""
  ) -> str:
    """
    Create windows command line for file comands.bat
    Input:
    - `filename_py:str` name of the python file to call
    - `command_name:str` name of the alias
    - `args:str=""` insert other default arguments (separated by a 
       space) if needed
    """
    command_file_path = os.path.join(os.getcwd(), filename_py)
    return f'doskey {command_name} = "{python_venv_full_path}" "{command_file_path}" {args} $*\n'


  # windows echo off
  commands = "@echo off\n\n"
  # add commands here!
  # # pdf_commands command
  # commands += windows_alias_command_line(strings.PDF_COMMANDS, "comm_pdf_commands.py")
  # # fname_format command
  # commands += windows_alias_command_line(strings.FNAME_FORMAT_COMM, "comm_filename_format.py")
  # # merge_pdf command
  # commands += windows_alias_command_line(strings.MERGE_PDF_COMM, "comm_pdf_merge.py")
  # # slice_pdf command
  # commands += windows_alias_command_line(strings.SLICE_PDF_COMM, "comm_pdf_slicer.py")


  # Write commands on 'commands.bat' file
  with open(strings.COMMANDS_BAT, "w") as txtfile:
    txtfile.write(commands)
  
  print("Done!\n")

  # Regedit Part
  bat_file_full_path: str = os.path.join(os.getcwd(), strings.COMMANDS_BAT)
  regedit_windows_setup(bat_file_full_path)


# LINUX SETUP
elif os.name == "posix":
  # TODO
  pass

  # TODO add automatically file to current shell.rc

else:
  raise OSError(f"Your os {os.name} is not supported")




print(f"PDF Commands Installed. Type '{strings.PDF_COMMANDS}' for more info")