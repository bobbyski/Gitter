#!/usr/bin/env python3

import argparse
from operator import index

from rich.markdown import Markdown

from CommandLine.CommandLineAddProject import add_project
from CommandLine.CommandLineIssue import issues
from CommandLine.CommandLineNotes import notes
from CommandLine.CommandLineStatus import status
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
            status( args.project )
        elif args.command.lower() == 'issues':
            issues( args.project, args.release )
        elif args.command.lower() == 'notes':
            notes( args.project, args.release, markdown=args.markdown, raw=False, code_theme=args.theme )
        elif args.command.lower() == 'raw':
            notes( args.project, args.release, markdown=False, raw=True )

if __name__ == '__main__':
    main()

