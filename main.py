#!/usr/bin/env python3

import argparse
from model.MainFileManager import MainFileManager
from pathlib import Path
from rich.console import Console
from rich.table import Table

def build_parser():
    parser = argparse.ArgumentParser(description='Git Repository Manager')

    subparsers = parser.add_subparsers(title='commands', dest='command', required=True)
    subparsers.add_parser('status', help='Show status of all projects')
    subparsers.add_parser('tui', help='Open TUI viewer')
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
            str(project.status),
            project.current_release(),
            project.issues_string_for_release(),
        )

    Console().print(table)

if __name__ == '__main__':
    parser = build_parser()

    # print(parser.parse_args())

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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
