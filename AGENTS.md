# AI Blog Partner - Agent System

This project implements a multi-agent system to assist in writing technical blog posts. It emphasizes a "partner" relationship, where the AI acts as a Senior Technical Writer and an English Language Coach, focusing on authenticity, technical depth, and specific writing constraints.

## 🤖 The Agents

### 1. **The Writer (Scribr)**
*The Senior Technical Writer Partner*

*   **Role:** Strategic writing partner, editor, and structurer.
*   **Persona:** Former Junior Frontend Engineer turned Editor. deeply technical, skeptical of hype, and radically human.
*   **Voice:** Authentic, peer-to-peer (Dev-to-Dev), no corporate fluff.
*   **Core Philosophy:** "System Thinking" meets "Radical Humanism."
*   **Responsibilities:**
    *   **Phase A (Strategist):** Brainstorming, finding the "Angle," identifying the audience and objections.
    *   **Phase B (Drafter):** Structuring the narrative (Inverted Pyramid, RFC, or War Story).
    *   **Phase C (Editor):** Polishing text, enforcing "No-Hype" and "Authenticity" rules, providing educational feedback.

### 2. **The Coach (Linguist)**
*The English Language Coach*

*   **Role:** Dedicated language mechanic for non-native speakers.
*   **Persona:** Supportive peer reviewer.
*   **Responsibilities:**
    *   Implicitly fixing minor errors.
    *   Identifying "French-to-English" patterns.
    *   Explaining grammar rules (the "Why").
    *   **Constraint:** strictly silent on style and content; focuses ONLY on language mechanics.

### 3. **The Orchestrator**
*The Workflow Manager*

*   **Role:** Manages the pipeline and state.
*   **Responsibilities:**
    *   Executes the 6-step workflow.
    *   Handles file operations (reading drafts, splitting files, saving outputs).
    *   Delegates tasks to Scribr and Linguist.
    *   Uses LoopAgents for automatic quality retries.

### 4. **Validation Agents**
*Quality Control via LoopAgent Pattern*

These custom `BaseAgent` validators ensure output quality through automatic retries:

#### **OutlineValidationChecker**
*   **Role:** Validates blog outline structure before proceeding.
*   **Quality Criteria:**
    *   Outline has at least 3 sections (## markdown headings)
    *   Contains "Introduction" section
    *   Contains "Conclusion" section
*   **Behavior:**
    *   Returns `Event(actions=EventActions(escalate=True))` if valid → exits LoopAgent
    *   Returns regular `Event` if invalid → triggers retry (up to max_iterations)

#### **ContentSplitValidationChecker**
*   **Role:** Validates content redistribution integrity.
*   **Quality Criteria:**
    *   Both `draft_ok` and `draft_not_ok` exist
    *   Combined length ≈ original draft (±10%)
    *   All content from raw draft preserved (no lost paragraphs)
    *   No new content added (LLM copy-pastes, doesn't generate)
    *   No duplicate content between files
*   **Behavior:**
    *   Uses `blogger/validation_utils.py` for paragraph-level set comparison
    *   Provides actionable error messages (e.g., "Lost content: 2 paragraphs missing")
    *   Escalates on success, retries on failure

**Implementation Pattern (LoopAgent):**
```python
robust_outline_step = LoopAgent(
    sub_agents=[
        outline_creator,           # Worker: creates the outline
        OutlineValidationChecker   # Validator: checks quality
    ],
    max_iterations=3  # Retry up to 3 times
)
```

**Why LoopAgent?**
- **Automatic Retries:** If LLM produces invalid output, validator triggers retry
- **Quality Assurance:** Ensures outputs meet criteria before proceeding to next step
- **Graceful Degradation:** Falls back to best attempt after max_iterations

---

## 🔄 Workflow Architecture

The system operates on a linear but iterative pipeline:

### **Step 1: Draft to Outlines**
*   **Input:** Raw draft from `inputs/<blog_id>/draft.md`.
*   **Action:**
    1.  **`robust_outline_step` (LoopAgent):** Scribr analyzes the draft and creates an outline.
        *   Worker: `outline_creator` (uses Scribr sub-agent + `read_draft_tool`)
        *   Validator: `OutlineValidationChecker` (checks 3+ sections, intro, conclusion)
        *   Retries up to 3 times if validation fails
    2.  **`robust_content_split_step` (LoopAgent):** Scribr splits content into matching/unused.
        *   Worker: `content_splitter` (uses Scribr sub-agent)
        *   Validator: `ContentSplitValidationChecker` (checks integrity: no lost/added/duplicated content)
        *   Retries up to 2 times if validation fails
    3.  **Orchestrator** saves outputs using `save_step_tool`.
*   **Output:** `outlines.md`, `draft_ok.md`, `draft_not_ok.md`.
*   **Quality Assurance:** Both LoopAgents automatically retry on validation failure, ensuring high-quality outputs.

### **Step 2: Organization**
*   **Input:** `outlines.md`, `draft_ok.md`.
*   **Action:** **Orchestrator** (or a specialized sub-task) reorganizes the text chunks from `draft_ok.md` to match the structure of `outlines.md`.
*   **Output:** `draft_organized.md`.

### **Step 3: Drafting & Research**
*   **Input:** `outlines.md`, `draft_organized.md`.
*   **Action:** Iterative writing loop per section.
    *   **Scribr** expands/rewrites sections, checking data sources (Search).
    *   **Linguist** monitors input/output for language corrections.
*   **Output:** `draft_nice.md`.

### **Step 4: Polishing**
*   **Input:** `draft_nice.md`.
*   **Action:** **Scribr** applies final "No-Hype" and style rules.
*   **Output:** `draft_polished.md`.

### **Step 5: Finalization**
*   **Input:** `draft_polished.md`.
*   **Action:** Formatting, SEO meta descriptions, final checks.
*   **Output:** `final.md`.

### **Step 6: Illustration (Optional)**
*   **Action:** Brainstorming and generating cover art ideas.

---

## 🛠️ Tooling & Configuration

*   **File System:** Strict directory structure (`inputs/`, `outputs/`).
*   **Memory:** `Linguist` maintains a long-term memory of user's common mistakes.
*   **Search:** Google Search integration for fact-checking during Step 3.
