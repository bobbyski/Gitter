from dataclasses import dataclass

from BusinessLogic.GitManager import GitManager


@dataclass
class Project:
    name: str
    directory: str
    status: str
    tagBranch: str
    issuePrefixes: list[str]
    prPatterns: list[str]

    def update_status(self):
        result = GitManager(self.directory).get_status()
        self.status = result
