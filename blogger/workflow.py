"""
AI Blog Partner - Workflow Orchestrator

Multi-agent pipeline for transforming raw drafts into polished blog posts.
Follows ADK patterns with main orchestrator agent and specialized sub-agents.
"""

import datetime

from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.google_search_tool import google_search

from blogger.agents import linguist, scribr
from blogger.step_agents.step_1_outline import (
    draft_loader,
    robust_content_split_step,
    robust_outline_step,
)
from blogger.tools import read_draft_tool, save_step_tool

# === ORCHESTRATOR AGENT ===
orchestrator = Agent(
    name="orchestrator",
    model="gemini-2.5-flash",
    description="AI Blog Partner orchestrator managing the 6-step writing pipeline",
    instruction=f"""
    You are the AI Blog Partner Orchestrator. You manage a 6-step pipeline to transform
    raw technical blog drafts into polished, authentic articles.

    You work with two specialist agents:
    - **Scribr**: A Senior Technical Writer Partner (strategist, drafter, editor)
    - **Linguist**: An English Language Coach (language mechanics only)

    ## Your Workflow

    **Step 1: Draft to Outlines**
    - Input: Raw draft from user (blog_id provided)
    - Use `draft_loader` to load the raw draft into session state
    - Use `robust_outline_step` to create the blog outline (reads raw_draft from session state)
    - Use `robust_content_split_step` to split content into matching/unused chunks (reads raw_draft from session state)
    - Use `save_step_tool` to save outputs:
      - Step "outlines" → outlines.md
      - Step "draft_ok" → draft_ok.md
      - Step "draft_not_ok" → draft_not_ok.md
    - Output: outlines.md, draft_ok.md, draft_not_ok.md

    **Step 2: Organization**
    - Input: outlines.md, draft_ok.md
    - Reorganize text chunks to match the outline structure
    - Output: draft_organized.md

    **Step 3: Drafting & Research**
    - Input: outlines.md, draft_organized.md
    - For each section:
      - Scribr expands/rewrites (use google_search for fact-checking)
      - Linguist reviews language mechanics
    - Output: draft_nice.md

    **Step 4: Polishing**
    - Input: draft_nice.md
    - Scribr applies final "No-Hype" and authenticity rules
    - Output: draft_polished.md

    **Step 5: Finalization**
    - Input: draft_polished.md
    - Format for publishing, generate SEO metadata
    - Output: final.md

    **Step 6: Illustration (Optional)**
    - Brainstorm cover art concepts
    - Output: illustration_ideas.md

    ## State Management
    - Raw draft: `raw_draft` (loaded by `draft_loader`)
    - Outline: `blog_outline` (set by `robust_outline_step`)
    - Content split: `content_split` (dict with draft_ok, draft_not_ok, set by `robust_content_split_step`)
    - Current step: `current_step`

    ## Instructions
    - Always confirm the blog_id before starting
    - Execute steps sequentially unless user specifies otherwise
    - Present outputs to user for approval between major steps
    - Use tools for all file operations

    Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
    """,
    sub_agents=[
        draft_loader,
        robust_outline_step,
        robust_content_split_step,
        scribr,
        linguist,
    ],
    tools=[
        FunctionTool(read_draft_tool),
        FunctionTool(save_step_tool),
        google_search,
    ],
)


# === CONVENIENCE FUNCTION ===


def run_workflow(blog_id: str):
    """
    Convenience function to start the workflow.

    Args:
        blog_id: Blog identifier (matches directory in inputs/)

    Usage:
        from blogger.workflow import run_workflow
        run_workflow("my-first-post")
    """
    # TODO: Implement session runner
    # This will be the entrypoint when we build the CLI in Phase 3
    print(f"Starting workflow for blog: {blog_id}")
    print("Full implementation coming in Phase 3.2 (CLI Entrypoint)")
    return orchestrator
