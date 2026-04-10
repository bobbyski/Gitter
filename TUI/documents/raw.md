# raw

Output raw Markdown release notes without any formatting or rendering.

## Usage

```
gitter raw [-p PROJECT] [-r RELEASE]
```

## Options

| Option | Description |
|--------|-------------|
| `-p PROJECT`, `--project PROJECT` | Show release notes for a specific project only (case-insensitive). |
| `-r RELEASE`, `--release RELEASE` | Filter to a specific release tag (prefix match, case-insensitive). |

## Output

Plain Markdown text printed to stdout with no Rich formatting applied. Suitable for piping into other tools or saving to a file.

## Examples

Print raw Markdown for all projects:

```bash
gitter raw
```

Print raw Markdown for a specific project:

```bash
gitter raw -p "My Project"
```

Save release notes to a file:

```bash
gitter raw -p "My Project" > RELEASE_NOTES.md
```

## Notes

- Use `notes -m` if you want terminal-rendered Markdown instead.
- Projects with no issues are omitted.
