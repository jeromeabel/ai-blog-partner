"""
Text processing utilities for blog content manipulation.

Pure functions for splitting, normalizing, and matching text content.
"""

from difflib import SequenceMatcher


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison.

    Args:
        text: Text to normalize

    Returns:
        Normalized text (lowercase, stripped)
    """
    return text.strip().lower()


def extract_headings(text: str, level: int = 2) -> list[dict]:
    """
    Extract markdown headings from text.

    Args:
        text: Markdown text
        level: Heading level to extract (2 for ##, 1 for #)

    Returns:
        List of dicts with keys: 'title', 'level', 'line_num'

    Example:
        >>> text = "# Title\\n\\n## Introduction\\n\\nSome text\\n\\n## Body"
        >>> extract_headings(text, level=2)
        [{'title': 'Introduction', 'level': 2, 'line_num': 2},
         {'title': 'Body', 'level': 2, 'line_num': 6}]
    """
    prefix = '#' * level + ' '
    headings = []

    for line_num, line in enumerate(text.split('\n')):
        if line.startswith(prefix):
            title = line[len(prefix):].strip()
            headings.append({
                'title': title,
                'level': level,
                'line_num': line_num
            })

    return headings


def fuzzy_match_score(text1: str, text2: str) -> float:
    """
    Calculate fuzzy match score between two strings.

    Uses difflib.SequenceMatcher for similarity calculation.

    Args:
        text1: First text
        text2: Second text

    Returns:
        Similarity score between 0.0 and 1.0
    """
    normalized1 = normalize_text(text1)
    normalized2 = normalize_text(text2)
    return SequenceMatcher(None, normalized1, normalized2).ratio()


def find_best_heading_match(
    search_heading: str,
    draft_headings: list[dict],
    threshold: float = 0.6
) -> dict | None:
    """
    Find the best matching heading in draft for a given outline heading.

    Args:
        search_heading: Heading from outline
        draft_headings: List of heading dicts from draft (from extract_headings)
        threshold: Minimum similarity score (0.0-1.0)

    Returns:
        Best matching heading dict or None if no match above threshold
    """
    best_match = None
    best_score = threshold

    for draft_heading in draft_headings:
        score = fuzzy_match_score(search_heading, draft_heading['title'])
        if score > best_score:
            best_score = score
            best_match = draft_heading

    return best_match


def split_text_by_headings(text: str, heading_positions: list[int]) -> list[str]:
    """
    Split text into chunks based on heading line numbers.

    Args:
        text: Full text to split
        heading_positions: List of line numbers where sections start

    Returns:
        List of text chunks

    Example:
        >>> text = "Line 0\\nLine 1\\nLine 2\\nLine 3\\nLine 4"
        >>> split_text_by_headings(text, [1, 3])
        ['Line 0', 'Line 1\\nLine 2', 'Line 3\\nLine 4']
    """
    lines = text.split('\n')
    chunks = []

    # Add sentinel at end for easier iteration
    positions = sorted(heading_positions) + [len(lines)]

    # First chunk is everything before first heading
    if positions[0] > 0:
        chunks.append('\n'.join(lines[0:positions[0]]))

    # Split between headings
    for i in range(len(positions) - 1):
        start = positions[i]
        end = positions[i + 1]
        chunks.append('\n'.join(lines[start:end]))

    return chunks


# ============================================================================
# Validation Functions (extracted from legacy_v1/validation_utils.py)
# ============================================================================


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

    # Split by single newlines, then normalize each non-empty line
    lines = text.split("\n")
    normalized = {line.strip().lower() for line in lines if line.strip()}
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

    # Check 5: Has conclusion (check for "conclus", "conclud", "wrap", "summary", "final" to match all variants)
    conclusion_keywords = ["conclus", "conclud", "wrap", "summary", "final", "takeaway"]
    has_conclusion = any(
        any(keyword in s.lower() for keyword in conclusion_keywords) for s in sections
    )
    if not has_conclusion:
        reasons.append(f"missing Conclusion section (looked for: {', '.join(conclusion_keywords)})")

    is_valid = len(reasons) == 0
    return is_valid, reasons


def check_reorganization_integrity(
    draft_ok: str, outline_text: str, reorganized_text: str
) -> tuple[bool, str]:
    """
    Check that reorganized content preserves draft content and only adds outline headings.

    Validates:
    1. All paragraphs from draft_ok exist in reorganized_text (no lost content)
    2. Any content in reorganized_text NOT in draft_ok must exist in outline_text (only headings added)

    Args:
        draft_ok: Content matching outline (source)
        outline_text: The outline containing allowed headings
        reorganized_text: The reorganized content

    Returns:
        (is_valid, error_message) tuple
        - is_valid: True if all checks pass
        - error_message: Empty string if valid, descriptive error if invalid

    Examples:
        >>> # Valid: reorganized contains draft + outline heading
        >>> check_reorganization_integrity("Content", "# Title", "# Title\\n\\nContent")
        (True, '')

        >>> # Lost content
        >>> check_reorganization_integrity("Content", "# Title", "# Title")
        (False, "Lost content: 1 paragraphs missing (e.g., 'content')")

        >>> # Unauthorized addition
        >>> check_reorganization_integrity("Content", "# Title", "# Title\\n\\nContent\\n\\nNew stuff")
        (False, "Added content: 1 paragraphs not in draft or outline (e.g., 'new stuff')")
    """
    # 1. Normalize and split all texts
    draft_paragraphs = normalize_and_split(draft_ok)

    # Only consider HEADINGS from the outline as authorized/expected content.
    # Ignore descriptions/body text within the outline.
    outline_lines = outline_text.split('\n')
    outline_paragraphs = {
        line.strip().lower()
        for line in outline_lines
        if line.strip().startswith('#')
    }

    reorganized_paragraphs = normalize_and_split(reorganized_text)

    # 2. Define Expected Content: Union of draft content and outline headings
    expected_paragraphs = draft_paragraphs | outline_paragraphs

    # 3. Check for Lost Content: Ensure all expected paragraphs exist in reorganized
    missing_content = expected_paragraphs - reorganized_paragraphs
    if missing_content:
        sample = list(missing_content)[:2]
        sample_text = ", ".join(
            [f"'{p[:50]}...'" if len(p) > 50 else f"'{p}'" for p in sample]
        )
        return (
            False,
            f"Lost content: {len(missing_content)} paragraphs missing (e.g., {sample_text})",
        )

    # 4. Check for Unauthorized Additions: Identify paragraphs in reorganized not in expected
    added_content = reorganized_paragraphs - expected_paragraphs
    if added_content:
        sample = list(added_content)[:2]
        sample_text = ", ".join(
            [f"'{p[:50]}...'" if len(p) > 50 else f"'{p}'" for p in sample]
        )
        return (
            False,
            f"Added content: {len(added_content)} paragraphs not in draft or outline (e.g., {sample_text})",
        )

    return True, ""


def check_heading_order(outline_text: str, reorganized_text: str) -> tuple[bool, str]:
    """
    Check if Level 2 headings (##) in reorganized text match the order in the outline.

    Args:
        outline_text: The source outline
        reorganized_text: The reorganized content

    Returns:
        (is_valid, error_message)
    """
    def extract_headings(text: str) -> list[str]:
        return [
            line.strip().lower()
            for line in text.split("\n")
            if line.strip().startswith("## ")
        ]

    outline_headings = extract_headings(outline_text)
    reorg_headings = extract_headings(reorganized_text)

    # 1. Check for exact match first
    if outline_headings == reorg_headings:
        return True, ""

    # 2. Check for missing headings
    outline_set = set(outline_headings)
    reorg_set = set(reorg_headings)

    missing = outline_set - reorg_set
    if missing:
        # Sort for deterministic error message
        sample = sorted(list(missing))[0]
        return False, f"Missing heading: '{sample}' found in outline but not in reorganized text"

    # 3. Check for extra headings
    extra = reorg_set - outline_set
    if extra:
        sample = sorted(list(extra))[0]
        return False, f"Extra heading: '{sample}' found in reorganized text but not in outline"

    # 4. If sets match but order differs
    for i, (out_h, reorg_h) in enumerate(zip(outline_headings, reorg_headings)):
        if out_h != reorg_h:
            return False, f"Heading order mismatch at #{i+1}: expected '{out_h}', found '{reorg_h}'"

    return True, ""
