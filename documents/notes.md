# notes

Display formatted release notes for tracked projects.

## Usage

```
gitter [-p PROJECT] [-r RELEASE] [-m] [-t THEME] notes
```

## Options

| Option | Description |
|--------|-------------|
| `-p PROJECT`, `--project PROJECT` | Show release notes for a specific project only (case-insensitive). |
| `-r RELEASE`, `--release RELEASE` | Filter to a specific release tag (prefix match, case-insensitive). |
| `-m`, `--markdown` | Render the release notes as Markdown using Rich's Markdown renderer. |
| `-t THEME`, `--theme THEME` | Syntax highlighting theme for Markdown code blocks (default: `monokai`). |

## Output

By default, release notes are printed as plain Rich-formatted text. With `-m`, they are rendered as formatted Markdown in the terminal.

## Examples

Show release notes for all projects:

```bash
gitter notes
```

Show release notes for a specific project:

```bash
gitter -p "My Project" notes
```

Show release notes for a specific release:

```bash
gitter -r 1.2.0 notes
```

Render as Markdown:

```bash
gitter -m notes
```

Render as Markdown with a custom theme:

```bash
gitter -m -t github-dark notes
```

## Notes

- Projects with no issues are omitted.
- Use `raw` to output the unrendered Markdown source instead.
