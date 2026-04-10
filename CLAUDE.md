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
main.py                         # CLI entry point — add, status, issues, notes, raw, tui, version, help subcommands

TUI/
  MenuApp.py                    # App class — wires together MenuBar, ProjectView, ReleaseNotes, LogWindow
  menu_app.tcss                 # CSS for the main app layout and all menu modal positioning

  Menu/
    MenuBar.py                  # Top menu bar widget (File, Edit, View, Git, Help labels)
    FileMenu.py                 # File menu modal screen
    ViewMenu.py                 # View menu modal — takes current visibility state, dismisses with action
    GitMenu.py                  # Git menu modal — Pull, Fetch, Push, Commit, git-flow options;
                                #   enabled/disabled based on current branch; dismisses with action string

  GitFlow/
    start_feature.py            # StartFeatureModal — Input for feature name; dismisses with name or None
    finish_feature.py           # FinishFeatureModal — confirms finish; dismisses with bool
    start_release.py            # StartReleaseModal — version field pre-filled via auto-increment; dismisses with version or None
    finish_release.py           # FinishReleaseModal — confirms finish; dismisses with bool
    start_feature.tcss
    finish_feature.tcss
    start_release.tcss
    finish_release.tcss

  Help/
    help_menu.py                # HelpMenu modal — About Gitter, doc topics, separator, License at bottom;
                                #   HELP_TOPICS list + ABOUT_LABEL + LICENSE_LABEL/LICENSE_FILE constants
    markdown_viewer.py          # MarkdownViewerModal — scrollable modal for displaying markdown content
    about_gitter.py             # AboutGitter modal — version, description, credits, copyright
    markdown_viewer.tcss
    about_gitter.tcss

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
    git_staging.py              # GitStagingView — staged/unstaged/untracked file lists; double-click to
                                #   stage/unstage; state labels color-coded by type; Stage all / Unstage all
                                #   buttons call GitManager directly
    git_commit.tcss
    git_staging.tcss

  debug/
    rich_log.py                 # GitterLogger (logging helper) and RichLogWindow (log panel widget)

BusinessLogic/
  GitManager.py                 # Runs git CLI commands via subprocess:
                                #   get_status, get_logs, commit, stage, stage_all, unstage, unstage_all,
                                #   push, push_main_and_develop, pull, fetch,
                                #   flow_feature_start, flow_feature_finish,
                                #   flow_release_start, flow_release_finish, _detect_main_branch
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

documents/                      # Markdown help files (one per CLI command + license)
  add.md, status.md, issues.md, notes.md, raw.md, tui.md, version.md, help.md, license.md

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
python main.py help TOPIC       # Display help doc for a topic (e.g. help tui)
```

## Key patterns

- **Textual widgets**: UI components subclass `Static`, `ModalScreen`, or `App`. Compose the widget tree in `compose()`.
- **CSS**: Styles live in `.tcss` files co-located with their widgets. `CSS_PATH` in `MenuApp` lists them as paths relative to `TUI/MenuApp.py` (e.g. `"commit/git_commit.tcss"`). All CSS files must be listed to take effect.
- **Menu positioning**: Menus use `align: left top` on the modal and a fixed `margin-left` on the list widget to position the dropdown under the correct menu bar label. Values are in `menu_app.tcss`.
- **Menu dismiss**: All menus dismiss on Escape (via `BINDINGS`) and on clicking the backdrop (`on_click` checks `event.widget is self`).
- **Git access**: All git operations go through `GitManager`, which shells out via `subprocess`.
- **Git flow**: `flow_release_finish` auto-detects `main` vs `master` using `_detect_main_branch()` (`git show-ref --verify refs/heads/main`).
- **Staging view**: `GitStagingView` shows staged, unstaged, and untracked files. State labels are color-coded: green=new, yellow=modified, red=deleted, cyan=renamed, muted=untracked. Double-click to stage/unstage.
- **Help system**: `HelpMenu` lists About Gitter, doc topics (from `HELP_TOPICS`), and License (after a separator). Selecting a topic opens `MarkdownViewerModal` with the matching file from `documents/`. "About Gitter" opens `AboutGitter`. CLI: `python main.py help <topic>` renders the matching `.md` file.
- **Project view colors**: Project name is green (up to date) or yellow (has changes). Status column uses `GitStatus.to_rich()`. Issues column is yellow when showing "Next release" items. Directory column replaces home dir with `~`.
- **Logging**: Use `GitterLogger.log(...)` (defined in `TUI/debug/rich_log.py`) instead of `print`.
- **Timer-based refresh**: `ProjectView.on_mount` sets a 90-second interval calling `update_all()`.
- **Commit flow**: `Ctrl+K` opens `GitCommitModal` for the selected project. The modal auto-fills type/issue/summary from the branch name (e.g. `feature/GIT-15_My_summary`). Dismisses with `(message, add_unstaged)`.
- **Git menu**: `Ctrl+G` (or clicking "Git" in the menu bar) opens `GitMenu`. Pull/Fetch/Push/Commit disabled when no project selected. "Push Master and Develop" pushes both branches and is only enabled on `develop`. Start/Finish Feature enabled on feature branches; Start/Finish Release enabled on develop/release branches. GitMenu takes `branch` and `project_selected` parameters.
- **Python version**: Targets Python 3.9+. Use `Optional[X]` instead of `X | None` and `from __future__ import annotations` for forward references.

## Branch strategy

- `develop` is the main working branch
- Features branch off `develop` as `feature/GIT-N_Description`
- Releases use `release/x.y.z` branches
