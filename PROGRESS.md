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

### 🎓 Lesson 2.1: LoopAgent Pattern & Validation Checkers
*   **BaseAgent Pattern:** Custom agents extend `BaseAgent` and implement `async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]`. This is the foundation for all custom agent logic in ADK.
*   **Loop Termination Signal:** Use `yield Event(author=self.name, actions=EventActions(escalate=True))` to signal LoopAgent to exit successfully. The `escalate=True` flag tells the LoopAgent "quality check passed, stop looping."
*   **Continue Loop Signal:** Use `yield Event(author=self.name, content=...)` without `escalate` to signal LoopAgent to retry. This lets the worker agent try again.
*   **Session State Access:** Read from session state with `ctx.session.state.get("key", default)`. This is how agents share data within a single conversation session (short-term memory).
*   **Event Structure:** Events must have `author=self.name`, optional `content` (types.Content with types.Part for messages), and optional `actions` (EventActions for control signals like escalate).
*   **EventActions Usage:** `EventActions(escalate=True)` goes INSIDE the Event, not as a direct parameter. Common mistake: `Event(escalate=True)` ❌ vs `Event(actions=EventActions(escalate=True))` ✅
*   **Validation Best Practices:**
  - Check existence before accessing data to avoid KeyError
  - Provide specific, actionable error messages that help debugging
  - Handle edge cases (empty data, type mismatches, zero-length inputs)
  - Validate quality criteria (structure, completeness), not just existence
  - Use defensive programming (isinstance checks, default values)
*   **LoopAgent Quality Control:** The "Polisher" pattern wraps a worker agent + validator. Worker creates output → Validator checks quality → If valid, escalate=True exits loop; if invalid, retry up to max_iterations.

### 🎓 Lesson 2.1.1 (Extended): Testing & Refactoring
*   **Extract Pure Functions for Testability:** Move validation logic from class methods to module-level pure functions. This enables easy unit testing without mocking ADK runtime.
*   **Separation of Concerns:** Keep business logic (validation rules) separate from framework integration (ADK agents). Functions do the logic, agents handle Events/state.
*   **Utils Module Pattern:** Create `validation_utils.py` for reusable validation functions. Import into checkers with `from blogger.validation_utils import func`.
*   **Comprehensive Unit Testing:** Write tests for edge cases (empty input, whitespace, case sensitivity, duplicates, missing data). Aim for 100% code coverage.
*   **Pytest Basics:** Use `pytest` for test discovery, `assert` for assertions, class-based test organization (`class TestFunctionName`), and fixtures for setup/teardown.
*   **Test-Driven Development Benefits:** Writing tests reveals edge cases early (e.g., "concluding" vs "conclusion" substring matching). Tests serve as living documentation.
*   **Coverage Analysis:** Use `pytest --cov=module --cov-report=term-missing` to identify untested code paths. 100% coverage ensures all logic branches are validated.
*   **Pure Functions Advantages:**
  - Easy to test (no mocking needed)
  - Reusable across validators
  - No async complexity for logic
  - Clear input/output contracts
*   **Test Organization:** Group related tests in classes (`TestNormalizeAndSplit`, `TestCheckContentIntegrity`). Use descriptive test names (`test_detects_lost_content`).

### 🎓 Lesson 2.1.2: Agent Instructions & Multi-Agent Delegation
*   **Agent Instruction Structure (Official Pattern):** Follow the ADK-recommended hierarchy: (1) Role definition ("You are..."), (2) Primary task ("Your task is..."), (3) Tool guidance (when/why to use each tool), (4) Constraints (scope limitations), (5) Output format (explicit specification).
*   **Tool Reference Pattern:** Never just list tools. Explain WHEN and WHY to use each tool with specific conditions. Example: "Use `read_draft_tool` to load the raw draft content" (good) vs "You have tools: read_draft_tool" (bad). Tool docstrings are the primary source of truth for the LLM.
*   **Sub-Agent Delegation Pattern:** In coordinator instructions, explicitly state delegation triggers: "Collaborate with Scribr to analyze..." or "Use the `robust_blog_planner` tool to..." (ADK treats sub-agents as invokable tools). Include clear `description` fields on sub-agents to guide routing decisions.
*   **Session State Access:** Reference state keys naturally in instructions: "Read the `blog_outline` from session state" or use template syntax `{key_name}` for interpolation. ADK automatically replaces `{var}` with `session.state['var']`.
*   **Output Format Specification:** Show the EXACT expected format with examples (few-shot learning). Use markdown code blocks to demonstrate structure. This reduces hallucination and ensures consistency.
*   **Worker vs Coordinator Instructions:** Workers have narrow scope ("Your ONLY task is..."), focus on direct execution, and use domain tools. Coordinators focus on routing/delegation ("Use X agent when...", "Delegate to Y for..."), make high-level decisions, and orchestrate workflow.
*   **Variable Naming Convention:** Agent variable names must match the `name=""` parameter exactly. Example: `outline_creator = Agent(name="outline_creator", ...)`. This convention ensures consistency in logs, debugging, and imports.
*   **LLM Interpretation Hierarchy:** The LLM learns from (1) Tool docstrings (primary), (2) Agent descriptions (primary for delegation), (3) Instruction text (behavioral guidance), (4) Tool return values (feedback loop). All layers must be coherent.
*   **Markdown Structure Aids Comprehension:** Use headers (`##`), numbered lists, and bullet points in instructions. This improves LLM parsing and creates hierarchical understanding of tasks.
*   **Agent Hierarchy is Dynamic:** There's no fixed "main agent." Hierarchy is call-stack based: when `outline_creator` runs, IT is the boss and Scribr is its worker. When `orchestrator` runs, IT is the boss and `outline_creator` is its worker. Think of it like nested function calls.
*   **max_iterations Behavior:** When LoopAgent reaches max_iterations without `escalate=True`, it stops gracefully (no error), preserves the last output in session state, and returns control to parent. This is a safety net to prevent infinite loops while forcing forward progress.
*   **Explicit Constraints Prevent Scope Creep:** Use "ONLY" language and explicit negative constraints ("Do not engage in...") to keep agents focused. Vague language like "if appropriate" leads to unpredictable behavior.
*   **Delegation vs Self-Contained Agents:** Both patterns are valid. Use delegation when reusing specialized expertise (e.g., Scribr's writing rules). Use self-contained instructions when the task is mechanical and doesn't need the specialist's full knowledge base.
*   **Official ADK Resources:** [Agent Team Tutorial](https://google.github.io/adk-docs/tutorials/agent-team/), [LLM Agents](https://google.github.io/adk-docs/agents/llm-agents/), [Multi-Agent Systems](https://google.github.io/adk-docs/agents/multi-agents/)

## 🗺️ Roadmap

### Phase 1: Foundation & Tools 🛠️
- [x] **1.1 Agent Definitions:** Create `blogger/agents.py` and define `Scribr` and `Linguist` using `google.adk`.
- [x] **1.2 Tooling (File Ops):** Create `blogger/tools.py` for file reading/writing/splitting.
- [x] **1.3 Workflow Skeleton:** Create `blogger/workflow.py` to structure the pipeline.
  - [x] **1.3.1:** Update `blogger/tools.py` to return dicts (ADK convention)
  - [x] **1.3.2:** ~~Add `split_draft_tool` function~~ [REMOVED - agents do intelligence, tools do mechanics]
  - [x] **1.3.3:** Create `blogger/workflow.py` orchestrator agent

### Phase 2: Core Logic Implementation ⚙️
- [ ] **2.1 Step 1 (Draft to Outlines):** Implement outline creation with LoopAgent pattern.
  - [x] **2.1.1:** Create `blogger/validation_checkers.py` with `OutlineValidationChecker` and `ContentSplitValidationChecker`
  - [x] **2.1.2:** Create `blogger/step_agents/step_1_outline.py` with worker agents and LoopAgent wrappers
  - [ ] **2.1.3:** Update `blogger/workflow.py` to use the new step agents
- [ ] **2.2 Step 2 (Organizing):** Implement `outlines_to_draft_organized` logic.
- [ ] **2.3 Step 3 (Writing Loop):** Implement the iterative section writing with both agents.

### Phase 3: Refinement & UI 🚀
- [ ] **3.1 Polishing:** Implement Steps 4 & 5 (Style check & SEO).
- [ ] **3.2 CLI Entrypoint:** Create the main runner.
