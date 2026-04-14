
from rich.console import Console
from rich.markdown import Markdown

from model.MainFileManager import MainFileManager

def notes(project_name=None, release_name=None, markdown=False, raw=False, code_theme='monokai' ):
    console = Console()

    for project in MainFileManager.shared.projects:
        if project_name is not None and project_name.lower() not in project.name.lower():
            continue

        releases_with_issues = [r for r in project.releases if len(r.issues) > 0]
        if not releases_with_issues:
            continue

        if raw:
            text = project.release_notes_markdown( release_name=release_name )
            print(text)
        elif markdown:
            markdown = Markdown(project.release_notes_markdown( release_name=release_name ), code_theme=code_theme)
            console.print(markdown)
        else:
            console.print(project.release_notes( release_name=release_name ))