# Lesson: Phase 4 - The Analyzer (Light Mode)

**Date:** 2025-12-19
**Focus:** Preprocessing, Pure Tools, Agent Orchestration

## What We Built
We implemented the **Analyzer Agent**, a "Step 0" preprocessor that runs before the Architect. It analyzes the raw draft to detect complexity (quotes, code blocks) and recommends an outlining strategy.

## Key Learnings

### 1. Pure Tools vs. Agent Logic
- **Pure Tools:** We kept complexity detection (`detect_draft_complexity`) as a pure Python function using regex. This is fast, deterministic, and free (no tokens).
- **Agent Logic:** The Agent uses LLM reasoning to *interpret* the metrics (e.g., "High quote density = Narrative post") rather than counting them itself.
- **Benefit:** This separation proved critical. The LLM is great at qualitative summaries but terrible at counting. The regex tools provided the ground truth.

### 2. Regex in Tool Generation
- **Challenge:** Writing Python code with regex via an LLM tool (`write_file`) is tricky due to multiple layers of escaping.
- **Solution:** 
    - `\n` in a Python string literal means newline.
    - `\\n` in a Python string literal means literal backslash-n.
    - When generating code, always double-check how the target file interprets the string.
    - We encountered issues where `re.split(r'\\n\\n')` was written to the file, causing it to split on literal backslashes instead of newlines.
    - **Best Practice:** Use `splitlines()` where possible, or extremely simple regexes.

### 3. Agent Data Flow
- **Challenge:** The Analyzer Agent called `save_analysis_tool` but initially failed to pass the collected metrics (like `score`), resulting in "N/A" in the report.
- **Root Cause:** The Agent "forgot" to include fields from the previous tool's output when constructing the dictionary for the next tool.
- **Solution:** We explicitly updated `analyzer.md` (instructions) to list *exactly* which fields must be passed to `save_analysis_tool`. "Call `save_analysis_tool` with a dictionary containing ALL collected data: metrics, score..."
- **Takeaway:** Don't assume the Agent will automatically merge data. Be explicit in instructions about data payloads between steps.

### 4. Integration Testing
- We created a `test_analyzer_integration.py` script that spun up a local `Runner` and session. This allowed us to test the Agent's behavior (tool calling sequence) without the full UI.
- This "headless" testing is faster and more reliable than manual CLI testing.

## Next Steps (Phase 5)
- **Deep Mode:** Implement "Deep Analysis" which actually extracts content chunks and maps connections.
- **Curator Integration:** Use the analysis to help the Curator filter content more intelligently.
