from model.MainFileManager import MainFileManager
from rich.table import Table
from rich.text import Text
from rich.console import Console

def issues(project_name=None, release_name=None, invertReleases=False ):
    console = Console()
    table = Table(title="Issues", show_header=True, header_style="bold")
    table.add_column("Project", style="bold cyan", no_wrap=True)
    table.add_column("Release", no_wrap=True)
    table.add_column("Issue", style="cyan", no_wrap=True)
    table.add_column("Commit Summary" )

    project_name_lower = str(project_name).lower() if project_name is not None else None
    projects = MainFileManager.shared.projects
    for project in projects:
        if project_name is not None and project_name_lower not in project.name.lower():
            continue

        releases_with_issues = [r for r in project.releases if len(r.issues) > 0]
        if not releases_with_issues:
            continue

        if invertReleases:
            next_releases = [r for r in releases_with_issues if r.name == "Next release"]
            other_releases = [r for r in releases_with_issues if r.name != "Next release"]
            releases_with_issues = list(reversed(other_releases)) + next_releases

        SEP = Text("─" * 30, style="dim")

        rows = []
        for i, release in enumerate(releases_with_issues):
            if release_name is not None and release.name.lower().startswith( release_name.lower() ) is False:
                continue

            if i > 0:
                rows.append(("sep", None, None))
            release_label = Text(release.name, style="bold magenta" if release.name == "Next release" else "bold yellow")
            for j, issue in enumerate(release.issues):
                rows.append((release_label if j == 0 else Text(""), issue.number, issue.title))

        project_shown = False
        for k, (release_cell, number, title) in enumerate(rows):
            is_last = k == len(rows) - 1
            if release_cell == "sep":
                if release_name is None:
                    table.add_row(Text(""), SEP, SEP, SEP)
            else:
                table.add_row(
                    Text(project.name, style="bold cyan") if not project_shown else Text(""),
                    release_cell,
                    number,
                    title,
                    end_section=is_last,
                )
                project_shown = True

    console.print(table)
