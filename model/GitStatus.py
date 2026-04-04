from dataclasses import dataclass
from rich.text import Text

@dataclass
class GitStatus:
    branch: str
    filesAdded: list
    filesModified: list
    filesDeleted: list
    filesUntracked: list
    state: str

    def process_status_response(self, response: str):
        lines = response.split("\n")
        self.state = ""
        for line in lines:
            if line.startswith("On branch "):
                self.branch = line.split(" ")[2]
            elif line.startswith("Changes to be committed:"):
                self.filesAdded = [line.split(" ")[2] for line in lines if line.startswith(" ")]
            elif line.startswith("Changes not staged for commit:"):
                self.filesModified = [line.split(" ")[2] for line in lines if line.startswith(" ")]
            elif line.startswith("Untracked files:"):
                self.filesUntracked = [line.split(" ")[2] for line in lines if line.startswith(" ")]
            elif line.startswith("Your branch is up to date with"):
                self.state = "up to date"

    def __init__(self):
        self.branch = ""
        self.filesAdded = []
        self.filesModified = []
        self.filesDeleted = []
        self.filesUntracked = []
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
