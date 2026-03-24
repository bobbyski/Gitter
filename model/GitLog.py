from dataclasses import dataclass
import re

from model.Issue import Issue
from model.Release import Release
from rich_log import GitterLogger


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

    def get_release(self):
        result = None

        for tag in self.tags:
            if tag.startswith("v"):
                result = Release()
                result.name = tag
                result.date = self.date
                # result.commit.append(self)
            elif re.fullmatch(r"\d+(\.\d+)*", tag):
                result = Release()
                result.name = tag
                result.date = self.date
                # result.commit.append(self)

        return result

    def get_issue(self, issuePrefixes: list[str]):
        for prefix in issuePrefixes:
            match = re.search(rf"\b{re.escape(prefix)}[- ]?(\d+)\b", self.message)
            if match:
                return f"{prefix}{match.group(1)}"
        return None

    def __repr__(self):
        return f"GitLog(commit='{self.commit}', message='{self.message}', author='{self.author}', date='{self.date}', tags={self.tags}, heads={self.heads})"

    @classmethod
    def parse_logstring(cls, logstring: str):
        logs = []
        current = None
        message_lines = []

        def finalize_current():
            nonlocal current, message_lines
            if current is None:
                return

            current.message = "\n".join(message_lines).strip()
            logs.append(current)
            current = None
            message_lines = []

        if len(logstring) > 0:
            for raw_line in logstring.splitlines():
                line = raw_line.rstrip()

                if not line.strip():
                    continue

                if line.startswith("commit "):
                    finalize_current()
                    current = cls()

                    commit_part = line[len("commit "):].strip()
                    refs_match = re.search(r"\((.*?)\)", commit_part)

                    if refs_match:
                        current.commit = commit_part[:refs_match.start()].strip()
                        refs_text = refs_match.group(1)
                        refs = [ref.strip() for ref in refs_text.split(",")]

                        for ref in refs:
                            if ref.startswith("tag: "):
                                current.tags.append(ref[len("tag: "):].strip())
                            elif ref.startswith("HEAD -> "):
                                current.heads.append(ref[len("HEAD -> "):].strip())
                            else:
                                current.heads.append(ref)
                    else:
                        current.commit = commit_part

                elif current is not None and line.startswith("Author: "):
                    current.author = line[len("Author: "):].strip()

                elif current is not None and line.startswith("Date:   "):
                    current.date = line[len("Date:   "):].strip()

                elif current is not None:
                    if line.startswith("    "):
                        message_lines.append(line[4:])
                    else:
                        message_lines.append(line.strip())

            finalize_current()

        # GitterLogger.log(logs)

        return logs
