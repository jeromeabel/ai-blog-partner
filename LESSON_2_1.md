# Lesson 2.1: Draft to Outlines with LoopAgent Pattern

## 🎯 What You'll Learn

By completing this lesson, you will master:

1. **LoopAgent Orchestration** - Wrap worker agents with validators for automatic quality retries
2. **BaseAgent Validation** - Create custom quality checkers that signal loop termination via `escalate=True`
3. **Session State Management** - Use `output_key` for agent communication and `context.session.state` for data flow
4. **Multi-Agent Composition** - Break complex workflows into focused, reusable sub-agents
5. **ADK Official Patterns** - Follow Google's documented best practices for robust agent systems

**Official ADK Documentation:**
- [Loop Agents](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)
- [Custom Agents (BaseAgent)](https://google.github.io/adk-docs/agents/custom-agents/)
- [Events & EventActions](https://google.github.io/adk-docs/events/)

---

## 📋 Your Tasks

You will implement **Step 1: Draft to Outlines** by creating **three files**:

### Task 2.1.1: `blogger/validation_checkers.py`

Create two `BaseAgent` validators that check quality and signal LoopAgent termination:

**1. `OutlineValidationChecker`**
- ✅ Checks if `blog_outline` exists in session state
- ✅ Validates 3+ markdown sections (`## ` headings)
- ✅ Requires "Introduction" and "Conclusion" sections
- ✅ Returns `Event(actions=EventActions(escalate=True))` if valid → exits loop
- ✅ Returns `Event(author=self.name, content=...)` if invalid → continues loop

**2. `ContentSplitValidationChecker`**
- ✅ Checks if both `draft_ok` and `draft_not_ok` exist in session state
- ✅ Validates combined length ≈ original draft (within ±10%)
- ✅ Returns `Event(actions=EventActions(escalate=True))` if valid
- ✅ Returns `Event(author=self.name, content=...)` if invalid

### Task 2.1.2: `blogger/step_agents/step_1_outline.py`

Create four agents for Step 1 workflow:

**1. `outline_creator` (Worker Agent)**
- Uses Scribr as sub-agent
- Reads draft with `read_draft_tool`
- Creates structured outline
- Sets `output_key="blog_outline"`
- Model: `gemini-3-pro-preview`

**2. `content_splitter` (Worker Agent)**
- Uses Scribr as sub-agent
- Splits draft into matching/unused content
- Sets `output_key="content_split"` (dict with `draft_ok`, `draft_not_ok`)
- Model: `gemini-3-pro-preview`

**3. `robust_outline_step` (LoopAgent)**
- Wraps `[outline_creator, OutlineValidationChecker]`
- Max iterations: 3
- Auto-retries on quality failure

**4. `robust_content_split_step` (LoopAgent)**
- Wraps `[content_splitter, ContentSplitValidationChecker]`
- Max iterations: 2
- Auto-retries on quality failure

### Task 2.1.3: Update `blogger/workflow.py`

Integrate the new agents into the orchestrator:

- ✅ Import `robust_outline_step` and `robust_content_split_step`
- ✅ Add both to `orchestrator.sub_agents` list
- ✅ Update orchestrator instruction to reference the new agents
- ✅ Document session state keys (`blog_outline`, `content_split`, `raw_draft`)

---

## 🧠 Key Concepts

### 1. LoopAgent: The Polisher Pattern

From [ADK Loop Agents docs](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/):

> "The LoopAgent executes its sub-agents in a loop (iteratively). The loop stops if the optional max_iterations is reached, or if any sub-agent returns an Event with escalate=True."

**The Pattern:**
```
┌─────────────────────────────────────┐
│     LoopAgent (max_iterations=3)    │
│                                     │
│  1️⃣ Worker Agent → Creates Output   │
│         ↓                           │
│  2️⃣ Validator → Checks Quality      │
│         ↓                           │
│    ✅ Valid? → escalate=True → EXIT │
│    ❌ Invalid? → RETRY (back to 1️⃣) │
└─────────────────────────────────────┘
```

**Example:**
```python
from google.adk.agents import LoopAgent

robust_outline_step = LoopAgent(
    name="robust_outline_step",
    sub_agents=[
        outline_creator,          # Does the work
        OutlineValidationChecker  # Checks quality
    ],
    max_iterations=3  # Safety limit
)
```

### 2. BaseAgent + escalate: Loop Termination Signal

From [ADK Custom Agents docs](https://google.github.io/adk-docs/agents/custom-agents/):

> "A Custom Agent inherits from `google.adk.agents.BaseAgent` and implements `_run_async_impl`."

From [ADK Events docs](https://google.github.io/adk-docs/events/):

> "`escalate` is a boolean flag that signals a loop should terminate."

**Validation Checker Template:**
```python
from typing import AsyncGenerator
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.genai import types

class OutlineValidationChecker(BaseAgent):
    """Validates outline quality for LoopAgent termination."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        outline = ctx.session.state.get("blog_outline", "")

        # Validate quality criteria
        is_valid = self._check_quality(outline)

        if is_valid:
            # ✅ Quality passed - exit loop
            yield Event(
                author=self.name,
                content=types.Content(parts=[
                    types.Part(text="Validation passed: 4 sections found")
                ]),
                actions=EventActions(escalate=True)  # Signal: STOP LOOP
            )
        else:
            # ❌ Quality failed - continue loop (retry)
            yield Event(
                author=self.name,
                content=types.Content(parts=[
                    types.Part(text="Outline incomplete: only 2 sections, need 3+")
                ])
                # No escalate - signals: CONTINUE LOOP
            )
```

### 3. Session State: The Notebook 📓

**How Workers Write to State (Automatic):**
```python
outline_creator = Agent(
    name="outline_creator",
    output_key="blog_outline",  # Agent's output → state["blog_outline"]
    ...
)
```

**How Validators Read from State (Manual):**
```python
async def _run_async_impl(self, ctx: InvocationContext):
    outline = ctx.session.state.get("blog_outline", "")  # Read what worker wrote
    draft = ctx.session.state.get("raw_draft", "")       # Read other data
```

**State Keys for Step 1:**
- `raw_draft` - Original draft content
- `blog_outline` - Generated outline (from `outline_creator`)
- `content_split` - Dict with `draft_ok` and `draft_not_ok` (from `content_splitter`)

### 4. The Four Orchestration Patterns

| Pattern | When to Use | Step 1 Usage |
|---------|-------------|--------------|
| **Sequential** | Strict step-by-step flows | outline_creator → content_splitter |
| **Parallel** | Independent tasks | Not used (steps depend on each other) |
| **Loop** | Quality control, retries | LoopAgent wraps each worker |
| **LLM-Based** | Dynamic routing | Main orchestrator decides workflow |

---

## 💻 Implementation Guide

### Step 1: Create `blogger/validation_checkers.py`

```python
"""
AI Blog Partner - Validation Checkers

BaseAgent implementations that check quality and signal LoopAgent termination
via EventActions(escalate=True).

Official ADK Docs:
- https://google.github.io/adk-docs/agents/custom-agents/
- https://google.github.io/adk-docs/events/
"""

from typing import AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.genai import types


class OutlineValidationChecker(BaseAgent):
    """
    Validates blog outline quality for LoopAgent termination.

    Per ADK docs: "The loop stops if any sub-agent returns an Event
    with escalate=True in its Event Actions."

    Quality Criteria:
    - Outline exists in session state (key: "blog_outline")
    - Has at least 3 sections (## markdown headings)
    - Contains "Introduction" section
    - Contains "Conclusion" section

    Returns:
        Event with escalate=True if valid → exits LoopAgent
        Event without escalate if invalid → continues LoopAgent
    """

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # TODO: Implement validation
        # 1. Get outline from ctx.session.state
        # 2. Count sections (lines starting with "## ")
        # 3. Check for required sections
        # 4. Yield Event with escalate=True if valid
        # 5. Yield Event with helpful message if invalid
        pass


class ContentSplitValidationChecker(BaseAgent):
    """
    Validates content split completeness for LoopAgent termination.

    Quality Criteria:
    - Both draft_ok and draft_not_ok exist in session state
    - Combined length ≈ original draft length (within ±10%)

    Returns:
        Event with escalate=True if valid → exits LoopAgent
        Event without escalate if invalid → continues LoopAgent
    """

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # TODO: Implement validation
        # 1. Get draft_ok, draft_not_ok, raw_draft from state
        # 2. Check both exist
        # 3. Compare combined length to original (±10%)
        # 4. Yield Event with escalate=True if valid
        # 5. Yield Event with helpful message if invalid
        pass
```

**Implementation Hints:**

**Counting Markdown Sections:**
```python
outline_text = ctx.session.state.get("blog_outline", "")
sections = [line for line in outline_text.split("\n") if line.startswith("## ")]
num_sections = len(sections)
```

**Checking Required Sections:**
```python
has_intro = any("intro" in s.lower() for s in sections)
has_conclusion = any("conclusion" in s.lower() for s in sections)
is_valid = num_sections >= 3 and has_intro and has_conclusion
```

**Yielding Events:**
```python
# ✅ Valid - exit loop
yield Event(
    author=self.name,
    content=types.Content(parts=[
        types.Part(text=f"Validation passed: {num_sections} sections found")
    ]),
    actions=EventActions(escalate=True)
)

# ❌ Invalid - continue loop
yield Event(
    author=self.name,
    content=types.Content(parts=[
        types.Part(text=f"Outline incomplete: only {num_sections} sections, need 3+")
    ])
)
```

**Length Validation:**
```python
original = ctx.session.state.get("raw_draft", "")
split_ok = ctx.session.state.get("draft_ok", "")
split_not_ok = ctx.session.state.get("draft_not_ok", "")

if not (split_ok and split_not_ok):
    # Missing data - continue loop
    yield Event(author=self.name, content=types.Content(parts=[
        types.Part(text="Missing draft_ok or draft_not_ok")
    ]))
    return

combined_len = len(split_ok) + len(split_not_ok)
original_len = len(original)

# Allow ±10% variance
if original_len > 0:
    variance = abs(combined_len - original_len) / original_len
    is_complete = variance <= 0.10
else:
    is_complete = False

if is_complete:
    yield Event(author=self.name, actions=EventActions(escalate=True), ...)
else:
    yield Event(author=self.name, content=types.Content(...))
```

---

### Step 2: Create `blogger/step_agents/__init__.py`

```python
# Empty file to make step_agents a package
```

---

### Step 3: Create `blogger/step_agents/step_1_outline.py`

```python
"""
AI Blog Partner - Step 1: Draft to Outlines

Worker agents and LoopAgent wrappers for creating outlines and splitting content.
"""

from google.adk.agents import Agent, LoopAgent
from google.adk.tools.function_tool import FunctionTool

from blogger.agents import scribr
from blogger.tools import read_draft_tool
from blogger.validation_checkers import (
    OutlineValidationChecker,
    ContentSplitValidationChecker,
)

# === WORKER AGENTS ===

outline_creator = Agent(
    model="gemini-3-pro-preview",
    name="outline_creator",
    description="Analyzes raw draft and creates structured blog outline",
    instruction="""
    You are working with Scribr to create a blog post outline.

    Your task:
    1. Use the `read_draft_tool` to load the raw draft content
    2. Collaborate with Scribr to analyze the draft and create a structured outline
    3. The outline should have:
       - A clear title (# heading)
       - At least 3 main sections (## headings)
       - An Introduction section
       - A Conclusion section
       - Logical flow and structure

    Output the outline in Markdown format.
    """,
    sub_agents=[scribr],
    tools=[FunctionTool(read_draft_tool)],
    output_key="blog_outline",
)

content_splitter = Agent(
    model="gemini-3-pro-preview",
    name="content_splitter",
    description="Splits draft content into matching and unused chunks",
    instruction="""
    You are working with Scribr to split the raw draft content.

    Your task:
    1. Read the `blog_outline` from session state
    2. Read the `raw_draft` from session state
    3. Collaborate with Scribr to identify:
       - Content that matches the outline structure (draft_ok)
       - Content that doesn't fit the outline (draft_not_ok)
    4. Ensure all original content is preserved (nothing lost)

    Output a dict with two keys:
    - "draft_ok": Content that aligns with the outline
    - "draft_not_ok": Unused content for later review
    """,
    sub_agents=[scribr],
    output_key="content_split",
)

# === LOOP AGENTS (Quality Control) ===

robust_outline_step = LoopAgent(
    name="robust_outline_step",
    description="Creates blog outline with automatic quality retries",
    sub_agents=[
        outline_creator,
        OutlineValidationChecker(name="outline_validator"),
    ],
    max_iterations=3,
)

robust_content_split_step = LoopAgent(
    name="robust_content_split_step",
    description="Splits content into matching/unused with validation",
    sub_agents=[
        content_splitter,
        ContentSplitValidationChecker(name="content_split_validator"),
    ],
    max_iterations=2,
)
```

---

### Step 4: Update `blogger/workflow.py`

**Add imports:**
```python
from blogger.step_agents.step_1_outline import (
    robust_outline_step,
    robust_content_split_step,
)
```

**Update orchestrator:**
```python
orchestrator = Agent(
    name="orchestrator",
    model="gemini-2.5-flash",
    description="AI Blog Partner orchestrator managing the 6-step writing pipeline",
    instruction=f"""
    You are the AI Blog Partner Orchestrator. You manage a 6-step pipeline to transform
    raw technical blog drafts into polished, authentic articles.

    You work with two specialist agents:
    - **Scribr**: A Senior Technical Writer Partner (strategist, drafter, editor)
    - **Linguist**: An English Language Coach (language mechanics only)

    ## Your Workflow

    **Step 1: Draft to Outlines**
    - Input: Raw draft from user (blog_id provided)
    - Use `robust_outline_step` to create the blog outline (auto-retries for quality)
    - Use `robust_content_split_step` to split content into matching/unused chunks
    - Use `save_step_tool` to save outputs:
      - Step "outlines" → outlines.md
      - Step "draft_ok" → draft_ok.md
      - Step "draft_not_ok" → draft_not_ok.md
    - Output: outlines.md, draft_ok.md, draft_not_ok.md

    **Step 2: Organization**
    - Input: outlines.md, draft_ok.md
    - Reorganize text chunks to match the outline structure
    - Output: draft_organized.md

    **Step 3: Drafting & Research**
    - Input: outlines.md, draft_organized.md
    - For each section:
      - Scribr expands/rewrites (use google_search for fact-checking)
      - Linguist reviews language mechanics
    - Output: draft_nice.md

    **Step 4: Polishing**
    - Input: draft_nice.md
    - Scribr applies final "No-Hype" and authenticity rules
    - Output: draft_polished.md

    **Step 5: Finalization**
    - Input: draft_polished.md
    - Format for publishing, generate SEO metadata
    - Output: final.md

    **Step 6: Illustration (Optional)**
    - Brainstorm cover art concepts
    - Output: illustration_ideas.md

    ## State Management
    - Raw draft: `raw_draft` (loaded by robust_outline_step)
    - Outline: `blog_outline` (set by robust_outline_step)
    - Content split: `content_split` (dict with draft_ok, draft_not_ok, set by robust_content_split_step)
    - Current step: `current_step`

    ## Instructions
    - Always confirm the blog_id before starting
    - Execute steps sequentially unless user specifies otherwise
    - Present outputs to user for approval between major steps
    - Use tools for all file operations

    Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
    """,
    sub_agents=[
        robust_outline_step,
        robust_content_split_step,
        scribr,
        linguist,
    ],
    tools=[
        FunctionTool(read_draft_tool),
        FunctionTool(save_step_tool),
        google_search,
    ],
)
```

---

## ✅ Acceptance Criteria

Your implementation is complete when:

### 1. File Structure
```
blogger/
├── step_agents/
│   ├── __init__.py          ✅ Created
│   └── step_1_outline.py    ✅ Created
├── validation_checkers.py   ✅ Created
├── workflow.py              ✅ Updated
├── agents.py                (unchanged)
└── tools.py                 (unchanged)
```

### 2. Code Quality
- [ ] All imports resolve without errors
- [ ] All classes/functions have docstrings
- [ ] Code follows patterns from official ADK example
- [ ] No syntax errors when importing modules

### 3. Validation Logic
- [ ] `OutlineValidationChecker` checks: 3+ sections, intro, conclusion
- [ ] `ContentSplitValidationChecker` checks: both keys exist, length within ±10%
- [ ] Both return `Event(actions=EventActions(escalate=True))` on success
- [ ] Both return `Event(author=self.name, content=...)` on failure with helpful text

### 4. Agent Configuration
- [ ] `outline_creator`: has Scribr, uses `read_draft_tool`, sets `output_key="blog_outline"`
- [ ] `content_splitter`: has Scribr, sets `output_key="content_split"`
- [ ] `robust_outline_step`: wraps outline_creator + validator, max_iterations=3
- [ ] `robust_content_split_step`: wraps content_splitter + validator, max_iterations=2

### 5. Integration
- [ ] `workflow.py` imports both LoopAgents correctly
- [ ] Orchestrator includes both in `sub_agents` list
- [ ] Orchestrator instruction references the new agents
- [ ] Session state keys documented in instruction

---

## 🧪 Testing & Review

After writing the code:

1. **Show me your code** - Paste all three files
2. **I'll review using these questions:**
   - What happens if `outline_creator` produces an invalid outline 3 times in a row?
   - Why use `output_key` instead of manually setting `context.session.state["blog_outline"]`?
   - When should you use `escalate=True` vs. returning a regular `Event`?
   - What's the difference between session state and memory?

3. **If approved:**
   - ✅ Check `[x]` for Task 2.1.1, 2.1.2, 2.1.3 in `PROGRESS.md`
   - 📝 Add learned concepts to "Learned Concepts" section
   - 🎓 Move to Lesson 2.2

---

## 📖 Reference Materials

### Official ADK Documentation
- [Loop Agents](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/) - How LoopAgent works, termination
- [Custom Agents](https://google.github.io/adk-docs/agents/custom-agents/) - BaseAgent implementation
- [Events](https://google.github.io/adk-docs/events/) - Event structure, EventActions, escalate flag

### Example Code to Study
- `inputs/examples/blog-writer/blogger_agent/validation_checkers.py` - BaseAgent pattern
- `inputs/examples/blog-writer/blogger_agent/sub_agents/blog_planner.py` - LoopAgent usage
- `inputs/examples/blog-writer/blogger_agent/agent.py` - Orchestrator structure

### Key ADK Imports
```python
from google.adk.agents import Agent, BaseAgent, LoopAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from google.adk.tools.function_tool import FunctionTool
from google.genai import types
from typing import AsyncGenerator
```

---

## 💡 Pro Tips

1. **Start with validation checkers** - Simplest to implement (pure logic, no LLM)
2. **Copy patterns from official example** - Don't reinvent, adapt their structure
3. **Test in isolation** - Manually check validation logic before integrating
4. **Read official docs** - Understand why patterns work, not just how
5. **Keep agents focused** - One responsibility per agent
6. **Helpful error messages** - Make Events descriptive for debugging

---

**Ready to start? Begin with `blogger/validation_checkers.py` and work through the three tasks. Good luck!**
