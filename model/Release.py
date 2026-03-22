from dataclasses import dataclass
from BusinessLogic.GitManager import GitManager
from model.GitLog import GitLog
from model.Issue import Issue


@dataclass
class Release:
    name: str
    date: str
    commits: list[GitLog]
    issues: list[Issue]