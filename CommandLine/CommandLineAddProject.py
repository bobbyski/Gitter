from pathlib import Path
from model.MainFileManager import MainFileManager
from model.Project import Project
from rich.console import Console

def add_project(name=None,
        directory=str(Path.cwd()),
        status="",
        tagBranch="main",
        issuePrefixes=[],
        prPatterns=[],
        favorite=False,
        groups=[],
        commits=[],
        issues=[],
        releases=[] ):
    cwd = str(Path.cwd())
    for project in MainFileManager.shared.projects:
        if Path(project.directory).resolve() == Path(cwd).resolve():
            Console().print(f"[red]Already added:[/red] {project.name} ({project.directory})")
            return

    project_name = name if name else Path(cwd).name
    new_project = Project(
        name=project_name,
        directory=directory,
        status=status,
        tagBranch=tagBranch,
        issuePrefixes=issuePrefixes,
        prPatterns=prPatterns,
        favorite=favorite,
        groups=groups,
        commits=commits,
        issues=issues,
        releases=releases,
    )
    MainFileManager.shared.add_project(new_project)
    MainFileManager.save_shared_to_json(str(Path.home() / ".gitter"))
    Console().print(f"[green]Added:[/green] {project_name} ({cwd})")