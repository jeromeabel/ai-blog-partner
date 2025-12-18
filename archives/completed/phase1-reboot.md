# Phase 1: Foundation Reboot - The Architect

**Date:** 2025-12-16
**Status:** ✅ Complete
**Components:** Playground, Architect Agent, File Tools

---

## 🎯 Goal

Build an **Interactive Partner** system where the user collaborates with agents through conversational brainstorming, not automated loops.

**Deliverables:**
- `playground.py` - Interactive CLI for testing agents
- `step_agents/architect.py` - Outline creation through brainstorming
- File I/O tools for reading/saving drafts and outlines

---

## ✅ What Worked

### 1. File Tools Over Terminal Pasting
**Problem:** Terminal has issues with large text input (infinite loops, buggy behavior)

**Solution:**
- Created `read_draft_tool(blog_id)` to load drafts from `inputs/<blog_id>/draft.md`
- Created `read_file_tool(file_path)` for reading any markdown file (outline versions, etc.)
- Created `save_step_tool(blog_id, step_name, content)` for saving outputs

**Benefit:**
- Clean, reliable file operations
- Supports version-based iteration (`outline_v1.md`, `outline_v2.md`, etc.)
- No terminal buffer issues

### 2. Simplicity in Instructions
**Problem:** Initial `architect.md` was too complex (~92 lines, overwhelming details)

**Solution:**
- Simplified to ~77 lines focused on **BRAINSTORMING**
- Clear 4-step process:
  1. **Understand** - Read draft, identify themes
  2. **Brainstorm** - Ask questions, suggest angles
  3. **Draft Structure** - Create outline, call Scribr
  4. **Iterate** - Refine based on user feedback

**Benefit:**
- LLM has clearer focus
- User sees the collaborative loop more clearly
- Less cognitive overhead for both human and AI

### 3. Team Collaboration Model
**Problem:** Architect was working alone (no specialist help)

**Solution:**
- Added Scribr as collaborative agent: `agents=[scribr]`
- Division of labor:
  - **Architect:** Structure and flow
  - **Scribr:** Title polishing, LLM-ism detection
  - **User:** Vision and final decisions

**Benefit:**
- Mirrors the successful "old" `outline_creator` PHASE 5 pattern
- Agents have focused roles (Separation of Concerns)
- Better quality output (specialist review)

### 4. Version-Aware Iteration
**Observation:** Users naturally create multiple versions during brainstorming

**Solution:**
- Instructions explicitly support version workflow:
  - "Compare outline_v1 and outline_v4"
  - "Read outline_v3 and help me fix weak sections"
- Architect respects meta-commentary (`*Target Emotion: Relief*`)
- Saves with versioning: `outline_v5.md` vs final `outline.md`

**Benefit:**
- Matches real creative workflow
- User maintains control of version history
- Enables comparative analysis

### 5. Playground Event Handling
**Technical:** ADK event stream needs careful filtering

**Solution:**
```python
# Filter out system/framework events
if not hasattr(event, "content") or not event.content:
    continue

# Store content after validation
content = event.content

# Only process model responses
if not hasattr(content, "role") or content.role != "model":
    continue

# Check parts exists before iterating
if hasattr(content, "parts") and content.parts is not None:
    for part in content.parts:
        # Process text and function_call parts
```

**Benefit:**
- No type errors
- Clean tool usage display: `🔧 Agent is using tool: read_draft_tool`
- Proper separation of model responses from system events

---

## ⚠️ Challenges & Solutions

### 1. Instructions Overwhelming LLM
- **Problem:** Too many details, edge cases, and examples
- **Solution:** Cut 15 lines, focused on core loop
- **Lesson:** LLMs perform better with focused, simple instructions

### 2. Architect Working Alone
- **Problem:** Missing the specialist polishing step
- **Solution:** Added `agents=[scribr]` to enable collaboration
- **Lesson:** Multi-agent systems need explicit collaboration patterns

### 3. Terminal Paste Infinite Loop
- **Problem:** Large text input caused buggy terminal behavior
- **Solution:** Prioritized file reading tools
- **Lesson:** File-based workflows are more robust than stdin for complex inputs

### 4. Type Warnings in Event Handling
- **Problem:** `content.parts` could be `None`, causing type errors
- **Solution:** Added null check: `content.parts is not None`
- **Lesson:** Always guard against optional fields before iteration

---

## 🎯 Key Principles Reinforced

1. **Interactive Partner > Automation**
   - The Architect collaborates, doesn't replace the user
   - User drives the conversation, agent responds

2. **Simple First**
   - Start with minimal complexity
   - Add only what's needed
   - Ruthlessly remove overwhelming details

3. **Division of Labor**
   - Agents should have clear, focused roles
   - Specialist agents (Scribr) help generalists (Architect)
   - User remains the decision-maker

4. **File-Based Workflow**
   - More reliable than terminal I/O for complex content
   - Supports versioning naturally
   - Easier to debug and review

5. **Team > Solo**
   - Multi-agent collaboration produces better results
   - Each agent has a specialty (structure vs style)
   - Mirrors successful patterns from legacy code

---

## 📝 Implementation Details

### Files Created/Modified

```
blogger/
  ├── playground.py                 # Created - Interactive CLI
  ├── step_agents/
  │   └── architect.py              # Created - Outline agent
  ├── instructions/
  │   └── architect.md              # Created - Simple, focused prompt
  └── tools.py                      # Modified - Added read_file_tool
```

### Key Code Patterns

**Agent with Tools and Sub-Agents:**
```python
architect = Agent(
    model="gemini-3-pro-preview",
    name="architect",
    instruction=read_instructions("architect.md"),
    tools=[read_draft_tool, read_file_tool, save_step_tool],
    agents=[scribr],  # Collaboration
)
```

**Playground Event Handling:**
```python
for event in runner.run_async(...):
    if not event.content or content.role != "model":
        continue
    if content.parts is not None:
        for part in content.parts:
            # Handle text and function_call
```

---

## 🚀 Next Steps

Ready for **Phase 2: The Butcher (Step 2)** 🔪

- **2.1 Splitter Tool:** Deterministic content splitting (outline → sections)
- **2.2 Integration:** Connect Architect output to Butcher input

**Key Difference:** Step 2 is **tool-based** (deterministic logic), not agent-based.

---

## 🔗 Related Docs

- `AGENTS.md` - Architecture philosophy
- `learning/plans/reframe_step_1.md` - Original plan for this phase
- `learning/PROGRESS.md` - Current status tracker
