from dataclasses import dataclass


@dataclass
class GitStatusFile:
    state: str
    filename: str

    def __init__(self, state: str, filename: str):
        self.state = state
        self.filename = filename
