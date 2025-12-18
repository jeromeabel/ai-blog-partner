# AI Blog Partner - LLM Development Guide

This file guides all LLM agents (Gemini/Claude) working on the **AI Blog Partner** project.

---

## 🌟 Core Protocol: "The Interactive Partner"

This is **NOT** an automated content factory. It's a collaborative learning environment:

**Roles:**
- **AI (Teacher):** Plan, Review, Explain, Guide. *Never implement silently.*
- **Human (Student):** Write code, Run tests, Make decisions.
- **Workflow:** Small testable increments. No automation without approval.

---

## 🏗️ Architecture: 3-Step Linear Workflow

### Step 1: Architect (Draft → Outline)
- **Goal:** Collaborative outline creation through brainstorming
- **Agent:** `blogger/agents/architect.py` + `scribr.py` (title polishing)
- **Output:** `posts/{blog_id}/1-outline.md`

### Step 2: Curator (Outline → Organized Sections)
- **Goal:** Filter and organize draft content into outline structure
- **Agent:** `blogger/agents/curator.py`
- **Process:**
  1. **Filter:** Split into "In-Scope" vs "Out-of-Scope"
  2. **Organize:** Match In-Scope content to sections
  3. **Validate:** Check integrity (no content lost)
- **Output:** `posts/{blog_id}/2-draft_organized.md`

### Step 3: Writer (Sections → Polished Post)
- **Goal:** Iterative section polishing with user feedback
- **Agent:** `blogger/agents/writer.py` + `scribr.py` (text polishing)
- **Output:** `posts/{blog_id}/3-final.md`

---

## 🛠️ Coding Standards

### 1. Agents (`blogger/agents/`)
- **Location:** Co-locate code (`agent.py`) + instructions (`agent.md`)
- **Simplicity:** Prefer simple ADK Agent wrappers over complex loops
- **Testing:** Use `blogger/playground.py` for interactive testing

### 2. Tools (`blogger/utils/tools.py`)
- **Purity:** Pure functions (I/O or validation) with **NO LLM calls**
- **Pattern:** Agents do reasoning, tools provide capabilities
- **Return:** Always `{"status": "success", "data": ...}` or `{"status": "error", "message": ...}`
- **Example:** `validate_content_split_tool` checks integrity, doesn't decide what to filter

### 3. Testing
- **Interactive:** `python -m blogger.playground --agent <name>`
- **Unit:** `pytest blogger/tests/ -v`
- **Full workflow:** `adk web` (conversational UI)

---

## 🔄 Development Workflow: The Protocol

### Planning: One Plan Per Phase

**AI (Teacher) creates a single phase plan:**
1. Check `progress/PROGRESS.md` for next phase
2. Create `progress/plans/phaseX_<name>.md` with:
   - **Goal & Architecture** (what we're building, key decisions)
   - **Implementation Checklist** (tasks with checkboxes: `- [ ]`)
   - **Testing Strategy** (unit + integration tests)
   - **References** (related lessons, legacy code)
3. Present plan to Human for approval
4. Update plan based on feedback

**Target length:** ~250-300 lines per phase plan

**Plan Template:**
```markdown
# Phase X: [Name] - Implementation Plan

**Status:** Planning | In Progress | Complete

## 🎯 Goal
[What we're building and why]

## 🏗️ Architecture
[Agent design, tool design, key decisions]

## 📋 Implementation Checklist
### Task 1: [Name]
- [ ] Subtask A
- [ ] Subtask B

### Task 2: [Name]
- [ ] Subtask A

## 🧪 Testing Strategy
[Unit tests, integration tests]

## 📚 References
[Links to lessons, legacy code]
```

### Implementation: Iterative Execution

**AI (Teacher) guides:**
1. Read active plan from `progress/plans/phaseX_<name>.md`
2. Identify next unchecked task
3. Explain what Human should implement
4. Review code after Human writes it
5. Check off task in plan: `- [x]` when complete
6. Never implement code yourself

**Human (Student) executes:**
1. Write code (one file at a time)
2. Run tests (pytest for tools, playground for agents)
3. Tell AI when task done

**Plan is a living document:** Update checkboxes in real-time as work progresses.

### Completion: Archive & Document

**When phase complete:**
1. AI marks all tasks complete in plan: `**Status:** Complete`
2. AI moves plan to `archives/completed/phaseX_<name>.md`
3. AI creates lesson in `progress/lessons/phaseX_<name>.md` (what we learned)
4. Human reviews and approves lesson
5. AI updates `progress/PROGRESS.md` phase checkboxes

**Golden Rule:** AI never implements silently. Always explain, then wait for human to code.

---

## 📁 Quick Reference

### Key Files
```
blogger/
├── coordinator.py         # ADK app entry (adk run/web)
├── playground.py          # Interactive agent testing
├── agents/                # Agents (code + instructions)
│   ├── architect.py/.md   # Step 1
│   ├── curator.py/.md     # Step 2
│   ├── scribr.py/.md      # Style enforcer
│   └── ...
├── utils/
│   ├── tools.py           # Pure I/O/validation tools
│   └── text_utils.py      # Text processing
└── tests/                 # pytest unit tests

posts/{blog_id}/
├── draft.md               # User input
├── 1-outline.md           # Step 1 output
├── 2-draft_organized.md   # Step 2 output
└── 3-final.md             # Step 3 output

progress/
├── PROGRESS.md            # Current status
├── plans/                 # Phase plans (one per phase)
│   └── phaseX_name.md
└── lessons/               # Completed phase lessons
```

### Common Commands
```bash
# Test agent
python -m blogger.playground --agent architect

# Run full workflow
adk web              # Visual UI
adk run blogger      # CLI

# Run tests
pytest blogger/tests/ -v
```

---

## 📚 Documentation Links

- **AGENTS.md** (this file) - LLM development guide
- **README.md** - User-facing guide (installation, usage)
- **progress/PROGRESS.md** - Current roadmap & status
- **archives/** - Historical lessons & deprecated code

---

## Current Status

See `progress/PROGRESS.md` for latest status.
