# notes

Display formatted release notes for tracked projects.

## Usage

```
gitter notes [-p PROJECT] [-r RELEASE] [-m] [-t THEME]
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
gitter notes -p "My Project"
```

Show release notes for a specific release:

```bash
gitter notes -r 1.2.0
```

Render as Markdown:

```bash
gitter notes -m
```

Render as Markdown with a custom theme:

```bash
gitter notes -m -t github-dark
```

## Notes

- Projects with no issues are omitted.
- Use `raw` to output the unrendered Markdown source instead.
