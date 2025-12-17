# Phase 2: The Curator - Design Document

**Status:** Planning Complete - Ready for Implementation
**Date:** 2024-12-17
**Agent:** The Curator
**Goal:** Filter in-scope content and organize to match outline structure

---

## 🎯 Overview

The Curator is a single agent that orchestrates a two-phase workflow:
1. **Filter Scope:** Separate in-scope content from future topics
2. **Organize Content:** Reorganize in-scope content to match outline structure

**Philosophy:** Interactive checkpoints between phases, not black-box automation.

---

## 📊 Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                     The Curator Agent                       │
│                                                             │
│  Input: draft.md + outline.md                              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Phase 2.1: Filter Scope                             │  │
│  │ ├─ Tool: filter_scope_tool()                        │  │
│  │ ├─ LLM compares draft paragraphs to outline topics │  │
│  │ └─ Output: draft_ok.md + draft_not_ok.md           │  │
│  └─────────────────────────────────────────────────────┘  │
│                       ↓                                     │
│                  [CHECKPOINT]                               │
│            User reviews split in playground                 │
│                       ↓                                     │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Phase 2.2: Organize Content                         │  │
│  │ ├─ Tool: organize_content_tool()                    │  │
│  │ ├─ LLM reorganizes draft_ok to match outline order │  │
│  │ ├─ Validation: integrity + heading order           │  │
│  │ ├─ LLM-as-judge: logical flow check                │  │
│  │ └─ Output: draft_ok_organized.md                   │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Tools to Implement

### Tool 1: `filter_scope_tool(blog_id: str) -> dict`

**Purpose:** Split draft into in-scope vs future content using LLM.

**Algorithm:**
1. Read `draft.md` and `outline.md`
2. Extract outline topics (section headings + descriptions)
3. Split draft into paragraphs
4. For each paragraph, LLM determines: "Does this fit the outline topics?"
5. Collect paragraphs into `draft_ok` (matches) and `draft_not_ok` (future)
6. Save both files

**Output:**
```python
{
    "status": "success",
    "draft_ok_path": "outputs/<blog_id>/draft_ok.md",
    "draft_not_ok_path": "outputs/<blog_id>/draft_not_ok.md",
    "in_scope_paragraphs": 15,
    "future_paragraphs": 3
}
```

**Key Constraint:** Preserve ALL content (no lost paragraphs, no hallucinated content).

---

### Tool 2: `organize_content_tool(blog_id: str) -> dict`

**Purpose:** Reorganize `draft_ok` to match outline section order using LLM.

**Algorithm:**
1. Read `draft_ok.md` and `outline.md`
2. Extract outline sections (## headings) in order
3. LLM matches draft paragraphs to outline sections
4. Reorganize: place each paragraph under the correct section heading
5. Validate organization (see below)
6. Save `draft_ok_organized.md`

**Output:**
```python
{
    "status": "success",
    "organized_path": "outputs/<blog_id>/draft_ok_organized.md",
    "validation": {
        "integrity_check": True,
        "heading_order_check": True,
        "llm_judge_confident": True,
        "needs_human_review": False
    }
}
```

---

### Tool 3: `validate_with_llm_judge(draft_ok, outline, organized) -> dict`

**Purpose:** LLM evaluates if organization makes logical sense.

**Checks:**
1. **Automatic (deterministic):**
   - `check_reorganization_integrity()`: All content preserved, no additions
   - `check_heading_order()`: Sections match outline order

2. **LLM-as-Judge (semantic):**
   - Does content match section topics?
   - Are transitions logical?
   - Any sections seem misplaced?

**Output:**
```python
{
    "confident": True,  # LLM is confident in organization
    "issues": [],       # List of uncertain sections (if any)
    "recommendation": "approved"  # or "needs_human_review"
}
```

**Escalation Pattern:** If LLM is uncertain about specific sections, flag for human review:
```python
{
    "confident": False,
    "uncertain_sections": ["Introduction", "Conclusion"],
    "recommendation": "needs_human_review",
    "reason": "Content in Introduction seems more appropriate for Conclusion section"
}
```

---

## 📋 File Naming

| File | Description |
|------|-------------|
| `draft.md` | Original raw draft (input) |
| `outline.md` | Approved outline from Phase 1 (input) |
| `draft_ok.md` | In-scope content that matches outline topics |
| `draft_not_ok.md` | Out-of-scope content for future posts |
| `draft_ok_organized.md` | Organized content matching outline structure (output) |

**Rationale for `draft_ok` / `draft_not_ok`:**
- Matches legacy system naming (easier to understand old lessons)
- Clear intent: "ok" = fits this post, "not_ok" = doesn't fit (parking lot)
- Alternative names considered: `draft_in_scope` / `draft_future` (less clear)

---

## ✅ Validation Strategy

### Level 1: Automatic (Deterministic)

Extracted from legacy `validation_utils.py`:

**1. `check_reorganization_integrity(draft_ok, outline, organized)`**
- All paragraphs from `draft_ok` exist in `organized` (no lost content)
- All content in `organized` comes from `draft_ok` OR `outline` headings (no hallucinations)
- Uses set-based comparison with normalization

**2. `check_heading_order(outline, organized)`**
- Level 2 headings (##) in `organized` match `outline` order exactly
- Detects missing, extra, or out-of-order sections

**Test Coverage:** See `learning/archive/legacy_v1/test_validation_reorg.py`

---

### Level 2: LLM-as-Judge (Semantic)

After automatic checks pass, LLM evaluates:

**Prompt Structure:**
```
You are a content organization validator.

Review the following:
- Original content: [draft_ok]
- Intended structure: [outline]
- Organized result: [organized]

Questions:
1. Does content under each section match the section topic?
2. Are transitions between sections logical?
3. Are there any sections where content seems misplaced?

Rate your confidence:
- HIGH: Organization is clearly correct
- MEDIUM: Minor concerns but acceptable
- LOW: Significant issues, needs human review

If LOW or MEDIUM, specify which sections and why.
```

**Output Format:**
```json
{
    "confidence": "HIGH|MEDIUM|LOW",
    "issues": [
        {
            "section": "Introduction",
            "concern": "Contains technical details better suited for 'Implementation' section"
        }
    ],
    "recommendation": "approved|needs_review"
}
```

---

## 🎨 Agent Design: Single Curator vs Two Agents?

**Decision:** **Single Curator Agent** (orchestrates both phases)

### Why Single Agent?

**Pros:**
- ✅ Matches "Interactive Partner" philosophy (one conversation partner)
- ✅ Natural checkpoint flow (agent pauses between phases)
- ✅ Simpler UX (user doesn't manage agent sequence)
- ✅ Conversational continuity (agent remembers context)

**Cons:**
- ⚠️ Longer, more complex instruction
- ⚠️ Couples two operations

### Alternative Considered: Two Agents

```
curator_filter = Agent(...)   # Phase 2.1 only
curator_organizer = Agent(...) # Phase 2.2 only
```

**Rejected because:**
- Breaks conversational flow
- User must manually sequence agents
- Doesn't match "Interactive Partner" philosophy

---

## 🧪 Testing Strategy

### Unit Tests (pytest)

Test validation functions with edge cases:
```python
# test_validation.py
def test_reorganization_integrity_valid():
    draft_ok = "Intro.\n\nBody.\n\nConclusion."
    outline = "## Intro\n## Body\n## Conclusion"
    organized = "## Intro\nIntro.\n## Body\nBody.\n## Conclusion\nConclusion."
    assert check_reorganization_integrity(draft_ok, outline, organized) == (True, "")

def test_reorganization_integrity_lost_content():
    # Missing "Body" paragraph
    assert "Lost content" in error_msg
```

See: `learning/archive/legacy_v1/test_validation_reorg.py` for full test suite.

---

### Integration Tests (playground)

Test full Curator workflow:
1. Load real `draft.md` + `outline.md`
2. Run Phase 2.1 (filter scope)
3. Manually verify `draft_ok.md` + `draft_not_ok.md` split
4. Run Phase 2.2 (organize content)
5. Verify `draft_ok_organized.md` structure
6. Check validation results

---

## 📖 Instructions File: `instructions/curator.md`

```markdown
# The Curator

You are The Curator - you organize draft content to match the approved outline.

## Your Role

Filter out-of-scope content and reorganize in-scope content to match the outline structure.

## Your Workflow

### Phase 2.1: Filter Scope

1. Use `filter_scope_tool` to split the draft:
   - In-scope content → draft_ok.md
   - Out-of-scope content → draft_not_ok.md
2. Present results to user:
   - "I've filtered X paragraphs as in-scope, Y as future topics"
   - Show sample of each file
3. Wait for user confirmation: "Does this split look correct?"

### Phase 2.2: Organize Content (after user confirms)

1. Use `organize_content_tool` to reorganize draft_ok:
   - Match paragraphs to outline sections
   - Preserve all content (copy-paste only, no rewriting)
2. Use `validate_with_llm_judge` to check organization:
   - If confident: proceed
   - If uncertain: escalate to user review
3. Present final result:
   - "draft_ok_organized.md is ready"
   - Show validation results

## Critical Constraints

- **Preserve ALL content:** No lost paragraphs, no hallucinations
- **User checkpoints:** Wait for confirmation between phases
- **Copy-paste only:** Don't rewrite or paraphrase content
- **Escalate uncertainty:** If unsure, ask user for guidance
```

---

## 🚀 Implementation Order

1. ✅ Extract validation utils from legacy (`check_reorganization_integrity`, etc.)
2. ✅ Write unit tests for validation functions
3. 🔄 Implement `filter_scope_tool`
4. 🔄 Implement `organize_content_tool`
5. 🔄 Implement `validate_with_llm_judge`
6. 🔄 Create `step_agents/curator.py`
7. 🔄 Write `instructions/curator.md`
8. 🔄 Test in playground

---

## 🎓 Design Rationale

### Why stop at `draft_ok_organized.md` instead of section files?

**Decision:** Single organized file, NOT `sections/*.md`

**Reasoning:**
1. **Context for Phase 3 (Writer):**
   - Writer needs full document context for flow and transitions
   - "As mentioned in the introduction..." requires seeing the intro
   - Prevents repetition across sections

2. **Modern LLM capabilities:**
   - Can handle 10-50K word documents easily
   - Section-by-section focus can still be achieved with headings as anchors

3. **Simplicity:**
   - Fewer files to manage
   - Clearer progression: draft → draft_ok → draft_ok_organized → draft_polished

### Why LLM-as-judge instead of just automatic validation?

**Automatic validation catches:**
- ✅ Lost content
- ✅ Added content (hallucinations)
- ✅ Wrong section order

**But misses:**
- ❌ Content under wrong section (e.g., intro content in conclusion)
- ❌ Illogical flow (correct order but poor transitions)
- ❌ Topic mismatch (content exists but doesn't match section theme)

**LLM-as-judge adds semantic understanding while keeping human in the loop for uncertain cases.**

---

## 📚 References

- Legacy organizer: `learning/archive/legacy_v1/organizer.md`
- Legacy validation: `learning/archive/legacy_v1/validation_utils.py`
- Legacy tests: `learning/archive/legacy_v1/test_validation_reorg.py`
- Phase 1 lesson: `learning/lessons/phase1-reboot.md`

---

**Status:** Design approved - Ready to implement
**Next:** Extract validation utils and begin tool implementation
