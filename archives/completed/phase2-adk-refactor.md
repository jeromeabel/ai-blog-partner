# Phase 2: ADK Pattern Refactoring - Learning Notes

**Date:** 2024-12-17
**Status:** Complete ✅
**Learning Goal:** Understand and implement proper ADK Agent patterns

---

## What We Built

### Before (Hybrid Anti-Pattern)
```python
# ❌ BAD: Tools calling LLM directly with genai.Client()
def filter_scope_tool(blog_id: str) -> dict:
    draft = read_file(...)
    outline = read_file(...)

    # Tool does LLM reasoning internally
    client = genai.Client()
    response = client.models.generate_content(...)

    # Tool saves results
    save_file(...)
```

**Problems:**
- Low-level `genai.Client()` bypasses ADK patterns
- No conversation history, error handling, or agent features
- Tools doing "thinking" instead of just I/O
- Not following official ADK examples

### After (Proper ADK Pattern)
```python
# ✅ GOOD: Tools are pure I/O and validation
def validate_content_split_tool(original, part1, part2) -> dict:
    """Pure validation function"""
    is_valid, error = check_content_integrity(original, part1, part2)
    return {"valid": is_valid, "message": error}

# ✅ GOOD: Agent does the thinking
curator = Agent(
    model="gemini-2.0-flash-exp",
    tools=[
        read_draft_tool,
        save_step_tool,
        validate_content_split_tool,  # Agent validates its own work
    ],
    instruction="""
    You are The Curator. Read the draft and outline, then:
    1. Analyze each paragraph (YOU do this thinking)
    2. Split into in-scope vs out-of-scope (YOU decide)
    3. Validate your split with validate_content_split_tool
    4. Save using save_step_tool
    """
)
```

**Benefits:**
- Agent does LLM reasoning (as intended)
- Tools provide capabilities (read, validate, save)
- Follows official ADK architecture
- Clear separation of concerns

---

## Architecture Comparison

### Official ADK Example Pattern
From `/examples/blog-writer/blogger_agent/`:

```python
# tools.py - Simple I/O functions
def save_blog_post_to_file(content: str, filename: str) -> dict:
    with open(filename, "w") as f:
        f.write(content)
    return {"status": "success"}

# agent.py - Agent uses tools
blog_writer = Agent(
    model="gemini-3-pro-preview",
    tools=[FunctionTool(save_blog_post_to_file)],
    instruction="Write a blog post and save it using the tool"
)
```

**Pattern:** Tools = I/O, Agents = Thinking

### Our New Implementation
```python
# tools.py - Pure I/O + Validation
def validate_content_split_tool(...) -> dict:
    # Pure function, no LLM
    return {"valid": True/False, "message": "..."}

# curator.py - Agent uses validation tools
curator = Agent(
    model="gemini-2.0-flash-exp",
    tools=[
        FunctionTool(read_draft_tool),
        FunctionTool(validate_content_split_tool),
        FunctionTool(save_step_tool),
    ],
    instruction="Filter content, validate your work, then save"
)
```

**Same pattern!** We now match the official architecture.

---

## Key Learnings

### 1. **Tools Should Be "Dumb"**
Tools provide capabilities without decision-making:
- ✅ Read files
- ✅ Save files
- ✅ Validate data (pure functions)
- ❌ Call LLM internally
- ❌ Make decisions

### 2. **Agents Should Be "Smart"**
Agents use tools to accomplish goals:
- Agent reads draft → analyzes content → splits it → validates → saves
- Agent has conversation history and context
- Agent can retry, explain reasoning, ask for clarification

### 3. **Validation Tools Are Pure Functions**
```python
def validate_organization_tool(draft_ok, outline, organized):
    # No LLM, no I/O - just data validation
    integrity_ok = check_reorganization_integrity(...)
    heading_ok = check_heading_order(...)
    return {"valid": integrity_ok and heading_ok, ...}
```

This lets the agent **validate its own work** before saving.

### 4. **Instructions Guide Agent Behavior**
The `curator.md` instructions tell the agent:
- **What to do:** "Filter content into in-scope vs out-of-scope"
- **How to use tools:** "Validate with validate_content_split_tool"
- **When to checkpoint:** "Wait for user confirmation"

The agent interprets instructions and uses tools to execute.

---

## Files Modified

### Created
- ✅ `blogger/step_agents/curator.py` - Curator agent definition
- ✅ `blogger/instructions/curator.md` - Agent instructions (1300 lines!)
- ✅ `blogger/tools_phase2.py` - Validation tools (temporary)

### Modified
- ✅ `blogger/tools.py` - Added validation tool imports + functions
- ✅ `blogger/playground.py` - Added curator to agent map

### Deprecated (Left in place, but not used)
- `filter_scope_tool` (old version with internal LLM)
- `organize_content_tool` (incomplete stub)
- `_llm_filter_content` (internal LLM helper)

**Note:** Old tools still exist in `tools.py` for reference, but curator uses new validation tools instead.

---

## The Curator Agent Workflow

### Phase 2.1: Filter Scope
1. Agent reads draft and outline with `read_draft_tool`, `read_file_tool`
2. **Agent analyzes** each paragraph (LLM reasoning)
3. **Agent decides** which content is in-scope vs out-of-scope
4. Agent validates split with `validate_content_split_tool`
5. Agent saves with `save_step_tool`
6. Agent presents results and waits for user checkpoint

### Phase 2.2: Organize Content
1. Agent reads `draft_ok` and `outline`
2. **Agent matches** paragraphs to outline sections (LLM reasoning)
3. **Agent reorganizes** content under correct headings
4. Agent validates with `validate_organization_tool`
5. Agent saves with `save_step_tool`
6. Agent presents organized result

**Key:** Agent does all the "thinking", tools provide "capabilities"

---

## Testing Approach

### Integration Testing
```bash
python -m blogger.playground --agent curator
```

**Test script:**
```
You: Filter content for blog_id: test-post
# Agent will:
# 1. Read draft + outline
# 2. Split content (agent reasoning)
# 3. Validate split
# 4. Save draft_ok.md + draft_not_ok.md
# 5. Present results

You: Yes, proceed with organizing
# Agent will:
# 1. Read draft_ok + outline
# 2. Reorganize content (agent reasoning)
# 3. Validate organization
# 4. Save draft_ok_organized.md
# 5. Present final result
```

### Unit Testing
Validation functions can be tested independently:
```python
def test_validate_content_split():
    original = "A\n\nB\n\nC"
    part1 = "A\n\nB"
    part2 = "C"

    result = validate_content_split_tool(original, part1, part2)
    assert result["valid"] == True
```

---

## Comparison to Other Patterns

### Pattern 1: Simple Agent (No Internal Helpers)
```python
# Agent does everything, tools are just I/O
agent = Agent(tools=[read_tool, save_tool])
```
**Our choice:** ✅ This is what we implemented

### Pattern 2: Sub-Agents (Official Example)
```python
# Main agent delegates to specialized sub-agents
root_agent = Agent(
    sub_agents=[blog_planner, blog_writer, blog_editor],
    tools=[save_tool]
)
```
**Not needed yet:** Curator is simple enough to be a single agent

### Pattern 3: LoopAgent (Official Example)
```python
# Agent retries with validation checker
robust_agent = LoopAgent(
    sub_agents=[worker_agent, ValidationChecker],
    max_iterations=3
)
```
**Not needed yet:** We abandoned LoopAgent in favor of user checkpoints

---

## What's Next: Phase 3 (The Writer)

With the proper ADK pattern established:

1. **Writer agent** will be even simpler:
   - Read `draft_ok_organized.md`
   - Polish each section (agent does writing)
   - Save with `save_step_tool`

2. **No validation tools needed:**
   - Writing is subjective (no right/wrong)
   - User reviews the polished content directly

3. **Pattern consistency:**
   - Tools = I/O (read, save)
   - Agent = Thinking (writing, polishing)

---

## Mistakes and How We Fixed Them

### Mistake 1: Following Legacy Code
**Problem:** The old implementation used `genai.Client()` directly in tools
**Fix:** Studied official ADK examples, refactored to proper pattern

### Mistake 2: Over-Engineering
**Problem:** Considered creating internal helper agents within tools
**Fix:** Simplified - let the main agent do the work, tools just validate

### Mistake 3: Not Checking Official Examples
**Problem:** Didn't compare to `/examples/blog-writer/` initially
**Fix:** Read official code, saw the simple pattern, adopted it

---

## Key Takeaways

1. **When in doubt, check official examples**
   - `/examples/blog-writer/` shows the canonical pattern
   - Tools are simple I/O functions
   - Agents do the LLM reasoning

2. **Validation tools are a middle ground**
   - Pure functions (no LLM)
   - Agent uses them to check its own work
   - Escalates to user if validation fails

3. **Instructions are powerful**
   - `curator.md` is 250+ lines of guidance
   - Tells agent WHAT to do, not HOW (that's the agent's job)
   - Emphasizes constraints (preserve content, validate before saving)

4. **ADK vs genai.Client()**
   - `genai.Client()` = Low-level SDK
   - `Agent` = High-level with history, error handling, tool use
   - Always prefer `Agent` unless you need raw control

---

## Metrics

**Code Quality:**
- Removed 80+ lines of LLM helper functions from tools
- Added 2 pure validation functions (60 lines)
- Net: Simpler, cleaner architecture

**Complexity:**
- Before: Tools = 200 lines (with LLM logic)
- After: Tools = 120 lines (pure I/O + validation)
- Curator agent: 30 lines (ADK boilerplate)
- Curator instructions: 250 lines (clear guidance)

**Testability:**
- Before: Hard to test (LLM in tools)
- After: Easy to test (pure validation functions)

---

## Next Steps

1. ✅ **Done:** Refactored Phase 2 to ADK pattern
2. **Next:** Test curator in playground with real draft
3. **After:** Build Phase 3 (Writer) using same pattern
4. **Later:** Clean up old tools (remove deprecated filter_scope_tool)

---

**Lesson:** When adopting a new framework, always study official examples first. Don't carry over anti-patterns from previous codebases. The ADK way is: **Tools = Capabilities, Agents = Intelligence**.
