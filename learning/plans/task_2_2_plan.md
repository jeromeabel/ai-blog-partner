# Task 2.2: Step 2 (Organization)

**Status:** In Progress
**Started:** Dec 14, 2025

---

## 🎯 Goal

Reorganize draft_ok chunks to match outline structure, creating a properly sequenced draft.

**Input:**
- `blog_outline` (from session state)
- `draft_ok` (from session state - content matching outline)

**Output:**
- `draft_organized.md` (file)
- `draft_organized` (session state key)

---

## 🤔 Architecture Decisions

### Decision 1: LoopAgent vs Simple Agent?

**Question:** Should this step use LoopAgent for quality control?

**Considerations:**
- Task complexity: High (requires accurate mapping and completeness).
- Quality variance: Moderate to High (LLMs can hallucinate or skip sections).
- Retry value: High (validation can catch missing sections).

**Decision:** Use `LoopAgent`.

**Rationale:** We need to ensure that *every* section from the outline is represented and that *all* content from `draft_ok` is included. A LoopAgent with a validation check for completeness is essential here.

---

### Decision 2: Which Agents to Use?

**Options:**
- A) Create new `organizer_agent` worker
- B) Delegate directly to Scribr
- C) Use existing agents with new instructions

**Decision:** Create new `organizer_agent` in `blogger/step_agents/step_2_organize.py`.

**Rationale:** This is a specialized task involving structural reorganization, distinct from general writing or editing. A dedicated agent allows for focused prompting and easier debugging.

---

### Decision 3: Text Matching Strategy

**Question:** How should the agent match draft chunks to outline sections?

**Considerations:**
- Semantic matching (AI-powered)
- Structural markers (headings)
- Combination approach

**Decision:** Combination approach.

**Rationale:** The agent will be instructed to use the outline headings as the primary structure and semantically place the `draft_ok` chunks under the correct headings. We will rely on the LLM's understanding of the content to match it to the outline.

---

## 📊 Session State Flow

### Inputs (from Step 1)
- `raw_draft` - Original draft content
- `blog_outline` - Structured outline
- `draft_ok` - Content matching outline

### Outputs (for Step 3)
- `draft_organized` - Reorganized content matching outline structure

### Persistence
- Save to file: `outputs/<blog_id>/draft_organized.md`

---

## ✅ Acceptance Criteria

### Code Quality
- [x] Imports resolve without errors
- [x] Agent(s) have clear docstrings
- [ ] Follows patterns from Lesson 2.1

### Functionality
- [ ] Reads `blog_outline` from session state
- [ ] Reads `draft_ok` from session state
- [ ] Produces reorganized draft
- [ ] Sets `output_key="draft_organized"` (or equivalent)

### Integration
- [ ] Updates `blogger/workflow.py` Step 2 instructions
- [ ] Adds new agent(s) to orchestrator `sub_agents` (if needed)
- [ ] Orchestrator uses `save_step_tool` to persist output

### Quality
- [ ] Output preserves all content from `draft_ok`
- [ ] Output follows outline section order
- [ ] (If using LoopAgent) Validation checks quality

---

## 📝 Implementation Steps

1. **Analyze Task** (completed)
   - Understand requirements
   - Make architecture decisions
   - Document rationale

2. **Validation Logic** (Completed)
   - [x] Create `check_reorganization_integrity` in `validation_utils.py`
   - [x] Create `ReorganizationValidationChecker` in `validation_checkers.py`
   - [x] Create and run unit tests for `check_reorganization_integrity`
   - [x] Implement and run unit tests for `check_heading_order`
   - [x] Update `ReorganizationValidationChecker` to include `check_heading_order`
   - [x] Ensure outline descriptions are ignored by integrity and order checks

3. **Create Agent(s)** (In Progress)
   - [ ] Create `blogger/instructions/organizer.md`
   - [ ] File: `blogger/step_agents/step_2_organize.py`
   - [ ] Define worker agent(s) (`organizer_agent`)
   - [ ] Add `LoopAgent` wrapper (`robust_organize_step`)

4. **Update Workflow**
   - [ ] Update Step 2 instructions in `blogger/workflow.py`
   - [ ] Add new agents to `sub_agents` list
   - [ ] Test integration

---

## 💡 Questions to Answer Before Implementation

1. Is this task simple enough for Scribr alone, or do we need a specialized agent?
2. Does the output quality vary enough to warrant LoopAgent retry logic?
3. Should we validate that all content from `draft_ok` is preserved?
4. What session state keys should be used?

---

## 📖 Related Lessons

- **Lesson 2.1:** LoopAgent pattern, session state strategy, functional architecture
- **Lesson 1.3:** Workflow orchestration, agent delegation

---

## 🎓 Expected Learning Outcomes

By completing this task, you'll learn:
- When to use LoopAgent vs simple Agent (decision framework)
- Multi-file input orchestration patterns
- Text reorganization strategies with LLMs
- Balancing simplicity vs robustness in workflow design
