import os
import sys


def regedit_windows_setup(bat_file_full_path: str) -> None:
  # Regedit Part
  print("Adding commands to regedit AutoRun...")

  # path is inside \"...\" because in this way paths containing spaces
  # are supported
  commands_bat_full_path_str = f'\\"{bat_file_full_path}\\"'

  # add automatically commands.bat file to regedit AutoRun Value in 
  # Command Processor: Use a temporary file to get all the previous
  # values already in Autorun 
  tmp_file_path = "tmp.txt"
  try:
    os.system(f'reg query "HKLM\\SOFTWARE\\Microsoft\\Command Processor" /v AutoRun > "{tmp_file_path}"')
  except:
    print("Error: you must run this script as administrator")
    sys.exit()

  # read tmpfile and get all paths in AutoRun
  with open(tmp_file_path, "r") as txtfile:
    lines = txtfile.readlines()
  os.remove(tmp_file_path)

  # find existing paths
  paths = []
  for line in lines:
    if "AutoRun" in line:
      # get the list of all paths in value "AutoRun"
      paths = line[21:].strip().split("&")
      # base case if no paths in regedit AutoRun: otherwise then 
      # " & ".join(paths) joins element "" and break windows terminal
      if paths == [""]:
        paths = []
      
  # if a path starts and ends with ", we must add \ in front of "
  for i, path in enumerate(paths):
    # strip every path: it could contain spaces because we are splitting
    # with "&" but each path could be separated e.g with "  & "
    path = path.strip()
    if path.startswith('"') and path.endswith('"'):
      # add \ in front of each "
      path = f'\\"{path[1:-1]}\\"'
    # refresh path in paths list
    paths[i] = path

  # add commands.bat file full path to the values
  if commands_bat_full_path_str not in paths:
    paths.append(commands_bat_full_path_str)

  # join all paths separated by &
  concatenated_paths = " & ".join(paths)
  # print(concatenated_paths)
  os.system(f'reg add "HKLM\\SOFTWARE\\Microsoft\\Command Processor" /v AutoRun /t REG_SZ /d "{concatenated_paths}" /f')

  print("Done!\n")