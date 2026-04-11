# add

Add the current working directory as a tracked project in Gitter.

## Usage

```
gitter [-p NAME] add
```

## Options

| Option | Description |
|--------|-------------|
| `-p NAME`, `--project NAME` | Custom name for the project. Defaults to the directory's folder name. |

## Examples

Add the current directory using its folder name as the project name:

```bash
cd ~/projects/my-repo
gitter add
```

Add the current directory with a custom name:

```bash
gitter -p "My Project" add
```

## Notes

- If the current directory is already tracked, Gitter will print an error and skip it.
- Projects are saved to `~/.gitter` and persist across sessions.
