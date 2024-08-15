import sys


def help_and_error(
  help_message: str, 
  sys_argv: list, 
  argument_number: int = None, 
  min_arg_number: int = 0, 
  max_arg_number: int | None = None, 
  command_name: str = "command_name"
) -> None:
  """
  Input
  -----
    * `help_message`: multiline str containing -h or --help message when
       you type: "command_name -h" or "command_name -h"
    * `argv`: sys.argv list containing command arguments
    * `argument_number`: exact number of arguments (if None it does not
       matter)
    * `min_arg_number`: minimum number of arguments
    * `max_arg_number`: maximum number of arguments
    * `command_name` : command alias name
  
  Output 
  ------
    * Prints help message and stops command execution when you type
      "command_name --help" or "command_name -h" 
    * Prints error message and stops command execution when
      `argument_number` is wrong
  """
  # help message
  if len(sys_argv) > 1 and (sys_argv[1] == "--help" or sys_argv[1] == "-h"):
    print(help_message)
    sys.exit()

  # wrong arg number
  if argument_number is not None:
    if len(sys_argv) != argument_number + 1:
      print(
        "ERROR: Wrong Argument Number. Passed ",
        f"({len(sys_argv)-1} args instead of {argument_number})",
        f"\ntype '{command_name} --help' for more info"
      )
      sys.exit()

  # case passed arguments < min arg number
  if len(sys_argv) - 1 < min_arg_number:
    print(
      "ERROR: Not Enough Arguments", 
      f"(minimum argument number = {min_arg_number})",
      f"\ntype '{command_name} --help' for more info"
    )
    sys.exit()

  # case passed args > max arg number
  if max_arg_number is not None:
    if len(sys_argv) - 1 > max_arg_number:
      print(
        "ERROR: Too Many Arguments ",
        f"(maximum argument number = {max_arg_number})",
        f"\ntype '{command_name} --help' for more info"
      )
      sys.exit()