from inquirer_textual import prompts
from BusinessLogic.toml_helper import TomlHelper
from CommandLine.CommandLineIssue import issues
from CommandLine.CommandLineNotes import notes
from TUI.MenuApp import MenuApp
from model.MainFileManager import MainFileManager

def get_project():
    projects = ["All projects"] + sorted([p.name for p in MainFileManager.shared.projects], key=str.casefold)
    project = prompts.select("Select project", choices=projects)

    if project == "":
        project = None
    else:
        project = str(project)

    return project

def get_versions( project: str | None = None ):
    version = prompts.text("Enter version number (or partial version): ")

    if version == "":
        version = None
    else:
        version = str(version)

    return version

def get_markdown():
    markdown = prompts.confirm("Markdown?")
    return markdown


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
        project = get_project()
        version = get_versions(project)
        issues(project, version)
    elif choice.value.lower() == "notes":
        project = get_project()
        version = get_versions(project)
        markdown = get_markdown()
        notes(project, version, markdown=markdown , raw=False)
    elif choice.value.lower() == "raw":
        project = get_project()
        version = get_versions(project)
        notes(project, version, markdown=False, raw=True)
    elif choice.value.lower() == "exit":
        return
    else:
        print(f"Command yet available in easy mode: {choice} will be added later")
