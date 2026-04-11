# help

Display help documentation for a Gitter command.

## Usage

```
gitter help <topic>
```

## Arguments

| Argument | Description |
|----------|-------------|
| `topic` | The command or topic to show help for (e.g. `add`, `status`, `tui`) |

## Available Topics

| Topic | Description |
|-------|-------------|
| `add` | Add the current directory as a tracked project |
| `status` | Show a status table of all projects |
| `issues` | Show issues grouped by project and release |
| `notes` | Show formatted release notes |
| `raw` | Output raw Markdown release notes |
| `tui` | Launch the terminal UI |
| `version` | Print the current version |
| `help` | Show this help page |

## Examples

Show help for the `tui` command:

```bash
gitter help tui
```

Show help for the `issues` command:

```bash
gitter help issues
```

## Notes

- If no documentation is available for the requested topic, an error message is printed.
- Help files are Markdown documents stored in the `documents/` folder.
