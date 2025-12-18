# Phase 4: Analyzer Foundation (Light Mode) - Implementation Plan

**Status:** Planning
**Workflow Position:** Step 0 (runs before Architect)
**Started:** TBD
**Completed:** TBD

---

## 🎯 Goal

Build a draft analysis system that detects content complexity and provides contextual insights to guide the Architect agent. This is **Step 0** in the workflow—preprocessing that happens before outline creation.

**Input:** `posts/{blog_id}/draft.md` (user's chaotic draft)
**Output:** `posts/{blog_id}/0-analysis.md` (complexity summary + recommendations)

**Philosophy:** Start simple. Light analysis mode provides quick complexity assessment without heavy processing. Deep mode (Phase 5) comes later only if this proves valuable.

---

## 🏗️ Architecture

### What is "Light Analysis"?

**Light mode** = Quick preprocessing that tells the Architect:
- Is this a narrative post (quote-heavy) or practical post (technical)?
- How complex is the draft?
- What are the main topics?
- Should we use quote-driven or topic-driven outlining?

**Output:** Single file (`0-analysis.md`) with YAML front-matter for machine parsing + human-readable summary.

### Workflow Integration

```
OLD FLOW:
User creates draft.md → Calls Architect → Brainstorm outlines

NEW FLOW:
User creates draft.md
  → Calls Architect
    → Architect checks: "Does 0-analysis.md exist?"
      → NO: Auto-runs Analyzer (light mode)
      → YES: Uses cached analysis
  → User reviews quick summary
  → Architect uses analysis hints to brainstorm
```

**Key insight:** Analyzer runs **automatically** when missing, transparent to user.

### Agent Design

**Primary Agent:** `blogger/agents/analyzer.py`
- **Role:** Content preprocessor, complexity detector
- **Pattern:** Simple ADK Agent wrapper
- **Behavior:** Runs pure tools + LLM reasoning for summarization

**Tools Used (from `utils/tools.py`):**
- `detect_draft_complexity()` - Pure function (NO LLM)
- `extract_quotes_with_sources()` - Pure function
- `count_code_blocks()` - Pure function
- `extract_main_topics()` - Pure function

**LLM Reasoning (Analyzer agent does):**
- Interpret complexity score
- Summarize main themes
- Recommend post type (narrative vs practical)
- Write human-friendly summary

### Output Format: `0-analysis.md`

```markdown
---
# YAML Front-matter (machine-readable for Architect)
type: narrative              # or "practical" or "mixed"
complexity: high             # low, medium, high
mode: light                  # Always "light" in Phase 4
detected_quote_count: 15
detected_code_blocks: 2
main_topics:
  - debugging_philosophy
  - agent_architecture
  - learning_journey
recommended_architect_mode: quote-driven  # or "topic-driven"
---

# Draft Analysis (Light)

## Summary
This draft contains **15 quotes** woven through personal reflections on debugging and agent design. The high quote density (15 quotes, 2 code blocks) suggests a **narrative post** focused on connecting ideas through expert insights.

**Recommendation:** Use quote-driven outlining. The Architect should identify key quotes as narrative anchors.

## Detected Topics
1. **Debugging Philosophy** (5 references)
2. **Agent Architecture** (8 references)
3. **Learning Journey** (12 references - personal reflections)

## Complexity Assessment
- **Score:** 7.8/10 (high)
- **Rationale:** Many quotes from diverse sources, requires careful organization to thread narrative
- **Suggested Mode:** Light analysis sufficient for now. Consider deep mode if Architect struggles.

---

*This analysis was generated automatically. Review the summary, then proceed to Architect for outline creation.*
```

### Key Decisions

**Decision 1: Auto-run or explicit call?**
- **Chosen:** Auto-run when Architect starts (if `0-analysis.md` missing)
- **Rationale:**
  - Seamless user experience
  - Caching prevents re-analysis
  - User can manually delete `0-analysis.md` to force re-run

**Decision 2: Pure tools vs LLM for complexity?**
- **Chosen:** Pure tools for detection, LLM for interpretation
- **Rationale:**
  - Complexity score = heuristic (quote count, code blocks, topic diversity)
  - Summary/recommendations = LLM reasoning
  - Clear separation of concerns

**Decision 3: Store config separately or in front-matter?**
- **Chosen:** YAML front-matter in `0-analysis.md`
- **Rationale:**
  - Single file = simpler
  - Human can read analysis, machine can parse front-matter
  - No need for separate `config.yaml`

**Decision 4: What does Architect read?**
- **Chosen:** Architect reads both `0-analysis.md` front-matter AND `draft.md`
- **Rationale:**
  - Analysis is a **hint**, not a replacement
  - Architect still works with actual prose
  - Front-matter gives quick context (type, complexity, topics)

---

## 📋 Implementation Checklist

### Task 1: Complexity Detection Tools (Pure Functions)

**File:** `blogger/utils/tools.py`

- [ ] Create `detect_draft_complexity(draft_text: str) -> dict`
  - [ ] Count paragraphs
  - [ ] Count quotes (detect patterns: `"..."`, `>`, attribution lines)
  - [ ] Count code blocks (markdown fenced blocks)
  - [ ] Count unique sources/references
  - [ ] Estimate topic diversity (keyword-based, TF-IDF or simple)
  - [ ] Calculate heuristic complexity score (0-10)
  - [ ] Return metrics dict + suggested mode (light/deep)

- [ ] Create `extract_quotes_with_sources(draft_text: str) -> list[dict]`
  - [ ] Find quoted text (patterns: `"..."`, `> quote`, etc.)
  - [ ] Extract attribution (lines with `—`, `- Source`, `[source: url]`)
  - [ ] Return list of `{text, source, line_number}`

- [ ] Create `count_code_blocks(draft_text: str) -> dict`
  - [ ] Count markdown code fences (` ```python `, etc.)
  - [ ] Detect languages
  - [ ] Return `{count, languages: [...]}`

- [ ] Create `extract_main_topics(draft_text: str) -> list[str]`
  - [ ] Use simple keyword extraction (most frequent meaningful words)
  - [ ] Or basic NLP (exclude stopwords, get top N keywords)
  - [ ] Return list of 3-5 main topics

- [ ] Write unit tests: `blogger/tests/test_complexity_tools.py`
  - [ ] Test quote detection with various formats
  - [ ] Test code block counting
  - [ ] Test complexity scoring with sample drafts
  - [ ] Test edge cases (empty draft, no quotes, etc.)

### Task 2: Analyzer Agent

**Files:** `blogger/agents/analyzer.py` + `blogger/agents/analyzer.md`

- [ ] Create `blogger/agents/analyzer.py`
  - [ ] Import complexity tools from `utils/tools.py`
  - [ ] Define Analyzer agent with tools
  - [ ] Tool: `detect_draft_complexity_tool` (wraps pure function)
  - [ ] Tool: `extract_quotes_tool` (wraps pure function)
  - [ ] Tool: `save_analysis_tool` (writes `0-analysis.md`)

- [ ] Create `blogger/agents/analyzer.md` (instructions)
  - [ ] Define role: "Content preprocessor for draft analysis"
  - [ ] Workflow:
    1. Run complexity detection
    2. Extract quotes and code blocks
    3. Identify main topics
    4. Determine post type (narrative vs practical)
    5. Write human-friendly summary
    6. Save as `0-analysis.md` with YAML front-matter
  - [ ] Output format specification
  - [ ] Examples of different post types

- [ ] Create `save_analysis_tool(blog_id: str, analysis_data: dict) -> dict` in `utils/tools.py`
  - [ ] Generate YAML front-matter from analysis data
  - [ ] Generate markdown summary section
  - [ ] Write to `posts/{blog_id}/0-analysis.md`
  - [ ] Return success status

### Task 3: Architect Integration

**Goal:** Architect auto-runs Analyzer if `0-analysis.md` missing

- [ ] Update `blogger/agents/architect.py`
  - [ ] Add check: Does `0-analysis.md` exist?
  - [ ] If NO: Call Analyzer agent automatically
  - [ ] Show analysis summary to user
  - [ ] Continue with outlining using analysis hints

- [ ] Update `blogger/agents/architect.md` (instructions)
  - [ ] Add preprocessing step: "Check for analysis file"
  - [ ] Add guidance: "Use `type` and `recommended_architect_mode` from front-matter"
  - [ ] Example: "For narrative posts, identify quote clusters"

- [ ] Create tool: `read_analysis_tool(blog_id: str) -> dict` in `utils/tools.py`
  - [ ] Read `0-analysis.md`
  - [ ] Parse YAML front-matter
  - [ ] Return dict with `front_matter` and `summary_text`

### Task 4: Testing

- [ ] Register Analyzer in `blogger/playground.py`
  - [ ] Add to AGENTS dictionary
  - [ ] Verify agent loads without errors

- [ ] Create test draft samples
  - [ ] **Sample 1:** Narrative post (high quote count, personal reflections)
  - [ ] **Sample 2:** Practical post (code snippets, step-by-step, few quotes)
  - [ ] **Sample 3:** Mixed post (medium quotes + code)

- [ ] Test Analyzer standalone
  - [ ] Run: `python -m blogger.playground --agent analyzer`
  - [ ] Load Sample 1 (narrative) → Verify detects "narrative", high complexity
  - [ ] Load Sample 2 (practical) → Verify detects "practical", low complexity
  - [ ] Load Sample 3 (mixed) → Verify detects "mixed", medium complexity

- [ ] Test Architect integration
  - [ ] Delete `0-analysis.md` for test blog
  - [ ] Run Architect
  - [ ] Verify: Analyzer runs automatically
  - [ ] Verify: Analysis summary shown to user
  - [ ] Verify: `0-analysis.md` created
  - [ ] Run Architect again (same blog)
  - [ ] Verify: Uses cached analysis (doesn't re-run)

### Task 5: Documentation

- [ ] Update `progress/PROGRESS.md`
  - [ ] Add Phase 4 checklist
  - [ ] Mark tasks as complete when done

- [ ] Create lesson: `progress/lessons/phase4_analyzer_foundation.md`
  - [ ] Document complexity heuristics used
  - [ ] Document auto-run pattern (cache checking)
  - [ ] Capture key learnings

- [ ] Update `AGENTS.md`
  - [ ] Add Step 0: Analyzer to workflow diagram
  - [ ] Update file structure to show `0-analysis.md`
  - [ ] Add Analyzer to Quick Reference

---

## 🧪 Testing Strategy

### Unit Tests (pytest)

**File:** `blogger/tests/test_complexity_tools.py`

```python
def test_detect_draft_complexity_narrative():
    """Test complexity detection for quote-heavy narrative draft"""
    draft = """
    "Errors are teachers" — Karpathy
    This reminded me of my debugging struggles.
    "Constraints enable creativity" — My insight
    ...
    """
    result = detect_draft_complexity(draft)
    assert result["score"] > 6  # High complexity
    assert result["suggested_mode"] == "light"  # Phase 4 always suggests light
    assert result["metrics"]["quote_count"] >= 2

def test_detect_draft_complexity_practical():
    """Test complexity detection for technical draft"""
    draft = """
    Here's how to debug Python:
    ```python
    def debug():
        print("test")
    ```
    Step 1: Add logging...
    """
    result = detect_draft_complexity(draft)
    assert result["score"] < 6  # Low complexity
    assert result["metrics"]["code_block_count"] >= 1

def test_extract_quotes_with_sources():
    """Test quote extraction with various attribution formats"""
    draft = """
    "Quote 1" — Author Name
    > Quote 2
    - Source: Blog Post
    "Quote 3" [source: https://example.com]
    """
    quotes = extract_quotes_with_sources(draft)
    assert len(quotes) == 3
    assert quotes[0]["source"] == "Author Name"
    assert quotes[2]["source"] == "https://example.com"

def test_count_code_blocks():
    """Test code block detection"""
    draft = """
    ```python
    print("hello")
    ```
    Some text
    ```javascript
    console.log("world")
    ```
    """
    result = count_code_blocks(draft)
    assert result["count"] == 2
    assert "python" in result["languages"]
    assert "javascript" in result["languages"]
```

### Integration Tests (Playground)

**Scenario 1: Standalone Analyzer (Narrative Post)**
```bash
python -m blogger.playground --agent analyzer
```
1. User loads narrative draft (15 quotes, personal reflections)
2. Analyzer runs complexity detection
3. Verify output: `type: narrative`, `complexity: high`, `recommended_architect_mode: quote-driven`
4. Verify file created: `posts/test-blog/0-analysis.md`
5. User reads summary: "This draft contains 15 quotes... suggests narrative post"

**Scenario 2: Standalone Analyzer (Practical Post)**
1. User loads practical draft (code snippets, step-by-step guide)
2. Analyzer runs
3. Verify output: `type: practical`, `complexity: low`, `recommended_architect_mode: topic-driven`

**Scenario 3: Architect Auto-Run (Cache Miss)**
```bash
python -m blogger.playground --agent architect
```
1. User selects blog with draft but no `0-analysis.md`
2. Architect detects missing analysis
3. Verify: "Running content analysis first..." message
4. Verify: Analyzer runs, creates `0-analysis.md`
5. Verify: Architect continues with outlining, using analysis hints

**Scenario 4: Architect Auto-Run (Cache Hit)**
1. User runs Architect (analysis file already exists)
2. Verify: "Found existing analysis..." message
3. Verify: Analyzer does NOT re-run
4. Verify: Architect uses cached analysis

**Scenario 5: Manual Analysis Re-run**
1. User deletes `0-analysis.md`
2. User runs Architect
3. Verify: Analysis runs again (cache miss)

---

## 📚 References

### Completed Phases
- **Phase 1:** Architect agent (`blogger/agents/architect.py`)
- **Phase 2:** Curator agent (`blogger/agents/curator.py`)

### Related Code
- **File tools:** `blogger/utils/tools.py` (tool pattern examples)
- **Scribr agent:** `blogger/agents/scribr.py` (simple agent wrapper example)

### Lessons Learned (from previous phases)
- Keep tools pure: I/O and validation only
- Agents do reasoning, tools provide capabilities
- Sub-agent delegation for specialized tasks
- Cache when possible to avoid redundant work

---

## 🎓 Learning Outcomes

By completing Phase 4, you'll learn:
- **Heuristic complexity detection:** Using simple metrics (quote count, code blocks) to assess content
- **YAML front-matter:** Machine-readable metadata in markdown files
- **Auto-run patterns:** Checking for cached results, running preprocessing transparently
- **Pure function design:** Separation of data processing (pure) from reasoning (LLM)
- **Agent integration:** One agent calling another conditionally

---

## Success Criteria

Phase 4 is complete when:
1. ✅ Complexity detection tools work reliably (unit tests pass)
2. ✅ Analyzer agent produces valid `0-analysis.md` files
3. ✅ Architect auto-runs Analyzer when analysis missing
4. ✅ Architect uses cached analysis when present
5. ✅ Analysis provides useful hints (type, complexity, topics) for Architect
6. ✅ All tests pass (unit + integration)

---

## Notes

**Why start with light mode only?**
- Validate the concept before building complex chunk extraction (Phase 5)
- Light mode might be sufficient for most use cases
- User feedback will guide whether deep mode is needed

**Why auto-run instead of explicit step?**
- Smoother user experience (one less command)
- Analysis is preprocessing, not a creative decision point
- User can always review `0-analysis.md` after it's created

**What if complexity detection is wrong?**
- Human can manually edit `0-analysis.md` front-matter
- Architect uses it as a hint, not strict requirement
- Phase 5 (deep mode) will allow more sophisticated analysis

**Why YAML front-matter instead of separate config file?**
- Fewer files to manage
- Human-readable + machine-parseable in one place
- Common pattern in static site generators (Jekyll, Hugo)

---

## Next Steps

After Phase 4 completion:
- **Phase 5:** Analyzer Deep Mode (chunk extraction, connection mapping)
- Or proceed with **Phase 3:** Writer agent (if light mode proves sufficient)
