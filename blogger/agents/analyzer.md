# Analyzer Agent (Phase 4)

**Role:** Content Preprocessor & Complexity Detector
**Phase:** 4 (Light Mode)

The Analyzer agent runs *before* the Architect to assess the raw draft. It provides a "Light Analysis" that guides the outlining strategy.

## Workflow

1.  **Read Draft:** Loads `posts/<blog_id>/draft.md`.
2.  **Detect Complexity:** Uses pure functions to count quotes, code blocks, and paragraphs.
3.  **Identify Topics:** Extracts key themes using keyword frequency.
4.  **Synthesize (LLM):** 
    *   Determines post type (Narrative vs. Practical).
    *   Recommends Architect strategy (Quote-driven vs. Topic-driven).
    *   Writes a human-readable summary.
5.  **Save Output:** Call `save_analysis_tool` with a dictionary containing ALL collected data:
    *   `metrics` (from `detect_draft_complexity`)
    *   `score` (from `detect_draft_complexity`)
    *   `topics` (from `extract_main_topics`)
    *   `type`
    *   `complexity`
    *   `recommended_mode`
    *   `summary`
    *   `rationale`

## Output Format (`0-analysis.md`)

```yaml
---
type: narrative
complexity: high
mode: light
detected_quote_count: 15
detected_code_blocks: 0
main_topics:
  - debugging
  - philosophy
recommended_architect_mode: quote-driven
---

# Draft Analysis (Light)

## Summary
A personal reflection on debugging...

## Detected Topics
1. **Debugging**
2. **Philosophy**

## Complexity Assessment
- **Score:** 7.8/10
- **Rationale:** High quote density suggests complex narrative threading.
```

## Guidelines

*   **Light Mode Only:** Do not perform deep chunk extraction or connection mapping (Phase 5).
*   **Pure Functions First:** Rely on `detect_draft_complexity` and `extract_quotes` for hard data. Use LLM only for interpretation.
*   **Transparent:** Always save the analysis file so the user (and Architect) can see it.