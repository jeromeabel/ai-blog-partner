# Phase 2: The Curator - Learning Notes

**Date:** 2024-12-17
**Status:** In Progress 🚧 (Step 1 Complete)
**Reference:** `learning/plans/phase2_learning_guide.md`

---

## What I Built (So Far)

### ✅ Step 1: Validation Functions (Complete)
- **Extracted 5 validation functions** from `learning/archive/legacy_v1/validation_utils.py` to `blogger/text_utils.py`:
  1. `normalize_and_split()` - Split and normalize text for comparison
  2. `check_content_integrity()` - Validate content redistribution (no lost/added/duplicate content)
  3. `check_outline_structure()` - Validate outline has required structure
  4. `check_reorganization_integrity()` - Validate reorganization preserves content + only adds headings
  5. `check_heading_order()` - Validate heading order matches outline exactly

- **Created comprehensive test suite** in `tests/test_text_utils.py`:
  - 11 tests covering all critical validation scenarios
  - Tests for success cases AND error detection
  - 100% pass rate

---

## Key Learnings

### 1. Pure Validation Functions Pattern
**What I learned:**
- Validation functions should be **pure** (no LLM calls, no file I/O, just text processing)
- They belong in `text_utils.py` alongside other text utilities
- Pure functions are easy to test and reuse

**Why it matters:**
- Separates validation logic from tool implementation
- Makes debugging easier (can test validators independently)
- Reusable across different tools

**Example:**
```python
# GOOD: Pure function
def check_content_integrity(raw, ok, not_ok) -> tuple[bool, str]:
    # Just text comparison, returns (is_valid, error_msg)

# BAD: Mixed concerns
def check_content_integrity(blog_id):
    # Reads files, calls LLM, validates... too much!
```

---

### 2. Google ADK Sub-Agents Parameter
**What I learned:**
- The correct parameter is `sub_agents=` (NOT `agents=`)
- Sub-agents are collaborative partners the main agent can call
- Example: Architect calls Scribr to polish titles

**The Bug I Fixed:**
```python
# BEFORE (broken):
architect = Agent(
    ...,
    agents=[scribr],  # ❌ Wrong parameter name
)

# AFTER (fixed):
architect = Agent(
    ...,
    sub_agents=[scribr],  # ✅ Correct parameter name
)
```

**How to verify sub-agents work:**
```python
from blogger.step_agents.architect import architect
print(architect.sub_agents)  # Should show: [scribr]
```

---

### 3. Pytest Testing Patterns

#### A. The `self` Parameter
**What I learned:**
- `self` is required for methods in test classes
- It refers to the test instance (created by pytest)
- We usually don't use it - just local variables

**Example:**
```python
class TestContentIntegrity:
    def test_valid_split(self):  # ← self required by Python
        # Use local variables, not self:
        raw_draft = "A\n\nB\n\nC"  # ✅ Good
        self.raw_draft = "..."     # ❌ Unnecessary
```

#### B. String Assertion Patterns
**What I learned:**
- Use `in` for substring checks (NOT `.include()`)
- For error messages, check key phrases, not exact matches
- Empty strings for success cases

**Examples:**
```python
# Success case:
assert is_valid is True
assert error_message == ""  # ✅ Exact match for empty

# Error case - flexible checking:
assert is_valid is False
assert "Lost content" in error_message  # ✅ Key phrase
# NOT: assert error_message == "Lost content: B"  # ❌ Too brittle
```

#### C. Test Structure (AAA Pattern)
**What I learned:**
- **Arrange:** Set up test data
- **Act:** Call the function
- **Assert:** Check the result

**Example:**
```python
def test_valid_split(self):
    # ARRANGE: Set up test data
    raw_draft = "A\n\nB\n\nC"
    draft_ok = "A\n\nB"
    draft_not_ok = "C"

    # ACT: Call the function
    is_valid, error_message = check_content_integrity(
        raw_draft, draft_ok, draft_not_ok
    )

    # ASSERT: Check the result
    assert is_valid is True
    assert error_message == ""
```

---

### 4. Test-Driven Development (TDD)
**What I learned:**
- Write tests BEFORE moving to the next step
- Tests catch bugs early (found the architect sub_agents bug!)
- Tests document expected behavior

**The Workflow:**
1. Extract/write code
2. Write tests immediately
3. Fix any bugs found
4. Move to next step only when tests pass

**Why it matters:**
- Validates Step 1 was done correctly before Step 2
- Prevents compound bugs (bugs on top of bugs)
- Builds confidence in the foundation

---

## Challenges & Solutions

### Challenge 1: Import Error with Architect Agent
**Problem:**
```python
ValidationError: 1 validation error for LlmAgent
agents
  Extra inputs are not permitted
```

**Root cause:**
- Used `agents=` parameter instead of `sub_agents=`

**Solution:**
- Changed `agents=[scribr]` to `sub_agents=[scribr]` in `architect.py`

**Lesson:** Always check the framework's API documentation when parameters fail

---

### Challenge 2: Test File Location
**Problem:**
- Created test file in `blogger/tests/` instead of root `tests/`
- Import errors when running pytest

**Solution:**
- Moved test file to `tests/test_text_utils.py`
- Removed incorrect `blogger/tests/` directory

**Lesson:** Project structure matters - tests live at project root

---

### Challenge 3: Test Assertion Errors
**Problems:**
1. Used `error_message.include()` instead of `"text" in error_message`
2. Checked exact error messages instead of key phrases
3. Wrong assertion for valid split (checked for error instead of empty string)

**Solutions:**
1. Use Python's `in` operator for substring checks
2. Check for key phrases: `"Lost content" in error_message`
3. For valid cases: `assert error_message == ""`

**Lesson:**
- Error messages may change, test for meaning not exact wording
- Python strings use `in`, not `.include()`

---

## Testing Wins

### Test Coverage Achieved
- ✅ **11 tests** covering 4 validation functions
- ✅ **100% pass rate** on first full run (after fixes)
- ✅ Tests cover both **success** and **error** cases

### Critical Tests for Phase 2
1. **Content Integrity** - Ensures filter_scope_tool preserves all content
2. **Reorganization Integrity** - Ensures organize_content_tool doesn't lose/add content
3. **Heading Order** - Ensures organize_content_tool follows outline structure

These tests will validate Steps 2 & 3 when we implement them.

---

## Code Quality Insights

### What Makes Good Validation Functions?
1. **Pure functions** - no side effects, deterministic
2. **Clear return types** - `tuple[bool, str]` for (is_valid, error_message)
3. **Helpful error messages** - show examples of what's wrong
4. **Set operations** - use sets for efficient comparison (union, intersection, difference)

### Example from check_content_integrity:
```python
# Check for lost content
missing = raw_paragraphs - combined_paragraphs
if missing:
    sample = list(missing)[:2]  # Show examples
    sample_text = ", ".join([f"'{p[:50]}...'" for p in sample])
    return (False, f"Lost content: {len(missing)} paragraphs (e.g., {sample_text})")
```

**Why this is good:**
- Shows HOW MANY paragraphs lost
- Shows EXAMPLES of what's missing
- Truncates long paragraphs for readability

---

## Next Steps

### Immediate (Step 2):
- [ ] Implement `filter_scope_tool` - Use internal helper agent to split content
- [ ] Learn: How to create internal LLM helper agents in tools
- [ ] Challenge: Preserve ALL content during split (validation will catch mistakes!)

### After Step 2:
- [ ] Implement `organize_content_tool` - Reorganize content to match outline
- [ ] Implement `validate_with_llm_judge` - Semantic validation
- [ ] Create Curator agent
- [ ] Integration testing

---

## Patterns to Remember

### 1. Validation Function Pattern
```python
def check_something(input1, input2, output) -> tuple[bool, str]:
    """
    Check that output is valid given inputs.

    Returns:
        (is_valid, error_message)
        - is_valid: True if passes
        - error_message: "" if valid, descriptive error if invalid
    """
    # Normalize inputs
    # Check conditions
    # Return (True, "") or (False, "Error description")
```

### 2. Test Function Pattern
```python
def test_something(self):
    """Test description."""
    # ARRANGE: Setup
    input_data = "..."

    # ACT: Execute
    result = function_to_test(input_data)

    # ASSERT: Verify
    assert result == expected
```

### 3. Sub-Agent Pattern
```python
agent = Agent(
    name="main_agent",
    sub_agents=[helper_agent],  # NOT agents=
    tools=[...],
)
```

---

## Time Tracking

- **Step 1 (Validation Functions + Tests):** ~30 minutes
  - Extraction: 5 minutes
  - Test setup: 5 minutes
  - Writing 4 tests: 10 minutes
  - Debugging & fixes: 10 minutes

**Estimated total for Phase 2:** 2.5-4 hours (on track!)

---

## Reflections

### What Went Well
- ✅ Found and fixed the architect bug early
- ✅ Test-driven approach caught issues immediately
- ✅ Pure functions were easy to test
- ✅ Validation logic already tested in legacy (low risk extraction)

### What Was Challenging
- Understanding `sub_agents` vs `agents` parameter names
- Getting test assertions right on first try
- Understanding error message formats

### What I'd Do Differently
- Check ADK API docs BEFORE assuming parameter names
- Write one test at a time, run immediately (not batch)
- Read error messages more carefully (they often hint at the solution)

---

## Resources Used

- **Reference code:** `learning/archive/legacy_v1/validation_utils.py`
- **Reference tests:** `learning/archive/legacy_v1/test_validation_*.py`
- **Learning guide:** `learning/plans/phase2_learning_guide.md`
- **Design doc:** `learning/plans/phase2_curator.md`

---

**Status:** Ready for Step 2 - Building filter_scope_tool! 🚀
