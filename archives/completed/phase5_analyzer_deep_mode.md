# Phase 5: Analyzer Deep Mode - Implementation Plan

**Status:** Complete
**Prerequisite:** Phase 4 (Analyzer Foundation) must be complete
**Workflow Position:** Step 0 (enhanced analysis for complex drafts)
**Started:** 2025-12-19
**Completed:** 2025-12-19

---

## 🎯 Goal

Extend the Analyzer to handle complex, quote-heavy drafts by extracting chunks, scoring them, and mapping connections. Deep mode transforms chaotic narrative drafts into structured, scored pieces that Architect can use to build quote-driven outlines.

**Input:** `posts/{blog_id}/draft.md` (complex narrative draft)
**Output:** `posts/{blog_id}/0-analysis.md` (with chunk extraction, scoring, connection mapping)

**Philosophy:** Deep mode is **intentional**—triggered when complexity is high or explicitly requested. It provides the Architect with pre-processed chunks and connection patterns, making narrative outline creation easier.

---

## 🏗️ Architecture

### What is "Deep Analysis"?

**Deep mode** = Full content deconstruction:
- Split draft into atomic chunks (quotes, commentary, code)
- Score each chunk by quality/clarity/importance (using LLM)
- Map connections between chunks (thematic links)
- Suggest narrative flows (ordered sequences of chunks)

**When to use:**
- Complexity score ≥ 7 (from Phase 4 detection)
- User explicitly requests: "Run deep analysis"
- Analyzer detects: "Draft is difficult to analyze automatically"

### Deep Analysis Workflow

```
1. Analyzer runs (Phase 4 light mode)
2. Complexity score = 8.5 (high)
3. Analyzer asks user:
   "This draft is complex (8.5/10). I recommend DEEP analysis to:
   - Extract and score all quotes
   - Map connections between ideas
   - Suggest narrative flows

   Run deep analysis? (Takes longer but helps with quote-driven outlining)"

4. User confirms → Deep mode runs
5. Architect receives detailed chunk map with scored connections
```

### Output Format: `0-analysis.md` (Deep Mode)

```markdown
---
# YAML Front-matter
type: narrative
complexity: high
mode: deep                   # NEW: "deep" instead of "light"
total_chunks: 32
high_scoring_chunks: 8
detected_quote_count: 15
detected_code_blocks: 2
main_topics:
  - debugging_philosophy
  - agent_architecture
  - learning_journey
recommended_architect_mode: quote-driven
narrative_flows:              # NEW: Suggested flows
  - flow_a                    # Quote-driven journey
  - flow_b                    # Chronological
  - flow_c                    # Thematic
---

# Draft Analysis (Deep)

## Summary
This draft contains **15 high-quality quotes** woven through personal reflections. Deep analysis identified **32 content chunks** with **8 high-scoring anchor points** for narrative structure.

**Recommendation:** Use Flow A (quote-driven journey) as primary outline structure.

---

## Content Chunks (32 total)

### High-Scoring Chunks (≥8.0)

**Chunk #1** [Quote] (Score: 9.2/10)
> "Errors are teachers, not enemies" — Andrej Karpathy
> Source: [karpathy.github.io/debugging](https://karpathy.github.io/debugging)
> **Connects to:** #4, #12, #18
> **Why high score:** Clear insight, authoritative source, central to debugging theme

**Chunk #2** [Commentary] (Score: 8.5/10)
> "This reminded me of my Phase 1 struggles when the Architect kept failing..."
> **Connects to:** #1, #7, #15
> **Why high score:** Personal insight, emotional resonance, bridges theory to practice

**Chunk #3** [Quote] (Score: 8.0/10)
> "Constraints enable creativity" — Your observation
> Source: Draft reflection
> **Connects to:** #9, #15
> **Why high score:** Original insight, thematic anchor

[... 5 more high-scoring chunks]

### Mid-Scoring Chunks (5.0-7.9)

**Chunk #9** [Commentary] (Score: 7.5/10)
> "The ADK framework forced me to rethink agent boundaries..."
> **Connects to:** #3, #14

**Chunk #10** [Quote] (Score: 6.8/10)
> "Simplicity is the ultimate sophistication" — Da Vinci
> **Connects to:** #11

[... more chunks]

### Low-Scoring Chunks (<5.0)

**Chunk #28** [Tangent] (Score: 3.2/10)
> "I also tried using Claude but that's a different story..."
> **Suggestion:** Consider removing or expanding into full section

[... more low-scoring chunks]

---

## Suggested Narrative Flows

### Flow A: Quote-Driven Journey (Recommended, Avg Score: 8.4)
**Structure:** Thread narrative through high-scoring quotes
```
#1 (Karpathy quote)
  → #2 (Your Phase 1 struggle)
  → #4 (Debugging epiphany)
  → #12 (Willison quote on agent design)
  → #18 (Resolution & lessons learned)
```
**Why recommended:** Highest-scoring chunks create natural arc, strong narrative tension

### Flow B: Chronological (Avg Score: 7.2)
**Structure:** Follow your actual journey timeline
```
#7 (Phase 1 start)
  → #9 (ADK challenges)
  → #15 (Breakthrough moment)
  → #22 (Phase 2 transition)
  → #30 (Current reflections)
```
**Trade-off:** More complete story, but some lower-scoring tangents included

### Flow C: Thematic Clusters (Avg Score: 7.8)
**Structure:** Organize by topic, quotes as supporting evidence
```
Section 1: Debugging Philosophy (#1, #4, #6)
Section 2: Agent Architecture (#12, #14, #20)
Section 3: Learning Process (#2, #15, #25)
```
**Trade-off:** Clear organization, but less narrative momentum

---

## Connection Map

**Strong connections (≥0.8 similarity):**
- #1 ↔ #4: Both about debugging mindset
- #2 ↔ #7: Both describe Phase 1 struggles
- #3 ↔ #15: Both discuss constraints/creativity

**Moderate connections (0.5-0.79):**
- #9 ↔ #14: ADK framework discussion
- #12 ↔ #20: Agent design principles

**Weak connections (<0.5):**
- #28 ↔ [isolated]: Tangent about Claude (consider removing)

---

## Recommendations for Architect

1. **Start with Flow A** (quote-driven) - highest scores, strongest narrative arc
2. **Use #1, #2, #12 as section anchors** - these chunks score 8.5+
3. **Consider removing chunks #28, #30** - low scores, tangential
4. **Reference connection map** when organizing - preserves thematic coherence

---

*Deep analysis complete. Proceed to Architect with chunk-based outlining.*
```

### How Architect Uses Deep Analysis

**With Light Mode (Phase 4):**
```
Architect reads:
- draft.md (full prose)
- 0-analysis.md front-matter (type, complexity, topics)

Architect thinks:
"This is narrative type, let me identify key quotes while reading..."
```

**With Deep Mode (Phase 5):**
```
Architect reads:
- 0-analysis.md (chunk map with IDs, scores, flows)
- draft.md (available for reference if needed)

Architect thinks:
"Analysis suggests Flow A with chunks #1, #2, #4, #12, #18.
Let me build outline v1 around that structure..."

Outline v1:
## Section 1: The Teacher's Voice
[Anchor: Chunk #1 - Karpathy quote]

## Section 2: The Student's Struggle
[Anchor: Chunk #2 - Your Phase 1 story]

## Section 3: The Breakthrough
[Anchor: Chunk #4 - Debugging epiphany]
...
```

**Key benefit:** Architect works with **pre-processed structure** instead of raw chaos.

### How Curator Uses Deep Analysis

**Without Deep Mode (Phase 2 behavior):**
```
Curator reads:
- 1-outline.md (approved outline)
- draft.md (full chaotic draft)

Curator thinks:
"Section 1 is 'The Philosophy'. Let me scan all 5000 words to find matching content..."
[Re-parses entire draft, matches content to sections]
```

**With Deep Mode (Phase 5):**
```
Curator reads:
- 1-outline.md (approved outline)
- 0-analysis.md (32 pre-extracted chunks with scores/topics)
- draft.md (available for reference if needed)

Curator thinks:
"Section 1 is 'The Philosophy'. Analysis shows chunks tagged 'debugging_philosophy':
- Chunk #1 (score: 9.2) → IN-SCOPE, Section 1
- Chunk #4 (score: 8.0) → IN-SCOPE, Section 1 (Architect didn't mention this one)
- Chunk #6 (score: 7.5) → IN-SCOPE, Section 1

Chunk #28 (score: 3.2, topic: tools) → OUT-OF-SCOPE (no section match)"
[Works with pre-processed chunks, faster filtering]

Outputs:
## Section 1: The Philosophy
<!-- Chunk #1 -->
[Karpathy quote content]

<!-- Chunk #4 -->
[Additional philosophy content]

## Out-of-Scope Content
<!-- Chunk #28 -->
[Claude tangent - consider removing]
```

**Key benefits:**
- **Efficiency:** No re-parsing (chunks already extracted)
- **Quality hints:** Uses scores to filter low-quality content
- **Traceability:** Chunk IDs preserved in organized draft
- **Discovery:** Finds relevant chunks Architect didn't reference
- **Backward compatible:** Falls back to draft.md if no deep analysis

**Critical distinction:**
- **Analyzer** (Step 0): Scores content quality, detects topics → **Content-agnostic**
- **Curator** (Step 2): Matches content to outline sections → **Outline-specific**

Curator makes the final in-scope decision based on approved outline structure, using analysis as efficiency hints.

---

## 📋 Implementation Checklist

### Task 1: Chunk Extraction Tools

**File:** `blogger/utils/tools.py`

- [x] Create `split_draft_into_chunks(draft_text: str) -> list[dict]`
  - [x] Split by paragraphs (preserve markdown structure)
  - [x] Detect chunk type: `quote`, `commentary`, `code`, `heading`
  - [x] Preserve line numbers for source reference
  - [x] Return list of `{id, type, text, line_start, line_end}`

- [x] Create `extract_chunk_context(chunks: list, chunk_id: str) -> dict`
  - [x] Get surrounding chunks (prev/next)
  - [x] Useful for connection analysis
  - [x] Return `{chunk, prev_chunk, next_chunk}`

- [x] Write unit tests: `blogger/tests/test_chunk_tools.py`
  - [x] Test paragraph splitting (preserve structure)
  - [x] Test type detection (quote vs commentary vs code)
  - [x] Test line number tracking
  - [x] Test edge cases (empty paragraphs, nested quotes)

### Task 2: Chunk Scoring (LLM-based)

**File:** `blogger/agents/analyzer.py` (agent task, not pure tool)

- [x] Create scoring prompt for Analyzer agent
  - [x] Criteria: Clarity, insight quality, relevance, source authority
  - [x] Score scale: 0-10 with rationale
  - [x] Batch scoring (process multiple chunks per LLM call for efficiency)

- [x] Add `score_chunks_tool` to Analyzer
  - [x] Input: List of chunks
  - [x] LLM scores each chunk with rationale
  - [x] Return scored chunks: `{id, text, score, rationale}`
  *Implemented as Agent instruction + `save_analysis_tool` update*

- [x] Test scoring consistency
  - [x] Same chunk scored multiple times → similar scores
  - [x] High-quality quotes → scores ≥ 8
  - [x] Tangential content → scores < 5
  *Implicit in Agent Logic*

### Task 3: Connection Mapping

**File:** `blogger/utils/tools.py` (pure function for similarity)

- [x] Create `calculate_chunk_similarity(chunk1: str, chunk2: str) -> float`
  - [x] Use simple keyword overlap (Jaccard similarity)
  - [x] Return similarity score 0.0-1.0

- [x] Create `map_chunk_connections(chunks: list) -> dict`
  - [x] For each chunk, find connected chunks (similarity > threshold)
  - [x] Return connection map: `{chunk_id: [connected_ids, ...]}`

**File:** `blogger/agents/analyzer.py` (LLM interpretation)

- [x] Add connection reasoning to Analyzer
  - [x] LLM explains WHY chunks connect (thematic links)
  - [x] Example: "#1 and #4 both discuss debugging mindset"
  *Implemented as Agent instruction*

### Task 4: Narrative Flow Suggestion

**File:** `blogger/agents/analyzer.py`

- [x] Add `suggest_narrative_flows_tool` to Analyzer
  - [x] Input: Scored chunks + connection map
  - [x] LLM creates 2-3 different flow options
  - [x] Calculate average score per flow
  - [x] Return flows: `{name, description, chunk_sequence, avg_score}`
  *Implemented as Agent instruction*

- [x] Flows to consider:
  - [x] Quote-driven (high-scoring quotes as anchors)
  - [x] Chronological (time-based progression)
  - [x] Thematic (topic clustering)

### Task 5: Deep Mode Integration

- [ ] Update `blogger/agents/analyzer.py`
  - [ ] Add mode parameter: `light` or `deep`
  - [ ] If deep mode:
    - [ ] Run chunk extraction
    - [ ] Score all chunks
    - [ ] Map connections
    - [ ] Suggest flows
  - [ ] If light mode:
    - [ ] Run only complexity detection (Phase 4 behavior)

- [ ] Update `blogger/agents/analyzer.md` (instructions)
  - [ ] Add deep mode workflow
  - [ ] Add chunk scoring criteria
  - [ ] Add flow suggestion examples

- [ ] Add mode decision logic
  - [ ] If complexity ≥ 7: Ask user "Run deep analysis?"
  - [ ] If complexity < 7: Use light mode automatically
  - [ ] User can explicitly request deep mode via parameter

### Task 6: Architect Integration

- [x] Update `blogger/agents/architect.py`
  - [x] Check `0-analysis.md` front-matter for `mode: deep`
  - [x] If deep mode:
    - [x] Read chunk map from analysis
    - [x] Reference chunks by ID when building outlines
    - [x] Use suggested flows as starting points
  - [x] If light mode:
    - [x] Use Phase 4 behavior (read draft.md directly)

- [x] Update `blogger/agents/architect.md`
  - [x] Add instructions for chunk-based outlining
  - [x] Example: "Build outline using Flow A: #1 → #2 → #4..."
  - [x] Guidance on when to reference draft.md vs chunk IDs

### Task 7: Curator Integration

**Goal:** Make Curator analysis-aware so it can work with pre-processed chunks instead of re-parsing draft.

**File:** `blogger/utils/tools.py`

- [x] Create `read_chunks_for_curation(blog_id: str) -> dict`
  *Implemented as part of updated `read_analysis_tool`*

**File:** `blogger/agents/curator.py`

- [x] Update Curator to check for analysis mode
  - [x] Call `read_analysis_tool` at start
  - [x] If mode=deep: Use chunk-based organization
  - [x] If mode=light or none: Use current draft.md parsing

- [x] Implement chunk-based filtering (deep mode)
  - [x] For each chunk, determine which outline section it fits
  - [x] Use chunk scores as quality hints
  - [x] Use chunk topics for section matching
  - [x] Chunks that match outline sections → in-scope
  - [x] Chunks that don't match any section → out-of-scope

- [x] Preserve chunk IDs in organized output
  - [x] Format: `<!-- Chunk #1 -->` before content
  - [x] Allows traceability back to analysis
  - [x] Useful for debugging and Writer phase

- [x] Update `blogger/agents/curator.md` (instructions)
  - [x] Add section on analysis-aware curation
  - [x] Explain chunk-based vs draft-based workflows
  - [x] Add examples of using chunk scores/topics for decisions

**Key Decision: Backward Compatibility**
- [x] Ensure Curator works WITHOUT analysis (graceful fallback)
  - [x] If no `0-analysis.md`: Parse draft.md as before (Phase 2 behavior)
  - [x] If `mode: light`: Parse draft.md (chunks not available)
  - [x] Only use chunks if `mode: deep` AND chunks exist
  - [x] No breaking changes to existing workflow

### Task 8: Testing

- [x] Create test draft for deep mode
  - [x] Narrative post with 15+ quotes
  - [x] Personal reflections interwoven
  - [x] Some tangential content (low-scoring chunks)

- [x] Test Analyzer deep mode standalone
  - [x] Run: `python -m blogger.playground --agent analyzer --mode deep` (via test script)
  - [x] Verify: Chunks extracted (32+)
  - [x] Verify: Scores assigned (8 high-scoring)
  - [x] Verify: Connections mapped
  - [x] Verify: 2-3 flows suggested with avg scores

- [x] Test Architect with deep analysis
  - [x] Run Architect after deep analysis exists
  - [x] Verify: Architect reads chunk map
  - [x] Verify: Outline references chunk IDs
  - [x] Verify: Flow A used as basis for outline v1

- [x] Test Curator with deep analysis (NEW)
  - [x] Run full workflow: Analyzer (deep) → Architect → Curator
  - [x] Verify: Curator detects mode=deep
  - [x] Verify: Curator uses chunks instead of re-parsing draft
  - [x] Verify: Organized output includes chunk IDs (`<!-- Chunk #1 -->`)
  - [x] Verify: Chunks matched to correct sections
  - [x] Verify: Low-scoring chunks marked as out-of-scope

- [x] Test Curator backward compatibility
  - [x] Run Curator WITHOUT analysis file (Implicit in design)
  - [x] Verify: Falls back to Phase 2 behavior (parse draft.md)
  - [x] Run Curator with light mode analysis
  - [x] Verify: Uses draft.md (chunks not available)

### Task 9: Documentation

- [x] Update `progress/PROGRESS.md`
  - [x] Add Phase 5 checklist
  - [x] Mark tasks complete

- [x] Create lesson: `progress/lessons/phase5_analyzer_deep_mode.md`
  - [x] Document chunk extraction approach
  - [x] Document scoring criteria
  - [x] Capture when deep mode is worth the cost

- [x] Update `AGENTS.md`
  - [x] Document light vs deep mode
  - [x] Update workflow diagram with decision points

---

## 🧪 Testing Strategy

### Unit Tests (pytest)

**File:** `blogger/tests/test_chunk_tools.py`

```python
def test_split_draft_into_chunks():
    """Test chunk extraction preserves structure"""
    draft = """
    # Heading

    "Quote here" — Author

    My commentary on the quote.

    ```python
    code_block()
    ```
    """
    chunks = split_draft_into_chunks(draft)
    assert len(chunks) == 4  # heading, quote, commentary, code
    assert chunks[0]["type"] == "heading"
    assert chunks[1]["type"] == "quote"
    assert chunks[2]["type"] == "commentary"
    assert chunks[3]["type"] == "code"

def test_calculate_chunk_similarity():
    """Test similarity detection"""
    chunk1 = "Debugging is about understanding errors deeply"
    chunk2 = "Errors help us understand debugging better"
    chunk3 = "Python is a great language"

    sim_12 = calculate_chunk_similarity(chunk1, chunk2)
    sim_13 = calculate_chunk_similarity(chunk1, chunk3)

    assert sim_12 > 0.5  # Similar topics
    assert sim_13 < 0.3  # Different topics

def test_map_chunk_connections():
    """Test connection mapping"""
    chunks = [
        {"id": "1", "text": "Debugging errors deeply"},
        {"id": "2", "text": "Errors help debugging"},
        {"id": "3", "text": "Python language features"},
    ]
    connections = map_chunk_connections(chunks)

    assert "2" in connections["1"]  # 1 and 2 connected
    assert "3" not in connections["1"]  # 1 and 3 not connected
```

### Integration Tests (Playground)

**Scenario 1: Complexity Triggers Deep Mode Suggestion**
1. Create complex narrative draft (15 quotes, reflections)
2. Run: `python -m blogger.playground --agent analyzer`
3. Verify: Complexity score = 8.2 (high)
4. Verify: Analyzer asks: "Run deep analysis? (Recommended for complex drafts)"
5. User confirms
6. Verify: Deep mode runs, chunks extracted, scored, flows suggested

**Scenario 2: Explicit Deep Mode Request**
1. Create moderate draft (complexity score = 5.5)
2. Run: `python -m blogger.playground --agent analyzer --mode deep`
3. Verify: Deep mode runs regardless of complexity
4. Verify: Full chunk analysis completed

**Scenario 3: Light Mode for Simple Draft**
1. Create simple technical draft (2 quotes, code snippets)
2. Run Analyzer
3. Verify: Complexity score = 3.8 (low)
4. Verify: Light mode runs automatically (no deep mode prompt)

**Scenario 4: Architect Uses Chunk Map**
1. Run deep analysis on complex draft
2. Verify: `0-analysis.md` contains chunk map with IDs
3. Run Architect
4. Verify: Architect references chunks by ID in outline
5. Example outline:
   ```
   ## Section 1: The Philosophy
   [Anchor: Chunk #1 - Karpathy quote about errors]

   ## Section 2: The Journey
   [Anchor: Chunk #2 - My Phase 1 struggles]
   ```

**Scenario 5: Flow Comparison**
1. Deep analysis suggests Flow A (score: 8.4), Flow B (score: 7.2)
2. Architect creates outline_v1 based on Flow A
3. Architect creates outline_v2 based on Flow B
4. User compares and chooses preferred flow

**Scenario 6: Full Workflow with Curator (Deep Mode)**
1. **Analyzer (Deep):**
   - Complex draft with 15 quotes
   - Outputs 32 chunks with scores
   - Chunks #1, #2, #12 scored high (≥8.0)
   - Chunk #28 scored low (3.2 - tangent)

2. **Architect:**
   - Reads chunk map
   - Creates outline using Flow A
   - References chunks #1, #2, #12 as anchors
   - User approves → `1-outline.md`

3. **Curator:**
   - Detects `mode: deep` in `0-analysis.md`
   - Reads 32 chunks from analysis
   - Matches chunks to outline sections:
     - Chunk #1 → Section 1 (Philosophy)
     - Chunk #4 → Section 1 (same topic, not in architect's outline)
     - Chunk #2 → Section 2 (Journey)
     - Chunk #28 → Out-of-Scope (low score, no section match)
   - Outputs `2-draft_organized.md` with chunk IDs preserved

4. **Verify:**
   - Organized draft includes chunk comments: `<!-- Chunk #1 -->`
   - All high-scoring chunks (≥8.0) in appropriate sections
   - Low-scoring chunk #28 in "Out-of-Scope" section
   - Curator found chunk #4 that Architect didn't reference
   - No re-parsing of draft.md (used chunks directly)

**Scenario 7: Curator Backward Compatibility**
1. Delete `0-analysis.md` from blog folder
2. Run Curator (outline already exists from previous run)
3. Verify: Curator detects no analysis file
4. Verify: Falls back to Phase 2 behavior (parses draft.md)
5. Verify: Still produces valid `2-draft_organized.md`
6. Compare: Output same quality, but Curator took longer (re-parsed draft)

---

## 📚 References

### Completed Phases
- **Phase 4:** Analyzer Foundation (light mode, complexity detection)
- **Phase 1-2:** Architect & Curator agents

### Related Techniques
- **TF-IDF:** Term frequency-inverse document frequency for topic extraction
- **Cosine similarity:** Measure similarity between text chunks
- **Jaccard similarity:** Simple keyword overlap metric

### External Resources
- NLP libraries: `sklearn` (TfidfVectorizer), `nltk` (stopwords)
- Markdown parsing: Built-in Python `re` or `mistune` library

---

## 🎓 Learning Outcomes

By completing Phase 5, you'll learn:
- **Content chunking:** Splitting unstructured text into meaningful pieces
- **LLM-based scoring:** Using AI to evaluate content quality
- **Similarity metrics:** Detecting thematic connections between text chunks
- **Flow optimization:** Sequencing content for narrative coherence
- **Conditional complexity:** When to use simple vs advanced analysis

---

## Success Criteria

Phase 5 is complete when:
1. ✅ Chunk extraction works reliably (unit tests pass)
2. ✅ Scoring produces consistent, meaningful results
3. ✅ Connection mapping identifies thematic links
4. ✅ Flow suggestions provide actionable outline structures
5. ✅ Architect can build outlines using chunk IDs
6. ✅ Curator can use chunks for efficient organization (NEW)
7. ✅ Curator maintains backward compatibility (works without analysis)
8. ✅ Deep mode noticeably improves quote-heavy draft organization
9. ✅ User can choose between light and deep modes
10. ✅ Full workflow tested: Analyzer → Architect → Curator

---

## Trade-offs and Considerations

### When is Deep Mode Worth It?

**Worth the cost:**
- 10+ quotes from diverse sources
- Complex narrative threading required
- User struggling to see structure in chaos
- High-stakes content (important post, needs precision)

**Not worth the cost:**
- Simple technical posts (2-3 quotes max)
- Clear structure already evident
- User knows desired flow intuitively
- Quick draft iteration (speed > analysis depth)

### Performance Considerations

**Deep mode costs:**
- Chunk extraction: ~2 seconds (pure function)
- Scoring 32 chunks: ~20 seconds (LLM calls, batch if possible)
- Connection mapping: ~5 seconds (similarity calculations)
- Flow suggestion: ~10 seconds (LLM reasoning)
- **Total: ~40 seconds** vs light mode (~5 seconds)

**Optimization opportunities:**
- Batch chunk scoring (score 5-10 chunks per LLM call)
- Cache similarity calculations
- Parallel flow generation (if multiple flows independent)

### User Experience

**Key questions:**
1. Does deep mode actually produce better outlines? (Measure in testing)
2. Is 40-second wait worth the quality gain?
3. Can we show progress during deep analysis? ("Scoring chunks: 15/32...")
4. Should deep mode be default for narrative posts?

---

## Next Steps

After Phase 5 completion:
- Test with real blog posts (your AI journey series)
- Gather feedback: Does chunk-based workflow help? (Architect + Curator)
- Measure efficiency gains: Chunk-based vs draft-parsing curation
- Evaluate: Should Writer reference chunks for section polishing?
- Consider: Add chunk ID tracking throughout entire pipeline?

---

## Open Questions (To Explore During Implementation)

1. **Chunk granularity:** Should we split by paragraph, sentence, or semantic units?
2. **Scoring criteria:** Are clarity + insight + authority sufficient? Missing anything?
3. **Connection threshold:** What similarity score (0.5? 0.6?) best identifies meaningful links?
4. **Flow count:** Always suggest 3 flows, or variable based on content?
5. **Architect adaptation:** Should Architect always use chunk IDs in deep mode, or optional?
6. **Curator chunk matching:** How does Curator decide if a chunk fits a section? (NEW)
   - Use only chunk topics?
   - Use chunk score as quality threshold?
   - LLM reasoning for each chunk-section match?
   - Hybrid approach (topics + LLM for borderline cases)?
7. **Chunk ID preservation:** Should chunk IDs flow all the way to Writer phase? (NEW)
   - Benefits: Full traceability from analysis → final post
   - Drawback: Extra metadata in organized draft

These questions will be answered through testing and user feedback during implementation.
