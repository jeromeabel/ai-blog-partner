# Phase 3: The Writer - Implementation Plan

**Status:** Complete
**Started:** 2024-12-18
**Completed:** 2025-12-19

---

## 🎯 Goal

Build the Writer agent to iteratively polish sections with user feedback.

**Input:** `posts/{blog_id}/2-draft_organized.md` (from Curator)
**Output:** `posts/{blog_id}/3-final.md` (polished post)

**Philosophy:** Section-by-section polishing with full document context for flow and transitions.

---

## 🏗️ Architecture

### Agent Design

**Primary Agent:** `blogger/agents/writer.py`
- Role: Interactive polishing partner
- Pattern: Simple Agent with iterative feedback loop
- Sub-agent: `scribr.py` (style enforcement, hype removal)

**Interaction Flow:**
```
User: "Polish the Introduction section"
  ↓
Writer: [Reads section with context]
  ↓
Writer: [Calls Scribr for style check]
  ↓
Writer: [Presents polished version]
  ↓
User: "Looks good" or "Change X"
  ↓
Writer: [Saves if approved, iterates if changes requested]
```

### Tool Design

**Tool 1: `read_section_tool(blog_id: str, section_heading: str) -> dict`**
- **Purpose:** Extract specific section with surrounding context
- **Input:** Blog ID, section heading (e.g., "Introduction")
- **Output:**
  ```python
  {
      "status": "success",
      "section_content": "...",
      "prev_section": "...",  # For context
      "next_section": "..."   # For context
  }
  ```
- **Why context?** Writer needs to see surrounding sections for flow, transitions, avoiding repetition

**Tool 2: `save_section_tool(blog_id: str, section_heading: str, polished_content: str) -> dict`**
- **Purpose:** Replace section content with polished version
- **Validation:**
  - Heading structure preserved
  - No content from other sections modified
  - Section exists in organized draft
- **Output:**
  ```python
  {
      "status": "success",
      "updated_file": "posts/{blog_id}/2-draft_organized.md",
      "message": "Section 'Introduction' updated"
  }
  ```

**Tool 3: `finalize_post_tool(blog_id: str) -> dict`**
- **Purpose:** Create final polished post
- **Action:** Copy `2-draft_organized.md` → `3-final.md`
- **Output:**
  ```python
  {
      "status": "success",
      "final_path": "posts/{blog_id}/3-final.md"
  }
  ```

### Key Decisions

**Decision 1: Section-by-section vs full document?**
- **Chosen:** Section-by-section with context
- **Rationale:**
  - Focused feedback from user
  - Manageable chunks
  - Can iterate on specific sections without reprocessing entire document
  - Full context prevents flow issues

**Decision 2: In-place editing vs separate files?**
- **Chosen:** In-place editing of `2-draft_organized.md`
- **Rationale:**
  - Simpler workflow (one file evolves)
  - User can see current state at any time
  - Final copy created only when user approves all sections

**Decision 3: Scribr integration point?**
- **Chosen:** Writer calls Scribr as sub-agent for each section
- **Rationale:**
  - Separation of concerns (structure vs style)
  - Scribr specializes in hype removal, Writer focuses on polish
  - Natural delegation pattern

---

## 📋 Implementation Checklist

### Task 1: Section Tools
- [x] Create `read_section_tool` in `blogger/utils/tools.py`
  - [x] Parse markdown to extract section by heading
  - [x] Include prev/next section headings for context
  - [x] Handle edge cases (first/last section)
- [x] Create `save_section_tool` in `blogger/utils/tools.py`
  - [x] Replace section content in organized draft
  - [x] Validate heading structure preserved
  - [x] Ensure no other sections modified
- [x] Create `finalize_post_tool` in `blogger/utils/tools.py`
  - [x] Copy 2-draft_organized.md → 3-final.md
  - [x] Add metadata (date generated, etc.)
- [x] Write unit tests for section extraction
  - [x] Test section extraction with context
  - [x] Test section replacement validation
  - [x] Test edge cases (missing sections, malformed headings)

### Task 2: Writer Agent
- [x] Create `blogger/agents/writer.py`
  - [x] Import tools and Scribr agent
  - [x] Define Writer agent with tools
  - [x] Set up Scribr as sub-agent
- [x] Create `blogger/agents/writer.md` (instructions)
  - [x] Define role and workflow
  - [x] Specify section-by-section process
  - [x] Include Scribr delegation pattern
  - [x] Add examples of user interactions

### Task 3: Integration & Testing
- [x] Register Writer in `blogger/playground.py`
  - [x] Add to AGENTS dictionary
  - [x] Verify agent loads without errors
- [x] Test in playground with real draft
  - [x] Load organized draft from Phase 2
  - [x] Test: "Polish the Introduction"
  - [x] Verify: Only Introduction modified
  - [x] Test: "Now polish the Body"
  - [x] Verify: Body polished, Introduction unchanged
  - [x] Test: "Finalize the post"
  - [x] Verify: 3-final.md created correctly

### Task 4: Documentation
- [x] Update `progress/PROGRESS.md`
  - [x] Mark Phase 3 tasks complete
  - [x] Update status to Phase 3 Complete
- [x] Create `progress/lessons/phase3_writer.md`
  - [x] Document section-by-section pattern
  - [x] Document Scribr integration approach
  - [x] Capture key learnings
- [x] Update `AGENTS.md` if needed
  - [x] Add Writer to architecture description
  - [x] Update file paths if changed

---

## 🧪 Testing Strategy

### Unit Tests (pytest)

**File:** `blogger/tests/test_section_tools.py`

```python
def test_read_section_tool_extracts_correct_section():
    """Test section extraction with context"""
    # Given: Organized draft with ## Intro, ## Body, ## Conclusion
    # When: Reading "Body" section
    # Then: Returns Body content + prev (Intro) and next (Conclusion) headings

def test_save_section_tool_preserves_structure():
    """Test section replacement preserves other sections"""
    # Given: Section with polished content
    # When: Saving section
    # Then: Only target section modified, heading preserved

def test_read_section_tool_handles_edge_cases():
    """Test first and last sections"""
    # Test: First section (no prev_section)
    # Test: Last section (no next_section)
    # Test: Missing section (error handling)

def test_save_section_tool_validation():
    """Test validation catches issues"""
    # Test: Invalid section heading → error
    # Test: Malformed content → error
    # Test: Missing heading in replacement → error
```

### Integration Tests (Playground)

**Scenario 1: Basic Section Polishing**
1. Start playground: `python -m blogger.playground --agent writer`
2. Load real organized draft (from Phase 2 output)
3. User: "Polish the Introduction section to be more engaging"
4. Verify: Writer reads section, calls Scribr, presents polished version
5. User: "Looks good, save it"
6. Verify: Only Introduction section updated in 2-draft_organized.md

**Scenario 2: Iterative Refinement**
1. User: "Polish the Introduction"
2. Writer: [Shows polished version]
3. User: "Too formal, make it more conversational"
4. Writer: [Revises and shows updated version]
5. User: "Perfect, save it"
6. Verify: Final version matches user feedback

**Scenario 3: Full Workflow**
1. Polish Introduction → Body → Conclusion (section by section)
2. User: "Finalize the post"
3. Verify: 3-final.md created with all polished sections

**Scenario 4: Context Awareness**
1. User: "Polish the Conclusion section"
2. Verify: Writer mentions callbacks to Introduction/Body when appropriate
3. Verify: No repetition of concepts already covered

---

## 📚 References

### Completed Phases
- **Phase 1:** `archives/lessons/phase1-reboot.md` (Architect agent, file tools)
- **Phase 2:** `archives/completed/phase2_curator.md` (Curator agent, validation)

### Related Code
- **Scribr agent:** `blogger/agents/scribr.py` (style enforcement example)
- **Architect agent:** `blogger/agents/architect.py` (brainstorming example)
- **File tools:** `blogger/utils/tools.py` (tool patterns)

### Lessons Learned
- Keep tools pure (I/O only, no LLM calls)
- Agents do reasoning, tools provide capabilities
- Sub-agent delegation for specialized tasks
- User checkpoints for quality control

---

## 🎓 Learning Outcomes

By completing Phase 3, you'll learn:
- **Section-level manipulation:** Parsing and updating specific markdown sections
- **Context management:** Providing surrounding context without full document reprocessing
- **Sub-agent patterns:** When and how to delegate to specialized agents
- **Iterative refinement:** Building feedback loops into agent workflows
- **Tool validation:** Ensuring operations maintain document integrity

---

## Notes

**Why not polish entire document at once?**
- User loses control over specific sections
- Hard to give targeted feedback
- Risk of introducing inconsistencies across sections
- Section-by-section gives clear checkpoints

**Why modify 2-draft_organized.md instead of creating 3-final.md immediately?**
- User can see current state evolving
- Can resume work if interrupted
- Only create final copy when fully approved
- Clearer workflow: organized → polished → finalized

**Why include context (prev/next sections)?**
- Prevents repetition across sections
- Enables natural transitions ("As mentioned earlier...")
- Writer understands document flow
- Better overall coherence
