from dataclasses import dataclass
from BusinessLogic.GitManager import GitManager
from model.GitLog import GitLog
from model.Issue import Issue
from model.Release import Release


@dataclass
class Project:
    name: str
    directory: str
    status: str
    tagBranch: str
    issuePrefixes: list[str]
    prPatterns: list[str]

    commits: list[GitLog]
    issues: list[Issue]
    releases: list[Release]

    def update_status(self):
        result = GitManager(self.directory).get_status()
        self.status = result
