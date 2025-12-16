import pytest
from blogger.validation_utils import check_reorganization_integrity, normalize_and_split

class TestReorganizationIntegrity:
    """Group related tests for check_reorganization_integrity."""

    def test_valid_reorganization(self):
        """
        Tests a valid reorganization where draft_ok content is preserved
        and only outline headings are added.
        """
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
        assert is_valid is True, f"Validation failed unexpectedly: {error_msg}"
        assert error_msg == ""

    def test_lost_content(self):
        """
        Tests a scenario where some content from draft_ok is missing in
        the reorganized text.
        """
        draft_ok = "Intro content.\n\nSection A content.\n\nConclusion content."
        outline_text = "# Blog Title\n\n## Introduction\n\n## Section A\n\n## Conclusion"
        reorganized_text = (
            "# Blog Title\n\n## Introduction\nIntro content.\n\n"
            "## Conclusion\nConclusion content."
        ) # Missing "Section A content."
        is_valid, error_msg = check_reorganization_integrity(
            draft_ok, outline_text, reorganized_text
        )
        assert is_valid is False
        assert "Lost content: 2 paragraphs missing" in error_msg
        assert "'section a content.'" in error_msg.lower()

    def test_unauthorized_addition(self):
        """
        Tests a scenario where new content is added to the reorganized text
        that is not from draft_ok or outline.
        """
        draft_ok = "Intro content."
        outline_text = "## Introduction"
        reorganized_text = "## Introduction\nIntro content.\n\nUnauthorized new paragraph."
        is_valid, error_msg = check_reorganization_integrity(
            draft_ok, outline_text, reorganized_text
        )
        assert is_valid is False
        assert "Added content" in error_msg # Check for the presence of 'Added content' type error
        assert "unauthorized new paragraph" in error_msg.lower() # Check for the specific added content (case-insensitive)

    def test_valid_heading_variation(self):
        """
        Tests that outline headings, even with slight formatting variations
        (e.g., extra spaces, different case in outline vs reorganized),
        are correctly identified as authorized additions.
        """
        draft_ok = "Main point."
        outline_text = "# My Blog\n\n## Sub Heading"
        reorganized_text = "# My Blog\n\n## sub heading\nMain point." # 'sub heading' in reorganized
        is_valid, error_msg = check_reorganization_integrity(
            draft_ok, outline_text, reorganized_text
        )
        assert is_valid is True, f"Validation failed unexpectedly: {error_msg}"
        assert error_msg == ""

    def test_empty_inputs(self):
        """Tests handling of empty input strings."""
        is_valid, error_msg = check_reorganization_integrity("", "", "")
        assert is_valid is True
        assert error_msg == ""

        is_valid, error_msg = check_reorganization_integrity("Draft", "", "")
        assert is_valid is False
        assert "Lost content: 1 paragraphs missing" in error_msg

    def test_outline_with_descriptions(self):
        """
        Tests that descriptive text in the outline (which shouldn't appear in the
        final draft) does NOT trigger a 'Lost content' validation error.
        Only outline headings and draft content are required.
        """
        draft_ok = "Content A.\n\nContent B."
        # Outline has descriptions "Explain A..." and "Explain B..."
        outline_text = "# Title\n\n## Section A\nExplain A...\n\n## Section B\nExplain B..."
        
        # Reorganized text has headings + draft content, but NO outline descriptions
        reorganized_text = "# Title\n\n## Section A\nContent A.\n\n## Section B\nContent B."
        
        is_valid, error_msg = check_reorganization_integrity(
            draft_ok, outline_text, reorganized_text
        )
        assert is_valid is True, f"Validation failed: {error_msg}"
        assert error_msg == ""
