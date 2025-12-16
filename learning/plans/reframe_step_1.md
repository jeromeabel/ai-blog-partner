# Plan: Phase 1 - Foundation & The Architect

## Objective
Establish a reliable, interactive testing environment ("The Playground") and implement the first step of the pipeline: "The Architect" (Draft -> Outline).

## Context
We are restarting with a "Simple First" approach. Instead of a complex Orchestrator, we will build a `playground.py` script that allows us to load a specific agent and chat with it directly in the terminal. This is our primary "Verification" tool.

## Step 1.1: The Playground 🛝

**Goal:** Create a script to run a single agent interactively.

1.  **Create `blogger/playground.py`:**
    *   It should accept an argument (e.g., `--agent scribr`).
    *   It should initialize the `GenAI` client or ADK agent.
    *   It should run a simple `while True:` loop for input/output.
    *   *Constraint:* Keep it extremely simple. No complex state management yet.

2.  **Verify:**
    *   Run `python -m blogger.playground --agent scribr`
    *   Say "Hello".
    *   Receive a response.

## Step 1.2: The Architect Agent 🏛️

**Goal:** Turn a draft into an outline using the Playground.

1.  **Create `blogger/step_agents/architect.py`:**
    *   Define a simple function/agent that sets up the system prompt.
    *   System Prompt (`instructions/architect.md`): "You are an expert editor. Read the user's draft and propose a strong, logical outline."

2.  **Verify (The "Real" Test):**
    *   Run Playground with the Architect agent.
    *   Paste the content of `inputs/my-ai-journey-2/draft.md`.
    *   See if it produces a *good* outline.
    *   Refine the prompt until it does.

## Step 1.3: Save Tooling (Optional but good)

**Goal:** Allow the Architect to save the `outline.md` when the user says "Yes, that's perfect."

1.  **Add `save_file` tool** to the Architect.
2.  **Verify:**
    *   Chat -> "Create outline" -> "Looks good, save it." -> Check `outputs/my-ai-journey-2/outline.md`.

## User Instructions
1.  Read this plan.
2.  We will start with **Step 1.1**.
3.  I (The AI) will ask you to create the `playground.py` file.
