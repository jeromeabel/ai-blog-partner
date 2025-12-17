# Learning Progress Tracker

**Active Task:** Phase 1 - Foundation Reboot
**Status:** ✅ Step 1.2 Complete - Ready for Phase 2
**Plan File:** `learning/plans/reframe_step_1.md`

---

## 🗺️ Roadmap: The Interactive Partner

### ⚠️ OLD SYSTEM (Abandoned - 2024-12-14 to 2024-12-15)
**Approach:** Automated orchestrator with session state, LoopAgents, complex validation
**Why abandoned:** Over-engineered, black-box automation, didn't match "Interactive Partner" vision

**Completed (for reference):**
- [x] 1.1-1.3: Foundation (agents, tools, orchestrator) → See deprecated lessons
- [x] 2.1: LoopAgent pattern for outline creation → See deprecated lessons
- [x] 2.2: Automated organization with validation → See deprecated lessons

**Lessons learned:** Archived in `lessons/` with DEPRECATED markers

---

### ✅ NEW SYSTEM: Interactive Partner (Current - 2024-12-16+)
**Approach:** User-driven playground, simple agents, file-based workflow, manual checkpoints

### Phase 1: Foundation & The Architect (Step 1) 🏗️ ✅
- [x] **1.1 The Playground**
    - Created `playground.py` with ADK Runner integration
    - Supports multiple agents (scribr, linguist, architect)
    - Added proper event handling for tools and responses
    - **Verified:** Basic agent interaction works
- [x] **1.2 The Architect Agent**
    - Implemented `step_agents/architect.py`
    - Created `instructions/architect.md` (simplified, brainstorming-focused)
    - Added file I/O tools: `read_draft_tool`, `read_file_tool`, `save_step_tool`
    - Integrated Scribr as collaborative agent for title polishing
    - **Ready to Verify:** Test interactive outline creation with real draft
    - **Lesson:** `lessons/phase1-reboot.md`

### Phase 2: The Curator (Step 2) 🎨
- [ ] **2.1 Filter Scope Tool**
    - Implement `filter_scope_tool` (LLM splits in-scope vs future content)
    - Output: `draft_ok.md` + `draft_not_ok.md`
    - **Verify:** User checkpoint in playground
- [ ] **2.2 Organize Content Tool**
    - Implement `organize_content_tool` (LLM reorganizes paragraphs to match outline)
    - Extract validation utils from legacy (`check_reorganization_integrity`, `check_heading_order`)
    - Implement LLM-as-judge validation with escalation pattern
    - Output: `draft_ok_organized.md`
    - **Verify:** Unit tests for validation logic (`pytest`)
- [ ] **2.3 Curator Agent**
    - Create `step_agents/curator.py`
    - Orchestrates filter → organize workflow with checkpoints
    - **Verify:** Test in playground with real draft + outline

### Phase 3: The Writer (Step 3) ✍️
- [ ] **3.1 Writer Agent**
    - Implement `step_agents/writer.py`
    - Input: `draft_ok_organized.md` (full context for flow and transitions)
    - Process: Iterative expand & polish with section-by-section focus
    - **Verify:** Polish sections in Playground with full document context

---

## 📚 Lesson Index

### Current System (Interactive Partner)
- **Phase 1 (Reboot):** `lessons/phase1-reboot.md` - Foundation & The Architect

### Deprecated (OLD Automated System)
All marked with ⚠️ DEPRECATED headers, kept for historical reference:
- `lessons/1.1-agents.md` - Agent definitions (foundational patterns still valid)
- `lessons/1.2-tools.md` - File operations (patterns still valid)
- `lessons/1.3-workflow.md` - Orchestrator (abandoned approach)
- `lessons/2.1-loopagent.md` - LoopAgent pattern (over-engineered)
- `lessons/2.2-organizing.md` - Automated organization (abandoned)
- `lessons/2.2-validation-reorg.md` - Complex validation (abandoned)

### Architecture Reference
- **Current:** `AGENTS.md` (The Source of Truth for Interactive Partner approach)