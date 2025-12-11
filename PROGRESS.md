# AI Blog Partner - Progress & Learning Log

## 👨‍🏫 Teacher/Student Protocol
*   **My Role (Claude Code):** I am the Teacher. I explain concepts, provide specs, give tasks, and check your code.
*   **Your Role (Human):** You are the Student. You write the code to prove understanding.
*   **Process:**
    1.  I give you a specific coding task with context and guidance.
    2.  You write the code.
    3.  I review it and provide feedback.
    4.  If correct, we check the box ✅ in the roadmap and I record what you learned in "Learned Concepts".
*   **Goal:** Learn by doing. Every completed task adds new concepts to your knowledge base.

## 🧠 Learned Concepts

### 🎓 Lesson 1.1: Agent Definitions & Instructions
*   **Instruction Storage:** Store agent instructions in separate Markdown files (e.g., `blogger/instructions/`). This keeps Python code clean and allows for easy prompt iteration.
*   **Robust Path Handling:** When reading instruction files, always construct file paths relative to the current Python file (`Path(__file__).parent`) to ensure portability, especially when modules are imported.
*   **Instruction Structure (Markdown):** Use clear Markdown headings (`#`, `##`) to structure agent instructions (e.g., `## Persona & Role`, `## Rules`, `## Output Format`). This improves LLM comprehension and human readability.
*   **Persona Priming:** Explicitly define the agent's role at the very beginning of its instruction (e.g., "You are Scribr, a Senior Technical Writer Partner.").
*   **Negative Constraints:** Clearly state what the agent *must not* do (anti-patterns) to guide its behavior away from undesirable outputs.
*   **Few-Shot Examples:** Provide concrete examples of desired input-output pairs within the instructions. This is highly effective for shaping agent behavior, especially for specific output formats or stylistic requirements.
*   **Model Selection:** Choose the appropriate Gemini model based on the task's complexity (e.g., `gemini-1.5-pro` or `gemini-3-pro-preview`). Refer to [Gemini Models](https://ai.google.dev/gemini-api/docs/models).

### 🎓 Lesson 1.2: File Operations Tooling
*   **Project Root Navigation:** Use `Path(__file__).parent.parent` to navigate from a module (e.g., `blogger/tools.py`) to the project root directory, ensuring correct paths for project-wide directories like `inputs/` and `outputs/`.
*   **Path Constants:** Define directory paths as module-level constants (e.g., `INPUTS_DIR`, `OUTPUTS_DIR`) for reusability and clarity throughout the codebase.
*   **Path Composition:** Use the `/` operator with `Path` objects for clean, readable path construction (e.g., `INPUTS_DIR / blog_id / "draft.md"`).
*   **Safe Directory Creation:** Use `Path.mkdir(parents=True, exist_ok=True)` to create nested directories safely. `parents=True` creates intermediate directories (like `mkdir -p`), and `exist_ok=True` prevents errors if the directory already exists.
*   **Minimal Error Handling:** Check for file existence before reading and raise clear, descriptive exceptions (e.g., `FileNotFoundError` with custom message) to help debug issues early.

### 🎓 Lesson 1.3: Workflow Skeleton & ADK Orchestration
*   **ADK Tool Return Convention:** All tool functions must return `dict` (not `str`, `None`, or primitives). The LLM needs structured data to understand tool results and make decisions.
*   **Consistent Tool Signatures:** Use `{"status": "success", ...}` pattern for all successful tool returns. This provides uniform structure and makes it clear when operations complete successfully.
*   **Path Serialization:** When returning `Path` objects in dicts, convert them to strings using `str(path)`. ADK tools must return JSON-serializable data.
*   **Error Handling via Dicts:** Return `{"status": "error", "message": "..."}` for all failures. Never raise exceptions from tools - ADK framework expects dict returns. Make error messages actionable so agents can self-correct.
*   **Generic vs. Specific Keys:** Balance between generic key names (e.g., `"content"`) for reusability and specific names (e.g., `"draft_content"`) for clarity. Generic names work well when context is clear.
*   **Action-Focused Docstrings:** Tool docstrings are "user manuals" for the LLM. Describe WHAT the tool does and WHEN to use it, not HOW it's implemented. Avoid implementation details like "this is a placeholder" - the LLM doesn't need to know internal state.
*   **Error Propagation in Composite Tools:** When a tool calls other tools (e.g., `split_draft_tool` calls `save_step_tool`), check the nested tool's `status` and propagate errors immediately. Wrap everything in try/except for unexpected errors.
*   **Tools vs. Agents Separation:** Tools should be purely mechanical (file I/O, API calls, calculations). Intelligence (semantic analysis, content understanding, decision-making) belongs in agents. If a tool would need to "understand" content, that's a sign the work should be done by an agent instead.
*   **Orchestrator Pattern:** The orchestrator agent manages workflow via natural language `instruction` parameter, not imperative Python code. It delegates intelligence to sub-agents and uses tools for mechanical operations. The instruction describes what to do, and the LLM figures out how.
*   **Workflow as Natural Language:** Agent instructions are prompts, not code. Describe steps with "Use X tool", "Collaborate with Y agent", "Output Z file". The orchestrator interprets and executes based on this description.

## 🗺️ Roadmap

### Phase 1: Foundation & Tools 🛠️
- [x] **1.1 Agent Definitions:** Create `blogger/agents.py` and define `Scribr` and `Linguist` using `google.adk`.
- [x] **1.2 Tooling (File Ops):** Create `blogger/tools.py` for file reading/writing/splitting.
- [x] **1.3 Workflow Skeleton:** Create `blogger/workflow.py` to structure the pipeline.
  - [x] **1.3.1:** Update `blogger/tools.py` to return dicts (ADK convention)
  - [x] **1.3.2:** ~~Add `split_draft_tool` function~~ [REMOVED - agents do intelligence, tools do mechanics]
  - [x] **1.3.3:** Create `blogger/workflow.py` orchestrator agent

### Phase 2: Core Logic Implementation ⚙️
- [ ] **2.1 Step 1 (Drafting):** Implement `draft_to_outlines` logic.
- [ ] **2.2 Step 2 (Organizing):** Implement `outlines_to_draft_organized` logic.
- [ ] **2.3 Step 3 (Writing Loop):** Implement the iterative section writing with both agents.

### Phase 3: Refinement & UI 🚀
- [ ] **3.1 Polishing:** Implement Steps 4 & 5 (Style check & SEO).
- [ ] **3.2 CLI Entrypoint:** Create the main runner.
