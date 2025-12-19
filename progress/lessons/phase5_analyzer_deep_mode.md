# Lesson: Phase 5 - Analyzer Deep Mode

**Date:** 2025-12-19
**Focus:** Advanced Content Analysis & Chunk-Based Workflow

## What We Built
We extended the **Analyzer** agent to support "Deep Mode" for complex narrative drafts. This transforms the drafting process from a linear text parse to a structured, data-driven workflow.

### Key Components
1.  **Chunk Extraction:** Splitting drafts into atomic units (quotes, commentary, code) while preserving line numbers.
2.  **LLM Scoring:** Evaluating each chunk (0-10) for clarity, insight, and authority.
3.  **Connection Mapping:** Using Jaccard similarity to find thematic links between chunks.
4.  **Narrative Flows:** Suggesting structural arcs (e.g., "Quote-Driven Journey") based on high-scoring anchors.
5.  **Integration:**
    *   **Architect:** Uses high-scoring chunks as section anchors.
    *   **Curator:** Uses chunks for filtering, avoiding re-parsing and improving accuracy.

## Key Learnings

### 1. The Power of "Anchors"
By identifying high-scoring quotes (Score > 8.0) early, the Architect can build outlines around *content that matters* rather than generic headers. This prevents "fluff" sections.

### 2. Chunk-Based Curation vs. Text Parsing
*   **Old Way:** Curator parses raw text -> Matches to outline -> Often misses context or includes tangents.
*   **New Way (Deep Mode):** Curator iterates through pre-scored chunks -> "Chunk #21 (Score 2.0) is a tangent" -> Exclude.
*   **Result:** Much sharper filtering. The test run successfully cut a "mechanical keyboard" tangent because the Analyzer flagged it as low-value.

### 3. Traceability is Critical
Preserving `<!-- Chunk #ID -->` in the organized draft is essential. It allows:
*   **Debugging:** We can see exactly which chunk from analysis ended up where.
*   **Writer Context:** The Writer (Step 3) will know the source of every paragraph.

### 4. Backward Compatibility
We maintained a "Light Mode" fallback. Simple posts don't need 40 seconds of chunk analysis. The system seamlessly handles both `mode: deep` and `mode: light` files.

## Future Improvements
*   **Writer Integration:** The Writer agent could verify that high-scoring chunks are preserved in the final polish.
*   **Visualizing Flows:** A simple graphviz or mermaid diagram of the connections would be cool for the user.
*   **Custom Scoring:** Allow users to define what "High Score" means (e.g., "Focus on technical accuracy" vs "Focus on story").

## Conclusion
Deep Mode turns the "Chaos" of a first draft into a "Database" of ideas. This makes the subsequent agents (Architect, Curator) significantly smarter and more autonomous.
