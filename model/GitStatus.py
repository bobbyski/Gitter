from dataclasses import dataclass
from rich.text import Text

from model.GitStatusFile import GitStatusFile


@dataclass
class GitStatus:
    branch: str
    filesAdded: list
    filesModified: list
    filesDeleted: list
    filesUntracked: list
    state: str
    statgedFiles: list[GitStatusFile]
    unstagedFiles: list[GitStatusFile]

    def process_status_response(self, response: str):
        self.state = ""
        section = None  # "staged" | "unstaged" | "untracked"

        for line in response.split("\n"):
            if line.startswith("On branch "):
                self.branch = line.split(" ")[2]
            elif line.startswith("Your branch is up to date with"):
                self.state = "up to date"
            elif line.startswith("Changes to be committed:"):
                section = "staged"
            elif line.startswith("Changes not staged for commit:"):
                section = "unstaged"
            elif line.startswith("Untracked files:"):
                section = "untracked"
            elif line == "":
                section = None
            elif section and line.startswith("\t"):
                content = line.strip()
                if section in ("staged", "unstaged"):
                    if ":" in content:
                        raw_state, _, path = content.partition(":")
                        state = raw_state.strip()
                        path = path.strip()
                        f = GitStatusFile(state=state, filename=path)
                        if section == "staged":
                            self.stagedFiles.append(f)
                            if state == "new file":
                                self.filesAdded.append(path)
                            elif state == "deleted":
                                self.filesDeleted.append(path)
                            else:
                                self.filesModified.append(path)
                        else:
                            self.unstagedFiles.append(f)
                            if state == "deleted":
                                self.filesDeleted.append(path)
                            else:
                                self.filesModified.append(path)
                elif section == "untracked":
                    if not content.startswith("("):
                        self.filesUntracked.append(content)

        return

    def __init__(self):
        self.branch = ""
        self.filesAdded = []
        self.filesModified = []
        self.filesDeleted = []
        self.filesUntracked = []
        self.stagedFiles = []
        self.unstagedFiles = []
        self.state = ""

    def to_rich(self) -> Text:
        text = Text()

        if self.state != "":
            text.append(self.state, style="green")

        if len(self.filesAdded) > 0:
            if len(text) > 0:
                text.append(" ")
            text.append(f"new: {len(self.filesAdded)}", style="green")

        if len(self.filesModified) > 0:
            if len(text) > 0:
                text.append(" ")
            text.append(f"mod: {len(self.filesModified)}", style="yellow")

        if len(self.filesDeleted) > 0:
            if len(text) > 0:
                text.append(" ")
            text.append(f"del: {len(self.filesDeleted)}", style="red")

        if len(self.filesUntracked) > 0:
            if len(text) > 0:
                text.append(" ")
            text.append(f"ut: {len(self.filesUntracked)}")

        if len(text) > 0:
            text.append(" ")

        if self.branch != "":
            text.append("on ")
            if self.branch == "develop" or self.branch == "main" or self.branch == "master":
                text.append(f"{self.branch}", style="dim")
            else:
                text.append(f"{self.branch}", style="blue")

        return text

    def to_long_rich(self) -> Text:
        text = Text()

        if self.state != "":
            text.append(f"{self.state}\n", style="green")

        if len(self.filesAdded) > 0:
            if len(text) > 0:
                text.append(" ")
            text.append(f"   {len(self.filesAdded)} new files\n", style="green")

        if len(self.filesModified) > 0:
            if len(text) > 0:
                text.append(" ")
            text.append(f"   {len(self.filesModified)} modified files\n", style="yellow")

        if len(self.filesDeleted) > 0:
            if len(text) > 0:
                text.append(" ")
            text.append(f"   {len(self.filesDeleted)} deleted files\n", style="red")

        if len(self.filesUntracked) > 0:
            if len(text) > 0:
                text.append(" ")
            text.append(f"   {len(self.filesUntracked)} untracked files\n")

        if len(text) > 0:
            text.append(" ")

        if self.branch != "":
            if self.branch == "develop" or self.branch == "main" or self.branch == "master":
                text.append(f"Currently on {self.branch}\n", style="green")
            else:
                text.append(f"Currently on {self.branch}\n", style="blue")

        return text

    def __repr__(self):
        result = ""

        if self.state != "":
            result += f"{self.state}"

        if len(self.filesAdded) > 0:
            if result != "":
                result += " "
            result += f"new: {len(self.filesAdded)}"

        if len(self.filesModified ) > 0:
            if result != "":
                result += " "
            result += f"mod: {len(self.filesModified)}"

        if len(self.filesDeleted ) > 0:
            if result != "":
                result += " "
            result += f"del: {len(self.filesDeleted)}"

        if len(self.filesUntracked ) > 0:
            if result != "":
                result += " "
            result += f"ut: {len(self.filesUntracked)}"

        if result != "":
            result += " "
        result += f"on {self.branch}"

        return result
