# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) or Gemini CLI when working with code in this repository.

## Project Overview

**AI Blog Partner** is a multi-agent system built with **Google ADK (Agent Development Kit)** to transform raw technical blog drafts into polished, authentic articles. The system uses a "partner" relationship with two specialized AI agents: Scribr (Senior Technical Writer) and Linguist (English Language Coach).

See **README.md** for project vision, architecture, and detailed workflow steps.

## Development Protocol: Teacher/Student

This project follows a **strict Teacher/Student protocol**:
- **Teacher (You/Claude Code/Gemini CLI):** Explain concepts, provide specs, give tasks, check code, and guide learning
- **Student (Human):** Writes code to prove understanding

**Strict Adherence to Steps:** Each enumerated step in 'The Process' below requires explicit confirmation or action from the **Student** (human) before the **Teacher** (AI) proceeds to the next step. The Teacher will *never* move ahead without the Student's explicit instruction or approval.

**The Process:**
1. You give the student a specific coding task with context and guidance
2. Student writes the code
3. You review it and provide feedback
4. If correct, check the box ✅ in `learning/PROGRESS.md` and create/update lesson file

**Your Role as Teacher:**
1. **Give guided tasks** - use task plans in `learning/plans/` as curricula
2. **Check their code** - review for correctness and adherence to patterns
3. **Update learning files** - check boxes, create lesson files (see `learning/GUIDE.md` for protocol)
4. **Teach step-by-step** - don't implement yourself, guide them through implementation
5. **Provide feedback** - explain what's right/wrong and why

**Learning File Structure:**
- `learning/PROGRESS.md` - Lightweight status tracker (~50 lines)
- `learning/plans/` - Detailed plan for CURRENT task only
- `learning/lessons/` - Completed lessons (reference material)
- `learning/GUIDE.md` - Full documentation protocol

**See:** `learning/GUIDE.md` for complete update protocol

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
# ✅ Correct - returns dict with status
def read_draft_tool(blog_id: str) -> dict:
    try:
        content = Path(...).read_text()
        return {"status": "success", "content": content, "path": str(path)}
    except Exception as e:
        return {"status": "error", "message": f"Failed to read: {e}"}

# ❌ Wrong - returns string, no error handling
def read_draft(blog_id: str) -> str:
    return Path(...).read_text()
```

**Key ADK Concepts:**
- **Workflows are natural language:** Agent `instruction` parameter describes steps as text, not Python code
- **Sub-agents as specialists:** Scribr and Linguist are invoked by the orchestrator when needed
- **State management:** Agents communicate via `output_key` and `context.session.state`
- **Tool wrapping:** Python functions wrapped with `FunctionTool()` for automatic schema generation

### Tool Creation Guidelines (Golden Rules)

**1. Docstrings are User Manuals:**
- LLM reads docstrings to understand tool usage
- Describe WHAT the tool does (action), not HOW it's implemented
- Include when/why to use the tool
- Provide clear examples of arguments

**2. Error Handling via Dicts:**
- Return `{"status": "success", ...}` for successful operations
- Return `{"status": "error", "message": "Actionable description"}` for failures
- Make error messages actionable (tell agent how to fix)
- Never raise exceptions - ADK framework expects dict returns

**3. Consistent Return Structure:**
```python
# ✅ Correct - with error handling
def read_draft_tool(blog_id: str) -> dict:
    """
    Retrieves the raw draft content for a blog post.

    Use this to load the initial draft markdown file that needs
    to be processed through the blog writing pipeline.

    Args:
        blog_id: Unique identifier for the blog (e.g., "my-ai-journey-2")

    Returns:
        Success: {"status": "success", "content": "...", "path": "..."}
        Error: {"status": "error", "message": "Actionable error description"}
    """
    draft_path = INPUTS_DIR / blog_id / draft_filename
    if not draft_path.exists():
        return {
            "status": "error",
            "message": f"Draft not found for '{blog_id}'. Check inputs/{blog_id}/draft.md exists"
        }

    try:
        content = Path(draft_path).read_text()
        return {"status": "success", "content": content, "path": str(draft_path)}
    except Exception as e:
        return {"status": "error", "message": f"Failed to read draft: {e}"}

# ❌ Wrong - raises exceptions, no status dict
def read_draft(blog_id: str) -> str:
    if not path.exists():
        raise FileNotFoundError("Not found")
    return Path(...).read_text()
```

**4. Tool Granularity:**
- Create focused tools for specific tasks (e.g., `read_draft_tool`, `save_step_tool`)
- Avoid monolithic, complex functions
- Each tool should do one thing well

**5. Tools vs. Agents - Clear Separation:**
- **Tools are mechanical:** File I/O, API calls, calculations, data transformations
- **Agents are intelligent:** Semantic analysis, content understanding, decision-making, reasoning
- If a tool would need to "understand" content or make judgment calls, that work belongs in an agent
- Example: Splitting a draft based on semantic matching to an outline = agent work, not tool work

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

4. **Validation Agents** (`blogger/validation_checkers.py`)
   - Custom `BaseAgent` validators for quality control
   - Used in LoopAgent pattern for automatic retries
   - `OutlineValidationChecker` - validates outline structure
   - `ContentSplitValidationChecker` - validates content integrity

### Validation & Quality Control Patterns

**LoopAgent Pattern (The Polisher):**
```python
from google.adk.agents import LoopAgent

robust_outline_step = LoopAgent(
    name="robust_outline_step",
    sub_agents=[
        outline_creator,           # Worker: creates the outline
        OutlineValidationChecker   # Validator: checks quality
    ],
    max_iterations=3  # Retry up to 3 times
)
```

**Execution Flow:**
1. Worker agent produces output → writes to session state
2. Validator agent checks quality
   - If valid → `Event(actions=EventActions(escalate=True))` → exits loop ✅
   - If invalid → `Event(author=self.name)` → retry (back to step 1) 🔄
3. Repeat until valid OR max_iterations reached

**BaseAgent Validator Pattern:**
```python
from google.adk.agents import BaseAgent
from google.adk.events import Event, EventActions

class OutlineValidationChecker(BaseAgent):
    async def _run_async_impl(self, ctx):
        # Call pure function for validation logic
        is_valid, reasons = check_outline_structure(
            ctx.session.state.get("blog_outline", "")
        )

        if is_valid:
            # ✅ Quality passed - exit loop
            yield Event(
                author=self.name,
                actions=EventActions(escalate=True)  # Signal: STOP LOOP
            )
        else:
            # ❌ Quality failed - continue loop (retry)
            yield Event(
                author=self.name,
                content=types.Content(parts=[
                    types.Part(text=f"Validation failed: {', '.join(reasons)}")
                ])
            )
```

**Validation Utils Pattern:**
- Extract validation logic to pure functions in `blogger/validation_utils.py`
- Keep validators thin (just ADK integration)
- Enable easy unit testing without mocking ADK runtime

```python
# blogger/validation_utils.py (pure functions - easy to test)
def check_outline_structure(outline_text: str) -> tuple[bool, list[str]]:
    """Check outline has required structure."""
    # Validation logic here
    return is_valid, reasons

# blogger/validation_checkers.py (ADK integration)
from blogger.validation_utils import check_outline_structure

class OutlineValidationChecker(BaseAgent):
    async def _run_async_impl(self, ctx):
        is_valid, reasons = check_outline_structure(...)  # Use pure function
        # Yield appropriate Event
```

**Why Separate Utils:**
- ✅ Easy to unit test (no ADK mocking needed)
- ✅ Reusable across validators
- ✅ No async complexity for logic
- ✅ Clear separation: business logic vs. framework integration

### Testing Patterns

**Test-Driven Development:**
- Write comprehensive unit tests for all validation logic
- Aim for 100% code coverage
- Test edge cases: empty input, whitespace, case sensitivity, duplicates

**Project Testing Structure:**
```
tests/
├── __init__.py
└── test_validation_utils.py  # Unit tests for pure functions
```

**Running Tests:**
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=blogger --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=blogger --cov-report=html
```

**Test Organization:**
```python
import pytest
from blogger.validation_utils import normalize_and_split

class TestNormalizeAndSplit:
    """Group related tests in classes."""

    def test_splits_by_double_newline(self):
        """Descriptive test names."""
        text = "Intro\n\nBody\n\nConclusion"
        result = normalize_and_split(text)
        assert result == {"intro", "body", "conclusion"}

    def test_empty_string(self):
        """Test edge cases."""
        result = normalize_and_split("")
        assert result == set()
```

**Dependencies:**
```bash
pip install pytest pytest-cov  # Add to requirements
```

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

**See README.md** for complete workflow details with inputs/outputs/actions for each step.

**Current Status:** Phase 2.1 complete (Step 1 implementation). Check **learning/PROGRESS.md** for roadmap.

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

- **learning/PROGRESS.md:** Current roadmap status, completed tasks, learned concepts
- **README.md:** Project vision, architecture, and 6-step workflow
- **learning/lessons/*.md:** Completed lessons and reference material
- **inputs/examples/blog-writer/:** Official Google ADK example (reference for patterns)

## Important Constraints

1. **No Documentation Files:** Never create markdown files proactively (except when explicitly requested by the Teacher)
2. **Error Handling via Dicts:** Return `{"status": "error", "message": "..."}` for failures, never raise exceptions from tools
3. **No Over-Engineering:** Implement only what's requested in the current lesson
4. **Prefer Editing:** Always edit existing files rather than creating new ones unless required
5. **Follow the Protocol:** Wait for Teacher's task specification before coding

## Git Workflow

- Main branch: `main`
- Commit messages should reference completed tasks (e.g., "Implement Task 1.3.1: Tool return types")
- Use Claude Code / Gemini CLI commit co-authorship footer when committing code

## Model Selection

- **Scribr/Linguist:** `gemini-3-pro-preview` (complex reasoning, writing quality)
- **Orchestrator:** `gemini-2.5-flash` (workflow coordination, faster)
- See Google's [Gemini Models](https://ai.google.dev/gemini-api/docs/models) for capabilities
