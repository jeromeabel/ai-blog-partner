from blogger.text_utils import (
    check_content_integrity,
    check_heading_order,
    check_outline_structure,
    check_reorganization_integrity,
    normalize_and_split,
)


class TestNormalizeAndSplit:
    """Tests for normalize_and_split function."""

    def test_normalize_basic(self):
        text = "Intro\n\nBody\n\nConclusion"
        expected = {"intro", "body", "conclusion"}
        assert normalize_and_split(text) == expected


class TestContentIntegrity:
    """Tests for check_content_integrity function."""

    def test_valid_split(self):
        """Test that a valid content split passes validation."""
        raw_draft = "A\n\nB\n\nC"
        draft_ok = "A\n\nB"
        draft_not_ok = "C"

        is_valid, error_message = check_content_integrity(
            raw_draft, draft_ok, draft_not_ok
        )

        assert is_valid is True
        assert error_message == ""

    def test_lost_content(self):
        """Test that lost content is detected."""
        raw_draft = "A\n\nB\n\nC"
        draft_ok = "A"
        draft_not_ok = "C"

        is_valid, error_message = check_content_integrity(
            raw_draft, draft_ok, draft_not_ok
        )

        assert is_valid is False
        assert "Lost content" in error_message

    def test_extra_content(self):
        """Test that extra content is detected."""
        raw_draft = "A\n\nB\n\nC"
        draft_ok = "A\n\nB"
        draft_not_ok = "C\n\nD"

        is_valid, error_message = check_content_integrity(
            raw_draft, draft_ok, draft_not_ok
        )

        assert is_valid is False
        assert "Added content" in error_message


class TestReorganizationIntegrity:
    """Tests for check_reorganization_integrity function."""

    def test_valid_reorganization(self):
        """Test valid reorganization preserves content and adds outline headings."""
        draft_ok = "Intro content.\n\nSection A content.\n\nConclusion content."
        outline_text = "# Blog Title\n\n## Introduction\n\n## Section A\n\n## Conclusion"
        reorganized_text = (
            "# Blog Title\n\n## Introduction\nIntro content.\n\n"
            "## Section A\nSection A content.\n\n"
            "## Conclusion\nConclusion content."
        )

        is_valid, error_msg = check_reorganization_integrity(
            draft_ok, outline_text, reorganized_text
        )

        assert is_valid is True
        assert error_msg == ""

    def test_lost_content_in_reorganization(self):
        """Test that missing content is detected in reorganization."""
        draft_ok = "Intro content.\n\nSection A content.\n\nConclusion content."
        outline_text = "## Introduction\n## Section A\n## Conclusion"
        # Missing "Section A content"
        reorganized_text = "## Introduction\nIntro content.\n\n## Section A\n\n## Conclusion\nConclusion content."

        is_valid, error_msg = check_reorganization_integrity(
            draft_ok, outline_text, reorganized_text
        )

        assert is_valid is False
        assert "Lost content" in error_msg

    def test_unauthorized_addition(self):
        """Test that added content (not from draft or outline) is detected."""
        draft_ok = "Intro content.\n\nConclusion content."
        outline_text = "## Introduction\n## Conclusion"
        # Added "New stuff" that wasn't in draft or outline
        reorganized_text = "## Introduction\nIntro content.\n\nNew stuff\n\n## Conclusion\nConclusion content."

        is_valid, error_msg = check_reorganization_integrity(
            draft_ok, outline_text, reorganized_text
        )

        assert is_valid is False
        assert "Added content" in error_msg


class TestHeadingOrder:
    """Tests for check_heading_order function."""

    def test_valid_heading_order(self):
        """Test that correct heading order passes validation."""
        outline = "# Title\n\n## Intro\n\n## Body\n\n## Conclusion"
        reorganized = "# Title\n\n## Intro\nContent...\n\n## Body\nContent...\n\n## Conclusion\nContent..."

        is_valid, msg = check_heading_order(outline, reorganized)

        assert is_valid is True
        assert msg == ""

    def test_incorrect_heading_order(self):
        """Test that wrong heading order is detected."""
        outline = "# Title\n\n## Intro\n\n## Body\n\n## Conclusion"
        # Swapped Body and Intro
        reorganized = "# Title\n\n## Body\nContent...\n\n## Intro\nContent...\n\n## Conclusion"

        is_valid, msg = check_heading_order(outline, reorganized)

        assert is_valid is False
        assert "mismatch" in msg.lower() or "order" in msg.lower()

    def test_missing_heading(self):
        """Test that missing headings are detected."""
        outline = "# Title\n\n## Intro\n\n## Body\n\n## Conclusion"
        # Missing Body section
        reorganized = "# Title\n\n## Intro\nContent...\n\n## Conclusion"

        is_valid, msg = check_heading_order(outline, reorganized)

        assert is_valid is False
        assert "Missing heading" in msg or "missing" in msg.lower()

    def test_extra_heading(self):
        """Test that extra headings are detected."""
        outline = "# Title\n\n## Intro\n\n## Conclusion"
        # Added unexpected "Body" section
        reorganized = "# Title\n\n## Intro\nContent...\n\n## Body\nExtra...\n\n## Conclusion"

        is_valid, msg = check_heading_order(outline, reorganized)

        assert is_valid is False
        assert "Extra heading" in msg or "extra" in msg.lower()
