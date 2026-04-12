from model.GitStatus import GitStatus


CLEAN_STATUS = """\
On branch develop
Your branch is up to date with 'origin/develop'.

nothing to commit, working tree clean
"""

STAGED_STATUS = """\
On branch feature/my-branch
Changes to be committed:
\tnew file:   foo.py
\tmodified:   bar.py
\tdeleted:    baz.py

"""

UNSTAGED_STATUS = """\
On branch develop
Changes not staged for commit:
\tmodified:   README.md
\tdeleted:    old.py

"""

UNTRACKED_STATUS = """\
On branch develop
Untracked files:
\t(use "git add <file>..." to include in what will be committed)
\tnewfile.py

nothing added to commit but untracked files present
"""

MIXED_STATUS = """\
On branch feature/work
Changes to be committed:
\tnew file:   staged_new.py
\tmodified:   staged_mod.py

Changes not staged for commit:
\tmodified:   unstaged_mod.py

Untracked files:
\t(use "git add <file>..." to include in what will be committed)
\tuntracked.py

"""


class TestBranchParsing:
    def test_simple_branch(self):
        s = GitStatus()
        s.process_status_response(CLEAN_STATUS)
        assert s.branch == "develop"

    def test_feature_branch(self):
        s = GitStatus()
        s.process_status_response(STAGED_STATUS)
        assert s.branch == "feature/my-branch"


class TestStateParsing:
    def test_up_to_date_state(self):
        s = GitStatus()
        s.process_status_response(CLEAN_STATUS)
        assert s.state == "up to date"

    def test_no_state_when_absent(self):
        s = GitStatus()
        s.process_status_response(STAGED_STATUS)
        assert s.state == ""


class TestStagedFiles:
    def test_new_file_in_files_added(self):
        s = GitStatus()
        s.process_status_response(STAGED_STATUS)
        assert "foo.py" in s.filesAdded

    def test_modified_file_in_files_modified(self):
        s = GitStatus()
        s.process_status_response(STAGED_STATUS)
        assert "bar.py" in s.filesModified

    def test_deleted_file_in_files_deleted(self):
        s = GitStatus()
        s.process_status_response(STAGED_STATUS)
        assert "baz.py" in s.filesDeleted

    def test_staged_files_count(self):
        s = GitStatus()
        s.process_status_response(STAGED_STATUS)
        assert len(s.stagedFiles) == 3

    def test_staged_file_state_and_name(self):
        s = GitStatus()
        s.process_status_response(STAGED_STATUS)
        new_file = next(f for f in s.stagedFiles if f.filename == "foo.py")
        assert new_file.state == "new file"


class TestUnstagedFiles:
    def test_modified_in_files_modified(self):
        s = GitStatus()
        s.process_status_response(UNSTAGED_STATUS)
        assert "README.md" in s.filesModified

    def test_deleted_in_files_deleted(self):
        s = GitStatus()
        s.process_status_response(UNSTAGED_STATUS)
        assert "old.py" in s.filesDeleted

    def test_unstaged_files_count(self):
        s = GitStatus()
        s.process_status_response(UNSTAGED_STATUS)
        assert len(s.unstagedFiles) == 2


class TestUntrackedFiles:
    def test_untracked_file_found(self):
        s = GitStatus()
        s.process_status_response(UNTRACKED_STATUS)
        assert "newfile.py" in s.filesUntracked

    def test_hint_line_not_included(self):
        s = GitStatus()
        s.process_status_response(UNTRACKED_STATUS)
        assert not any(f.startswith("(") for f in s.filesUntracked)


class TestMixedStatus:
    def test_mixed_staged_and_unstaged(self):
        s = GitStatus()
        s.process_status_response(MIXED_STATUS)
        assert "staged_new.py" in s.filesAdded
        assert "staged_mod.py" in s.filesModified
        assert "unstaged_mod.py" in s.filesModified
        assert "untracked.py" in s.filesUntracked

    def test_staged_not_in_unstaged_list(self):
        s = GitStatus()
        s.process_status_response(MIXED_STATUS)
        unstaged_names = [f.filename for f in s.unstagedFiles]
        assert "staged_new.py" not in unstaged_names


class TestRepr:
    def test_repr_includes_branch(self):
        s = GitStatus()
        s.process_status_response(CLEAN_STATUS)
        assert "develop" in repr(s)

    def test_repr_includes_state(self):
        s = GitStatus()
        s.process_status_response(CLEAN_STATUS)
        assert "up to date" in repr(s)

    def test_repr_shows_counts(self):
        s = GitStatus()
        s.process_status_response(STAGED_STATUS)
        text = repr(s)
        assert "new:" in text or "mod:" in text or "del:" in text
