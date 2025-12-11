# Lesson 3: Workflow Skeleton & ADK Orchestration Patterns

## 🎯 Learning Objectives

By the end of this lesson, you will understand:
1. **ADK Orchestration Pattern**: How to structure multi-agent workflows using Google ADK
2. **Agent Composition**: Main agent with `sub_agents` vs. class-based orchestrators
3. **Tool Integration**: How to expose Python functions as agent tools via `FunctionTool`
4. **State Management**: How agents communicate via `output_key` and session state
5. **Workflow Instructions**: Describing complex pipelines in natural language

---

## 📚 Concepts from the Official Example

### Pattern 1: Agent-Based Orchestration (Not Class-Based)

**What we learned:**
```python
# ❌ NOT the ADK way (our first attempt)
class BlogWorkflow:
    def __init__(self, blog_id):
        self.blog_id = blog_id

    def run(self):
        self.step_1()
        self.step_2()

# ✅ The ADK way
orchestrator = Agent(
    name="orchestrator",
    model="gemini-2.5-flash",
    instruction="You manage a pipeline with these steps: ...",
    sub_agents=[agent1, agent2],
    tools=[FunctionTool(my_tool)],
)
```

**Why?** ADK agents are declarative and LLM-driven. The workflow is described in natural language, and the agent decides when to call sub-agents and tools.

---

### Pattern 2: Tools Return Dicts

**From the example:**
```python
def save_blog_post_to_file(blog_post: str, filename: str) -> dict:
    """Saves the blog post to a file."""
    with open(filename, "w") as f:
        f.write(blog_post)
    return {"status": "success"}  # ← Always return dict
```

**Why?** ADK tools communicate results via structured data. The dict is added to the agent's context.

---

### Pattern 3: Sub-Agents as Specialists

**From the example:**
```python
interactive_blogger_agent = Agent(
    name="interactive_blogger_agent",
    sub_agents=[
        robust_blog_writer,    # Specialist for writing
        robust_blog_planner,   # Specialist for planning
        blog_editor,           # Specialist for editing
        social_media_writer,   # Specialist for social posts
    ],
)
```

**Our mapping:**
- We have `scribr` (Writer) and `linguist` (Coach)
- The orchestrator delegates to them for specific tasks

---

### Pattern 4: Workflow as Natural Language

**From the example:**
```python
instruction="""
Your workflow is as follows:
1. **Plan:** Generate outline using `robust_blog_planner` tool.
2. **Refine:** Iterate with user feedback.
3. **Write:** Use `robust_blog_writer` tool.
4. **Edit:** Revise based on feedback.
...
"""
```

**Our mapping:**
- We describe our 6-step pipeline in the orchestrator's `instruction`
- Each step mentions which sub-agent or tool to use

---

### Pattern 5: FunctionTool Wrapper

**From the example:**
```python
from google.adk.tools.function_tool import FunctionTool

interactive_blogger_agent = Agent(
    tools=[
        FunctionTool(save_blog_post_to_file),
        FunctionTool(analyze_codebase),
    ],
)
```

**Why?** `FunctionTool` automatically:
- Parses function signatures
- Generates JSON schema for the LLM
- Handles parameter validation

---

## 📝 Your Coding Tasks

### Task 1.3.1: Update `blogger/tools.py` to Return Dicts

**Current state:**
```python
def read_draft(blog_id: str) -> str:
    # Returns string

def save_step_output(blog_id: str, step_name: str, content: str) -> None:
    # Returns None
```

**Your task:** Refactor these functions to follow ADK conventions:

1. Rename `read_draft` → `read_draft_tool`
2. Change return type to `dict`
3. Return a dict with keys: `{"draft_content": ..., "blog_id": ..., "path": ...}`

Do the same for `save_step_output` → `save_step_output_tool`

**Example:**
```python
def read_draft_tool(blog_id: str) -> dict:
    """Reads the raw draft file for a given blog."""
    draft_path = INPUTS_DIR / blog_id / DRAFT_FILENAME

    if not draft_path.exists():
        raise FileNotFoundError(f"Draft not found: {draft_path}")

    with open(draft_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {
        "draft_content": content,
        "blog_id": blog_id,
        "path": str(draft_path),
    }
```

---

### Task 1.3.2: Add a `split_draft_tool` Function

**Purpose:** This tool will be used in Step 1 to split the draft into `draft_ok.md` and `draft_not_ok.md`.

**Your task:** Write a function with this signature:
```python
def split_draft_tool(blog_id: str, draft_content: str, outline: str) -> dict:
    """
    Splits draft into content matching outline (ok) and unused content (not_ok).

    For now, this is a PLACEHOLDER - just save the full draft as draft_ok.
    Full splitting logic will be implemented in Phase 2.1.

    Returns:
        dict with keys:
            - status: "success"
            - draft_ok_path: Path to draft_ok.md
            - draft_not_ok_path: Path to draft_not_ok.md
    """
```

**Implementation hint:**
- Create output directory: `OUTPUTS_DIR / blog_id`
- Save `draft_content` to `draft_ok.md`
- Save a placeholder message to `draft_not_ok.md`
- Return paths as strings in the dict

---

### Task 1.3.3: Create `blogger/workflow.py`

**Your task:** Create a new file with an orchestrator agent.

**Structure:**
```python
"""
AI Blog Partner - Workflow Orchestrator
"""

import datetime
from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.google_search_tool import google_search

from blogger.agents import scribr, linguist
from blogger.tools import read_draft_tool, save_step_output_tool, split_draft_tool


orchestrator = Agent(
    name="orchestrator",
    model="gemini-2.5-flash",
    description="Manages the 6-step blog writing pipeline",
    instruction=f"""
    You are the AI Blog Partner Orchestrator...

    ## Your Workflow

    **Step 1: Draft to Outlines**
    - Use `read_draft_tool` to load draft
    - Collaborate with Scribr (scribr sub-agent) to create outline
    - Use `split_draft_tool` to separate content
    - Save outlines.md, draft_ok.md, draft_not_ok.md

    **Step 2: Organization**
    ...

    (Continue for all 6 steps)

    Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
    """,
    sub_agents=[
        scribr,
        linguist,
    ],
    tools=[
        FunctionTool(read_draft_tool),
        FunctionTool(save_step_output_tool),
        FunctionTool(split_draft_tool),
        google_search,
    ],
)
```

**Key points:**
1. Write a detailed workflow description in the `instruction` parameter
2. Reference tools by name (e.g., "Use `read_draft_tool`")
3. Reference sub-agents by name (e.g., "Collaborate with Scribr")
4. Include current date for time-aware behavior

---

## ✅ Validation Checklist

Before you submit your code:

- [ ] All tools return `dict` (not `str` or `None`)
- [ ] Tool names end with `_tool` for clarity
- [ ] `split_draft_tool` creates both `draft_ok.md` and `draft_not_ok.md`
- [ ] `orchestrator` agent references all tools via `FunctionTool()`
- [ ] `orchestrator` instruction describes all 6 steps clearly
- [ ] Sub-agents (`scribr`, `linguist`) are in the `sub_agents` list

---

## 🧠 Concepts to Master

After implementing this lesson, you should be able to explain:

1. **Why agents orchestrate instead of Python classes:** ADK agents are LLM-driven and can handle user interaction, retries, and dynamic flow without explicit control flow code.

2. **Tool return values:** Tools return dicts because the agent needs structured data to decide next actions and build context.

3. **Declarative workflow:** The `instruction` text is a prompt for the LLM. It's not executed linearly like Python code - the agent interprets it.

4. **Sub-agent delegation:** When the orchestrator sees "use scribr sub-agent," it invokes Scribr as a separate agent with its own context, then receives the result.

---

## 🚀 Next Steps (Phase 2)

Once this skeleton is complete, we'll implement:
- **Phase 2.1:** Full logic for Step 1 (outline creation + smart draft splitting)
- **Phase 2.2:** Step 2 (content reorganization)
- **Phase 2.3:** Step 3 (iterative section writing loop)

But for now, the skeleton provides the structure!

---

## 📖 Reference

- Example studied: `inputs/examples/blog-writer/`
- Key files reviewed:
  - `blogger_agent/agent.py` (orchestrator pattern)
  - `blogger_agent/tools.py` (tool functions returning dicts)
  - `blogger_agent/sub_agents/blog_planner.py` (sub-agent pattern)

---

Ready to code? Start with **Task 1.3.1** and work your way through! 🎓
