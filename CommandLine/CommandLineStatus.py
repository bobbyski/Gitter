
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from model.MainFileManager import MainFileManager

_STATE_STYLES = {
    "new file":  "green",
    "modified":  "yellow",
    "deleted":   "red",
    "renamed":   "cyan",
    "untracked": "dim",
}

def _state_text(state: str) -> Text:
    style = _STATE_STYLES.get(state, "")
    return Text(state, style=style)

def _files_table(title: str, rows) -> Table:
    table = Table(title=title, show_header=True, header_style="bold", box=None)
    table.add_column("State", no_wrap=True)
    table.add_column("File")
    for state, filename in rows:
        table.add_row(_state_text(state), Text(filename))
    return table

def status( project_name: str = None ):
    console = Console()

    if project_name is None:
        table = Table(title="Projects")
        table.add_column("Name", style="bold cyan", no_wrap=True)
        table.add_column("Directory", style="dim")
        table.add_column("Status")
        table.add_column("Release")
        table.add_column("Issues in Current/Next Release")

        for project in MainFileManager.shared.projects:
            table.add_row(
                project.name,
                project.directory,
                project.status.to_rich(),
                project.current_release(),
                project.issues_string_for_release(),
            )

        console.print(table)
    else:
        for project in MainFileManager.shared.projects:
            if project_name is not None and project.name.lower() != project_name.lower():
                continue

            console.print(f"[bold cyan]{project.name}[/bold cyan]")
            console.print(project.status.to_long_rich())

            if project.status.stagedFiles:
                table = Table(title="Staged", show_header=True, header_style="bold")
                table.add_column("State", no_wrap=True, min_width=15)
                table.add_column("File", min_width=60)
                for f in project.status.stagedFiles:
                    table.add_row(_state_text(f.state), Text(f.filename))
                console.print(table)

            if project.status.unstagedFiles or project.status.filesUntracked or project.status.untrackedFiles:
                table = Table(title="Unstaged", show_header=True, header_style="bold")
                table.add_column("State", no_wrap=True, min_width=15)
                table.add_column("File", no_wrap=True, min_width=60)
                for f in project.status.unstagedFiles:
                    table.add_row(_state_text(f.state), Text(f.filename))

                for f in project.status.filesUntracked:
                    table.add_row(_state_text( "untracked"), Text(f))
                console.print(table)

            # staged = [(f.state, f.filename) for f in project.status.stagedFiles]
            # unstaged = [(f.state, f.filename) for f in project.status.unstagedFiles]
            # untracked = [("untracked", f) for f in project.status.filesUntracked]
            #
            # if staged:
            #     console.print(_files_table("Staged", staged))
            # if unstaged or untracked:
            #     console.print(_files_table("Unstaged", unstaged + untracked))
            # if not staged and not unstaged and not untracked:
            #     console.print(Text("  Nothing to commit", style="dim"))
            console.print()