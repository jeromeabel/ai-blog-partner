"""
Unit tests for blogger.tools module.

Tests focus on filter_scope_tool and other Phase 2 tools.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from blogger.tools import filter_scope_tool, _llm_filter_content


class TestLLMFilterContent:
    """Tests for _llm_filter_content internal helper."""

    @patch("blogger.tools.genai.Client")
    def test_successful_filtering(self, mock_client_class):
        """Test that LLM successfully filters content into in-scope and out-of-scope."""
        # Mock the LLM response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = """
---IN-SCOPE---
This is in-scope content.
Another in-scope paragraph.

---OUT-OF-SCOPE---
This is out-of-scope content.
"""
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        draft = "This is in-scope content.\n\nAnother in-scope paragraph.\n\nThis is out-of-scope content."
        outline = "## Introduction\n\n## Body"

        result = _llm_filter_content(draft, outline)

        assert result["status"] == "success"
        assert "This is in-scope content" in result["draft_ok"]
        assert "This is out-of-scope content" in result["draft_not_ok"]

    @patch("blogger.tools.genai.Client")
    def test_missing_sections_in_response(self, mock_client_class):
        """Test that malformed LLM responses are caught."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Just some random text without proper sections"
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        draft = "Some content"
        outline = "## Introduction"

        result = _llm_filter_content(draft, outline)

        assert result["status"] == "error"
        assert "missing required sections" in result["message"]

    @patch("blogger.tools.genai.Client")
    def test_llm_api_error(self, mock_client_class):
        """Test that LLM API errors are handled gracefully."""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Error")
        mock_client_class.return_value = mock_client

        draft = "Some content"
        outline = "## Introduction"

        result = _llm_filter_content(draft, outline)

        assert result["status"] == "error"
        assert "LLM filtering failed" in result["message"]


class TestFilterScopeTool:
    """Tests for filter_scope_tool function."""

    @pytest.fixture
    def temp_blog_structure(self):
        """Create a temporary blog structure for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            blog_id = "test-blog"

            # Create input directory with draft.md
            input_dir = tmpdir / "inputs" / blog_id
            input_dir.mkdir(parents=True)
            draft_path = input_dir / "draft.md"
            draft_path.write_text("Draft intro.\n\nDraft body.\n\nDraft conclusion.")

            # Create output directory with outline.md
            output_dir = tmpdir / "outputs" / blog_id
            output_dir.mkdir(parents=True)
            outline_path = output_dir / "outline.md"
            outline_path.write_text("## Introduction\n\n## Body\n\n## Conclusion")

            # Patch the INPUTS_DIR and OUTPUTS_DIR in the tools module
            with patch("blogger.tools.INPUTS_DIR", tmpdir / "inputs"), \
                 patch("blogger.tools.OUTPUTS_DIR", tmpdir / "outputs"):
                yield {
                    "blog_id": blog_id,
                    "tmpdir": tmpdir,
                    "draft_path": draft_path,
                    "outline_path": outline_path,
                    "output_dir": output_dir,
                }

    def test_missing_draft_file(self):
        """Test error when draft.md doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            with patch("blogger.tools.INPUTS_DIR", tmpdir / "inputs"), \
                 patch("blogger.tools.OUTPUTS_DIR", tmpdir / "outputs"):
                result = filter_scope_tool("nonexistent-blog")

                assert result["status"] == "error"
                assert "Draft file not found" in result["message"]

    def test_missing_outline_file(self, temp_blog_structure):
        """Test error when outline.md doesn't exist."""
        # Remove the outline file
        temp_blog_structure["outline_path"].unlink()

        result = filter_scope_tool(temp_blog_structure["blog_id"])

        assert result["status"] == "error"
        assert "Outline file not found" in result["message"]
        assert "Run Step 1" in result["message"]

    @patch("blogger.tools._llm_filter_content")
    def test_llm_filtering_error(self, mock_llm_filter, temp_blog_structure):
        """Test that LLM errors are propagated."""
        mock_llm_filter.return_value = {
            "status": "error",
            "message": "LLM API error"
        }

        result = filter_scope_tool(temp_blog_structure["blog_id"])

        assert result["status"] == "error"
        assert result["message"] == "LLM API error"

    @patch("blogger.tools._llm_filter_content")
    def test_content_integrity_failure(self, mock_llm_filter, temp_blog_structure):
        """Test that content integrity validation catches rewritten content."""
        # Mock LLM to return content that doesn't match the draft (missing content)
        mock_llm_filter.return_value = {
            "status": "success",
            "draft_ok": "Draft intro.",  # Missing "Draft body" and "Draft conclusion"
            "draft_not_ok": ""
        }

        result = filter_scope_tool(temp_blog_structure["blog_id"])

        assert result["status"] == "error"
        assert "Content integrity check failed" in result["message"]

    @patch("blogger.tools._llm_filter_content")
    def test_successful_filtering(self, mock_llm_filter, temp_blog_structure):
        """Test successful content filtering with valid integrity."""
        # Mock LLM to return valid split content
        mock_llm_filter.return_value = {
            "status": "success",
            "draft_ok": "Draft intro.\n\nDraft body.",
            "draft_not_ok": "Draft conclusion."
        }

        result = filter_scope_tool(temp_blog_structure["blog_id"])

        assert result["status"] == "success"
        assert result["blog_id"] == temp_blog_structure["blog_id"]
        assert "draft_ok_path" in result
        assert "draft_not_ok_path" in result
        assert result["ok_count"] == 2  # Two paragraphs in draft_ok
        assert result["not_ok_count"] == 1  # One paragraph in draft_not_ok

        # Verify files were created
        draft_ok_path = temp_blog_structure["output_dir"] / "draft_ok.md"
        draft_not_ok_path = temp_blog_structure["output_dir"] / "draft_not_ok.md"
        assert draft_ok_path.exists()
        assert draft_not_ok_path.exists()
        assert "Draft intro" in draft_ok_path.read_text()
        assert "Draft conclusion" in draft_not_ok_path.read_text()
