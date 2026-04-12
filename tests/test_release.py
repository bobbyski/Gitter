from model.Release import Release
from model.Issue import Issue


def _issue(number: str, title: str = "") -> Issue:
    i = Issue()
    i.number = number
    i.title = title
    return i


class TestHasIssue:
    def test_finds_existing_issue(self):
        r = Release()
        r.issues.append(_issue("GIT-1"))
        assert r.has_issue("GIT-1") is True

    def test_returns_false_for_absent_issue(self):
        r = Release()
        r.issues.append(_issue("GIT-1"))
        assert r.has_issue("GIT-2") is False

    def test_empty_issues_list(self):
        r = Release()
        assert r.has_issue("GIT-1") is False

    def test_multiple_issues_found(self):
        r = Release()
        r.issues = [_issue("GIT-1"), _issue("GIT-2"), _issue("GIT-3")]
        assert r.has_issue("GIT-2") is True
        assert r.has_issue("GIT-3") is True


class TestIssuesList:
    def test_returns_issue_numbers(self):
        r = Release()
        r.issues = [_issue("GIT-1"), _issue("GIT-2")]
        assert r.issues_list() == ["GIT-1", "GIT-2"]

    def test_empty_returns_empty_list(self):
        r = Release()
        assert r.issues_list() == []

    def test_order_preserved(self):
        r = Release()
        r.issues = [_issue("GIT-5"), _issue("GIT-1"), _issue("GIT-3")]
        assert r.issues_list() == ["GIT-5", "GIT-1", "GIT-3"]


class TestReleaseInit:
    def test_default_values(self):
        r = Release()
        assert r.name == ""
        assert r.date == ""
        assert r.issues == []
