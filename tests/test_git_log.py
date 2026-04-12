from model.GitLog import GitLog


SAMPLE_LOG = """\
commit abc123def456 (HEAD -> develop, origin/develop)
Author: John Doe <john@example.com>
Date:   Mon Jan 1 12:00:00 2024 +0000

    feat(GIT-10): add new feature

commit bcd234efg567 (tag: v1.0.0, tag: 1.0.0)
Author: Jane Smith <jane@example.com>
Date:   Sun Dec 31 10:00:00 2023 +0000

    Release 1.0.0

commit cde345fgh678
Author: John Doe <john@example.com>
Date:   Sat Dec 30 09:00:00 2023 +0000

    fix(GIT-9): fix a bug
"""


class TestParseLogstring:
    def test_empty_string_returns_empty_list(self):
        assert GitLog.parse_logstring("") == []

    def test_single_commit_fields(self):
        log = "commit abc123\nAuthor: A <a@b.com>\nDate:   Mon Jan 1 12:00:00 2024 +0000\n\n    my message\n"
        result = GitLog.parse_logstring(log)
        assert len(result) == 1
        assert result[0].commit == "abc123"
        assert result[0].message == "my message"
        assert result[0].author == "A <a@b.com>"
        assert result[0].date == "Mon Jan 1 12:00:00 2024 +0000"
        assert result[0].tags == []

    def test_multiple_commits_count(self):
        result = GitLog.parse_logstring(SAMPLE_LOG)
        assert len(result) == 3

    def test_version_tags_parsed(self):
        result = GitLog.parse_logstring(SAMPLE_LOG)
        tag_commit = result[1]
        assert "v1.0.0" in tag_commit.tags
        assert "1.0.0" in tag_commit.tags

    def test_head_ref_parsed(self):
        result = GitLog.parse_logstring(SAMPLE_LOG)
        assert "develop" in result[0].heads

    def test_remote_ref_parsed(self):
        result = GitLog.parse_logstring(SAMPLE_LOG)
        assert "origin/develop" in result[0].heads

    def test_multiline_message_joined(self):
        log = (
            "commit abc123\nAuthor: A <a@b.com>\nDate:   Mon Jan 1 12:00:00 2024 +0000\n\n"
            "    line one\n    line two\n"
        )
        result = GitLog.parse_logstring(log)
        assert result[0].message == "line one\nline two"

    def test_commit_hash_no_refs(self):
        result = GitLog.parse_logstring(SAMPLE_LOG)
        assert result[2].commit == "cde345fgh678"
        assert result[2].tags == []
        assert result[2].heads == []


class TestGetRelease:
    def test_v_prefixed_tag(self):
        log = GitLog()
        log.tags = ["v1.2.3"]
        log.date = "Mon Jan 1 12:00:00 2024 +0000"
        release = log.get_release()
        assert release is not None
        assert release.name == "v1.2.3"
        assert release.date == log.date

    def test_numeric_tag(self):
        log = GitLog()
        log.tags = ["1.2.3"]
        log.date = "Mon Jan 1 12:00:00 2024 +0000"
        release = log.get_release()
        assert release is not None
        assert release.name == "1.2.3"

    def test_rc_suffix_tag(self):
        log = GitLog()
        log.tags = ["1.2.3rc1"]
        log.date = "Mon Jan 1 12:00:00 2024 +0000"
        release = log.get_release()
        assert release is not None
        assert release.name == "1.2.3rc1"

    def test_beta_suffix_tag(self):
        log = GitLog()
        log.tags = ["2.0.0b2"]
        log.date = "Mon Jan 1 12:00:00 2024 +0000"
        release = log.get_release()
        assert release is not None
        assert release.name == "2.0.0b2"

    def test_no_tags_returns_none(self):
        log = GitLog()
        log.tags = []
        assert log.get_release() is None

    def test_non_version_tag_returns_none(self):
        log = GitLog()
        log.tags = ["latest", "HEAD"]
        assert log.get_release() is None

    def test_last_matching_tag_wins(self):
        log = GitLog()
        log.tags = ["v1.0.0", "v1.0.1"]
        log.date = ""
        release = log.get_release()
        assert release.name == "v1.0.1"


class TestGetIssue:
    def test_matches_prefix_with_hyphen(self):
        log = GitLog()
        log.message = "feat(GIT-42): add feature"
        assert log.get_issue(["GIT-"]) == "GIT-42"

    def test_matches_prefix_without_separator(self):
        log = GitLog()
        log.message = "fix GIT42 some bug"
        assert log.get_issue(["GIT"]) == "GIT42"

    def test_no_match_returns_none(self):
        log = GitLog()
        log.message = "chore: update deps"
        assert log.get_issue(["GIT-"]) is None

    def test_first_matching_prefix_wins(self):
        log = GitLog()
        log.message = "fix GIT-5: something"
        result = log.get_issue(["GIT-", "PROJ-"])
        assert result == "GIT-5"

    def test_second_prefix_matched_when_first_absent(self):
        log = GitLog()
        log.message = "fix PROJ-10: something else"
        result = log.get_issue(["GIT-", "PROJ-"])
        assert result == "PROJ-10"

    def test_empty_prefixes_returns_none(self):
        log = GitLog()
        log.message = "feat(GIT-1): something"
        assert log.get_issue([]) is None
