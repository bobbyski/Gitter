from inquirer_textual import prompts

from BusinessLogic.toml_helper import TomlHelper
from TUI.MenuApp import MenuApp

def interactive():
    commands = ["add", "status", "issues", "notes", "raw", "version", "help", "tui", "exit"]
    choice = prompts.select("What would you like to do?", choices=commands)

    if choice.value == "exit":
        return
    elif choice.value.lower() == "tui":
        app = MenuApp()
        app.run()
    elif choice.value.lower() == "help":
        commands = ["add", "status", "issues", "notes", "raw", "version", "help", "tui", "exit"]
        cmd = prompts.select("What would you like to do?", choices=commands)
        help(cmd)
    elif choice.value.lower() == "version":
        print(f"Version: {TomlHelper().get_version()}")
    elif choice.value.lower() == "issues":
        from main import issues
        issues()
    else:
        print(f"Command yet available in easy mode: {choice} will be added later")
