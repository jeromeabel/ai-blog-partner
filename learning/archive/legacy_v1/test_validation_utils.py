"""
Unit tests for blogger.validation_utils

These tests verify the validation utility functions work correctly
before they're integrated into validation checker agents.
"""

import pytest
from blogger.validation_utils import (
    normalize_and_split,
    check_content_integrity,
    check_outline_structure,
)


class TestNormalizeAndSplit:
    """Test normalize_and_split function."""

    def test_splits_by_double_newline(self):
        """Should split paragraphs by double newline."""
        text = "Intro\n\nBody\n\nConclusion"
        result = normalize_and_split(text)
        assert result == {"intro", "body", "conclusion"}

    def test_falls_back_to_single_newline(self):
        """Should split by single newline if no double newlines."""
        text = "Intro\nBody\nConclusion"
        result = normalize_and_split(text)
        assert result == {"intro", "body", "conclusion"}

    def test_strips_whitespace(self):
        """Should strip leading/trailing whitespace."""
        text = "  Intro  \n\n  Body  "
        result = normalize_and_split(text)
        assert result == {"intro", "body"}

    def test_lowercases(self):
        """Should convert to lowercase."""
        text = "INTRO\n\nBODY"
        result = normalize_and_split(text)
        assert result == {"intro", "body"}

    def test_removes_empty_paragraphs(self):
        """Should remove empty strings."""
        text = "Intro\n\n\n\nBody"
        result = normalize_and_split(text)
        assert result == {"intro", "body"}

    def test_empty_string(self):
        """Should return empty set for empty input."""
        result = normalize_and_split("")
        assert result == set()

    def test_complex_markdown(self):
        """Should handle markdown formatting."""
        text = "## Introduction\n\nSome text here.\n\n## Body\n\nMore text."
        result = normalize_and_split(text)
        assert "## introduction" in result
        assert "some text here." in result
        assert "## body" in result
        assert "more text." in result


class TestCheckContentIntegrity:
    """Test check_content_integrity function."""

    def test_valid_split(self):
        """Should pass when all content accounted for."""
        raw = "Intro\n\nBody\n\nConclusion"
        ok = "Intro\n\nBody"
        not_ok = "Conclusion"

        is_valid, error = check_content_integrity(raw, ok, not_ok)
        assert is_valid is True
        assert error == ""

    def test_valid_split_all_in_ok(self):
        """Should pass when all content matches outline."""
        raw = "Intro\n\nBody"
        ok = "Intro\n\nBody"
        not_ok = ""

        is_valid, error = check_content_integrity(raw, ok, not_ok)
        assert is_valid is True
        assert error == ""

    def test_valid_split_all_in_not_ok(self):
        """Should pass when all content is unused."""
        raw = "Unused1\n\nUnused2"
        ok = ""
        not_ok = "Unused1\n\nUnused2"

        is_valid, error = check_content_integrity(raw, ok, not_ok)
        assert is_valid is True
        assert error == ""

    def test_detects_lost_content(self):
        """Should fail when content is missing."""
        raw = "Intro\n\nBody\n\nConclusion"
        ok = "Intro"
        not_ok = "Conclusion"

        is_valid, error = check_content_integrity(raw, ok, not_ok)
        assert is_valid is False
        assert "Lost content" in error
        assert "1 paragraphs" in error
        assert "'body'" in error.lower()

    def test_detects_multiple_lost_paragraphs(self):
        """Should detect when multiple paragraphs are missing."""
        raw = "A\n\nB\n\nC\n\nD"
        ok = "A"
        not_ok = "D"

        is_valid, error = check_content_integrity(raw, ok, not_ok)
        assert is_valid is False
        assert "Lost content" in error
        assert "2 paragraphs" in error

    def test_detects_added_content(self):
        """Should fail when LLM adds new content."""
        raw = "Intro\n\nBody"
        ok = "Intro\n\nBody\n\nHallucination"
        not_ok = ""

        is_valid, error = check_content_integrity(raw, ok, not_ok)
        assert is_valid is False
        assert "Added content" in error
        assert "1 paragraphs" in error
        assert "'hallucination'" in error.lower()

    def test_detects_duplicates(self):
        """Should fail when same content in both files."""
        raw = "Intro\n\nBody\n\nConclusion"
        ok = "Intro\n\nBody"
        not_ok = "Body\n\nConclusion"

        is_valid, error = check_content_integrity(raw, ok, not_ok)
        assert is_valid is False
        assert "Duplicate content" in error
        assert "1 paragraphs" in error
        assert "'body'" in error.lower()

    def test_detects_rewritten_content(self):
        """Should fail when LLM paraphrases instead of copy-paste."""
        raw = "The quick brown fox jumps over the lazy dog"
        ok = "A fast brown fox leaps over the sleeping dog"
        not_ok = ""

        is_valid, error = check_content_integrity(raw, ok, not_ok)
        assert is_valid is False
        # Should detect both lost (original) and added (paraphrased)
        assert "Lost content" in error or "Added content" in error

    def test_handles_empty_raw_draft(self):
        """Should handle edge case of empty raw draft."""
        raw = ""
        ok = ""
        not_ok = ""

        is_valid, error = check_content_integrity(raw, ok, not_ok)
        # Empty everything is technically valid (nothing to validate)
        assert is_valid is True

    def test_handles_whitespace_differences(self):
        """Should tolerate whitespace differences."""
        raw = "  Intro  \n\n  Body  "
        ok = "Intro"
        not_ok = "Body"

        is_valid, error = check_content_integrity(raw, ok, not_ok)
        assert is_valid is True
        assert error == ""

    def test_handles_case_differences(self):
        """Should tolerate case differences."""
        raw = "INTRO\n\nBODY"
        ok = "intro"
        not_ok = "body"

        is_valid, error = check_content_integrity(raw, ok, not_ok)
        assert is_valid is True
        assert error == ""


class TestCheckOutlineStructure:
    """Test check_outline_structure function."""

    def test_valid_outline(self):
        """Should pass for valid outline with all requirements."""
        outline = "# Title\n\n## Introduction\n\n## Body\n\n## Conclusion"

        is_valid, reasons = check_outline_structure(outline)
        assert is_valid is True
        assert reasons == []

    def test_valid_outline_extra_sections(self):
        """Should pass when there are more than 3 sections."""
        outline = "# Title\n\n## Introduction\n\n## Section 1\n\n## Section 2\n\n## Conclusion"

        is_valid, reasons = check_outline_structure(outline)
        assert is_valid is True
        assert reasons == []

    def test_empty_outline(self):
        """Should fail for empty outline."""
        outline = ""

        is_valid, reasons = check_outline_structure(outline)
        assert is_valid is False
        assert "outline is empty" in reasons

    def test_too_few_sections(self):
        """Should fail when fewer than 3 sections."""
        outline = "# Title\n\n## Introduction"

        is_valid, reasons = check_outline_structure(outline)
        assert is_valid is False
        assert any("only 1 sections" in r for r in reasons)

    def test_missing_introduction(self):
        """Should fail when Introduction section is missing."""
        outline = "# Title\n\n## Body\n\n## Summary\n\n## Conclusion"

        is_valid, reasons = check_outline_structure(outline)
        assert is_valid is False
        assert "missing Introduction section" in reasons

    def test_missing_conclusion(self):
        """Should fail when Conclusion section is missing."""
        outline = "# Title\n\n## Introduction\n\n## Body\n\n## Summary"

        is_valid, reasons = check_outline_structure(outline)
        assert is_valid is False
        assert "missing Conclusion section" in reasons

    def test_multiple_failures(self):
        """Should report all failures."""
        outline = "# Title\n\n## Body"

        is_valid, reasons = check_outline_structure(outline)
        assert is_valid is False
        assert len(reasons) == 3  # Too few, no intro, no conclusion
        assert any("only 1 sections" in r for r in reasons)
        assert "missing Introduction section" in reasons
        assert "missing Conclusion section" in reasons

    def test_case_insensitive_section_matching(self):
        """Should match sections case-insensitively."""
        outline = "# Title\n\n## INTRODUCTION\n\n## Body\n\n## CONCLUSION"

        is_valid, reasons = check_outline_structure(outline)
        assert is_valid is True
        assert reasons == []

    def test_partial_section_name_match(self):
        """Should match partial section names (e.g., 'intro' in 'Introduction')."""
        outline = "# Title\n\n## Introductory Remarks\n\n## Body\n\n## Concluding Thoughts"

        is_valid, reasons = check_outline_structure(outline)
        assert is_valid is True
        assert reasons == []

    def test_single_level_headings_ignored(self):
        """Should only count ## headings, not # headings."""
        outline = "# Title\n\n# Another Title\n\n## Introduction\n\n## Body\n\n## Conclusion"

        is_valid, reasons = check_outline_structure(outline)
        assert is_valid is True  # Only ## headings count
        assert reasons == []


# Integration tests (combining multiple functions)
class TestIntegration:
    """Test how functions work together."""

    def test_realistic_blog_workflow(self):
        """Test with realistic blog content."""
        raw_draft = """
## Introduction

This is my intro paragraph about AI agents.

## Main Content

Here I talk about LLMs and their capabilities.

## Conclusion

Summary of key points.
"""

        # Simulate agent splitting the draft
        draft_ok = """
## Introduction

This is my intro paragraph about AI agents.

## Main Content

Here I talk about LLMs and their capabilities.
"""

        draft_not_ok = """
## Conclusion

Summary of key points.
"""

        # Check integrity
        is_valid, error = check_content_integrity(raw_draft, draft_ok, draft_not_ok)
        assert is_valid is True
        assert error == ""

        # Check outline structure
        outline = "# AI Agents\n\n## Introduction\n\n## Main Content\n\n## Conclusion"
        is_valid, reasons = check_outline_structure(outline)
        assert is_valid is True
        assert reasons == []
