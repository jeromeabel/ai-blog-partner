"""
AI Blog Partner - Validation Utilities

Pure functions for content validation logic.
These are extracted from validators to enable easy unit testing.
"""


def normalize_and_split(text: str) -> set[str]:
    """
    Split text into normalized paragraphs for comparison.

    Normalizes by:
    - Stripping whitespace
    - Converting to lowercase
    - Splitting by double newlines (paragraphs) or single newlines (lines)

    Args:
        text: The text to split and normalize

    Returns:
        Set of normalized paragraphs/lines (empty strings removed)

    Examples:
        >>> normalize_and_split("Intro\\n\\nBody\\n\\nConclusion")
        {'intro', 'body', 'conclusion'}

        >>> normalize_and_split("  INTRO  \\n\\n  Body  ")
        {'intro', 'body'}

        >>> normalize_and_split("")
        set()
    """
    if not text:
        return set()

    # Split by paragraphs (double newline) or lines (single newline)
    # Try paragraph split first
    paragraphs = text.split("\n\n")
    if len(paragraphs) == 1:
        # No paragraph breaks, split by lines
        paragraphs = text.split("\n")

    # Normalize: strip whitespace, lowercase, remove empty
    normalized = {p.strip().lower() for p in paragraphs if p.strip()}
    return normalized


def check_content_integrity(
    raw_draft: str, draft_ok: str, draft_not_ok: str
) -> tuple[bool, str]:
    """
    Check that content was redistributed, not rewritten or lost.

    Validates:
    1. All paragraphs from raw_draft exist in draft_ok OR draft_not_ok (no lost content)
    2. All paragraphs from combined split exist in raw_draft (no added content)
    3. No overlap between draft_ok and draft_not_ok (no duplicates)

    Args:
        raw_draft: Original draft content
        draft_ok: Content matching outline
        draft_not_ok: Content not matching outline

    Returns:
        (is_valid, error_message) tuple
        - is_valid: True if all checks pass
        - error_message: Empty string if valid, descriptive error if invalid

    Examples:
        >>> # Valid split
        >>> check_content_integrity("A\\n\\nB\\n\\nC", "A\\n\\nB", "C")
        (True, '')

        >>> # Lost content
        >>> check_content_integrity("A\\n\\nB\\n\\nC", "A", "C")
        (False, "Lost content: 1 paragraphs missing from split (e.g., 'b')")

        >>> # Added content
        >>> check_content_integrity("A\\n\\nB", "A\\n\\nB\\n\\nX", "")
        (False, "Added content: 1 paragraphs not in original (e.g., 'x')")

        >>> # Duplicate content
        >>> check_content_integrity("A\\n\\nB\\n\\nC", "A\\n\\nB", "B\\n\\nC")
        (False, "Duplicate content: 1 paragraphs in both files (e.g., 'b')")
    """
    # Normalize and split all texts
    raw_paragraphs = normalize_and_split(raw_draft)
    ok_paragraphs = normalize_and_split(draft_ok)
    not_ok_paragraphs = normalize_and_split(draft_not_ok)
    combined_paragraphs = ok_paragraphs | not_ok_paragraphs  # Union

    # Check 1: All raw content exists in split (no lost content)
    missing_from_split = raw_paragraphs - combined_paragraphs
    if missing_from_split:
        # Show first few missing paragraphs (truncated)
        sample = list(missing_from_split)[:2]
        sample_text = ", ".join(
            [f"'{p[:50]}...'" if len(p) > 50 else f"'{p}'" for p in sample]
        )
        return (
            False,
            f"Lost content: {len(missing_from_split)} paragraphs missing from split (e.g., {sample_text})",
        )

    # Check 2: All split content exists in raw (no added content)
    added_to_split = combined_paragraphs - raw_paragraphs
    if added_to_split:
        # Show first few added paragraphs (truncated)
        sample = list(added_to_split)[:2]
        sample_text = ", ".join(
            [f"'{p[:50]}...'" if len(p) > 50 else f"'{p}'" for p in sample]
        )
        return (
            False,
            f"Added content: {len(added_to_split)} paragraphs not in original (e.g., {sample_text})",
        )

    # Check 3: Ensure draft_ok and draft_not_ok don't overlap (no duplicates)
    overlap = ok_paragraphs & not_ok_paragraphs
    if overlap:
        sample = list(overlap)[:2]
        sample_text = ", ".join(
            [f"'{p[:50]}...'" if len(p) > 50 else f"'{p}'" for p in sample]
        )
        return (
            False,
            f"Duplicate content: {len(overlap)} paragraphs in both files (e.g., {sample_text})",
        )

    return True, ""


def check_outline_structure(outline_text: str) -> tuple[bool, list[str]]:
    """
    Check if outline has required structure and sections.

    Validates:
    - Outline is not empty
    - Has at least 3 sections (## markdown headings)
    - Contains "Introduction" section
    - Contains "Conclusion" section

    Args:
        outline_text: The outline markdown text

    Returns:
        (is_valid, reasons) tuple
        - is_valid: True if all checks pass
        - reasons: List of failure reasons (empty if valid)

    Examples:
        >>> outline = "# Title\\n\\n## Introduction\\n\\n## Body\\n\\n## Conclusion"
        >>> check_outline_structure(outline)
        (True, [])

        >>> outline = "# Title\\n\\n## Introduction"
        >>> is_valid, reasons = check_outline_structure(outline)
        >>> is_valid
        False
        >>> "only 1 sections (need 3+)" in reasons
        True
    """
    reasons = []

    # Check 1: Not empty
    if not outline_text:
        reasons.append("outline is empty")
        return False, reasons

    # Check 2: Extract sections (lines starting with "## ")
    sections = [line for line in outline_text.split("\n") if line.startswith("## ")]
    num_sections = len(sections)

    # Check 3: At least 3 sections
    if num_sections < 3:
        reasons.append(f"only {num_sections} sections (need 3+)")

    # Check 4: Has introduction
    has_intro = any("intro" in s.lower() for s in sections)
    if not has_intro:
        reasons.append("missing Introduction section")

    # Check 5: Has conclusion (check for "conclus" or "conclud" to match all variants)
    has_conclusion = any(
        "conclus" in s.lower() or "conclud" in s.lower() for s in sections
    )
    if not has_conclusion:
        reasons.append("missing Conclusion section")

    is_valid = len(reasons) == 0
    return is_valid, reasons
