from unittest.mock import patch, MagicMock

from BusinessLogic.GitManager import GitManager


def _proc(returncode=0, stdout="", stderr=""):
    m = MagicMock()
    m.returncode = returncode
    m.stdout = stdout
    m.stderr = stderr
    return m


class TestGetStatus:
    def test_none_repo_returns_error_string(self):
        gm = GitManager(None)
        assert gm.get_status() == "No repository initialized"

    def test_calls_git_status_command(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(stdout="On branch develop\n")
            gm = GitManager("/some/path")
            gm.get_status()
            args = mock_run.call_args[0][0]
            assert "status" in args
            assert "/some/path" in args

    def test_returns_git_status_object(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(stdout="On branch develop\n")
            from model.GitStatus import GitStatus
            gm = GitManager("/some/path")
            result = gm.get_status()
            assert isinstance(result, GitStatus)


class TestGetLogs:
    def test_none_repo_returns_error_string(self):
        gm = GitManager(None)
        assert gm.get_logs() == "No repository initialized"

    def test_returns_list(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(stdout="")
            gm = GitManager("/repo")
            result = gm.get_logs()
            assert isinstance(result, list)

    def test_branch_arg_appended(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(stdout="")
            gm = GitManager("/repo")
            gm.get_logs(branch="develop")
            args = mock_run.call_args[0][0]
            assert "develop" in args

    def test_no_branch_arg_when_empty(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(stdout="")
            gm = GitManager("/repo")
            gm.get_logs(branch="")
            args = mock_run.call_args[0][0]
            # "develop" should not appear as a trailing positional arg
            assert args[-1] != "develop"


class TestCommit:
    def test_success_returns_true(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0, stdout="[develop abc] msg")
            gm = GitManager("/repo")
            ok, out = gm.commit("msg")
            assert ok is True
            assert "[develop abc] msg" in out

    def test_failure_returns_false(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=1, stderr="nothing to commit")
            gm = GitManager("/repo")
            ok, out = gm.commit("msg")
            assert ok is False
            assert "nothing to commit" in out

    def test_add_unstaged_includes_flag(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0, stdout="ok")
            gm = GitManager("/repo")
            gm.commit("msg", add_unstaged=True)
            assert "-a" in mock_run.call_args[0][0]

    def test_no_add_unstaged_omits_flag(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0, stdout="ok")
            gm = GitManager("/repo")
            gm.commit("msg", add_unstaged=False)
            assert "-a" not in mock_run.call_args[0][0]


class TestStage:
    def test_stage_single_file(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            ok, _ = gm.stage("file.py")
            assert ok is True
            args = mock_run.call_args[0][0]
            assert "add" in args
            assert "file.py" in args

    def test_stage_failure(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=1, stderr="pathspec error")
            gm = GitManager("/repo")
            ok, out = gm.stage("missing.py")
            assert ok is False
            assert "pathspec error" in out

    def test_stage_all_uses_dash_a(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            ok, _ = gm.stage_all()
            assert ok is True
            assert "-A" in mock_run.call_args[0][0]


class TestUnstage:
    def test_unstage_single_file(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            ok, _ = gm.unstage("file.py")
            assert ok is True
            args = mock_run.call_args[0][0]
            assert "restore" in args
            assert "--staged" in args
            assert "file.py" in args

    def test_unstage_all_uses_dot(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            ok, _ = gm.unstage_all()
            assert ok is True
            assert "." in mock_run.call_args[0][0]


class TestPush:
    def test_push_default_origin(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            ok, _ = gm.push()
            args = mock_run.call_args[0][0]
            assert "push" in args
            assert "origin" in args

    def test_push_with_branch(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            gm.push(branch="develop")
            assert "develop" in mock_run.call_args[0][0]

    def test_push_without_branch_omits_branch_arg(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            gm.push()
            # last arg should be "origin", not a branch name
            args = mock_run.call_args[0][0]
            assert args[-1] == "origin"


class TestPull:
    def test_pull_success(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0, stdout="Already up to date.")
            gm = GitManager("/repo")
            ok, out = gm.pull()
            assert ok is True
            assert "Already up to date." in out

    def test_pull_with_branch(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            gm.pull(branch="main")
            assert "main" in mock_run.call_args[0][0]


class TestFetch:
    def test_fetch_with_prune(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            gm.fetch(prune=True)
            assert "--prune" in mock_run.call_args[0][0]

    def test_fetch_without_prune(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            gm.fetch(prune=False)
            assert "--prune" not in mock_run.call_args[0][0]


class TestDetectMainBranch:
    def test_returns_main_when_ref_exists(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            assert gm._detect_main_branch() == "main"

    def test_returns_master_when_main_absent(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=1)
            gm = GitManager("/repo")
            assert gm._detect_main_branch() == "master"


class TestRunSequence:
    def test_stops_on_first_failure(self):
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                _proc(returncode=0, stdout="first ok"),
                _proc(returncode=1, stderr="second failed"),
                _proc(returncode=0, stdout="third ok"),
            ]
            gm = GitManager("/repo")
            ok, out = gm._run_sequence(["cmd1"], ["cmd2"], ["cmd3"])
            assert ok is False
            assert mock_run.call_count == 2

    def test_all_succeed(self):
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                _proc(returncode=0, stdout="a"),
                _proc(returncode=0, stdout="b"),
            ]
            gm = GitManager("/repo")
            ok, out = gm._run_sequence(["cmd1"], ["cmd2"])
            assert ok is True
            assert "a" in out
            assert "b" in out

    def test_output_from_failed_step_included(self):
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                _proc(returncode=0, stdout="step1 output"),
                _proc(returncode=1, stderr="step2 error"),
            ]
            gm = GitManager("/repo")
            ok, out = gm._run_sequence(["cmd1"], ["cmd2"])
            assert "step1 output" in out
            assert "step2 error" in out


class TestFlowFeatureStart:
    def test_spaces_replaced_with_underscores(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            gm.flow_feature_start("my feature name")
            calls = [c[0][0] for c in mock_run.call_args_list]
            assert any("feature/my_feature_name" in str(c) for c in calls)

    def test_checks_out_develop_first(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            gm.flow_feature_start("GIT-50_desc")
            first_call_args = mock_run.call_args_list[0][0][0]
            assert "checkout" in first_call_args
            assert "develop" in first_call_args

    def test_creates_feature_branch(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            gm.flow_feature_start("my-feature")
            second_call_args = mock_run.call_args_list[1][0][0]
            assert "feature/my-feature" in second_call_args


class TestFlowReleaseStart:
    def test_checks_out_develop_first(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            gm.flow_release_start("1.2.0")
            first_call_args = mock_run.call_args_list[0][0][0]
            assert "develop" in first_call_args

    def test_creates_release_branch(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _proc(returncode=0)
            gm = GitManager("/repo")
            gm.flow_release_start("1.2.0")
            second_call_args = mock_run.call_args_list[1][0][0]
            assert "release/1.2.0" in second_call_args
