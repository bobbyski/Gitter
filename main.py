#!/usr/bin/env python3

import argparse

import rich_log
from model.MainFileManager import MainFileManager
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.text import Text

def build_parser():
    parser = argparse.ArgumentParser(description='Git Repository Manager')

    subparsers = parser.add_subparsers(title='commands', dest='command', required=True)
    subparsers.add_parser('status', help='Show status of all projects')
    subparsers.add_parser('tui', help='Open TUI viewer')
    subparsers.add_parser('issues', help='Show issues for all projects')
    subparsers.add_parser('version', help='show version information')

    parser.add_argument( '-p', '--project', type=str, help='Project name to show')
    parser.add_argument( '-r', '--release', type=str, help='The release number to show')

    return parser

def show_version(version):
    """Display the version information and exit."""
    print(f"Version {version}")
    exit(0)

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
            if release_name is not None and release.name.lower() != release_name.lower():
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

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()

    if parser.parse_args().command == 'tui':
        from MenuApp import MenuApp
        app = MenuApp()
        app.run()
    elif parser.parse_args().command == 'version':
        show_version('0.0.8')
    else:
        pathname = str(Path.home() / ".gitter")
        MainFileManager.load_shared_from_json(pathname)

        for project in MainFileManager.shared.projects:
            project.update()

        if parser.parse_args().command == 'status':
            status()
        elif parser.parse_args().command == 'issues':
            issues( args.project, args.release )

