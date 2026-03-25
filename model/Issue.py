from dataclasses import dataclass

@dataclass
class Issue:
    number: str
    title: str

    def __init__(self):
        self.number = ""
        self.title = ""
