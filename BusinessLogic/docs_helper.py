from __future__ import annotations

from pathlib import Path


def get_document(filename: str) -> str | None:
    """
    Return the text content of a document file, or None if not found.
    Works both in development (root documents/ folder) and when installed via pip
    (TUI/documents/ bundled as package data).
    """
    # Installed package: documents are inside the TUI package
    try:
        from importlib.resources import files
        data = files("TUI").joinpath(f"documents/{filename}")
        return data.read_text(encoding="utf-8")
    except (FileNotFoundError, TypeError, ModuleNotFoundError):
        pass

    # Development fallback: root-level documents/ folder
    dev_path = Path(__file__).parent.parent / "documents" / filename
    if dev_path.exists():
        return dev_path.read_text(encoding="utf-8")

    return None
