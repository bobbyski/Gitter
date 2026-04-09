# status

Display a summary table of all tracked projects, showing their current git status, latest release, and open issues.

## Usage

```
python main.py status
```

## Options

None.

## Output

A Rich-formatted table with the following columns:

| Column | Description |
|--------|-------------|
| Name | Project name |
| Directory | Absolute path to the repository |
| Status | Current branch and working tree state (color-coded) |
| Release | Most recent tagged release |
| Issues in Current/Next Release | Issues associated with the current or next release |

## Example

```bash
python main.py status
```

## Notes

- All projects are fetched from `~/.gitter`.
- Git data is fetched live from each repository on each run.
- Status colors: green = clean/up-to-date, yellow = modified, red = deleted.
