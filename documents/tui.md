# tui

Launch the Gitter terminal user interface (TUI).

## Usage

```
gitter tui
```

## Options

None.

## Description

Opens an interactive terminal dashboard for monitoring all tracked git repositories. The TUI refreshes project status automatically every 90 seconds and supports keyboard-driven navigation.

## Layout

| Panel | Description |
|-------|-------------|
| Project list (left) | All tracked projects with their git status |
| Release notes (right) | Markdown release notes for the selected project |
| Log window (bottom) | Output log for git operations |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Q` | Quit |
| `Ctrl+A` | Add a new project |
| `Ctrl+E` | Edit the selected project |
| `Ctrl+D` | Delete the selected project |
| `Ctrl+K` | Open git commit dialog for the selected project |
| `Ctrl+G` | Open Git menu (Pull, Fetch, Push, git-flow operations) |
| `Ctrl+F` | Open File menu |
| `Ctrl+V` | Open View menu (toggle log window / release notes panel) |
| `Ctrl+L` | Toggle log window |
| `Ctrl+R` | Toggle release notes panel |

## Git Menu Actions

Accessible via `Ctrl+G` or clicking "Git" in the menu bar:

| Action | Available When |
|--------|---------------|
| Commit | Any project selected |
| Pull | Any project selected |
| Fetch | Any project selected |
| Push | Any project selected |
| Start Feature | On `develop` branch |
| Finish Feature | On a `feature/` branch |
| Start Release | On `develop` branch |
| Finish Release | On a `release/` branch |

## Notes

- Projects must be added first with `gitter add`.
- All git operations are performed via the native `git` CLI.
