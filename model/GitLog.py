from dataclasses import dataclass

@dataclass
class GitLog:
    commit: str
    message: str
    author: str
    date: str
    tags: list[str]
    heads: list[str]

    def __init__(self):
        self.commit = ""
        self.message = ""
        self.author = ""
        self.date = ""
        self.tags = []
        self.heads = []


    def __repr__(self):
        return f"GitLog(commit='{self.commit}', message='{self.message}', author='{self.author}', date='{self.date}', tags={self.tags}, heads={self.heads})"
