from model.Project import Project
from model.GitLog import GitLog
from model.Issue import Issue
from model.Release import Release


def _project(name="TestProject", issue_prefixes=None) -> Project:
    """Build a Project instance without hitting git."""
    p = Project.__new__(Project)
    p.name = name
    p.directory = "/nonexistent"
    p.status = None
    p.tagBranch = ""
    p.issuePrefixes = issue_prefixes or ["GIT-"]
    p.prPatterns = []
    p.favorite = False
    p.groups = []
    p.commits = []
    p.issues = []
    p.releases = []
    return p


def _log(message: str, tags=None) -> GitLog:
    log = GitLog()
    log.message = message
    log.tags = tags or []
    log.commit = "abc123"
    log.date = "Mon Jan 1 12:00:00 2024 +0000"
    return log


class TestStripIssue:
    def test_strips_issue_from_conventional_commit(self):
        p = _project()
        result = p.strip_issue("GIT-5", "feat(GIT-5): add something")
        assert result == "add something"

    def test_strips_issue_at_start(self):
        p = _project()
        result = p.strip_issue("GIT-5", "GIT-5 some title")
        assert result == "some title"

    def test_leading_punctuation_removed(self):
        p = _project()
        result = p.strip_issue("GIT-5", "fix: GIT-5 - the bug")
        # leading non-alnum chars stripped
        assert result[0].isalnum()

    def test_returns_longest_segment(self):
        p = _project()
        # "short" vs "this is the longer segment"
        result = p.strip_issue("GIT-5", "short GIT-5 this is the longer segment")
        assert result == "this is the longer segment"


class TestProcessCommits:
    def test_always_creates_next_release(self):
        p = _project()
        p.process_commits()
        assert len(p.releases) == 1
        assert p.releases[0].name == "Next release"

    def test_issue_goes_into_next_release(self):
        p = _project()
        p.commits = [_log("feat(GIT-1): new thing")]
        p.process_commits()
        assert any(i.number == "GIT-1" for i in p.releases[0].issues)

    def test_tagged_commit_creates_new_release(self):
        p = _project()
        p.commits = [
            _log("feat(GIT-2): after tag"),
            _log("Release 1.0.0", tags=["v1.0.0"]),
            _log("fix(GIT-1): before tag"),
        ]
        p.process_commits()
        names = [r.name for r in p.releases]
        assert "Next release" in names
        assert "v1.0.0" in names

    def test_issue_before_tag_goes_into_tagged_release(self):
        p = _project()
        p.commits = [
            _log("Release 1.0.0", tags=["v1.0.0"]),
            _log("fix(GIT-1): fix in 1.0.0"),
        ]
        p.process_commits()
        release = next(r for r in p.releases if r.name == "v1.0.0")
        assert any(i.number == "GIT-1" for i in release.issues)

    def test_duplicate_issue_not_added_twice(self):
        p = _project()
        p.commits = [
            _log("feat(GIT-1): feature"),
            _log("fix(GIT-1): also references GIT-1"),
        ]
        p.process_commits()
        count = sum(1 for i in p.releases[0].issues if i.number == "GIT-1")
        assert count == 1

    def test_commit_without_issue_ignored(self):
        p = _project()
        p.commits = [_log("chore: update deps")]
        p.process_commits()
        assert p.releases[0].issues == []


class TestCurrentRelease:
    def test_returns_first_tagged_release(self):
        p = _project()
        p.commits = [_log("Release 1.0.0", tags=["v1.0.0"])]
        p.process_commits()
        assert p.current_release() == "v1.0.0"

    def test_returns_empty_when_no_tags(self):
        p = _project()
        p.process_commits()
        assert p.current_release() == ""

    def test_skips_next_release_entry(self):
        p = _project()
        p.commits = [_log("Release 2.0.0", tags=["v2.0.0"])]
        p.process_commits()
        assert p.current_release() != "Next release"


class TestReleaseSummary:
    def test_shows_release_with_pending_issues(self):
        p = _project()
        p.commits = [
            _log("feat(GIT-2): pending feature"),
            _log("Release 1.0.0", tags=["v1.0.0"]),
        ]
        p.process_commits()
        summary = p.release_summary()
        assert "v1.0.0" in summary
        assert "1 issue" in summary

    def test_plural_issues(self):
        p = _project()
        p.commits = [
            _log("feat(GIT-2): thing one"),
            _log("feat(GIT-3): thing two"),
            _log("Release 1.0.0", tags=["v1.0.0"]),
        ]
        p.process_commits()
        assert "issues" in p.release_summary()

    def test_empty_when_no_releases_and_no_issues(self):
        p = _project()
        p.process_commits()
        assert p.release_summary() == ""


class TestReleaseNotesMarkdown:
    def test_contains_project_name(self):
        p = _project(name="MyRepo")
        p.process_commits()
        assert "MyRepo" in p.release_notes_markdown()

    def test_contains_issue_number(self):
        p = _project()
        p.commits = [_log("feat(GIT-7): my feature")]
        p.process_commits()
        assert "GIT-7" in p.release_notes_markdown()

    def test_no_issues_returns_only_header(self):
        p = _project()
        # no commits → no issues → only the header line is generated
        p.process_commits()
        notes = p.release_notes_markdown()
        assert "TestProject" in notes
        assert "GIT-" not in notes

    def test_filter_by_release_name(self):
        p = _project()
        # commits are processed in order: GIT-3 arrives before the v1.0.0 tag
        # so it lands in "Next release"; GIT-1 arrives after, landing in v1.0.0
        p.commits = [
            _log("fix(GIT-3): in next release"),
            _log("Release 1.0.0", tags=["v1.0.0"]),
            _log("fix(GIT-1): in 1.0"),
            _log("Release 2.0.0", tags=["v2.0.0"]),
        ]
        p.process_commits()
        notes = p.release_notes_markdown(release_name="v1.0.0")
        assert "GIT-1" in notes
        assert "GIT-3" not in notes
