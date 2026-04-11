#!/usr/bin/env python3

import argparse
from rich.markdown import Markdown

from model.MainFileManager import MainFileManager
from model.Project import Project
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.text import Text

from BusinessLogic.toml_helper import TomlHelper


def build_parser():
    # styles = list(get_all_styles())
    parser = argparse.ArgumentParser(description='Git Repository Manager')

    subparsers = parser.add_subparsers(title='commands', dest='command', required=True)
    add_parser = subparsers.add_parser('add', help='Add current directory as a project', aliases=['Add', 'ADD'])
    subparsers.add_parser('status', help='Show status of all projects', aliases=['Status', 'STATUS'])
    subparsers.add_parser('tui', help='Open TUI viewer', aliases=['TUI', 'tui'])
    subparsers.add_parser('issues', help='Show issues for projects', aliases=['Issues', 'ISSUES'])
    subparsers.add_parser('version', help='show version information', aliases=['Version', 'VERSION'] )
    subparsers.add_parser('notes', help='Show release notes markdown without formatting', aliases=['Notes', 'NOTES'] )
    subparsers.add_parser('raw', help='Show release notes markdown without formatting', aliases=['Raw', 'RAW'] )
    help_parser = subparsers.add_parser('help', help='Show help for a topic', aliases=['Help', 'HELP'])
    help_parser.add_argument('topic', type=str, help='Topic to show help for (e.g. add, status, tui)')

    parser.add_argument( '-p', '--project', type=str, help='Project name to show')
    parser.add_argument( '-r', '--release', type=str, help='The release number to show')
    parser.add_argument( '-m', '--markdown', action='store_true', help='Show release notes in markdown format')
    # parser.add_argument( '-t', '--theme', type=str, help='The theme to use', choices=styles, default='monokai')
    parser.add_argument( '-t', '--theme', type=str, help='The theme to use', default='monokai')

    return parser

def show_help(topic: str):
    from BusinessLogic.docs_helper import get_document
    content = get_document(f"{topic.lower()}.md")
    if content is None:
        Console().print(f"[red]No help available for '{topic}'.[/red]")
        return
    Console().print(Markdown(content))

def show_version(version):
    """Display the version information and exit."""
    version = TomlHelper().get_version()
    print(f"Version {version}")
    exit(0)

def add_project(name=None):
    cwd = str(Path.cwd())
    for project in MainFileManager.shared.projects:
        if Path(project.directory).resolve() == Path(cwd).resolve():
            Console().print(f"[red]Already added:[/red] {project.name} ({project.directory})")
            return

    project_name = name if name else Path(cwd).name
    new_project = Project(
        name=project_name,
        directory=cwd,
        status="",
        tagBranch="main",
        issuePrefixes=[],
        prPatterns=[],
        favorite=False,
        groups=[],
        commits=[],
        issues=[],
        releases=[],
    )
    MainFileManager.shared.add_project(new_project)
    MainFileManager.save_shared_to_json(str(Path.home() / ".gitter"))
    Console().print(f"[green]Added:[/green] {project_name} ({cwd})")


def status():
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

    Console().print(table)

def issues(project_name=None, release_name=None):
    console = Console()
    table = Table(title="Issues", show_header=True, header_style="bold")
    table.add_column("Project", style="bold cyan", no_wrap=True)
    table.add_column("Release", no_wrap=True)
    table.add_column("Issue", style="cyan", no_wrap=True)
    table.add_column("Commit Summary" )

    first_project = True
    for project in MainFileManager.shared.projects:
        if project_name is not None and project.name.lower() != project_name.lower():
            continue

        releases_with_issues = [r for r in project.releases if len(r.issues) > 0]
        if not releases_with_issues:
            continue

        first_project = False

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


def notes(project_name=None, release_name=None, markdown=False, raw=False, code_theme='monokai' ):
    console = Console()

    for project in MainFileManager.shared.projects:
        if project_name is not None and project.name.lower() != project_name.lower():
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

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command.lower() == 'tui':
        from TUI.MenuApp import MenuApp
        app = MenuApp()
        app.run()
    elif args.command.lower() == 'version':
        show_version('0.1.0')
    elif args.command.lower() == 'add':
        pathname = str(Path.home() / ".gitter")
        MainFileManager.load_shared_from_json(pathname)
        add_project(args.project)
    elif args.command.lower() == 'help':
        show_help(args.topic)
    else:
        pathname = str(Path.home() / ".gitter")
        MainFileManager.load_shared_from_json(pathname)

        for project in MainFileManager.shared.projects:
            project.update()

        if args.command.lower() == 'status':
            status()
        elif args.command.lower() == 'issues':
            issues( args.project, args.release )
        elif args.command.lower() == 'notes':
            notes( args.project, args.release, markdown=args.markdown, raw=False, code_theme=args.theme )
        elif args.command.lower() == 'raw':
            notes( args.project, args.release, markdown=False, raw=True )

if __name__ == '__main__':
    main()

