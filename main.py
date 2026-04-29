#!/usr/bin/env python3
import argparse
from CommandLine.CommandLineAddProject import add_project
from CommandLine.CommandLineHelp import show_help
from CommandLine.CommandLineInteractive import interactive
from CommandLine.CommandLineIssue import issues
from CommandLine.CommandLineNotes import notes
from CommandLine.CommandLineStatus import status
from CommandLine.CommandLineVersion import show_version
from model.MainFileManager import MainFileManager
from pathlib import Path

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
    subparsers.add_parser('easy', help='Ask ne what to do', aliases=['Easy', 'EASY'] )
    help_parser = subparsers.add_parser('help', help='Show help for a topic', aliases=['Help', 'HELP'])
    help_parser.add_argument('topic', type=str, help='Topic to show help for (e.g. add, status, tui)')

    parser.add_argument( '-p', '--project', type=str, help='Project name to show')
    parser.add_argument( '-r', '--release', type=str, help='The release number to show')
    parser.add_argument( '-m', '--markdown', action='store_true', help='Show release notes in markdown format')
    # parser.add_argument( '-t', '--theme', type=str, help='The theme to use', choices=styles, default='monokai')
    parser.add_argument( '-t', '--theme', type=str, help='The theme to use', default='monokai')
    parser.add_argument( '-s', '--sparse', action='store_true', help='Just show number on issues, no issue title')

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command.lower() == 'version':
        show_version('0.1.0')
    elif args.command.lower() == 'help':
        show_help(args.topic)
    else:
        pathname = str(Path.home() / ".gitter")
        MainFileManager.load_shared_from_json(pathname)
        MainFileManager.update_all_projects()

        if args.command.lower() == 'tui':
            from TUI.MenuApp import MenuApp
            app = MenuApp()
            app.run()
        elif args.command.lower() == 'add':
            pathname = str(Path.home() / ".gitter")
            MainFileManager.load_shared_from_json(pathname)
            add_project(args.project)
        elif args.command.lower() == 'status':
            status( args.project )
        elif args.command.lower() == 'easy':
            interactive()
        elif args.command.lower() == 'issues':
            issues( args.project, args.release, invertReleases=True, numbersOnly=args.sparse )
        elif args.command.lower() == 'notes':
            notes( args.project, args.release, markdown=args.markdown, raw=False, code_theme=args.theme )
        elif args.command.lower() == 'raw':
            notes( args.project, args.release, markdown=False, raw=True )

if __name__ == '__main__':
    main()

