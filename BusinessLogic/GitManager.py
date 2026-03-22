
import subprocess

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

    def get_logs(self, limit: int = 1000, branch: str = "master"):
        pass


