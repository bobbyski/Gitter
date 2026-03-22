from dataclasses import dataclass
import re

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

        GitterLogger.log( f"Parsing logstring of length {len(logstring)}" )

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
                    refs = [ref.strip() for ref in refs_match.group(1).split(",")]

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

        GitterLogger.log( f"Parsed {len(logs)} logs" )

        return logs
