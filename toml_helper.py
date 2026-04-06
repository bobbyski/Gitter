#!/usr/bin/env python3

class TomlHelper:
    def __init__(self):
        self.filename = "pyproject.toml"

    """Helper class for working with TOML files."""
    def get_version(self) -> str:
        with open(self.filename, "r") as file:
            for line in file:
                strip_line = line.strip()
                if strip_line.startswith("version"):
                    return strip_line.split("=")[1].strip()

        return "ERROR: Version not found in pyproject.toml"


if __name__ == "__main__":
    helper = TomlHelper()
    version = helper.get_version(helper.filename)
    print(f"Project version: {version}")
