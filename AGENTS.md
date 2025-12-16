# AGENTS.md

This file provides guidance to Claude Code or Gemini CLI when working with code in this repository.

## Project Overview

**AI Blog Partner** is a system designed to help users transform raw thoughts/drafts into polished technical articles.
**Core Philosophy:** "Interactive Co-Pilot". The AI does not run a black-box loop. It collaborates with the user at key checkpoints.

## Development Protocol: Teacher/Student

- **Teacher (AI):** Guide, Explain, Plan, Review.
- **Student (Human):** Implement, Verify, Learn.

**Strict Adherence:** We build one small, testable piece at a time. We do not move forward until the current piece is verified working.

## New Architecture: The "Interactive Partner"

We have moved away from complex `LoopAgents` and rigid state machines. The new workflow is linear and interactive.

### The 3-Step Core

1.  **Step 1: The Architect (Outline)**
    *   **Goal:** Create a solid structure.
    *   **Input:** Raw Draft (`draft.md`).
    *   **Process:** Conversational brainstorming. User critiques, Agent iterates.
    *   **Output:** `outline.md` (Approved by user).

2.  **Step 2: The Butcher (Split)**
    *   **Goal:** Organize content.
    *   **Input:** `draft.md` + `outline.md`.
    *   **Process:** Deterministic splitting (Tool-based).
    *   **Output:** `sections/01_intro.md`, `sections/02_body.md`, etc.

3.  **Step 3: The Writer (Expand & Polish)**
    *   **Goal:** High-quality prose.
    *   **Input:** Specific `section_X.md`.
    *   **Process:** Iterative writing/editing on a per-section basis.
    *   **Output:** Polished section.

## Coding Standards

### 1. Agents
- **Simple is better.** Agents should generally be simple `GenAI` wrappers or basic ADK Agents.
- **Instructions:** Instructions live in `blogger/instructions/*.md`. Keep them focused on *role* and *tone*, not complex procedural logic.

### 2. Tools
- **Pure Functions.** Tools should be easy to test without an LLM.
- **Return Dicts.** Always return `{"status": "success", "data": ...}` or `{"status": "error", "message": ...}`.

### 3. Testing
- **Interactive Playground:** We verify Agent behavior by talking to them in a `playground.py` script.
- **Unit Tests:** We verify Tool logic (splitting, file I/O) with standard `pytest`.

## File Structure

```
blogger/
  ├── agents.py            # Base agent definitions (Scribr, Linguist)
  ├── tools.py             # File operation tools
  ├── playground.py        # INTERACTIVE TESTING SCRIPT (The new entrypoint)
  ├── instructions/        # Agent system prompts
  └── step_agents/         # specific logic for the 3 steps
       ├── architect.py    # Step 1
       ├── butcher.py      # Step 2
       └── writer.py       # Step 3
```

## Git Workflow
- Commit often.
- Reference the Task ID from `learning/PROGRESS.md`.