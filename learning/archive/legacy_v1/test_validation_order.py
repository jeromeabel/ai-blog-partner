from blogger.validation_utils import check_heading_order

class TestHeadingOrder:
    """Tests for checking heading order consistency."""

    def test_valid_order(self):
        """Headings match perfectly in order."""
        outline = "# Title\n\n## Intro\n\n## Body\n\n## Conclusion"
        reorganized = "# Title\n\n## Intro\nContent...\n\n## Body\nContent...\n\n## Conclusion\nContent..."
        is_valid, msg = check_heading_order(outline, reorganized)
        assert is_valid is True
        assert msg == ""

    def test_incorrect_order(self):
        """Headings are present but in wrong order."""
        outline = "# Title\n\n## Intro\n\n## Body\n\n## Conclusion"
        # Swapped Body and Intro
        reorganized = "# Title\n\n## Body\nContent...\n\n## Intro\nContent...\n\n## Conclusion"
        is_valid, msg = check_heading_order(outline, reorganized)
        assert is_valid is False
        assert "Heading order mismatch" in msg
        assert "expected '## intro'" in msg.lower()

    def test_missing_heading(self):
        """A required heading from outline is missing in reorganized text."""
        outline = "# Title\n\n## Intro\n\n## Body\n\n## Conclusion"
        reorganized = "# Title\n\n## Intro\nContent...\n\n## Conclusion" # Missing Body
        is_valid, msg = check_heading_order(outline, reorganized)
        assert is_valid is False
        assert "Missing heading" in msg
        assert "'## body'" in msg.lower()

    def test_extra_heading(self):
        """Reorganized text has an extra heading not in outline."""
        outline = "# Title\n\n## Intro\n\n## Conclusion"
        reorganized = "# Title\n\n## Intro\n\n## Surprise\n\n## Conclusion"
        is_valid, msg = check_heading_order(outline, reorganized)
        assert is_valid is False
        assert "Extra heading" in msg
        assert "'## surprise'" in msg.lower()

    def test_case_insensitive_match(self):
        """Headings should match even if casing differs slightly."""
        outline = "## Section One"
        reorganized = "## section ONE\nContent..."
        is_valid, msg = check_heading_order(outline, reorganized)
        assert is_valid is True
        assert msg == ""

    def test_ignores_lower_levels(self):
        """Should strictly check ## headings, potentially ignoring # or ### if desired.
        For this implementation, let's assume strict checking of all ## headings.
        """
        outline = "## Intro\n\n## Body"
        # Reorganized has ### sub-item which is fine, as long as ## order is kept
        reorganized = "## Intro\n\n### Sub-point\n\n## Body"
        is_valid, msg = check_heading_order(outline, reorganized)
        assert is_valid is True
