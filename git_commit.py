from __future__ import annotations

from typing import Optional

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, Input, Label, Select, TextArea
from textual.containers import Horizontal, Vertical

from model.Project import Project


CommitResult = Optional[tuple]  # (message: str, add_unstaged: bool)


class GitCommitModal(ModalScreen[CommitResult]):
    """Modal for composing and submitting a git commit message.

    Dismisses with the commit message string on commit, or None on cancel.
    """

    def __init__(self, project: Project):
        super().__init__()
        self._project = project

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(f"Commit — {self._project.name}", id="commit_title"),
            Horizontal(
                Select(
                    [("feat", "feat"), ("fix", "fix"), ("chore", "chore"), ("spike", "spike")],
                    prompt="type",
                    id="commit_type",
                ),
                Input(placeholder="issue", id="commit_issue"),
                Input(placeholder="summary", id="commit_summary"),
                Checkbox("add unstaged", value=True, id="commit_add_unstaged"),
                id="commit_header_row",
            ),
            TextArea(id="commit_message"),
            Horizontal(
                Button("Cancel", variant="default", id="btn_cancel"),
                Button("Commit", variant="primary", id="btn_commit"),
                id="commit_button_row",
            ),
            id="commit_container",
        )

    def on_mount(self) -> None:
        self.query_one("#commit_summary", Input).focus()

    @on(Button.Pressed, "#btn_cancel")
    def handle_cancel(self) -> None:
        self.dismiss(None)

    @on(Button.Pressed, "#btn_commit")
    def handle_commit(self) -> None:
        commit_type = self.query_one("#commit_type", Select).value
        issue = self.query_one("#commit_issue", Input).value.strip()
        summary = self.query_one("#commit_summary", Input).value.strip()
        body = self.query_one("#commit_message", TextArea).text.strip()

        parts = []
        if commit_type and commit_type is not Select.BLANK:
            parts.append(f"{commit_type}")
        if issue:
            parts.append(issue)
        if summary:
            parts.append(summary)

        first_line = " ".join(parts)
        if not first_line:
            return

        add_unstaged = self.query_one("#commit_add_unstaged", Checkbox).value
        message = f"{first_line}\n\n{body}".strip() if body else first_line
        self.dismiss((message, add_unstaged))
