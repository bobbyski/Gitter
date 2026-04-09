from __future__ import annotations

from textual import on, events
from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import Button, Label, Static
from textual.containers import Horizontal, Vertical, VerticalScroll

from BusinessLogic.GitManager import GitManager
from model.GitStatus import GitStatus


class GitStagingView(Static):
    """A reusable view showing staged and unstaged files with stage/unstage controls."""

    class StageAll(Message):
        pass

    class UnstageAll(Message):
        pass

    def __init__(self, git_status: GitStatus, repo_path: str, **kwargs):
        super().__init__(**kwargs)
        self._git_status = git_status
        self._repo_path = repo_path

    @staticmethod
    def _state_class(state: str) -> str:
        if state in ("new file",):
            return "staging_new"
        if state in ("modified",):
            return "staging_modified"
        if state in ("deleted",):
            return "staging_deleted"
        if state in ("renamed",):
            return "staging_renamed"
        if state in ("untracked",):
            return "staging_untracked"
        return "staging_other"

    def compose(self) -> ComposeResult:
        staged = self._git_status.stagedFiles if self._git_status else []
        unstaged = self._git_status.unstagedFiles if self._git_status else []
        untracked = self._git_status.filesUntracked if self._git_status else []

        with Vertical(id="staging_container"):
            with VerticalScroll(id="staged_box"):
                for f in staged:
                    row = Horizontal(
                        Label(f.state, classes=f"staging_state {self._state_class(f.state)}"),
                        Label(f.filename, classes="staging_filename"),
                        classes="staging_row",
                    )
                    row.data = ("staged", f.filename)
                    yield row

            with Horizontal(id="staging_buttons"):
                yield Button("↑  Stage all", id="btn_stage_all", variant="primary")
                yield Button("↓  Unstage all", id="btn_unstage_all", variant="default")

            with VerticalScroll(id="unstaged_box"):
                for f in unstaged:
                    row = Horizontal(
                        Label(f.state, classes=f"staging_state {self._state_class(f.state)}"),
                        Label(f.filename, classes="staging_filename"),
                        classes="staging_row",
                    )
                    row.data = ("unstaged", f.filename)
                    yield row
                for filename in untracked:
                    row = Horizontal(
                        Label("untracked", classes="staging_state staging_untracked"),
                        Label(filename, classes="staging_filename"),
                        classes="staging_row",
                    )
                    row.data = ("unstaged", filename)
                    yield row

    def on_mount(self) -> None:
        self.query_one("#staged_box").border_title = "Staged"
        self.query_one("#unstaged_box").border_title = "Unstaged"

    def _refresh_status(self) -> None:
        self._git_status = GitManager(self._repo_path).get_status()
        self.refresh(recompose=True)
        self.call_after_refresh(self._restore_titles)

    def _restore_titles(self) -> None:
        self.query_one("#staged_box").border_title = "Staged"
        self.query_one("#unstaged_box").border_title = "Unstaged"

    @on(events.Click)
    def handle_row_click(self, event: events.Click) -> None:
        if event.chain != 2:
            return
        widget = event.control
        while widget is not None and widget is not self:
            if hasattr(widget, "data"):
                section, filename = widget.data
                git = GitManager(self._repo_path)
                if section == "unstaged":
                    git.stage(filename)
                else:
                    git.unstage(filename)
                self._refresh_status()
                return
            widget = widget.parent

    @on(Button.Pressed, "#btn_stage_all")
    def handle_stage_all(self) -> None:
        GitManager(self._repo_path).stage_all()
        self._refresh_status()

    @on(Button.Pressed, "#btn_unstage_all")
    def handle_unstage_all(self) -> None:
        GitManager(self._repo_path).unstage_all()
        self._refresh_status()
