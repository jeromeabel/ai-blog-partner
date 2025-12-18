# Phase 2 Debugging - Lessons Learned

**Date:** 2025-12-18
**Context:** Fixed Curator agent issues after major refactoring

---

## 🐛 Problems Encountered

### 1. Files Not Being Saved
**Symptom:** Agent said "I will split the content" but never saved draft_ok.md, draft_not_ok.md, or 2-draft_organized.md

**Root Cause:** Ambiguous instruction language
- Instructions said: "Step 4: Save Results" → "Step 5: Present Results (CHECKPOINT)"
- Agent interpreted checkpoint as "wait for user approval BEFORE saving"
- Should have been: "validate → save → present → wait for approval to proceed"

**Fix:** Made Step 4 explicit with "MANDATORY - Do This BEFORE Presenting"
```markdown
**CRITICAL:** You MUST save files immediately after validation passes.
Do NOT wait for user confirmation.
```

### 2. Agent Stopped Mid-Workflow
**Symptom:** Agent disappeared after saying "Now I will split the content"

**Root Cause:** Lightweight model (gemini-2.0-flash-exp) couldn't follow complex instructions reliably

**Fix:** Upgraded to gemini-3-pro-preview (same as Architect)
- Trade-off: Slower but more reliable
- User preference: Reliability > Speed for workflow agents

### 3. ADK Template Variable Errors
**Symptom:** `KeyError: 'Context variable not found: blog_id'`

**Root Cause:** Using `{blog_id}` in instruction text
- ADK interprets `{variable}` as template variables to inject from session context
- We don't use session variables for blog_id (it's passed through tools)

**Fix:** Changed all `{blog_id}` → `<blog_id>` in instructions
- Keeps clarity as placeholder without triggering ADK template injection

**Where this occurred:**
- Line 109, 110: `posts/{blog_id}/draft_ok.md`
- Line 184: `posts/{blog_id}/2-draft_organized.md`

### 4. Poor Visibility Into Progress
**Symptom:** User couldn't see what agent was doing ("takes a long time, we don't know which files are read")

**Root Cause:** No progress reporting guidance in instructions

**Fix:** Added two improvements:
1. **Progress Reporting section in instructions:**
   ```markdown
   ✅ GOOD:
   - "Reading draft from posts/my-ai-journey-2/draft.md..."
   - "Validation passed! Saving results..."
   - "✅ Saved draft_ok.md (15 paragraphs)"

   ❌ BAD:
   - "I will split the content" (then disappears)
   ```

2. **Verbose mode in playground:**
   ```bash
   python -m blogger.playground --agent curator --verbose
   ```
   Shows all tool calls with arguments and results

### 5. Incorrect Filename Convention
**Symptom:** Agent saved as `draft_ok_organized.md` instead of following step pattern

**Root Cause:** Instructions didn't follow the step naming convention:
- Step 1: `1-outline.md`
- Step 2: Should be `2-draft_organized.md` (not `draft_ok_organized.md`)
- Step 3: `3-final.md`

**Fix:** Updated all references to use `2-draft_organized.md`

---

## ✅ Key Lessons

### Lesson 1: LLM Instructions Must Be Explicit About Timing
**Bad:**
```markdown
Step 4: Save results
Step 5: Present results and wait for confirmation
```

**Good:**
```markdown
Step 4: Save results (MANDATORY - Do This BEFORE Presenting)
**CRITICAL:** Save immediately after validation. Do NOT wait.

Step 5: Present results
After successfully saving, show the user...
```

**Why:** LLMs are literal. "Checkpoint" language can be interpreted as "stop and wait before saving."

### Lesson 2: ADK Template Variables vs Plain Text
**Rule:** Never use `{variable}` in instruction markdown unless you want ADK to inject it from session context

**Safe patterns:**
- `<variable>` - Placeholder in instructions ✅
- `$variable` - Placeholder in instructions ✅
- `{{variable}}` - Escaped in some contexts ✅
- `{variable}` - ADK template injection ❌

**When to use session variables:**
- Simple context that doesn't change (user_id, app_name)
- NOT for workflow state (blog_id, step numbers)

**Our approach:** Pass blog_id through tool parameters, not session variables

### Lesson 3: Model Selection Trade-offs
**Lightweight models (gemini-2.0-flash-exp):**
- ✅ Fast (2-3x faster)
- ✅ Cheap
- ❌ May skip steps
- ❌ Weaker instruction following
- **Use for:** Simple, single-step agents

**Premium models (gemini-3-pro-preview):**
- ✅ Reliable completion
- ✅ Strong instruction following
- ❌ Slower
- ❌ More expensive
- **Use for:** Multi-step workflow agents (Architect, Curator)

**Decision:** For workflow agents, reliability > speed

### Lesson 4: Progress Reporting is Critical for User Experience
**Problem:** User feels agent is "frozen" when it's actually working

**Solution:** Two layers of feedback:
1. **Agent instructions:** Teach agent to report progress naturally
   - "Reading X... ✅"
   - "Analyzing Y..."
   - "Saving Z... ✅"

2. **Tool-level logging:** Verbose mode for debugging
   - Shows exact function calls
   - Shows arguments and results
   - User can see what's happening under the hood

**Impact:** Makes slow operations feel responsive

### Lesson 5: Naming Conventions Must Be Consistent
**Pattern established:**
- Draft → `draft.md` (user input)
- Step 1 output → `1-outline.md` (numbered)
- Step 2 output → `2-draft_organized.md` (numbered)
- Step 3 output → `3-final.md` (numbered)

**Why numbers:**
- Clear progression
- Alphabetical sort matches workflow order
- Easy to identify completion state

**Anti-pattern:** Descriptive names like `draft_ok_organized.md`
- Doesn't show step number
- Inconsistent with other steps

---

## 🔧 Tools and Techniques Used

### Exploration Pattern
1. **Explore agents** to understand code before planning
2. **Read actual files** to confirm findings
3. **Ask user questions** to clarify requirements
4. **Plan agent** to design solution
5. **Execute fixes** systematically

### Testing Approach
1. **Unit tests first** - Verify validation functions work
2. **Integration tests** - Test agent end-to-end in playground
3. **Verbose mode** - Debug tool calls and responses

### Documentation Pattern
- **Inline examples** in instructions show expected behavior
- **Error handling** sections guide agents when things fail
- **Why explanations** help agents understand intent, not just mechanics

---

## 📊 Impact Summary

**Before fixes:**
- ❌ No files saved
- ❌ Agent stops mid-workflow
- ❌ Template variable errors
- ❌ No visibility into progress

**After fixes:**
- ✅ All files saved reliably
- ✅ Complete workflow execution
- ✅ No template errors
- ✅ Clear progress reporting
- ✅ Verbose mode for debugging
- ✅ Correct filename conventions

**Files Modified:** 4
- `curator.py` - Model upgrade (1 line)
- `curator.md` - Instruction improvements (~60 lines)
- `architect.md` - Finalization clarity (~15 lines)
- `playground.py` - Verbose logging (~25 lines)

**Tests:** 29 passing (unchanged)

---

## 🚀 Recommendations for Future Agents

### When Writing Agent Instructions:
1. ✅ Be explicit about timing ("immediately", "before", "after")
2. ✅ Use `<placeholders>` not `{templates}` in example text
3. ✅ Include progress reporting guidance
4. ✅ Show complete examples with tool calls
5. ✅ Add error handling sections
6. ✅ Follow naming conventions

### When Choosing Models:
1. ✅ Use premium models for multi-step workflows
2. ✅ Use flash models for simple, single-purpose agents
3. ✅ Test both and measure reliability vs speed

### When Testing:
1. ✅ Add verbose/debug modes early
2. ✅ Test with real data, not minimal examples
3. ✅ Verify file outputs, not just agent responses

### When Debugging:
1. ✅ Search for template variables (`{.*}` patterns)
2. ✅ Check instruction clarity at decision points
3. ✅ Verify model selection matches task complexity

---

## 📚 Related Documentation

- **Architecture:** `/CLAUDE.md` - Defines "Interactive Partner" protocol
- **Agent Code:** `/blogger/agents/curator.py`
- **Agent Instructions:** `/blogger/agents/curator.md`
- **Tools:** `/blogger/utils/tools.py`
- **Tests:** `/blogger/tests/test_validation_tools.py`

---

## 🎯 Key Takeaway

**The most important lesson:** Agent instructions are code. They must be precise, explicit, and tested just like Python code. Ambiguity in natural language instructions causes bugs just as surely as ambiguity in programming language syntax.

**Second most important:** Always optimize for reliability first, performance second, especially for workflow agents where partial completion is worse than slow completion.
