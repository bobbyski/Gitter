# Gitter

A terminal dashboard for monitoring multiple Git repositories. Built with Python and [Textual](https://github.com/Textualize/textual).

Gitter shows the status, current release, and upcoming issues for all your configured repos at a glance — and lets you stage files and write commits without leaving the terminal.

---

## Features

- **Multi-repo dashboard** — see branch status, release version, and next-release issues for all projects in one view
- **Release notes** — commits are parsed into tagged releases and issues, displayed as a Markdown panel
- **Git commit modal** — type/issue/summary fields auto-filled from the branch name, with a staging view for reviewing changes before committing
- **Stage/unstage files** — double-click files to stage or unstage; one-click stage all / unstage all
- **CLI interface** — `status` and `issues` commands with Rich-formatted tables for use in scripts or pipelines
- **Auto-refresh** — repos are polled every 90 seconds in the background

## Requirements

- Python 3.9+
- Git installed and available on `PATH`

## Installation

```bash
git clone https://github.com/bobbyskinnerart/Gitter.git
cd Gitter
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### TUI (interactive dashboard)

```bash
python main.py tui
```

### CLI commands

```bash
python main.py status                   # Table of all projects with status and release info
python main.py issues                   # All issues grouped by project and release
python main.py issues -p <project>      # Filter by project name
python main.py issues -r <release>      # Filter by release tag
python main.py version                  # Print version
```

### Key bindings (TUI)

| Key | Action |
|-----|--------|
| `Ctrl+K` | Commit selected project |
| `Ctrl+A` | Add project |
| `Ctrl+E` | Edit selected project |
| `Ctrl+D` | Delete selected project |
| `Ctrl+R` | Toggle release notes panel |
| `Ctrl+L` | Toggle log panel |
| `Ctrl+Q` | Quit |

Double-click a project row to edit it.

## Configuration

Projects are stored in `~/.gitter` as JSON. Add a repo via `Ctrl+A` in the TUI or by editing the file directly.

Each project entry supports:

| Field | Description |
|-------|-------------|
| `name` | Display name |
| `directory` | Absolute path to the git repo |
| `tagBranch` | Branch where release tags live (e.g. `main`) |
| `issuePrefixes` | Issue prefixes to detect in commit messages (e.g. `GIT`, `PROJ`) |
| `prPatterns` | PR number patterns (regex) |
| `groups` | Optional grouping labels |
| `favorite` | Mark as favorite |

## License

MIT — see [LICENSE.md](LICENSE.md) for details.
