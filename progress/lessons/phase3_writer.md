# Phase 3 Lesson: The Writer & Section Manipulation

## 🎯 What we built
We implemented the Writer agent, the third and final step in the blog writing pipeline. This agent focuses on polishing specific sections of the blog post with user feedback, ensuring high quality and style consistency.

### Key Components:
1.  **Section Tools:**
    *   `read_section_tool`: Extracts a specific `##` section from the organized draft, providing previous/next titles for context.
    *   `save_section_tool`: Replaces a section's content while validating that the heading is preserved and matches the target.
    *   `finalize_post_tool`: Copies the polished draft to `3-final.md` and adds a generation timestamp footer.
2.  **Writer Agent:**
    *   Iterative workflow: Read → Draft/Review (with Scribr) → Present to User → Save/Iterate.
    *   Context-aware: Uses surrounding section titles to ensure smooth transitions.
    *   Collaboration-first: Operates on one section at a time to maintain focus and quality.
3.  **Scribr Integration:**
    *   Uses Scribr as a sub-agent for specialized style review and hype removal.

## 💡 Key Learnings

### 1. Section-level Granularity
Polishing an entire document at once is overwhelming for both the LLM and the user. By breaking the document into `##` sections, we:
*   Allow the user to give highly targeted feedback.
*   Reduce the token load per interaction.
*   Make it easy to "undo" or "retry" a specific part of the post without losing progress elsewhere.

### 2. Context is King
Even when working on a single section, the agent needs context. Providing the titles of the `prev_section` and `next_section` is a lightweight way to help the Writer:
*   Avoid repeating information already covered.
*   Write natural transitions ("Now that we've covered X...", "This leads us to Y...").

### 3. Validation and Integrity
Our `save_section_tool` enforces that the heading remains intact. This is critical for maintaining the overall document structure and ensuring that subsequent tool calls (which rely on those headings) still work.

### 4. ADK Parent-Child Constraints
We discovered that in the Google ADK, an agent instance can only have ONE parent.
*   **Problem:** We tried to use the same `scribr` instance as a sub-agent for both `architect` and `writer`.
*   **Error:** `Agent scribr already has a parent agent, current parent: architect`.
*   **Solution:** We refactored `scribr.py` to provide a factory function `create_scribr()` so each parent agent gets its own fresh instance of the assistant.

## 🚀 Future Improvements
*   **Diff-based Previews:** Instead of showing the full polished section, show a diff of what changed (or both).
*   **Batch Polishing:** Allow users to say "Polish the next 3 sections" while still maintaining the section-by-section internal logic.
*   **Section Ordering:** Add a tool to reorder sections in Step 3 if the user realizes the flow needs adjustment.
