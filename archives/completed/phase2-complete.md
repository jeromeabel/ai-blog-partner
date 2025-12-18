# Phase 2: The Curator - Complete Documentation

**Date:** 2024-12-17  
**Status:** ✅ Complete  
**Key Learning:** Proper ADK Pattern - Tools = Capabilities, Agents = Intelligence

---

## Table of Contents

1. [Overview](#overview)
2. [What We Built](#what-we-built)
3. [ADK Pattern Transformation](#adk-pattern-transformation)
4. [Architecture](#architecture)
5. [Implementation Details](#implementation-details)
6. [Testing](#testing)
7. [Lessons Learned](#lessons-learned)
8. [Code Cleanup](#code-cleanup)

---

## Overview

Phase 2 involved building **The Curator** - an agent that filters and organizes draft content to match an approved outline. This phase also marked a major architectural refactor from hybrid anti-patterns to proper ADK patterns.

### The Challenge

Transform from a system where:
- ❌ Tools called LLMs internally (`genai.Client()`)
- ❌ Decision-making logic hidden in tools
- ❌ Not following official ADK examples

To a system where:
- ✅ Agents do LLM reasoning
- ✅ Tools provide pure I/O and validation
- ✅ Matches official Google ADK architecture

---

## What We Built

### 1. Validation Functions (`text_utils.py`)

Extracted from legacy code, these pure functions validate content manipulation:

```python
# Content split validation
check_content_integrity(original, part1, part2)

# Organization validation  
check_reorganization_integrity(draft_ok, outline, organized)
check_heading_order(outline, organized)
```

**Key:** Pure functions, no LLM calls, easily testable

### 2. Validation Tools (`tools.py`)

Agents use these tools to validate their own work:

```python
validate_content_split_tool(original, part1, part2)
  → Verifies filtering preserved all content
  
validate_organization_tool(draft_ok, outline, organized)
  → Verifies organization matches outline structure
```

**Key:** Tools wrap validation functions, return structured results

### 3. Curator Agent (`agents/curator.py`)

The intelligent agent that does the actual work:

```python
curator = Agent(
    model="gemini-2.0-flash-exp",
    tools=[
        read_draft_tool,
        save_step_tool,
        validate_content_split_tool,
        validate_organization_tool,
    ],
    instruction=read_instructions("curator.md"),
)
```

**Key:** Agent does filtering/organizing, tools provide capabilities

### 4. Curator Instructions (`instructions/curator.md`)

250+ lines of guidance telling the agent HOW to work:

- Phase 2.1: Filter content (in-scope vs out-of-scope)
- Phase 2.2: Organize content (match outline structure)
- Critical constraints (preserve content, validate, checkpoint)
- Conversation style (transparent, patient, helpful)

**Key:** Instructions guide behavior, agent interprets and executes

---

## ADK Pattern Transformation

### Before: Hybrid Anti-Pattern ❌

```python
def filter_scope_tool(blog_id):
    """Tool that calls LLM internally"""
    draft = read_file(...)
    outline = read_file(...)
    
    # ❌ Tool does LLM reasoning
    client = genai.Client()
    response = client.models.generate_content(...)
    
    draft_ok, draft_not_ok = parse(response)
    save_file(draft_ok, ...)
    save_file(draft_not_ok, ...)
```

**Problems:**
- Low-level `genai.Client()` bypasses ADK features
- Tool makes decisions (what's in-scope?)
- Hard to test (LLM inside tool)
- Doesn't match official examples

### After: Proper ADK Pattern ✅

```python
# Tool: Pure validation
def validate_content_split_tool(original, part1, part2):
    """Validate split without LLM"""
    is_valid, error = check_content_integrity(...)
    return {"valid": is_valid, "message": error}

# Agent: Does the thinking
curator = Agent(
    tools=[read_draft_tool, validate_content_split_tool, save_step_tool],
    instruction="""
    Read draft and outline.
    YOU analyze each paragraph.
    YOU decide what's in-scope vs out-of-scope.
    Validate your split with validate_content_split_tool.
    Save with save_step_tool.
    """
)
```

**Benefits:**
- Agent has conversation history and context
- Agent explains its reasoning to user
- Tools are testable pure functions
- Matches official Google ADK examples

---

## Architecture

### Agent Structure (Consolidated)

```
blogger/agents/
├── __init__.py          # Exports all agents
├── scribr.py            # General-purpose writing helper
├── linguist.py          # General-purpose language helper
├── architect.py         # Phase 1: Outline creation
└── curator.py           # Phase 2: Filter & organize
```

**Rationale:** All agents in one place, clear organization

### Tool Structure

```python
# Basic I/O (5 tools)
read_draft_tool(), read_file_tool(), save_step_tool(),
read_previous_content_tool(), fetch_webpage_tool()

# Validation (2 tools - NEW)
validate_content_split_tool(), validate_organization_tool()
```

**Key:** 0 tools with LLM calls (all pure I/O or validation)

### Instructions

```
blogger/instructions/
├── scribr.md       # For scribr agent
├── linguist.md     # For linguist agent  
├── architect.md    # For architect agent
├── curator.md      # For curator agent (250+ lines)
└── coordinator.md  # For coordinator agent
```

**Key:** Each agent has corresponding instruction file

---

## Implementation Details

### Phase 2.1: Filter Scope

**User:** "Filter content for blog_id: my-post"

**Curator's workflow:**
1. Calls `read_draft_tool("my-post")` → gets draft
2. Calls `read_file_tool("outputs/my-post/outline.md")` → gets outline
3. **Analyzes each paragraph** (agent LLM reasoning)
4. **Splits content** into in-scope vs out-of-scope (agent decision)
5. Calls `validate_content_split_tool(draft, draft_ok, draft_not_ok)`
6. If validation passes:
   - Saves `draft_ok.md` and `draft_not_ok.md`
7. Presents results and waits for user confirmation

**Key:** Steps 3-4 are LLM reasoning by the agent, not by a tool

### Phase 2.2: Organize Content

**User:** "Yes, proceed with organizing"

**Curator's workflow:**
1. Reads `draft_ok.md` and `outline.md`
2. **Matches paragraphs to sections** (agent LLM reasoning)
3. **Reorganizes content** under headings (agent decision)
4. Calls `validate_organization_tool(draft_ok, outline, organized)`
5. If validation passes:
   - Saves `draft_ok_organized.md`
6. Presents organized result

**Key:** Agent does the organizing, tools validate and save

---

## Testing

### Current Test Coverage

```
tests/
├── test_text_utils.py (11 tests) ✅
│   ├── Validation functions
│   └── All passing
└── test_tools_deprecated.py.bak (deprecated)
```

### Test Results

```bash
pytest tests/ -v
# 11/11 tests passing
```

### Manual Testing

```bash
python -m blogger.playground --agent curator

# Test Phase 2.1
You: Filter content for blog_id: test-post
# Verify filtering works

# Test Phase 2.2  
You: Yes, proceed with organizing
# Verify organization works
```

---

## Lessons Learned

### 1. Always Study Official Examples First

**Mistake:** Started with `genai.Client()` directly in tools  
**Fix:** Read `/examples/blog-writer/`, saw the proper pattern, refactored  
**Lesson:** When adopting a framework, follow official patterns

### 2. Tools = Capabilities, Agents = Intelligence

**Pattern learned:**
- Tools provide abilities (read, save, validate)
- Agents use abilities to accomplish goals
- Agent has context, history, can explain reasoning
- Tools are pure, testable, simple

### 3. Validation Tools Are the Middle Ground

**Discovery:** Agents can validate their own work before saving
- Pure functions check data integrity
- Tools wrap functions with standard interface
- Agent calls tool to verify before proceeding
- If validation fails, agent fixes and retries

### 4. Instructions Are Powerful

**Realization:** 250-line `curator.md` guides behavior effectively
- Tells agent WHAT to do, not HOW
- Emphasizes constraints and priorities
- Defines conversation style
- Agent interprets and executes intelligently

### 5. Consolidation Matters

**Problem:** Had 5 different Phase 2 documents scattered everywhere  
**Solution:** ONE comprehensive document (this file)  
**Benefit:** Single source of truth, easy to find information

---

## Code Cleanup

### Documentation Consolidation

**Before:** 15+ files, redundant content  
**After:** 8 core files, ONE source per topic

**Consolidated into this file:**
- `CLEANUP_SUMMARY.md` → Merged here
- `learning/lessons/phase2-adk-refactor.md` → Merged here
- `learning/plans/phase2_curator.md` → Archived
- `learning/plans/phase2_learning_guide.md` → Archived

### Code Simplification

**Lines of code:**
- Before: `tools.py` = 613 lines
- After: `tools.py` = 360 lines
- **Reduction:** -253 lines (-41%)

**Removed functions:**
- ❌ `_llm_filter_content()` - Internal LLM helper
- ❌ `filter_scope_tool()` - Tool with internal LLM
- ❌ `organize_content_tool()` - Incomplete stub

**Why removed:** In ADK pattern, agents do the thinking

### Agent Structure Cleanup

**Before:**
```
blogger/
├── agents.py (scribr, linguist)
└── step_agents/ (architect, curator)
```

**After:**
```
blogger/agents/
├── scribr.py
├── linguist.py
├── architect.py
└── curator.py
```

**Benefit:** All agents in one place, clearer organization

---

## Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Lines of code (tools.py) | 613 | 360 | -41% |
| LLM-calling tools | 3 | 0 | Removed all |
| Pure tools | 5 | 7 | +2 validation |
| Tests passing | 11 | 11 | Stable |
| Phase 2 docs | 5 | 1 | Consolidated |

---

## Next Steps

### Phase 3: The Writer

Following the same ADK pattern:

**Agent:**
```python
writer = Agent(
    tools=[read_file_tool, save_step_tool],
    instruction="Read organized content, polish sections, save"
)
```

**No validation tools needed:**
- Writing is subjective
- User reviews polished content directly
- Focus on quality, not correctness

**Pattern consistency:**
- Tools = I/O (read, save)
- Agent = Intelligence (writing, polishing)
- Same clean architecture

---

## Key Takeaway

> **"Clean code isn't just about working code - it's about code that follows the framework's intended patterns. We refactored from 'it works' to 'it works the right way.'"**

The ADK pattern is simple:
- **Tools = Capabilities** (what you can do)
- **Agents = Intelligence** (what you should do)

Always follow this pattern. It makes code:
- ✅ Cleaner and more maintainable
- ✅ Easier to test and debug
- ✅ Consistent with framework expectations
- ✅ Ready for future enhancements

---

**Phase 2 Complete!** Ready for Phase 3: The Writer 🚀
