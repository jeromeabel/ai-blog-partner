# Learning System Guide

## 👨‍🏫 Teacher/Student Protocol

### Roles
- **Teacher (Claude Code, Gemini):** Explains concepts, provides specs, gives tasks, checks code, guides learning
- **Student (You):** Writes code to prove understanding

**Strict Adherence to Steps:** The Teacher (AI) will strictly follow the enumerated steps in 'Process' below. Each step, including all code modifications, test implementations, and task completions, requires explicit confirmation and approval from the **Student** (human) before the Teacher proceeds. The Teacher will *never* take the next action without the Student's clear instruction or validation.

### Process
1. Teacher gives specific coding task with context and guidance
2. Student writes the code
3. Teacher reviews and provides feedback
4. If correct → check box ✅ in roadmap, record learned concepts
5. Move to next task

### Goal
Learn by doing. Every completed task adds new concepts to your knowledge base.

---

**Quick Start:**
1. Check current status → Read `PROGRESS.md`
2. See current task → Read `plans/task_X_X_plan.md`
3. Review concepts → Browse `lessons/` folder
4. Understand protocol → Read this file

---

## 📚 File Organization

This `learning/` folder contains all student materials for the Teacher/Student protocol. These files are **separate from project documentation** and can be archived when learning is complete.

### Directory Structure

```
learning/
├── GUIDE.md              # This file - explains the learning system
├── PROGRESS.md           # Lightweight status tracker
├── lessons/              # Detailed concepts from COMPLETED tasks
│   ├── 1.1-agents.md
│   ├── 1.2-tools.md
│   ├── 1.3-workflow.md
│   └── 2.1-loopagent.md
└── plans/                # Detailed plan for CURRENT task only
    └── task_2_2_plan.md
```

---

## 🎯 File Purposes

### PROGRESS.md (Status Tracker)
**Purpose:** Quick reference for current status and roadmap
- Current active task
- Roadmap with checkboxes (what's done, what's next)
- Links to detailed lesson files
- **Max length:** ~50 lines (intentionally lightweight)

**When to read:** Start of session, when checking what's next

**When to update:**
- Start new task → update "Active Task"
- Complete task → check roadmap box ✅
- Complete task → add link to lesson file

### plans/ (Current Task Plans)
**Purpose:** Detailed implementation plan for the task you're CURRENTLY working on
- Architecture decisions with rationale
- Step-by-step implementation guide
- Session state flow
- Acceptance criteria checklist
- **Lifecycle:** Created when task starts, archived when task completes

**When to read:** Throughout current task implementation

**When to update:**
- Task start → create plan file
- Make architecture decision → document it
- Complete subtask → check acceptance criteria
- Task complete → move to archive (or delete)

### lessons/ (Completed Concepts)
**Purpose:** Reference material for concepts you've already learned
- Deep explanations of patterns and principles
- "Why" things work, not just "what" to implement
- Examples and best practices
- **Lifecycle:** Created when task completes, permanent reference

**When to read:**
- When you need to remember how something works
- Before similar tasks (review related patterns)
- When reviewing for understanding

**When to update:**
- Task complete → extract learned concepts from plan
- Never update old lessons (they're historical record)

---

## 🔄 Documentation Update Protocol

### During a Task Session

| Event | File to Update | What to Update |
|-------|---------------|----------------|
| **Start new task** | `PROGRESS.md` | Set "Active Task" and status |
| | `plans/task_X_X_plan.md` | Create new plan file |
| **Make architecture decision** | Current plan file | Document decision + rationale |
| **Complete subtask** | Current plan file | Check acceptance criteria box |
| **Complete entire task** | `PROGRESS.md` | Check roadmap box ✅ |
| | `PROGRESS.md` | Add link to lesson file |
| | `lessons/X_X-name.md` | Create lesson with learned concepts |
| | Current plan file | Archive or delete |

### What NOT to Update
- ❌ Don't update project README.md during learning (it's for users/contributors)
- ❌ Don't keep adding to lesson files (they're snapshots of what you learned)
- ❌ Don't duplicate content across files (each file has distinct purpose)

---

## 📂 Separation: Learning vs Project Docs

### Learning Materials (this folder)
- **Audience:** You (the student)
- **Purpose:** Teaching, tracking, understanding
- **Lifecycle:** Temporary (can be archived after learning)
- **Location:** `learning/`

### Project Documentation
- **Audience:** Users, contributors, future developers
- **Purpose:** Project overview, architecture, API docs
- **Lifecycle:** Permanent (part of the project)
- **Location:** Root files README.md and `docs/` (if created)

---

## 🎓 Tips for Effective Learning

1. **Read the plan file at task start** - Understand the goal before coding
2. **Update as you go** - Don't batch documentation at the end
3. **Write concepts in your own words** - Best way to solidify understanding
4. **Review previous lessons** - Refresh related patterns before similar tasks
5. **Keep PROGRESS.md light** - It's a tracker, not a textbook
6. **Archive completed plans** - Don't clutter the plans/ folder

---

## 🔗 Related Files

- **Root:** `CLAUDE.md` - Instructions for Claude Code (references this guide)
- **Project Docs:** `README.md` - Project documentation
- **Source:** `blogger/` - Implementation code
- **Protocol:** `UPDATE_PROTOCOL.md` - When to update which files (detailed workflow)
