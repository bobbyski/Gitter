from __future__ import annotations

import re
from typing import Optional

import gitStatus
from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, Input, Label, Select, TextArea
from textual.containers import Horizontal, Vertical

from git_staging import GitStagingView
from model.Project import Project


CommitResult = Optional[tuple]  # (message: str, add_unstaged: bool)


class GitCommitModal(ModalScreen[CommitResult]):
    """Modal for composing and submitting a git commit message.

    Dismisses with the commit message string on commit, or None on cancel.
    """

    def __init__(self, project: Project):
        super().__init__()
        self._project = project
        self.border_title = "Commit"
        self.commitType = "feat"
        self.commitIssue = ""
        self.commitSummary = ""

        if project is not None and project.status is not None:
            self.setupDefaults()

    def setupDefaults( self ):
        elements = self._project.status.branch.split("/")

        if len(elements) > 1:
            type = elements[0].lower()
            if type == "feature" or type == "feat":
                self.commitType = "feat"
            elif type == "bugfix" or type == "fix":
                self.commitType = "fix"
            elif type == "chore":
                self.commitType = "chore"
            elif type == "spike":
                self.commitType = "spike"
            else:
                self.commitType = "feat"

            last = elements[-1]
            issue_match = re.search(r"([A-Za-z]+-\d+)", last)
            if issue_match:
                self.commitIssue = issue_match.group(1)
                after = last[issue_match.end():]
                after = re.sub(r"^[^A-Za-z0-9]+", "", after)
                after = re.sub(r"[^A-Za-z0-9]+$", "", after)
                self.commitSummary = after.replace("_", " ").replace("-", " ")


    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(f"Commit — {self._project.name}", id="commit_title"),
            Horizontal(
                Vertical(


                    Horizontal(
                        Vertical(
                            Horizontal(
                                Select([("feat", "feat"), ("fix", "fix"), ("chore", "chore"), ("spike", "spike")],
                                       value=self.commitType,
                                       prompt="type",
                                       id="commit_type"),

                                Input(value=self.commitIssue, placeholder="issue", id="commit_issue"),
                                Input(value=self.commitSummary, placeholder="summary", id="commit_summary"),
                                Checkbox("add unstaged", value=False, id="commit_add_unstaged"),
                                id="commit_header_row"),
                            TextArea(id="commit_message"), id="commit_message_container"
                        ),
                        GitStagingView(git_status=self._project.status, repo_path=self._project.directory), id="main_commit_container")
                )
            ),
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
            parts.append( f"({issue})")
        if summary:
            parts.append(f": {summary}")

        first_line = "".join(parts)
        if not first_line:
            return

        add_unstaged = self.query_one("#commit_add_unstaged", Checkbox).value
        message = f"{first_line}\n\n{body}".strip() if body else first_line
        self.dismiss((message, add_unstaged))
