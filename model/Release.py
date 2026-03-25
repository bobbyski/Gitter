from dataclasses import dataclass
from model.Issue import Issue


@dataclass
class Release:
    name: str
    date: str
    issues: list[Issue]

    def __init__(self):
        self.name = ""
        self.date = ""
        self.issues = []

    def has_issue(self, issue_number: str ):
        result = False

        for issue in self.issues:
            if issue.number == issue_number:
                result = True
                break

        return result

    def issues_list(self):
        result: list[str] = []

        for issue in self.issues:
            result.append(issue.number)

        return result


