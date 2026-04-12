from BusinessLogic.docs_helper import get_document


class TestGetDocument:
    def test_existing_doc_returns_content(self):
        content = get_document("help.md")
        assert content is not None
        assert len(content) > 0

    def test_missing_doc_returns_none(self):
        content = get_document("does_not_exist_xyz.md")
        assert content is None

    def test_tui_doc_readable(self):
        content = get_document("tui.md")
        assert content is not None

    def test_license_doc_readable(self):
        content = get_document("license.md")
        assert content is not None

    def test_add_doc_readable(self):
        content = get_document("add.md")
        assert content is not None

    def test_content_is_string(self):
        content = get_document("help.md")
        assert isinstance(content, str)
