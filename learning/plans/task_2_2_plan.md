# Task 2.2: Step 2 (Organization)

**Status:** Planning
**Started:** (pending)

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
- Task complexity: ?
- Quality variance: ?
- Retry value: ?

**Decision:** (To be determined)

**Rationale:** (To be documented)

---

### Decision 2: Which Agents to Use?

**Options:**
- A) Create new `organizer_agent` worker
- B) Delegate directly to Scribr
- C) Use existing agents with new instructions

**Decision:** (To be determined)

**Rationale:** (To be documented)

---

### Decision 3: Text Matching Strategy

**Question:** How should the agent match draft chunks to outline sections?

**Considerations:**
- Semantic matching (AI-powered)
- Structural markers (headings)
- Combination approach

**Decision:** (To be determined)

**Rationale:** (To be documented)

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
- [ ] Imports resolve without errors
- [ ] Agent(s) have clear docstrings
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

1. **Analyze Task** (current)
   - Understand requirements
   - Make architecture decisions
   - Document rationale

2. **Create Agent(s)**
   - File: `blogger/step_agents/step_2_organize.py` (if needed)
   - Define worker agent(s)
   - Add validation (if using LoopAgent)

3. **Update Workflow**
   - Update Step 2 instructions in `blogger/workflow.py`
   - Add new agents to `sub_agents` list
   - Test integration

4. **Test & Validate**
   - Run with sample data
   - Verify output quality
   - Check all acceptance criteria

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
