"""
Unit tests for Phase 2 validation tools.

These tests verify that the validation tool wrappers return the correct
dict structure for use by the Curator agent.
"""

from blogger.utils.tools import (
    validate_content_split_tool,
    validate_organization_tool,
)


class TestValidateContentSplitTool:
    """Tests for validate_content_split_tool wrapper."""

    def test_valid_split_returns_success(self):
        """Should return success dict when split is valid."""
        original = "A\n\nB\n\nC"
        part1 = "A\n\nB"
        part2 = "C"

        result = validate_content_split_tool(original, part1, part2)

        assert result["status"] == "success"
        assert result["valid"] is True
        assert "valid" in result["message"].lower()
        assert "preserved" in result["message"].lower()

    def test_valid_split_all_in_part1(self):
        """Should pass when all content goes to part1."""
        original = "A\n\nB\n\nC"
        part1 = "A\n\nB\n\nC"
        part2 = ""

        result = validate_content_split_tool(original, part1, part2)

        assert result["status"] == "success"
        assert result["valid"] is True

    def test_valid_split_all_in_part2(self):
        """Should pass when all content goes to part2."""
        original = "A\n\nB\n\nC"
        part1 = ""
        part2 = "A\n\nB\n\nC"

        result = validate_content_split_tool(original, part1, part2)

        assert result["status"] == "success"
        assert result["valid"] is True

    def test_lost_content_returns_error(self):
        """Should return error dict when content is lost."""
        original = "A\n\nB\n\nC"
        part1 = "A"
        part2 = "C"  # B is missing

        result = validate_content_split_tool(original, part1, part2)

        assert result["status"] == "error"
        assert result["valid"] is False
        assert "lost content" in result["message"].lower()
        assert "1 paragraphs" in result["message"].lower()

    def test_added_content_returns_error(self):
        """Should return error dict when content is added."""
        original = "A\n\nB"
        part1 = "A\n\nB\n\nHallucination"
        part2 = ""

        result = validate_content_split_tool(original, part1, part2)

        assert result["status"] == "error"
        assert result["valid"] is False
        assert "added content" in result["message"].lower()

    def test_duplicate_content_returns_error(self):
        """Should return error dict when content appears in both parts."""
        original = "A\n\nB\n\nC"
        part1 = "A\n\nB"
        part2 = "B\n\nC"  # B duplicated

        result = validate_content_split_tool(original, part1, part2)

        assert result["status"] == "error"
        assert result["valid"] is False
        assert "duplicate content" in result["message"].lower()

    def test_empty_inputs(self):
        """Should handle empty inputs gracefully."""
        original = ""
        part1 = ""
        part2 = ""

        result = validate_content_split_tool(original, part1, part2)

        assert result["status"] == "success"
        assert result["valid"] is True

    def test_whitespace_tolerance(self):
        """Should tolerate whitespace differences."""
        original = "  A  \n\n  B  "
        part1 = "A"
        part2 = "B"

        result = validate_content_split_tool(original, part1, part2)

        assert result["status"] == "success"
        assert result["valid"] is True

    def test_case_tolerance(self):
        """Should tolerate case differences."""
        original = "HELLO\n\nWORLD"
        part1 = "hello"
        part2 = "world"

        result = validate_content_split_tool(original, part1, part2)

        assert result["status"] == "success"
        assert result["valid"] is True


class TestValidateOrganizationTool:
    """Tests for validate_organization_tool wrapper."""

    def test_valid_organization_returns_success(self):
        """Should return success dict when organization is valid."""
        draft_ok = "Intro content.\n\nBody content.\n\nConclusion content."
        outline = "# Title\n\n## Introduction\n\n## Body\n\n## Conclusion"
        organized = (
            "# Title\n\n"
            "## Introduction\n\nIntro content.\n\n"
            "## Body\n\nBody content.\n\n"
            "## Conclusion\n\nConclusion content."
        )

        result = validate_organization_tool(draft_ok, outline, organized)

        assert result["status"] == "success"
        assert result["valid"] is True
        assert result["checks"]["integrity"] is True
        assert result["checks"]["heading_order"] is True
        assert "valid" in result["message"].lower()

    def test_lost_content_returns_error(self):
        """Should return error dict when content is lost during reorganization."""
        draft_ok = "Intro content.\n\nBody content.\n\nConclusion content."
        outline = "# Title\n\n## Introduction\n\n## Body\n\n## Conclusion"
        organized = (
            "# Title\n\n"
            "## Introduction\n\nIntro content.\n\n"
            "## Body\n\n"  # Body content missing
            "## Conclusion\n\nConclusion content."
        )

        result = validate_organization_tool(draft_ok, outline, organized)

        assert result["status"] == "error"
        assert result["valid"] is False
        assert result["checks"]["integrity"] is False
        assert "integrity" in result["errors"][0].lower()
        assert "lost content" in result["message"].lower()

    def test_wrong_heading_order_returns_error(self):
        """Should return error dict when heading order is wrong."""
        draft_ok = "Intro content.\n\nBody content.\n\nConclusion content."
        outline = "# Title\n\n## Introduction\n\n## Body\n\n## Conclusion"
        organized = (
            "# Title\n\n"
            "## Body\n\nBody content.\n\n"  # Wrong order!
            "## Introduction\n\nIntro content.\n\n"
            "## Conclusion\n\nConclusion content."
        )

        result = validate_organization_tool(draft_ok, outline, organized)

        assert result["status"] == "error"
        assert result["valid"] is False
        assert result["checks"]["heading_order"] is False
        assert "heading order" in result["errors"][0].lower()

    def test_missing_heading_returns_error(self):
        """Should return error dict when outline heading is missing."""
        draft_ok = "Intro content.\n\nConclusion content."
        outline = "# Title\n\n## Introduction\n\n## Body\n\n## Conclusion"
        organized = (
            "# Title\n\n"
            "## Introduction\n\nIntro content.\n\n"
            # Body section missing
            "## Conclusion\n\nConclusion content."
        )

        result = validate_organization_tool(draft_ok, outline, organized)

        assert result["status"] == "error"
        assert result["valid"] is False
        assert result["checks"]["heading_order"] is False
        assert "missing heading" in result["message"].lower()

    def test_extra_heading_returns_error(self):
        """Should return error dict when extra heading not in outline."""
        draft_ok = "Intro content.\n\nConclusion content."
        outline = "# Title\n\n## Introduction\n\n## Conclusion"
        organized = (
            "# Title\n\n"
            "## Introduction\n\nIntro content.\n\n"
            "## Extra Section\n\nExtra content.\n\n"  # Not in outline!
            "## Conclusion\n\nConclusion content."
        )

        result = validate_organization_tool(draft_ok, outline, organized)

        assert result["status"] == "error"
        assert result["valid"] is False
        assert result["checks"]["heading_order"] is False
        assert "extra heading" in result["message"].lower()

    def test_both_checks_fail(self):
        """Should return error with both checks failing."""
        draft_ok = "Intro content.\n\nBody content.\n\nConclusion content."
        outline = "# Title\n\n## Introduction\n\n## Body\n\n## Conclusion"
        organized = (
            "# Title\n\n"
            "## Body\n\nBody content.\n\n"  # Wrong order
            "## Introduction\n\n"  # Missing intro content
            "## Conclusion\n\nConclusion content."
        )

        result = validate_organization_tool(draft_ok, outline, organized)

        assert result["status"] == "error"
        assert result["valid"] is False
        # At least one check should fail (could be both)
        assert (
            result["checks"]["integrity"] is False
            or result["checks"]["heading_order"] is False
        )
        assert len(result["errors"]) >= 1

    def test_valid_with_empty_sections(self):
        """Should pass when sections have no content yet (just headings)."""
        draft_ok = "Intro content."
        outline = "# Title\n\n## Introduction\n\n## Body\n\n## Conclusion"
        organized = (
            "# Title\n\n"
            "## Introduction\n\nIntro content.\n\n"
            "## Body\n\n"  # Empty is okay
            "## Conclusion"  # Empty is okay
        )

        result = validate_organization_tool(draft_ok, outline, organized)

        assert result["status"] == "success"
        assert result["valid"] is True
        assert result["checks"]["integrity"] is True
        assert result["checks"]["heading_order"] is True

    def test_unauthorized_content_addition(self):
        """Should detect when new content is added (not from draft or outline)."""
        draft_ok = "Intro content.\n\nConclusion content."
        outline = "# Title\n\n## Introduction\n\n## Conclusion"
        organized = (
            "# Title\n\n"
            "## Introduction\n\nIntro content.\n\n"
            "Unauthorized new paragraph.\n\n"  # Not in draft or outline!
            "## Conclusion\n\nConclusion content."
        )

        result = validate_organization_tool(draft_ok, outline, organized)

        assert result["status"] == "error"
        assert result["valid"] is False
        assert result["checks"]["integrity"] is False
        assert "added content" in result["message"].lower()

    def test_realistic_blog_organization(self):
        """Test with realistic blog post content."""
        draft_ok = """
## Introduction
This is my intro about AI.

## The Problem
AI is complex and hard to understand.

## My Solution
I created a framework to simplify it.

## Conclusion
This approach works well.
"""

        outline = """
# My AI Journey

## Introduction
Brief intro to the topic

## The Problem
What challenges exist

## My Solution
How I solved it

## Conclusion
Final thoughts
"""

        organized = """
# My AI Journey

## Introduction
This is my intro about AI.

## The Problem
AI is complex and hard to understand.

## My Solution
I created a framework to simplify it.

## Conclusion
This approach works well.
"""

        result = validate_organization_tool(draft_ok, outline, organized)

        assert result["status"] == "success"
        assert result["valid"] is True
        assert result["checks"]["integrity"] is True
        assert result["checks"]["heading_order"] is True
