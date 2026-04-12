import re
from unittest.mock import patch, mock_open

from BusinessLogic.toml_helper import TomlHelper


class TestGetVersion:
    def test_returns_a_string(self):
        helper = TomlHelper()
        assert isinstance(helper.get_version(), str)

    def test_returns_non_empty(self):
        helper = TomlHelper()
        assert helper.get_version() != ""

    def test_reads_from_pyproject_toml(self):
        # pyproject.toml exists in dev environment — version should be semver-like
        helper = TomlHelper()
        version = helper.get_version()
        assert re.match(r"\d+\.\d+", version), f"Unexpected version format: {version}"

    def test_fallback_to_unknown_when_no_toml_and_no_package(self):
        # Patch Path.exists so the pyproject.toml fallback is skipped,
        # and patch the module-level `version` name so the metadata lookup fails.
        with patch("pathlib.Path.exists", return_value=False), \
             patch("BusinessLogic.toml_helper.version", side_effect=FileNotFoundError):
            helper = TomlHelper()
            result = helper.get_version()
            assert result == "unknown"

    def test_reads_version_line_from_toml_content(self):
        fake_toml = 'name = "gitterApp"\nversion = "9.9.9"\n'
        with patch("pathlib.Path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data=fake_toml)):
            helper = TomlHelper()
            assert helper.get_version() == "9.9.9"
