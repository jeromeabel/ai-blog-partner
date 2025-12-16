"""
AI Blog Partner - Workflow Orchestrator

Multi-agent pipeline for transforming raw drafts into polished blog posts.
Follows ADK patterns with main orchestrator agent and specialized sub-agents.
"""

import datetime
from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool

# from google.adk.tools.google_search_tool import google_search  # Temporarily disabled for testing
# from blogger.step_agents.step_1_outline import (
#     draft_loader,
#     robust_content_split_step,
#     robust_outline_step,
# )
# from blogger.step_agents.step_2_organize import (
#     robust_organizer_step,
# )
from blogger.tools import read_draft_tool, save_step_tool
from blogger.utils import read_instructions

# === ORCHESTRATOR AGENT ===
class OrchestratorAgent(Agent):
    """Custom Agent class to avoid app name mismatch warnings."""
    pass

orchestrator = OrchestratorAgent(
    name="orchestrator",
    model="gemini-2.5-flash",
    description="AI Blog Partner orchestrator managing the 6-step writing pipeline",
    instruction=f"{read_instructions('orchestrator.md')}\n\nCurrent date: {datetime.datetime.now().strftime('%Y-%m-%d')}",
    sub_agents=[
        # draft_loader,  # Removed: draft_loader is now a sub-agent of robust_outline_step
        # robust_outline_step,
        # robust_content_split_step,
        # robust_organizer_step,
        # Note: scribr and linguist are sub-agents of specific step agents
        # They cannot also be sub-agents of orchestrator (ADK limitation)
    ],
    tools=[
        FunctionTool(read_draft_tool),
        FunctionTool(save_step_tool),
        # google_search,  # Temporarily disabled - not supported by gemini-2.5-flash
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
