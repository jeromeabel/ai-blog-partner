"""
The Architect Agent - Step 1: Draft → Outline

This agent helps users transform raw drafts into structured outlines
through interactive conversation.
"""

from google.adk.agents.llm_agent import Agent

from blogger.agents.scribr import scribr
from blogger.utils.tools import (
    get_workflow_status_tool,
    infer_blog_id_tool,
    read_draft_tool,
    read_file_tool,
    save_step_tool,
)
from blogger.utils.utils import read_instructions

architect = Agent(
    model="gemini-3-pro-preview",
    name="architect",
    description="The Architect - Expert Editor & Structural Thinker",
    instruction=read_instructions("architect.md"),
    tools=[
        get_workflow_status_tool,
        infer_blog_id_tool,
        read_draft_tool,
        read_file_tool,
        save_step_tool,
    ],
    sub_agents=[scribr],
)
