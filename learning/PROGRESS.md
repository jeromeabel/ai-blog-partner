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

### Phase 2: The Butcher (Step 2) 🔪
- [ ] **2.1 Splitter Tool**
    - Implement deterministic splitting logic (regex/fuzzy match)
    - **Verify:** Unit tests (`pytest`)
- [ ] **2.2 Integration**
    - Connect Architect output to Butcher input

### Phase 3: The Writer (Step 3) ✍️
- [ ] **3.1 Section Writer Agent**
    - Implement `step_agents/writer.py`
    - **Verify:** Polish one section in Playground

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