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
    favorite: bool
    groups: list[str]
    commits: list[GitLog]
    issues: list[Issue]
    releases: list[Release]

    def update(self):
        self.issues = []
        self.releases = []

        self.update_status()
        self.commits = GitManager(self.directory).get_logs()
        self.process_commits()

        # GitterLogger.log( f"Project {self.name} updated" )
        # GitterLogger.log( self )

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

    def first_issues_release_name(self):
        for release in self.releases:
            if len( release.issues ) > 0:
                return release.name

        return "Next release"

    def issues_for_release(self, releaseName: str = ""):
        result: list[Issue] = []

        if releaseName == "":
            releaseName = self.first_issues_release_name()

        for release in self.releases:
            if release.name == releaseName:
                for issue in release.issues:
                    result.append(issue.number)

        return result

    def issues_list(self):
        result: list[Issue] = []

        for release in self.releases:
            for issue in release.issues:
                result.append(issue.number)

        return result

    def issues_string_for_release(self, releaseName: str = "", delimiter = ", "):
        result = ""
        if releaseName == "":
            releaseName = self.first_issues_release_name()

            if releaseName != "Next release":
                result += f"{releaseName}: "

        result += delimiter.join( self.issues_for_release(releaseName ))

        return result

    def current_release(self):
        for release in self.releases:
            if release.name != "Next release":
                return release.name

        return ""

    def next_release_issues(self):
        return self.issues_for_release( "Next release" )

    def release_summary(self):
        result = self.current_release()
        total = len(self.next_release_issues())
        if total > 0 and result !="":
            result += f" + {len(self.next_release_issues())} issue"
            if total > 1:
                result += "s"

        return result

    def release_notes_markdown( self, release_name: str = None ) -> str:
        markdown_lines = [f"#  {self.name} Release Notes"]
        current = self.current_release()

        if current != "":
            markdown_lines.append(f" - version: {current}")

        markdown_lines.append("\n")

        if self.releases:
            for release in self.releases:

                if release_name is not None and release.name.lower().startswith(release_name.lower()) is False:
                    continue

                if len( release.issues ) > 0:
                    markdown_lines.append(f"## {release.name}")

                    markdown_lines.append( "\n" )

                    if release.issues:
                        for issue in release.issues:
                            if issue.number:
                                markdown_lines.append(f"#### {issue.number} \n")
                            markdown_lines.append(f"{issue.title}\n")

                    markdown_lines.append("\n")

        if len(markdown_lines) == 1:
            markdown_lines.append("No releases found.\n")

        return "".join(markdown_lines)

    def release_notes( self, release_name: str = None ) -> str:
        markdown_lines = [f"                              {self.name} Release Notes"]
        current = self.current_release()

        if current != "":
            markdown_lines.append(f" - version: {current}")

        markdown_lines.append("\n")

        if self.releases:
            for release in self.releases:

                if release_name is not None and release.name.lower().startswith(release_name.lower()) is False:
                    continue

                if len( release.issues ) > 0:
                    markdown_lines.append(f"{release.name}")

                    markdown_lines.append( "\n" )

                    if release.issues:
                        for issue in release.issues:
                            if issue.number:
                                markdown_lines.append(f"{issue.number} \n")
                            markdown_lines.append(f"{issue.title}\n")

                    markdown_lines.append("\n")

        if len(markdown_lines) == 1:
            markdown_lines.append("No releases found.\n")

        return "".join(markdown_lines)

