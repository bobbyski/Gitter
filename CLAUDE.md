# Gitter

A terminal UI application for monitoring multiple Git repositories. Built with Python and [Textual](https://textual.textualize.io/).

## What it does

Gitter displays a dashboard of configured Git projects, showing their current status and upcoming/recent release notes. It polls git repos on a timer (every 90s) and lets users view release notes grouped by tag.

## Running the app

```bash
python main.py tui
```

Requires Python 3.9+ and the dependencies in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Project structure

```
main.py                         # CLI entry point — add, status, issues, notes, raw, tui, version subcommands

TUI/
  MenuApp.py                    # App class — wires together MenuBar, ProjectView, ReleaseNotes, LogWindow
  menu_app.tcss                 # CSS for the main app layout

  Menu/
    MenuBar.py                  # Top menu bar widget
    FileMenu.py                 # File menu modal screen
    ViewMenu.py                 # View menu modal — takes current visibility state, dismisses with action
    GitMenu.py                  # Git menu modal — Pull, Fetch, Push options; dismisses with action string

  project/
    ProjectView.py              # Main project table; defines RefreshRequested, ResizeRequested, ProjectSelected
    ReleaseNotes.py             # Release notes markdown panel
    add_or_edit_project.py      # Modal for adding/editing a project; includes DirectoryPickerModal
    project_view.tcss
    ReleaseNotes.tcss
    add_or_edit_project.tcss

  commit/
    git_commit.py               # GitCommitModal — type/issue/summary fields auto-filled from branch name;
                                #   embeds GitStagingView; dismisses with (message, add_unstaged) tuple
    git_staging.py              # GitStagingView — staged/unstaged file lists; double-click to stage/unstage;
                                #   Stage all / Unstage all buttons call GitManager directly
    git_commit.tcss
    git_staging.tcss

  debug/
    rich_log.py                 # GitterLogger (logging helper) and RichLogWindow (log panel widget)

BusinessLogic/
  GitManager.py                 # Runs git CLI commands via subprocess:
                                #   get_status, get_logs, commit, stage, stage_all, unstage, unstage_all,
                                #   push, pull, fetch
  toml_helper.py                # Reads version from pyproject.toml; path resolved relative to file location

model/
  MainFile.py                   # Top-level data model: name + list of Projects
  MainFileManager.py            # Loads/saves MainFile to ~/.gitter (JSON)
  Project.py                    # Per-repo model: parses commits into Releases and Issues
  GitLog.py                     # Parses raw git log output; matches release tags incl. suffixes (rc1, b2)
  GitStatus.py                  # Parses git status into staged/unstaged/untracked file lists
  GitStatusFile.py              # Per-file model: state (modified/new file/deleted) + filename
  Release.py                    # A tagged release with associated Issues
  Issue.py                      # A single issue (number + title)

README.md
LICENSE.md
pyproject.toml
```

## Data persistence

Projects are stored in `~/.gitter` as JSON, managed by `MainFileManager`. On startup `MenuApp` loads this file and calls `project.update()` for each project to fetch live git data.

## CLI usage

```bash
python main.py add              # Add current directory as a project (name = directory name)
python main.py add -p NAME      # Add current directory with a custom name
python main.py status           # Rich table of all projects with status, release, issues
python main.py issues           # Rich table of issues grouped by project and release
python main.py issues -p NAME   # Filter by project name
python main.py issues -r TAG    # Filter by release tag
python main.py notes            # Formatted release notes
python main.py notes -p NAME    # Release notes for one project
python main.py notes -m         # Render as Markdown
python main.py raw              # Raw Markdown release notes (no formatting)
python main.py tui              # Launch the Textual TUI
python main.py version          # Print version from pyproject.toml
```

## Key patterns

- **Textual widgets**: UI components subclass `Static`, `ModalScreen`, or `App`. Compose the widget tree in `compose()`.
- **CSS**: Styles live in `.tcss` files co-located with their widgets. `CSS_PATH` in `MenuApp` lists them as paths relative to `TUI/MenuApp.py` (e.g. `"commit/git_commit.tcss"`). All CSS files must be listed to take effect.
- **Git access**: All git operations go through `GitManager`, which shells out via `subprocess`.
- **Logging**: Use `GitterLogger.log(...)` (defined in `TUI/debug/rich_log.py`) instead of `print`.
- **Timer-based refresh**: `ProjectView.on_mount` sets a 90-second interval calling `update_all()`.
- **Commit flow**: `Ctrl+K` opens `GitCommitModal` for the selected project. The modal auto-fills type/issue/summary from the branch name (e.g. `feature/GIT-15_My_summary`). Dismisses with `(message, add_unstaged)`.
- **Git menu**: `Ctrl+G` (or clicking "Git" in the menu bar) opens `GitMenu` for Pull, Fetch, and Push on the selected project. Results are logged via `GitterLogger`; Pull and Fetch also refresh the project view on success.
- **Python version**: Targets Python 3.9+. Use `Optional[X]` instead of `X | None` and `from __future__ import annotations` for forward references.

## Branch strategy

- `develop` is the main working branch
- Features branch off `develop` as `feature/GIT-N_Description`
- Releases use `release/x.y.z` branches
