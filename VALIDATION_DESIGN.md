# Content Split Validation Design

## Problem Statement

When the LLM splits draft content into `draft_ok` (matches outline) and `draft_not_ok` (unused content), we need to ensure:

1. ❌ **No lost content** - All paragraphs from original draft exist in one of the split files
2. ❌ **No added content** - The LLM should copy-paste, not generate new text
3. ❌ **No duplicates** - Same paragraph shouldn't appear in both files
4. ✅ **Faithful redistribution** - Content is moved, not rewritten

## Solution: Content Integrity Check

### Implementation Location

**`blogger/validation_checkers.py` → `ContentSplitValidationChecker`**

**Why here?**
- ✅ Validation logic belongs in validators (not tools or sub-agents)
- ✅ Deterministic check (pure Python set operations)
- ✅ Fast execution (no LLM calls needed)
- ✅ Keeps all split validation in one place

### Algorithm

```
1. Normalize text (strip whitespace, lowercase)
2. Split into paragraphs (by \n\n or \n)
3. Create sets: raw_paragraphs, ok_paragraphs, not_ok_paragraphs
4. Check: raw_paragraphs ⊆ (ok_paragraphs ∪ not_ok_paragraphs)  [No lost content]
5. Check: (ok_paragraphs ∪ not_ok_paragraphs) ⊆ raw_paragraphs  [No added content]
6. Check: ok_paragraphs ∩ not_ok_paragraphs = ∅  [No duplicates]
```

### Code Structure

```python
class ContentSplitValidationChecker(BaseAgent):
    def _normalize_and_split(self, text: str) -> set[str]:
        """Split text into normalized paragraph set."""
        # Split by \n\n (paragraphs) or \n (lines)
        # Normalize: strip, lowercase, remove empty
        # Return set of normalized strings

    def _check_content_integrity(
        self, raw_draft: str, draft_ok: str, draft_not_ok: str
    ) -> tuple[bool, str]:
        """
        Validate content redistribution integrity.

        Returns:
            (is_valid, error_message) tuple
        """
        # Check 1: All raw content in split (no lost content)
        missing = raw_paragraphs - combined_paragraphs
        if missing:
            return False, "Lost content: X paragraphs missing"

        # Check 2: All split content in raw (no added content)
        added = combined_paragraphs - raw_paragraphs
        if added:
            return False, "Added content: X paragraphs not in original"

        # Check 3: No overlap between ok and not_ok
        overlap = ok_paragraphs & not_ok_paragraphs
        if overlap:
            return False, "Duplicate content: X paragraphs in both files"

        return True, ""

    async def _run_async_impl(self, ctx):
        # ... existing checks ...

        # Check length (±10%)
        length_ok = variance <= 0.10

        # Check content integrity
        integrity_ok, integrity_error = self._check_content_integrity(...)

        # Both must pass
        is_valid = length_ok and integrity_ok

        if is_valid:
            yield Event(actions=EventActions(escalate=True))
        else:
            # Report specific failures
            yield Event(content=f"Failed: {failures}")
```

## Validation Levels

| Check | Type | What It Catches | Example Failure |
|-------|------|-----------------|-----------------|
| **Existence** | Basic | Missing files | `draft_ok` not in state |
| **Length** | Quantitative | Major content loss/addition | 5000 chars → 2000 chars |
| **Integrity** | Structural | Paragraph-level changes | LLM rewrote a paragraph |

## Example Scenarios

### ✅ Valid Split
```
raw_draft = "Intro\n\nBody\n\nConclusion"
draft_ok = "Intro\n\nBody"
draft_not_ok = "Conclusion"

Result: ✅ All paragraphs accounted for, no overlap
```

### ❌ Lost Content
```
raw_draft = "Intro\n\nBody\n\nConclusion"
draft_ok = "Intro"
draft_not_ok = "Conclusion"

Result: ❌ Missing: "Body" paragraph
Error: "Lost content: 1 paragraphs missing from split (e.g., 'body')"
```

### ❌ Added Content (Hallucination)
```
raw_draft = "Intro\n\nBody"
draft_ok = "Intro\n\nBody\n\nExtra paragraph the LLM invented"
draft_not_ok = ""

Result: ❌ Added: "Extra paragraph..."
Error: "Added content: 1 paragraphs not in original (e.g., 'extra paragraph...')"
```

### ❌ Duplicate Content
```
raw_draft = "Intro\n\nBody\n\nConclusion"
draft_ok = "Intro\n\nBody"
draft_not_ok = "Body\n\nConclusion"

Result: ❌ Overlap: "Body" appears in both
Error: "Duplicate content: 1 paragraphs in both files (e.g., 'body')"
```

### ❌ Rewritten Content
```
raw_draft = "The quick brown fox jumps"
draft_ok = "A fast brown fox leaps"  # LLM paraphrased instead of copy-paste
draft_not_ok = ""

Result: ❌ Set mismatch detected
Error: "Lost content: 1 paragraphs missing; Added content: 1 paragraphs not in original"
```

## Trade-offs

### Paragraph-level vs. Sentence-level

**Current: Paragraph-level** (split by `\n\n` or `\n`)

**Pros:**
- ✅ Tolerates minor formatting changes (extra spaces)
- ✅ Fast comparison (fewer elements)
- ✅ Reasonable granularity for blog content

**Cons:**
- ⚠️ Won't catch intra-paragraph rewrites
- ⚠️ Depends on consistent paragraph formatting

**Alternative: Sentence-level** (split by `.` or `!` or `?`)

**Pros:**
- ✅ Finer-grained detection
- ✅ Catches more rewrites

**Cons:**
- ❌ Slower (more elements to compare)
- ❌ Brittle to punctuation changes
- ❌ May trigger false positives

**Decision: Start with paragraph-level, upgrade to sentence-level if needed.**

## Normalization Strategy

**Current normalization:**
```python
p.strip().lower()  # Remove whitespace, lowercase
```

**What this allows:**
- ✅ Whitespace differences (`"Intro"` == `"  Intro  "`)
- ✅ Case differences (`"INTRO"` == `"intro"`)

**What this catches:**
- ❌ Word changes (`"Intro"` != `"Introduction"`)
- ❌ Paraphrasing (`"The fox jumps"` != `"A fox leaps"`)

**Intentional strictness:** We want to catch any semantic changes, not just major rewrites.

## Performance Considerations

**Complexity:**
- Set operations: O(n) where n = number of paragraphs
- Typically: n < 100 for blog drafts
- **Fast enough for real-time validation**

**Memory:**
- 3 sets of strings (raw, ok, not_ok)
- Typical blog: ~50 paragraphs × ~200 chars = ~10KB
- **Negligible memory footprint**

## Error Messages

**Design principle:** Show what went wrong + sample of problematic content

```python
# ✅ Good error message
"Lost content: 3 paragraphs missing from split (e.g., 'body paragraph about...', 'another section...')"

# ❌ Bad error message
"Content validation failed"
```

**Why show samples:**
- Helps LLM understand what to fix
- Helps human debugging
- Truncate to 50 chars to avoid overwhelming output

## Future Enhancements

1. **Semantic similarity** (if paragraph-level is too strict)
   - Use embeddings to allow minor paraphrasing
   - Threshold: 95% similarity = same content

2. **Line-level tracking** (if paragraph-level is too coarse)
   - Split by `\n` instead of `\n\n`
   - More granular but slower

3. **Edit distance** (for fuzzy matching)
   - Allow small typo corrections
   - Levenshtein distance threshold

4. **LLM-based validation** (if deterministic fails)
   - Ask LLM: "Did you copy-paste or rewrite?"
   - Slower, non-deterministic, but handles edge cases

**For now: Start simple, iterate based on real failures.**

---

**Status:** ✅ Implemented in `blogger/validation_checkers.py`
**Testing:** Pending (will test with Task 2.1.2 step agents)
