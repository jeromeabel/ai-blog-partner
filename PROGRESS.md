# AI Blog Partner - Progress & Learning Log

## 👨‍🏫 Teacher/Student Protocol
*   **My Role:** I am the Teacher. I explain concepts and provide specs.
*   **Your Role:** You are the Student. You write the code to prove understanding.
*   **Process:**
    1.  I give you a specific coding task with context.
    2.  You write the code.
    3.  I review it.
    4.  If correct, we check the box and record the concept in "Learned Concepts".

## 🧠 Learned Concepts

### 🎓 Lesson 1: Agent Definitions & Instructions
*   **Instruction Storage:** Store agent instructions in separate Markdown files (e.g., `blogger/instructions/`). This keeps Python code clean and allows for easy prompt iteration.
*   **Robust Path Handling:** When reading instruction files, always construct file paths relative to the current Python file (`Path(__file__).parent`) to ensure portability, especially when modules are imported.
*   **Instruction Structure (Markdown):** Use clear Markdown headings (`#`, `##`) to structure agent instructions (e.g., `## Persona & Role`, `## Rules`, `## Output Format`). This improves LLM comprehension and human readability.
*   **Persona Priming:** Explicitly define the agent's role at the very beginning of its instruction (e.g., "You are Scribr, a Senior Technical Writer Partner.").
*   **Negative Constraints:** Clearly state what the agent *must not* do (anti-patterns) to guide its behavior away from undesirable outputs.
*   **Few-Shot Examples:** Provide concrete examples of desired input-output pairs within the instructions. This is highly effective for shaping agent behavior, especially for specific output formats or stylistic requirements.
*   **Model Selection:** Choose the appropriate Gemini model based on the task's complexity (e.g., `gemini-1.5-pro` or `gemini-3-pro-preview`). Refer to [Gemini Models](https://ai.google.dev/gemini-api/docs/models).

## 🗺️ Roadmap

### Phase 1: Foundation & Tools 🛠️
- [x] **1.1 Agent Definitions:** Create `blogger/agents.py` and define `Scribr` and `Linguist` using `google.adk`.
- [ ] **1.2 Tooling (File Ops):** Create `blogger/tools.py` for file reading/writing/splitting.
- [ ] **1.3 Workflow Skeleton:** Create `blogger/workflow.py` to structure the pipeline.

### Phase 2: Core Logic Implementation ⚙️
- [ ] **2.1 Step 1 (Drafting):** Implement `draft_to_outlines` logic.
- [ ] **2.2 Step 2 (Organizing):** Implement `outlines_to_draft_organized` logic.
- [ ] **2.3 Step 3 (Writing Loop):** Implement the iterative section writing with both agents.

### Phase 3: Refinement & UI 🚀
- [ ] **3.1 Polishing:** Implement Steps 4 & 5 (Style check & SEO).
- [ ] **3.2 CLI Entrypoint:** Create the main runner.