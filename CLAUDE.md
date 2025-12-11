# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AI Blog Partner** is a multi-agent system built with **Google ADK (Agent Development Kit)** to transform raw technical blog drafts into polished, authentic articles. The system uses a "partner" relationship with two specialized AI agents: Scribr (Senior Technical Writer) and Linguist (English Language Coach).

See **README.md** for project vision and **AGENTS.md** for detailed agent personas and workflow architecture.

## Development Protocol: Teacher/Student

This project follows a **strict Teacher/Student protocol**:
- **Teacher (You/Claude Code):** Explain concepts, provide specs, give tasks, check code, and guide learning
- **Student (Human):** Writes code to prove understanding

**The Process:**
1. You give the student a specific coding task with context and guidance
2. Student writes the code
3. You review it and provide feedback
4. If correct, check the box ✅ in PROGRESS.md roadmap and record what they learned in "Learned Concepts"

**Your Role as Teacher:**
1. **Give guided tasks** - use `LESSON_*.md` files as teaching curricula
2. **Check their code** - review for correctness and adherence to patterns
3. **Update PROGRESS.md** - check boxes when tasks complete, add learned concepts
4. **Teach step-by-step** - don't implement yourself, guide them through implementation
5. **Provide feedback** - explain what's right/wrong and why

## Architecture

### Google ADK Patterns (Critical)

This project follows official ADK conventions. **Do NOT use class-based orchestrators or imperative workflows.**

**Agent-Based Orchestration (Not Classes):**
```python
# ✅ Correct: Declarative agent with sub-agents
orchestrator = Agent(
    name="orchestrator",
    instruction="Your workflow: 1. Do X using tool_a 2. Do Y with sub_agent...",
    sub_agents=[scribr, linguist],
    tools=[FunctionTool(my_tool)],
)

# ❌ Wrong: Imperative class orchestrator
class Workflow:
    def run(self):
        self.step_1()
        self.step_2()
```

**Tool Functions Return Dicts:**
```python
# ✅ Correct
def read_draft_tool(blog_id: str) -> dict:
    content = Path(...).read_text()
    return {"draft_content": content, "path": str(path)}

# ❌ Wrong
def read_draft(blog_id: str) -> str:
    return Path(...).read_text()
```

**Key ADK Concepts:**
- **Workflows are natural language:** Agent `instruction` parameter describes steps as text, not Python code
- **Sub-agents as specialists:** Scribr and Linguist are invoked by the orchestrator when needed
- **State management:** Agents communicate via `output_key` and `context.session.state`
- **Tool wrapping:** Python functions wrapped with `FunctionTool()` for automatic schema generation

### Multi-Agent System

**Three-Agent Architecture:**

1. **Orchestrator** (`blogger/workflow.py`)
   - Manages the 6-step pipeline
   - Delegates to Scribr and Linguist
   - Handles file I/O via tools

2. **Scribr** (`blogger/agents.py`)
   - Senior Technical Writer Partner
   - Instructions in `blogger/instructions/scribr.md`
   - Responsible for: brainstorming, structuring, drafting, editing
   - Enforces "No-Hype" and authenticity rules
   - Model: `gemini-3-pro-preview`

3. **Linguist** (`blogger/agents.py`)
   - English Language Coach
   - Instructions in `blogger/instructions/linguist.md`
   - **Constraint:** Only focuses on language mechanics, never style/content
   - Provides educational feedback on grammar patterns
   - Model: `gemini-3-pro-preview`

### Agent Instructions Pattern

**Agent instructions are stored as separate Markdown files** (`blogger/instructions/`), not inline strings:

```python
def read_instructions(filename: str) -> str:
    current_dir = Path(__file__).parent
    instruction_path = current_dir / "instructions" / filename
    return instruction_path.read_text()

scribr = Agent(
    instruction=read_instructions("scribr.md"),  # Not inline!
)
```

**Why:**
- Keeps Python code clean
- Allows prompt iteration without code changes
- Uses `Path(__file__).parent` for portability

### File Structure Conventions

**Directory Layout:**
```
inputs/<blog_id>/          # User's raw drafts
  └── draft.md             # Entry point for each blog

outputs/<blog_id>/         # Generated artifacts
  ├── outlines.md          # Step 1: Approved outline
  ├── draft_ok.md          # Step 1: Content matching outline
  ├── draft_not_ok.md      # Step 1: Unused content
  ├── draft_organized.md   # Step 2: Reorganized content
  ├── draft_nice.md        # Step 3: Expanded sections
  ├── draft_polished.md    # Step 4: No-Hype check applied
  └── final.md             # Step 5: Ready to publish

blogger/
  ├── agents.py            # Agent definitions (Scribr, Linguist)
  ├── tools.py             # File operation tools
  ├── workflow.py          # Orchestrator agent
  └── instructions/        # Agent system prompts (Markdown)
```

**Path Construction:**
- Use `Path(__file__).parent.parent` to navigate from module to project root
- Define constants: `INPUTS_DIR = CURRENT_DIR / "inputs"`
- Use `/` operator for path composition: `INPUTS_DIR / blog_id / "draft.md"`
- Safe directory creation: `path.mkdir(parents=True, exist_ok=True)`

## Six-Step Pipeline

The system transforms drafts through: Draft to Outlines → Organization → Drafting & Research → Polishing → Finalization → Illustration (optional).

**See AGENTS.md** for complete workflow details with inputs/outputs/actions for each step.

**Current Status:** Phase 1 complete (Agents + Tools defined). Phases 2-3 are placeholders. Check **PROGRESS.md** for roadmap.

## Environment Setup

See **README.md** for setup instructions. Key points:
- Virtual environment: `.venv`
- Main dependency: `google-adk`
- API key stored in `blogger/.env`

## Working with Agent Instructions

Agent instructions are in `blogger/instructions/*.md` files. See those files for full personas and rules.

**Key constraint:** Linguist focuses ONLY on language mechanics, never style/content.

**When modifying instructions:**
- Edit Markdown files directly (`blogger/instructions/*.md`)
- No code changes needed - agents read instructions at runtime
- Use clear headings (`##`) and few-shot examples

## Key References

- **PROGRESS.md:** Current roadmap status, completed tasks, learned concepts
- **AGENTS.md:** Full agent personas, responsibilities, and workflow architecture
- **LESSON_*.md:** Step-by-step teaching guides for implementing features
- **inputs/examples/blog-writer/:** Official Google ADK example (reference for patterns)

## Important Constraints

1. **No Documentation Files:** Never create markdown files proactively (except when explicitly requested by the Teacher)
2. **Minimal Error Handling:** Only check file existence and raise descriptive exceptions
3. **No Over-Engineering:** Implement only what's requested in the current lesson
4. **Prefer Editing:** Always edit existing files rather than creating new ones unless required
5. **Follow the Protocol:** Wait for Teacher's task specification before coding

## Git Workflow

- Main branch: `main`
- Commit messages should reference completed tasks (e.g., "Implement Task 1.3.1: Tool return types")
- Use Claude Code commit co-authorship footer when committing code

## Model Selection

- **Scribr/Linguist:** `gemini-3-pro-preview` (complex reasoning, writing quality)
- **Orchestrator:** `gemini-2.5-flash` (workflow coordination, faster)
- See Google's [Gemini Models](https://ai.google.dev/gemini-api/docs/models) for capabilities
