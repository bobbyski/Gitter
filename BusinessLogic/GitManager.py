
import subprocess

from model.GitLog import GitLog
from model.GitStatus import GitStatus


class GitManager:
    """Runs git CLI commands via subprocess for a given repository path."""

    def __init__(self, repo_path: str):
        """
        :param repo_path: Absolute path to the git repository.
        """
        self.repo = repo_path

    def get_status(self):
        """
        Returns the current working tree status as a GitStatus object.

        :returns: GitStatus with staged, unstaged, and untracked file lists,
                  or a string error message if no repository is set.
        """
        if self.repo is None:
            return "No repository initialized"

        theStatus = subprocess.run(["git", "-C", self.repo, "status"], capture_output=True, text=True)

        result = GitStatus()
        result.process_status_response(theStatus.stdout)

        return result

    def commit(self, message: str, add_unstaged: bool = False) -> tuple:
        """
        Creates a commit with the given message.

        :param message: The commit message.
        :param add_unstaged: If True, passes -a to also stage tracked modified files.
        :returns: (success, output) tuple where success is True if returncode == 0.
        """
        args = ["git", "-C", self.repo, "commit"]
        if add_unstaged:
            args.append("-a")
        args += ["-m", message]
        result = subprocess.run(args, capture_output=True, text=True)
        success = result.returncode == 0
        output = result.stdout.strip() or result.stderr.strip()
        return success, output

    def stage(self, filename: str) -> tuple:
        """
        Stages a single file.

        :param filename: Path to the file to stage, relative to the repository root.
        :returns: (success, output) tuple.
        """
        result = subprocess.run(
            ["git", "-C", self.repo, "add", filename],
            capture_output=True, text=True,
        )
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def stage_all(self) -> tuple:
        """
        Stages all changes in the repository (git add -A).

        :returns: (success, output) tuple.
        """
        result = subprocess.run(
            ["git", "-C", self.repo, "add", "-A"],
            capture_output=True, text=True,
        )
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def unstage(self, filename: str) -> tuple:
        """
        Unstages a single file, keeping working tree changes intact.

        :param filename: Path to the file to unstage, relative to the repository root.
        :returns: (success, output) tuple.
        """
        result = subprocess.run(
            ["git", "-C", self.repo, "restore", "--staged", filename],
            capture_output=True, text=True,
        )
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def unstage_all(self) -> tuple:
        """
        Unstages all staged changes, keeping working tree changes intact.

        :returns: (success, output) tuple.
        """
        result = subprocess.run(
            ["git", "-C", self.repo, "restore", "--staged", "."],
            capture_output=True, text=True,
        )
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def push(self, remote: str = "origin", branch: str = "") -> tuple:
        """
        Pushes commits to a remote repository.

        :param remote: The remote name to push to (default: "origin").
        :param branch: The branch to push. If empty, uses the current tracking branch.
        :returns: (success, output) tuple.
        """
        args = ["git", "-C", self.repo, "push", remote]
        if branch:
            args.append(branch)
        result = subprocess.run(args, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def pull(self, remote: str = "origin", branch: str = "") -> tuple:
        """
        Pulls and merges changes from a remote repository.

        :param remote: The remote name to pull from (default: "origin").
        :param branch: The branch to pull. If empty, uses the current tracking branch.
        :returns: (success, output) tuple.
        """
        args = ["git", "-C", self.repo, "pull", remote]
        if branch:
            args.append(branch)
        result = subprocess.run(args, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def fetch(self, remote: str = "origin", prune: bool = False) -> tuple:
        """
        Fetches changes from a remote without merging.

        :param remote: The remote name to fetch from (default: "origin").
        :param prune: If True, removes remote-tracking branches that no longer exist on the remote.
        :returns: (success, output) tuple.
        """
        args = ["git", "-C", self.repo, "fetch", remote]
        if prune:
            args.append("--prune")
        result = subprocess.run(args, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def _run(self, *args) -> tuple:
        """Run a single git command, returning (success, output)."""
        result = subprocess.run(
            ["git", "-C", self.repo] + list(args),
            capture_output=True, text=True,
        )
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()

    def _run_sequence(self, *commands) -> tuple:
        """Run a sequence of git command arg-lists, stopping on first failure."""
        output_lines = []
        for args in commands:
            success, output = self._run(*args)
            if output:
                output_lines.append(output)
            if not success:
                return False, "\n".join(output_lines)
        return True, "\n".join(output_lines)

    def flow_feature_start(self, name: str) -> tuple:
        """
        Starts a feature branch from develop: checkout develop, create feature/<name>.

        :param name: Feature branch name (without the feature/ prefix).
        :returns: (success, output) tuple.
        """
        safe_name = name.replace(" ", "_")
        return self._run_sequence(
            ["checkout", "develop"],
            ["checkout", "-b", f"feature/{safe_name}"],
        )

    def flow_feature_finish(self, name: str) -> tuple:
        """
        Finishes a feature branch: merge --no-ff into develop, delete the branch.

        :param name: Feature branch name (without the feature/ prefix).
        :returns: (success, output) tuple.
        """
        branch = f"feature/{name}"
        return self._run_sequence(
            ["checkout", "develop"],
            ["merge", "--no-ff", branch, "-m", f"Merge feature '{name}' into develop"],
            ["branch", "-d", branch],
        )

    def flow_release_start(self, version: str) -> tuple:
        """
        Starts a release branch from develop: checkout develop, create release/<version>.

        :param version: Release version string (e.g. "1.2.0").
        :returns: (success, output) tuple.
        """
        return self._run_sequence(
            ["checkout", "develop"],
            ["checkout", "-b", f"release/{version}"],
        )

    def _detect_main_branch(self) -> str:
        """Returns 'main' if it exists as a local branch, otherwise 'master'."""
        result = subprocess.run(
            ["git", "-C", self.repo, "show-ref", "--verify", "--quiet", "refs/heads/main"],
            capture_output=True, text=True,
        )
        return "main" if result.returncode == 0 else "master"

    def flow_release_finish(self, version: str) -> tuple:
        """
        Finishes a release branch: merge into main/master, tag, merge into develop, delete branch.

        :param version: Release version string (e.g. "1.2.0").
        :returns: (success, output) tuple.
        """
        main_branch = self._detect_main_branch()
        branch = f"release/{version}"
        return self._run_sequence(
            ["checkout", main_branch],
            ["merge", "--no-ff", branch, "-m", f"Release {version}"],
            ["tag", "-a", version, "-m", f"Release {version}"],
            ["checkout", "develop"],
            ["merge", "--no-ff", branch, "-m", f"Merge release '{version}' into develop"],
            ["branch", "-d", branch],
        )

    def get_logs(self, limit: int = 1000, branch: str = ""):
        """
        Returns parsed git log entries for the repository.

        :param limit: Maximum number of commits to retrieve (default: 1000).
        :param branch: Branch to retrieve logs for. If empty, uses the current branch.
        :returns: List of parsed GitLog entries.
        """
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
