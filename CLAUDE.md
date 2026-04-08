# Gitter

A terminal UI application for monitoring multiple Git repositories. Built with Python and [Textual](https://textual.textualize.io/).

## What it does

Gitter displays a dashboard of configured Git projects, showing their current status and upcoming/recent release notes. It polls git repos on a timer (every 90s) and lets users view release notes grouped by tag.

## Running the app

```bash
python MenuApp.py
```

Requires Python 3.9+ and the dependencies in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Project structure

```
MenuApp.py              # Entry point — App class, wires together MenuBar + ProjectView
MenuBar.py              # Top menu bar widget
FileMenu.py             # File menu modal screen
ViewMenu.py             # View menu modal screen — takes current log visibility, dismisses with selected action
ProjectView.py          # Main project table view; Refresh/Release notes/Logs/Add toolbar buttons;
                        #   defines RefreshRequested and ResizeRequested messages
ReleaseNotes.py         # Release notes panel widget
TextWidget.py           # Custom text widget
rich_log.py             # GitterLogger (logging helper) and RichLogWindow (log panel widget)
add_or_edit_project.py  # Modal for adding/editing a project; includes DirectoryPickerModal
git_commit.py           # GitCommitModal — commit message composer with type/issue/summary fields
                        #   and GitStagingView embedded; dismisses with (message, add_unstaged) tuple
git_staging.py          # GitStagingView — reusable widget showing staged/unstaged files;
                        #   posts StageAll / UnstageAll messages
main.py                 # CLI entry point — `status`, `issues`, `tui`, `version` subcommands
toml_helper.py          # TOML utility helpers

BusinessLogic/
  GitManager.py         # Runs git CLI commands (status, log, commit) via subprocess

model/
  MainFile.py           # Top-level data model: name + list of Projects
  MainFileManager.py    # Loads/saves MainFile to ~/.gitter (JSON)
  Project.py            # Per-repo model: parses commits into Releases and Issues
  GitLog.py             # Parses raw git log output; matches release tags (including suffixes like rc1, b2)
  GitStatus.py          # Parses git status output into staged/unstaged/untracked file lists
  GitStatusFile.py      # Per-file model: state (modified/new file/deleted) + filename
  Release.py            # A tagged release with associated Issues
  Issue.py              # A single issue (number + title)

menu_app.tcss           # Textual CSS for the main app layout
project_view.tcss       # Textual CSS for the project table
ReleaseNotes.tcss       # Textual CSS for the release notes panel
add_or_edit_project.tcss# Textual CSS for the add/edit project modal
git_commit.tcss         # Textual CSS for the commit modal
git_staging.tcss        # Textual CSS for the staging view

README.md
LICENSE.md
```

## Data persistence

Projects are stored in `~/.gitter` as JSON, managed by `MainFileManager`. On startup `MenuApp` loads this file and calls `project.update()` for each project to fetch live git data.

## CLI usage

```bash
python main.py status           # Rich table of all projects with status, release, issues
python main.py issues           # Rich table of issues grouped by project and release
python main.py issues -p NAME   # Filter by project name
python main.py issues -r TAG    # Filter by release tag
python main.py tui              # Launch the Textual TUI
python main.py version          # Print version
```

## Key patterns

- **Textual widgets**: UI components subclass `Static`, `ModalScreen`, or `App`. Compose the widget tree in `compose()`.
- **CSS**: Styles live in `.tcss` files; `CSS_PATH` on the App class lists them. All `.tcss` files must be listed in `MenuApp.CSS_PATH` to take effect.
- **Git access**: All git operations go through `GitManager`, which shells out via `subprocess`.
- **Logging**: Use `GitterLogger.log(...)` (defined in `rich_log.py`) instead of `print`.
- **Timer-based refresh**: `ProjectView.on_mount` sets a 90-second interval calling `update_all()`.
- **Commit flow**: `Ctrl+K` opens `GitCommitModal` for the selected project. The modal auto-fills type/issue/summary from the branch name (e.g. `feature/GIT-15_My_summary`). Dismisses with `(message, add_unstaged)`.
- **Python version**: Targets Python 3.9+. Use `Optional[X]` instead of `X | None` and `from __future__ import annotations` for forward references.

## Branch strategy

- `develop` is the main working branch
- Features branch off `develop` as `feature/GIT-N_Description`
- Releases use `release/x.y.z` branches
