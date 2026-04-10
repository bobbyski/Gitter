#!/usr/bin/env python3

from importlib.metadata import version, PackageNotFoundError


class TomlHelper:
    """Helper class for reading package metadata."""

    def get_version(self) -> str:
        try:
            return version("gitterApp")
        except PackageNotFoundError:
            pass

        # Fallback: read pyproject.toml directly (dev environment)
        from pathlib import Path
        toml_path = Path(__file__).parent.parent / "pyproject.toml"
        if toml_path.exists():
            with open(toml_path, "r") as file:
                for line in file:
                    strip_line = line.strip()
                    if strip_line.startswith("version"):
                        return strip_line.split("=")[1].strip().strip('"')

        return "unknown"


if __name__ == "__main__":
    helper = TomlHelper()
    version = helper.get_version()
    print(f"Project version: {version}")
