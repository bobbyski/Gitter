
import subprocess

from model.GitLog import GitLog
from model.GitStatus import GitStatus
from rich_log import GitterLogger


class GitManager:
    def __init__(self, repo_path: str):
        self.repo = repo_path

    def get_status(self):
        if self.repo is None:
            return "No repository initialized"

        theStatus = subprocess.run(["git", "-C", self.repo, "status"], capture_output=True, text=True)

        result = GitStatus()
        result.process_status_response(theStatus.stdout)

        return result

    def get_logs(self, limit: int = 1000, branch: str = "master"):
        if self.repo is None:
            return "No repository initialized"

        theLogs = subprocess.run( ["git", "-C", self.repo, "log", "-n", f"{limit}", f"{branch}"],
                                  capture_output=True, text=True)

        # GitterLogger.log( f"Git logs: {theLogs.stdout}" )
        # GitterLogger.log( f"Git error: {theLogs.stderr}" )

        return GitLog.parse_logstring( theLogs.stdout )

