
import subprocess

from model.GitLog import GitLog
from model.GitStatus import GitStatus


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

    def commit(self, message: str, add_unstaged: bool = False) -> tuple:
        args = ["git", "-C", self.repo, "commit"]
        if add_unstaged:
            args.append("-a")
        args += ["-m", message]
        result = subprocess.run(args, capture_output=True, text=True)
        success = result.returncode == 0
        output = result.stdout.strip() or result.stderr.strip()
        return success, output

    def stage(self, filename: str) -> tuple:
        result = subprocess.run(
            ["git", "-C", self.repo, "add", filename],
            capture_output=True, text=True,
        )
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def stage_all(self) -> tuple:
        result = subprocess.run(
            ["git", "-C", self.repo, "add", "-A"],
            capture_output=True, text=True,
        )
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def unstage(self, filename: str) -> tuple:
        result = subprocess.run(
            ["git", "-C", self.repo, "restore", "--staged", filename],
            capture_output=True, text=True,
        )
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def unstage_all(self) -> tuple:
        result = subprocess.run(
            ["git", "-C", self.repo, "restore", "--staged", "."],
            capture_output=True, text=True,
        )
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def get_logs(self, limit: int = 1000, branch: str = ""):
        # GitterLogger.log( f"**********************************\nGetting logs for branch {branch} at {self.repo}\n**********************************" )

        if self.repo is None:
            return "No repository initialized"

        args = ["git", "-C", self.repo, "log", "--decorate", "-n", f"{limit}"]
        if (branch != ""):
            args.append( branch)

        theLogs = subprocess.run( args, capture_output=True, text=True)

        # GitterLogger.log( f"Git logs: {theLogs.stdout}" )
        # GitterLogger.log( f"Git error: {theLogs.stderr}" )

        return GitLog.parse_logstring( theLogs.stdout )

