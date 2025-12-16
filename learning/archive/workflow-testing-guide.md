# Workflow Testing Guide

**Created:** December 15, 2025
**Status:** Reference document for testing multi-agent workflows
**Related:** Task 2.2 (Organization), lessons/2.2-organizing.md

---

## 📚 Official ADK Testing Patterns

Based on the official `examples/blog-writer` reference:

### Pattern 1: ADK CLI (Recommended for Development)

The simplest approach - no Runner/Session boilerplate needed!

```bash
# Interactive CLI
adk run blogger

# Web UI (best for visual testing)
adk web .

# With custom session storage
adk run blogger --session_service_uri="sqlite://sessions.db"
```

**Requirements:**
- `blogger/__init__.py` must export `app` (App object) OR `root_agent` (Agent object)
- ADK CLI handles Runner and Session automatically

**Example `__init__.py`:**
```python
# Option A: Export App (recommended)
from google.adk.apps import App
from blogger.workflow import orchestrator

app = App(
    name="ai_blog_partner",  # Must be valid Python identifier
    root_agent=orchestrator,
)

# Option B: Export agent directly (simpler)
from blogger.workflow import orchestrator as root_agent
__all__ = ["root_agent"]
```

---

### Pattern 2: Programmatic Testing (For Automated Tests)

Use Runner + InMemorySessionService for scripted tests.

**From `examples/blog-writer/tests/test_agent.py`:**

```python
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types
from blogger.workflow import orchestrator

async def main():
    # 1. Create session service
    session_service = InMemorySessionService()

    # 2. Create session FIRST
    await session_service.create_session(
        app_name="app",
        user_id="test_user",
        session_id="test_session"
    )

    # 3. Create runner
    runner = Runner(
        agent=orchestrator,
        app_name="app",
        session_service=session_service
    )

    # 4. Run queries
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text="Your prompt")]
        ),
    ):
        # Process events
        if event.is_final_response() and event.content:
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())
```

**Key Points:**
- Session must be created BEFORE calling `runner.run_async()`
- `app_name` must match between session creation and Runner
- Use `event.is_final_response()` to filter agent responses

---

## 🐛 Issues Discovered During Testing

### Issue 1: Orchestrator Doesn't Save Files

**Problem:**
The orchestrator agent processes content but doesn't call `save_step_tool` to persist outputs.

**Root Cause:**
Orchestrator instructions were too vague - "Output: X" was interpreted as "mention the output" not "save to file".

**Solution Applied:**
Made tool calls impossible to miss in orchestrator instructions:

```markdown
**IMMEDIATELY after robust_outline_step completes:**
→ Call save_step_tool with parameters: (blog_id, "outlines", session.state["blog_outline"])
→ Verify the tool returns {"status": "success"}
→ Report to user: "✅ Saved: outputs/<blog_id>/outlines.md"
```

Added **"CRITICAL - File Saving Pattern"** section with 5-step protocol.

**Files Modified:**
- `blogger/instructions/orchestrator.md` - Explicit save instructions with verification
- `blogger/workflow.py` - Now uses instruction file instead of inline f-string

**Status:** ✅ **FIXED** - Files are now saved immediately after each sub-agent completes

---

### Issue 2: Session State Not Properly Set

**Problem:**
`draft_loader` and `content_splitter` agents with `output_key` didn't properly populate session state with correct data types.

**Root Cause:**
- `draft_loader`: Used `read_draft_tool` which returns a dict `{"status": "success", "content": "..."}`, but `output_key` only captures final text response
- `content_splitter`: LLM output JSON text, but ADK stored it as a string instead of a parsed dict

**Solution Applied:**
Converted both agents to custom `BaseAgent` classes:

```python
class DraftLoaderAgent(BaseAgent):
    async def _run_async_impl(self, ctx):
        # Call read_draft_tool directly
        result = read_draft_tool(blog_id)
        # Extract content and set session state manually
        ctx.session.state["raw_draft"] = result.get("content", "")
        yield Event(...)

class ContentSplitterAgent(BaseAgent):
    async def _run_async_impl(self, ctx):
        # Call LLM with structured prompt
        response = await ctx.client.aio.models.generate_content(...)
        # Parse JSON and set session state as dict
        result = json.loads(llm_output)
        ctx.session.state["content_split"] = {
            "draft_ok": str(result["draft_ok"]),
            "draft_not_ok": str(result["draft_not_ok"])
        }
        yield Event(...)
```

**Files Modified:**
- `blogger/step_agents/step_1_outline.py` - Replaced simple Agents with custom BaseAgents

**Status:** ✅ **FIXED** - Session state now properly set with correct types

---

### Issue 3: Agents Skip Ahead / Poor Coordination

**Problem:**
Sub-agents (Scribr, content_splitter) performed multiple steps instead of completing their single task and returning control.

**Root Cause:**
1. Agents were too proactive and tried to be "helpful"
2. Orchestrator instructions didn't enforce sequential execution with pauses
3. Sub-agents lacked clear scope boundaries

**Solution Applied:**

**Part A: Constrain Sub-Agent Scope**

Added **"CONSTRAINTS (CRITICAL)"** section to `scribr.md` and inline prompts for custom agents:

```markdown
**CRITICAL RULES:**
1. Do ONLY what you're asked - Never jump ahead to future steps
2. No autonomous workflow - Wait for coordinator to request next action
3. One task at a time - Complete current request, then stop
4. No file operations - You process content, coordinators handle files
5. Return control immediately - Once your task is complete, stop
```

**Part B: Strengthen Orchestrator Control**

Added **"CRITICAL - Sequential Execution"** and **"CRITICAL - Interactive Mode"** sections:

```markdown
**CRITICAL - Interactive Mode:**
1. This is an INTERACTIVE workflow - you are a PARTNER, not an autonomous pipeline
2. PAUSE at ALL checkpoints to ask user for input or approval
3. When instructions say "PAUSE AND WAIT", you MUST stop and wait for user response
4. NEVER auto-proceed through multiple sub-steps without user approval
```

Added explicit pause points:
- After outline creation: Ask for approval
- After split content: Ask for approval
- After Step 1 complete: Ask if user wants Step 2

**Files Modified:**
- `blogger/instructions/scribr.md` - Added CONSTRAINTS section
- `blogger/instructions/orchestrator.md` - Added sequential execution rules and interactive checkpoints
- `blogger/step_agents/step_1_outline.py` - Added constraints to inline prompts

**Status:** ✅ **FIXED** - Agents now stay in scope and orchestrator pauses for approval

---

### Issue 4: Sub-Agent Parent Conflicts

**Problem:**
Cannot use same agent (e.g., `scribr`) as sub-agent in multiple places.

**Error:**
```
ValidationError: Agent `scribr` already has a parent agent,
current parent: `outline_creator`, trying to add: `organizer`
```

**Root Cause:**
ADK enforces single-parent hierarchy - each agent can only have one parent.

**Solution (Applied):**
Remove agents from places where they're not needed:

```python
# ❌ Wrong - scribr used in multiple places
outline_creator = Agent(sub_agents=[scribr])
organizer = Agent(sub_agents=[scribr])
orchestrator = Agent(sub_agents=[scribr, ...])

# ✅ Correct - scribr only where truly needed
outline_creator = Agent(sub_agents=[scribr])
organizer = Agent(sub_agents=[])  # Doesn't need scribr
orchestrator = Agent(sub_agents=[
    # scribr is already a sub-agent of outline_creator
    # Don't duplicate here
])
```

**Alternative - Clone Pattern:**
If you truly need the same functionality in multiple places, create separate instances:

```python
# Create factory function
def create_scribr_agent():
    return Agent(
        name="scribr",
        instruction=read_instructions("scribr.md"),
        # ...
    )

# Use separate instances
scribr_for_outline = create_scribr_agent()
scribr_for_organization = create_scribr_agent()
```

**Status:** ✅ Fixed - Removed scribr from organizer and orchestrator

---

### Issue 5: google_search Tool Not Supported

**Problem:**
Model `gemini-2.5-flash` doesn't support the `google_search` tool.

**Error:**
```
400 INVALID_ARGUMENT: Tool use with function calling is unsupported
```

**Root Cause:**
Not all models support all tools. Flash models have limited tool support.

**Solution (Applied):**
Temporarily disabled google_search:

```python
# blogger/workflow.py
tools=[
    FunctionTool(read_draft_tool),
    FunctionTool(save_step_tool),
    # google_search,  # Disabled - not supported by gemini-2.5-flash
],
```

**Long-term Solution:**
Use appropriate models for different steps:

```python
# For steps needing search: use gemini-3-pro-preview
research_agent = Agent(
    model="gemini-3-pro-preview",  # Supports google_search
    tools=[google_search],
)

# For simple coordination: use gemini-2.5-flash
orchestrator = Agent(
    model="gemini-2.5-flash",  # Fast, no search needed
    tools=[FunctionTool(save_step_tool)],
)
```

**Status:** ✅ Workaround applied - Need to restore for Step 3

---

## ✅ What Actually Works

### Working: Multi-Agent Execution

**Evidence:**
Agents successfully coordinated (orchestrator → scribr → outline_creator → validators)

**Output:**
```
[scribr]: Created outline and organized content
[outline_creator]: Generated structured outline
[outline_validator]: ✅ Outline validation passed: 5 sections found
```

**Takeaway:**
The multi-agent architecture works! Coordination just needs refinement.

---

### Working: LoopAgent Quality Control

**Evidence:**
Validators ran and checked quality (even though they failed due to missing data)

**Output:**
```
[outline_validator]: ❌ Outline validation failed: outline is empty
[outline_validator]: ❌ Outline validation failed: missing Introduction section
```

**Takeaway:**
LoopAgent + BaseAgent validation pattern is functional. Just need to fix data flow.

---

### Working: ADK CLI Integration

**Evidence:**
Both `adk run` and `adk web` successfully launched the app.

**Output:**
```
Running agent ai_blog_partner, type exit to exit.
[user]: [outline_creator]: Based on the raw draft provided...
```

**Takeaway:**
Official ADK patterns work perfectly - simpler than custom Runner scripts!

---

## 🎯 Testing Checklist

Before marking workflow as production-ready:

### Functional Tests
- [ ] **Files are saved**: `save_step_tool` creates outputs/{blog_id}/*.md
- [ ] **Session state works**: `output_key` values accessible by next agents
- [ ] **Sequential execution**: Steps run in order (1 → 2 → 3...)
- [ ] **Validation works**: LoopAgents retry on failure
- [ ] **Content preserved**: No hallucinated additions, no lost content

### Integration Tests
- [ ] **ADK CLI works**: `adk run blogger` completes workflow
- [ ] **Web UI works**: `adk web .` provides visual interface
- [ ] **Full pipeline**: Can process real blog draft end-to-end

### Quality Tests
- [ ] **Outline quality**: 3+ sections, intro/conclusion present
- [ ] **Content integrity**: All draft content accounted for
- [ ] **Structure alignment**: Organized draft matches outline

---

## 📖 Recommended Testing Workflow

### Phase 1: Quick Validation (Use ADK Web)
```bash
adk web . --port 8000
# Open http://localhost:8000
# Send: "Execute Step 1 for blog_id: my-ai-journey-2"
# Visually inspect outputs
```

**Why:** Fastest feedback loop, easiest debugging

---

### Phase 2: Automated Testing (Use Runner Script)
```python
# tests/test_full_workflow.py
async def test_step_1():
    runner = Runner(...)
    async for event in runner.run_async(...):
        # Collect events

    # Assert files created
    assert (OUTPUTS_DIR / "my-ai-journey-2" / "outlines.md").exists()

    # Assert session state
    session = await session_service.get_session(...)
    assert "blog_outline" in session.state
```

**Why:** Regression testing, CI/CD integration

---

### Phase 3: Manual End-to-End (Use ADK CLI)
```bash
adk run blogger

# At prompts, paste test queries:
> Execute Step 1 for blog_id: my-ai-journey-2
> (verify outputs)
> Execute Step 2
> (verify outputs)
```

**Why:** Full integration test with human oversight

---

## 🔗 References

**Official ADK Docs:**
- [Runtime & Sessions](https://google.github.io/adk-docs/runtime/)
- [Testing Agents](https://google.github.io/adk-docs/testing/)

**Official Examples:**
- `examples/blog-writer/` - Multi-agent blog writing system
- `examples/blog-writer/tests/test_agent.py` - Runner test pattern

**Project Lessons:**
- `learning/lessons/2.1-loopagent.md` - LoopAgent patterns
- `learning/lessons/2.2-organizing.md` - Multi-agent architecture
- `learning/PROGRESS.md` - Current task status

---

## 💡 Key Learnings

1. **ADK CLI is simpler than custom Runner scripts** - Use `adk web` for development
2. **Session state is not magic** - Requires proper agent output formatting
3. **Coordination requires explicit instructions** - LLMs won't infer workflow boundaries
4. **Tool calls must be explicit** - "Output: X" ≠ "Call save_step_tool(X)"
5. **Agent hierarchy is strict** - One parent per agent, no sharing

---

## 🚀 Current Testing & Debugging Workflow

**Status:** All major issues fixed! Steps 1 & 2 are functional.

### Quick Test (Recommended)

```bash
# Terminal 1: Start the interactive CLI
adk run blogger

# When prompted, enter:
Execute Step 1 for blog_id: my-ai-journey-2

# Follow the interactive prompts:
# 1. Provide previous blog URLs (or say "no")
# 2. Review and approve the outline
# 3. Wait for content split to complete
# 4. Decide whether to proceed to Step 2
```

**Expected Outputs:**
- ✅ Files created: `outputs/my-ai-journey-2/outlines.md`, `draft_ok.md`, `draft_not_ok.md`
- ✅ Interactive pauses at checkpoints
- ✅ Explicit approval requests before proceeding
- ✅ Clear status messages with file paths

---

### Debugging Checklist

If something goes wrong:

**1. Check ADK Logs**
```bash
# View latest log
tail -F /tmp/agents_log/agent.latest.log

# Or specific session log
tail -F /tmp/agents_log/agent.YYYYMMDD_HHMMSS.log
```

**2. Verify File Structure**
```bash
# Check inputs exist
ls -la inputs/my-ai-journey-2/draft.md

# Check outputs were created
ls -la outputs/my-ai-journey-2/
```

**3. Check Session State (Programmatic Test)**
```bash
# Run the programmatic test (shows session state)
python tests/test_workflow.py
```

**4. Common Issues**

| Issue | Solution |
|-------|----------|
| "No raw_draft found" | `draft_loader` failed - check blog_id in conversation history |
| "Content split incomplete" | `content_splitter` failed - check JSON parsing in logs |
| Files not saved | Check `save_step_tool` calls in orchestrator output |
| Agent jumps ahead | Review agent instructions for CONSTRAINTS section |

---

### Architecture Documentation

**File Structure (Updated December 15, 2025):**

```
blogger/
├── instructions/
│   ├── orchestrator.md      # NEW: Workflow coordination instructions
│   ├── scribr.md             # Updated: Added CONSTRAINTS section
│   ├── linguist.md
│   └── organizer.md
├── step_agents/
│   ├── step_1_outline.py     # Updated: Custom BaseAgent classes
│   └── step_2_organize.py
├── validation_checkers.py    # Quality control validators
├── validation_utils.py       # Pure validation functions
├── agents.py                 # Scribr and Linguist definitions
├── tools.py                  # File I/O tools
└── workflow.py               # Updated: Uses instruction file

tests/
├── test_validation_utils.py  # Unit tests for validators
└── test_workflow.py          # NEW: Programmatic workflow test
```

**Key Patterns Used:**

1. **Custom BaseAgent for Session State**
   - `DraftLoaderAgent` - Loads draft and sets `raw_draft`
   - `ContentSplitterAgent` - Splits content and sets `content_split` dict

2. **Instruction Files**
   - All agent instructions in separate `.md` files
   - Loaded via `read_instructions(filename)`
   - Easier to iterate on prompts

3. **Interactive Workflow**
   - Multiple pause checkpoints
   - User approval required between major steps
   - Clear status messages and file paths

---

### Next Steps

1. ✅ **Step 1 & 2 Complete** - Outline creation and organization working
2. ⏸️ **Step 3: Drafting & Research** - Implement section expansion with Scribr
3. ⏸️ **Step 4: Polishing** - Implement No-Hype checker
4. ⏸️ **Step 5 & 6** - Finalization and illustration ideation

**To Test Steps 1 & 2:**
```bash
adk run blogger
# Then: Execute Step 1 for blog_id: my-ai-journey-2
# Then: (approve outline)
# Then: Execute Step 2
```
