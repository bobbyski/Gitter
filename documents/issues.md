# issues

Display a table of issues grouped by project and release.

## Usage

```
gitter issues [-p PROJECT] [-r RELEASE]
```

## Options

| Option | Description |
|--------|-------------|
| `-p PROJECT`, `--project PROJECT` | Filter output to a specific project name (case-insensitive). |
| `-r RELEASE`, `--release RELEASE` | Filter output to a specific release tag (prefix match, case-insensitive). |

## Output

A Rich-formatted table with the following columns:

| Column | Description |
|--------|-------------|
| Project | Project name (shown once per project) |
| Release | Release tag (e.g. `1.2.0`, `Next release`) |
| Issue | Issue number or identifier |
| Commit Summary | The commit message associated with the issue |

Releases within a project are separated by a divider line. Projects are separated by a section break.

## Examples

Show all issues across all projects:

```bash
gitter issues
```

Show issues for a specific project:

```bash
gitter issues -p "My Project"
```

Show issues for a specific release:

```bash
gitter issues -r 1.2.0
```

Combine filters:

```bash
gitter issues -p "My Project" -r 1.2.0
```

## Notes

- Projects with no issues are omitted from the output.
- Issues are parsed from git commit history using the configured issue prefixes.
