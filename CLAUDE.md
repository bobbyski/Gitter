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
MenuApp.py          # Entry point — App class, wires together MenuBar + ProjectView
MenuBar.py          # Top menu bar widget
FileMenu.py         # File menu modal screen
ViewMenu.py         # View menu modal screen — takes current log visibility, dismisses with selected action
ProjectView.py      # Main project table view; Refresh/Release notes/Logs/Add toolbar buttons;
                    #   defines RefreshRequested and ResizeRequested messages
TextWidget.py       # Custom text widget
rich_log.py         # GitterLogger (logging helper) and RichLogWindow (log panel widget)

BusinessLogic/
  GitManager.py     # Runs git CLI commands (status, log) via subprocess

model/
  MainFile.py       # Top-level data model: name + list of Projects
  MainFileManager.py# Loads/saves MainFile to ~/.gitter (JSON)
  Project.py        # Per-repo model: parses commits into Releases and Issues
  GitLog.py         # Parses raw git log output
  GitStatus.py      # Parses git status output
  Release.py        # A tagged release with associated Issues
  Issue.py          # A single issue (number + title)

menu_app.tcss       # Textual CSS for the main app layout
project_view.tcss   # Textual CSS for the project table

README.md
LICENSE.md
```

## Data persistence

Projects are stored in `~/.gitter` as JSON, managed by `MainFileManager`. On startup `MenuApp` loads this file and calls `project.update()` for each project to fetch live git data.

## Key patterns

- **Textual widgets**: UI components subclass `Static`, `ModalScreen`, or `App`. Compose the widget tree in `compose()`.
- **CSS**: Styles live in `.tcss` files; `CSS_PATH` on the App class lists them.
- **Git access**: All git operations go through `GitManager`, which shells out via `subprocess`.
- **Logging**: Use `GitterLogger.log(...)` (defined in `rich_log.py`) instead of `print`.
- **Timer-based refresh**: `ProjectView.on_mount` sets a 90-second interval calling `update_all()`.

## Branch strategy

- `develop` is the main working branch
- Features branch off `develop` as `feature/GIT-N_Description`
- Releases use `release/x.y.z` branches
