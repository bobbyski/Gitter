#!/usr/bin/env python3

import argparse

import rich_log
from model.MainFileManager import MainFileManager
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

def build_parser():
    parser = argparse.ArgumentParser(description='Git Repository Manager')

    subparsers = parser.add_subparsers(title='commands', dest='command', required=True)
    subparsers.add_parser('status', help='Show status of all projects')
    subparsers.add_parser('tui', help='Open TUI viewer')
    subparsers.add_parser('issues', help='Show issues for all projects')
    subparsers.add_parser('version', help='show version information')

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

def issues(project_name=None):
    console = Console()

    for project in MainFileManager.shared.projects:
        if project_name is not None and project.name != project_name:
            continue

        releases_with_issues = [r for r in project.releases if len(r.issues) > 0]
        if not releases_with_issues:
            continue

        table = Table(show_header=True, header_style="bold", box=None, padding=(0, 1))
        table.add_column("Release", style="bold magenta", no_wrap=True)
        table.add_column("Issue", style="cyan", no_wrap=True)
        table.add_column("Title")

        for i, release in enumerate(releases_with_issues):
            release_label = Text(release.name, style="bold magenta" if release.name == "Next release" else "bold yellow")
            for j, issue in enumerate(release.issues):
                table.add_row(
                    release_label if j == 0 else Text(""),
                    issue.number,
                    issue.title,
                )
            if i < len(releases_with_issues) - 1:
                table.add_row("", "", "")

        console.print(Panel(table, title=f"[bold cyan]{project.name}[/bold cyan]", expand=False))


if __name__ == '__main__':
    parser = build_parser()

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
            issues()

