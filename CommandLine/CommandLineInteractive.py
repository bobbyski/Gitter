from inquirer_textual import prompts
from TUI.MenuApp import MenuApp

def interactive():
    commands = ["add", "status", "issues", "notes", "raw", "version", "help", "tui", "exit"]
    choice = prompts.select("What would you like to do?", choices=commands)

    if choice == "exit":
        return
    elif choice.lower() == "tui":
        app = MenuApp()
        app.run()
    elif choice.lower() == "help":
        commands = ["add", "status", "issues", "notes", "raw", "version", "help", "tui", "exit"]
        cmd = prompts.select("What would you like to do?", choices=commands)
        help(cmd)
    elif choice.lower() == "version":
        from main import __version__
        print(f"Version: {__version__}")
    elif choice.lower() == "issues":
        from main import issues
        issues()
    else:
        print(f"Command yet available in easy mode: {choice} will be added later")
