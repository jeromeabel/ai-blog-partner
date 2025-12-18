# Phase 2: The Curator - Learning Guide

**Your Mission:** Build Phase 2 (The Curator) step-by-step
**Learning Approach:** Teacher/Student - AI guides, you implement, we verify together
**Reference:** `/home/jabel/workspace/ai-blog-partner/learning/plans/phase2_curator.md`

---

## What You'll Build

The Curator agent that:
1. **Filters** draft content into in-scope vs future topics
2. **Organizes** in-scope content to match outline structure
3. **Validates** organization with automatic checks + LLM-as-judge

**Philosophy:** Build one small piece at a time. Don't move forward until verified working.

---

## Current State

### ✅ Already Implemented
- `blogger/tools.py` - Basic file I/O tools (read_draft, save_step, read_file)
- `blogger/text_utils.py` - Helper functions (normalize_text, extract_headings, fuzzy_match_score)
- `blogger/step_agents/architect.py` - Phase 1 agent (reference pattern)
- Legacy validation code exists at: `learning/archive/legacy_v1/validation_utils.py`

### ❌ Missing (To Implement)
1. Validation functions in `text_utils.py`
2. Three new tools in `tools.py`:
   - `filter_scope_tool`
   - `organize_content_tool`
   - `validate_with_llm_judge`
3. Curator agent at `blogger/step_agents/curator.py`
4. Instructions at `blogger/instructions/curator.md`

---

## Learning Steps

---

### 📚 Step 1: Extract Validation Functions (Foundation)

**Goal:** Add pure validation functions to `text_utils.py` that we'll use later

**Your Task:**
1. Open `blogger/text_utils.py`
2. Copy 5 functions from `learning/archive/legacy_v1/validation_utils.py`:
   - `normalize_and_split()` (lines 9-40)
   - `check_content_integrity()` (lines 43-125)
   - `check_outline_structure()` (lines 128-187)
   - `check_reorganization_integrity()` (lines 190-264)
   - `check_heading_order()` (lines 267-313)
3. Paste them at the end of `text_utils.py`

**Why these functions?**
- They're **pure functions** - no LLM calls, no file I/O, just text processing
- Already tested in legacy code (see `test_validation_reorg.py`)
- We'll use them to validate content splitting and reorganization

**Verify:**
```bash
# Test that functions were copied correctly
python -c "from blogger.text_utils import normalize_and_split, check_content_integrity, check_reorganization_integrity, check_heading_order, check_outline_structure; print('✅ All validation functions imported successfully')"
```

**Expected output:** `✅ All validation functions imported successfully`

**What you learned:**
- How to extract and reuse tested utility functions
- Pattern: Pure validation functions belong in `text_utils.py`

---

### 🔧 Step 2: Build filter_scope_tool (Content Filtering)

**Goal:** Create a tool that splits draft into in-scope vs future content using LLM

**Your Task:**
1. Open `blogger/tools.py`
2. Add a new function at the end:

```python
def filter_scope_tool(blog_id: str) -> dict:
    """
    Split draft content into in-scope (matches outline) vs future topics.

    Args:
        blog_id: Blog identifier

    Returns:
        Success: {
            "status": "success",
            "draft_ok_path": "...",
            "draft_not_ok_path": "...",
            "in_scope_count": 15,
            "future_count": 3
        }
        Error: {"status": "error", "message": "..."}
    """
    # TODO: Implement in next sub-step
    pass
```

**Implementation Algorithm:**
1. Read `draft.md` and `outline.md` (use existing `read_draft_tool`, `read_file_tool`)
2. Create internal helper agent (use `GenAI` or lightweight `Agent`)
   - Model: `gemini-2.0-flash-exp`
   - Prompt: "For each paragraph, determine if it fits the outline topics"
   - Return: Two lists of paragraphs (in-scope, future)
3. Validate split using `check_content_integrity()`
4. Save to `draft_ok.md` and `draft_not_ok.md` using existing save logic

**Verify:**
- Ask me: "How do I create an internal helper agent for LLM calls?"
- Test with real draft + outline in playground

**What you'll learn:**
- How tools can use LLM internally (via helper agents)
- Content preservation validation pattern
- File I/O with Path, mkdir patterns

---

### 🗂️ Step 3: Build organize_content_tool (Content Organization)

**Goal:** Create a tool that reorganizes content to match outline structure

**Your Task:**
1. Open `blogger/tools.py`
2. Add a new function:

```python
def organize_content_tool(blog_id: str) -> dict:
    """
    Reorganize draft_ok content to match outline section order.

    Args:
        blog_id: Blog identifier

    Returns:
        Success: {
            "status": "success",
            "organized_path": "...",
            "validation": {
                "integrity_check": True,
                "heading_order_check": True,
                "llm_judge_confident": True,
                "needs_human_review": False
            }
        }
        Error: {"status": "error", "message": "..."}
    """
    # TODO: Implement in next sub-step
    pass
```

**Implementation Algorithm:**
1. Read `draft_ok.md` and `outline.md`
2. Extract outline section headings (## level) using `extract_headings()` from text_utils
3. Create internal helper agent to reorganize:
   - Model: `gemini-2.0-flash-exp`
   - Prompt: "Match each paragraph to correct section, preserve ALL content"
4. **Validate automatically:**
   - `check_reorganization_integrity()` - content preserved
   - `check_heading_order()` - sections match outline order
5. **Validate semantically:**
   - Call `validate_with_llm_judge()` (Step 4)
6. Save `draft_ok_organized.md`

**Verify:**
- Automatic checks should catch structural errors
- LLM-as-judge should catch semantic errors (content in wrong section)

**What you'll learn:**
- Multi-layered validation (automatic + semantic)
- Heading extraction and matching patterns

---

### 🧠 Step 4: Build validate_with_llm_judge (Semantic Validation)

**Goal:** Create LLM-as-judge to catch semantic issues automatic checks miss

**Your Task:**
1. Open `blogger/tools.py`
2. Add internal helper function (not a tool, just a function):

```python
def validate_with_llm_judge(draft_ok: str, outline: str, organized: str) -> dict:
    """
    Use LLM to validate organization makes semantic sense.

    Returns:
        {
            "confident": True/False,
            "issues": [...],
            "recommendation": "approved" | "needs_human_review"
        }
    """
    # TODO: Implement
    pass
```

**Implementation Algorithm:**
1. Create internal helper agent (GenAI or Agent)
2. Prompt structure (from design doc):
   ```
   You are a content organization validator.

   Review:
   - Original content: [draft_ok]
   - Intended structure: [outline]
   - Organized result: [organized]

   Questions:
   1. Does content under each section match the section topic?
   2. Are transitions between sections logical?
   3. Are there sections where content seems misplaced?

   Rate confidence: HIGH/MEDIUM/LOW
   If MEDIUM/LOW, specify which sections and why.
   ```
3. Parse LLM response for confidence + issues
4. Return structured result

**Verify:**
- Test with good organization → HIGH confidence
- Test with misplaced content → MEDIUM/LOW confidence with specific issues

**What you'll learn:**
- LLM-as-judge pattern for semantic validation
- Escalation: automatic checks + LLM judge + human review

---

### 🤖 Step 5: Create the Curator Agent

**Goal:** Build the agent that orchestrates filter + organize workflow

**Your Task:**
1. Create new file: `blogger/step_agents/curator.py`
2. Follow the `architect.py` pattern:

```python
from google.adk import Agent
from blogger.tools import (
    read_draft_tool,
    read_file_tool,
    save_step_tool,
    filter_scope_tool,
    organize_content_tool,
)
from blogger.agents import read_instructions

curator = Agent(
    model="gemini-2.0-flash-exp",  # Lighter model for orchestration
    name="curator",
    description="Filter and organize draft content to match outline structure",
    instruction=read_instructions("curator.md"),  # You'll create this next
    tools=[
        read_draft_tool,
        read_file_tool,
        save_step_tool,
        filter_scope_tool,
        organize_content_tool,
    ],
)
```

**Key differences from Architect:**
- Lighter model (`gemini-2.0-flash-exp` vs `gemini-3-pro-preview`)
- No sub-agents needed (Curator just orchestrates tools)
- Two-phase workflow with user checkpoint

**Verify:**
```bash
python -c "from blogger.step_agents.curator import curator; print(f'✅ Curator agent created: {curator.name}')"
```

**What you'll learn:**
- Agent configuration pattern
- When to use lighter vs heavier models
- Tool-focused agents vs collaborative agents

---

### 📝 Step 6: Write Curator Instructions

**Goal:** Create conversational instructions for the Curator agent

**Your Task:**
1. Create new file: `blogger/instructions/curator.md`
2. Follow `architect.md` pattern (read it for reference)
3. Use this template:

```markdown
You are The Curator - you organize draft content to match the approved outline.

# MISSION
Filter out-of-scope content and reorganize in-scope content to match outline structure.

# TOOLS
- **filter_scope_tool(blog_id):** Split draft into in-scope vs future topics
- **organize_content_tool(blog_id):** Reorganize content to match outline order
- **read_file_tool(file_path):** Read outlines and drafts
- **save_step_tool(blog_id, step_name, content):** Save intermediate results

---

# THE PROCESS

## Phase 2.1: Filter Scope

1. Use `filter_scope_tool(blog_id)` to split the draft
2. Present results:
   - "I've filtered X paragraphs as in-scope, Y as future topics"
   - Show sample from each file
3. **CHECKPOINT:** Wait for user: "Does this split look correct?"

## Phase 2.2: Organize Content (after user confirms)

1. Use `organize_content_tool(blog_id)` to reorganize
2. Tool automatically validates (integrity + heading order + LLM-as-judge)
3. Present results:
   - If validation passes: "draft_ok_organized.md is ready"
   - If uncertain: "I found possible issues in [sections], please review"

---

# CRITICAL CONSTRAINTS

- **Preserve ALL content:** No lost paragraphs, no hallucinations
- **User checkpoints:** Wait for confirmation between phases
- **Copy-paste only:** Don't rewrite or paraphrase content
- **Escalate uncertainty:** If validation flags issues, ask user

---

# STYLE

- **Conversational:** You're a colleague organizing files together
- **Transparent:** Show what you're doing at each step
- **Patient:** User reviews and approves before moving forward
```

**Verify:** Read it aloud - does it sound conversational, not robotic?

**What you'll learn:**
- Instructions are role-focused, not procedural logic
- Checkpoints = collaboration, not automation

---

### 🎮 Step 7: Add Curator to Playground

**Goal:** Enable interactive testing of the Curator agent

**Your Task:**
1. Open `blogger/playground.py`
2. Add import at top:
```python
from blogger.step_agents.curator import curator
```
3. Add to `agent_map` dict:
```python
agent_map = {
    "scribr": scribr,
    "linguist": linguist,
    "architect": architect,
    "curator": curator,  # NEW
}
```

**Verify:**
```bash
python -m blogger.playground --agent curator
```

**Expected:** Curator agent starts, ready to accept commands

**What you'll learn:**
- How playground.py discovers agents
- Interactive testing workflow

---

### ✅ Step 8: Integration Testing

**Goal:** Verify the full Curator workflow works end-to-end

**Your Test Plan:**

**Setup:**
1. Create test directory:
   ```bash
   mkdir -p inputs/test-curator outputs/test-curator
   ```
2. Copy a real draft to `inputs/test-curator/draft.md`
3. Copy outline from Phase 1 to `outputs/test-curator/outline.md`

**Test Phase 2.1 - Filter Scope:**
```bash
python -m blogger.playground --agent curator
```
1. Tell curator: "Filter content for blog_id: test-curator"
2. ✓ Curator calls `filter_scope_tool`
3. ✓ Check `outputs/test-curator/draft_ok.md` created
4. ✓ Check `outputs/test-curator/draft_not_ok.md` created
5. ✓ Verify split makes sense (in-scope vs future)
6. ✓ Curator waits for your confirmation (checkpoint!)

**Test Phase 2.2 - Organize Content:**
1. Tell curator: "Looks good, proceed with organizing"
2. ✓ Curator calls `organize_content_tool`
3. ✓ Check `outputs/test-curator/draft_ok_organized.md` created
4. ✓ Verify sections match outline order
5. ✓ Verify all content preserved (no lost paragraphs)
6. ✓ Check validation report (integrity + heading order + LLM judge)

**Test Edge Cases:**
- Missing outline → Error message
- Empty draft → Error message
- Content mismatched to outline → LLM-as-judge flags for review

**Success Criteria:** ✅ All checkpoints pass, files created correctly

**What you'll learn:**
- End-to-end workflow testing
- User checkpoint pattern in action
- Validation catches errors

---

### 🧪 Step 9: Optional - Unit Tests

**Goal:** Add pytest tests for validation functions (if you want TDD practice)

**Your Task:**
1. Create `tests/test_text_utils.py`
2. Port tests from `learning/archive/legacy_v1/test_validation_reorg.py`:
   - `test_reorganization_integrity_valid()`
   - `test_reorganization_integrity_lost_content()`
   - `test_heading_order_valid()`
   - `test_heading_order_mismatch()`

**Example:**
```python
from blogger.text_utils import check_reorganization_integrity

def test_reorganization_integrity_valid():
    draft_ok = "Intro.\n\nBody.\n\nConclusion."
    outline = "## Intro\n## Body\n## Conclusion"
    organized = "## Intro\nIntro.\n## Body\nBody.\n## Conclusion\nConclusion."

    is_valid, error = check_reorganization_integrity(draft_ok, outline, organized)
    assert is_valid
    assert error == ""
```

**Verify:**
```bash
pytest tests/test_text_utils.py -v
```

**Priority:** Optional - validation functions already tested in legacy
**What you'll learn:** TDD pattern for pure functions

---

### 📖 Step 10: Document Your Learning

**Goal:** Record what you learned for Phase 3

**Your Task:**
1. Create `learning/lessons/phase2-curator.md`
2. Document:
   - What worked well
   - What was challenging
   - Key patterns learned (internal helper agents, validation layers, checkpoints)
   - Mistakes and how you fixed them

**Template:**
```markdown
# Phase 2: The Curator - Learning Notes

**Date:** [Your date]
**Status:** Complete ✅

## What I Built
- filter_scope_tool: LLM-based content filtering
- organize_content_tool: LLM-based reorganization with multi-layer validation
- Curator agent: Two-phase workflow with user checkpoints

## Key Learnings
1. **Internal helper agents:** Tools can use LLM internally for smart operations
2. **Multi-layer validation:** Automatic (structural) + LLM-as-judge (semantic) + Human (edge cases)
3. **Checkpoint pattern:** User reviews between phases = collaboration, not automation

## Challenges
[What was hard? How did you solve it?]

## Next Time
[What would you do differently?]
```

**What you'll learn:**
- Reflection cements learning
- Documentation helps future you (and Phase 3!)

---

## Critical Files

**To Modify:**
- `blogger/text_utils.py` - Add validation functions
- `blogger/tools.py` - Add 3 new tools
- `blogger/playground.py` - Add curator to agent map

**To Create:**
- `blogger/step_agents/curator.py` - New agent
- `blogger/instructions/curator.md` - Instructions

**Reference:**
- `learning/archive/legacy_v1/validation_utils.py` - Source for validation functions
- `learning/plans/phase2_curator.md` - Design document
- `blogger/step_agents/architect.py` - Pattern reference

---

## Design Decisions (from design doc)

### 1. Single Curator Agent (not two separate agents)
**Rationale:** Matches "Interactive Partner" philosophy, conversational continuity

### 2. Single organized file (not section files)
**Rationale:** Writer needs full document context for flow and transitions

### 3. LLM-as-judge + automatic validation
**Rationale:** Automatic catches structural issues, LLM catches semantic issues

### 4. File naming: draft_ok / draft_not_ok
**Rationale:** Clear intent, matches legacy naming for easier reference

---

## Success Criteria

✅ Validation functions work (can test with legacy unit tests)
✅ filter_scope_tool splits content correctly (preserves all paragraphs)
✅ organize_content_tool reorganizes to match outline order
✅ Validation catches lost content, wrong order, hallucinations
✅ LLM-as-judge escalates uncertain cases
✅ Curator agent runs full workflow in playground
✅ User can checkpoint between filter and organize phases

---

## 🎯 Summary: Your Learning Path

| Step | What You Build | Verify By | Time |
|------|---------------|-----------|------|
| 1 | Copy validation functions | Import test | 10 min |
| 2 | filter_scope_tool | Ask for help with helper agent | 30-60 min |
| 3 | organize_content_tool | Unit test with sample data | 30-60 min |
| 4 | validate_with_llm_judge | Test with good/bad organization | 20-30 min |
| 5 | curator.py agent | Import test | 5 min |
| 6 | curator.md instructions | Read aloud test | 15-20 min |
| 7 | Add to playground | Run curator | 5 min |
| 8 | Integration testing | Full workflow test | 20-30 min |
| 9 | Unit tests (optional) | pytest | 20-30 min |
| 10 | Document learnings | Create lesson file | 10-15 min |

**Total:** 2.5-4 hours (with breaks!)

---

## 💡 Tips for Success

1. **One step at a time:** Don't skip ahead. Verify each step works.
2. **Ask for help:** Stuck on Step 2 (helper agents)? Ask me: "How do I create an internal helper agent?"
3. **Test early, test often:** Use playground between steps, not just at the end
4. **Read the references:** Legacy code and design doc have answers
5. **Take breaks:** This is a marathon, not a sprint

---

## 🆘 When to Ask for Help

- "How do I create an internal helper agent in Step 2?"
- "My validation is failing in Step 3, can you review my code?"
- "The LLM-as-judge prompt isn't working, what should I change?"
- "Integration test is failing in Step 8, help me debug"

I'm here to guide, explain, and review - you're here to implement and learn!

---

**Ready?** Start with Step 1: Copy validation functions to `text_utils.py`
