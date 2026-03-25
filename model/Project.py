from dataclasses import dataclass
from BusinessLogic.GitManager import GitManager
from model.GitLog import GitLog
from model.Issue import Issue
from model.Release import Release
import re

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

    def process_commits(self):
        current = Release()
        current.name = "Next release"
        self.releases.append(current)

        for commit in self.commits:
            release = commit.get_release()
            if release is not None:
                current = release
                self.releases.append(current)

            issue = commit.get_issue(self.issuePrefixes)
            if issue is not None:
                if current.has_issue( issue ) == False:
                    theIssue = Issue()
                    theIssue.number = issue
                    theIssue.title = self.strip_issue( issue, commit.message )

                    current.issues.append(theIssue)

    def strip_issue(self, issue_number: str, source: str ):
        longest = ""
        segments = source.split(issue_number)

        for segment in segments:
            if len(segment) > len(longest):
                longest = segment

        while longest and not longest[0].isalnum():
            longest = longest[1:]

        return longest

    def issues_for_release(self, release: Release = "Next release"):
        result: list[Issue] = []

        for release in self.releases:
            if release.name == release:
                for issue in release.issues:
                    result.append(issue.number)

        return result


    def issues_string_for_release(self, release: Release = "Next release", delimiter = ", "):
        return delimiter.join(self.issues_for_release(release))

