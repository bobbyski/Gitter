from __future__ import annotations

from pathlib import Path


def get_document(filename: str) -> str | None:
    """
    Return the text content of a document file, or None if not found.
    Documents live in TUI/documents/ and are bundled as package data.
    Works in both development and when installed via pip.
    """
    # Installed package: use importlib.resources
    try:
        from importlib.resources import files
        data = files("TUI").joinpath(f"documents/{filename}")
        return data.read_text(encoding="utf-8")
    except (FileNotFoundError, TypeError, ModuleNotFoundError):
        pass

    # Development fallback: resolve relative to this file
    dev_path = Path(__file__).parent.parent / "TUI" / "documents" / filename
    if dev_path.exists():
        return dev_path.read_text(encoding="utf-8")

    return None
