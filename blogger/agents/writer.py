"""
Writer Agent - Polishing Partner

Iteratively polishes blog sections with user feedback and style enforcement.
"""

from google.adk.agents.llm_agent import Agent
from blogger.agents.scribr import create_scribr
from blogger.utils.tools import (
    read_section_tool,
    save_section_tool,
    finalize_post_tool,
    infer_blog_id_tool,
    get_workflow_status_tool
)
from blogger.utils.utils import read_instructions


writer = Agent(
    model="gemini-3-pro-preview",
    name="writer",
    description="The Writer Agent - Polishes blog sections iteratively.",
    instruction=read_instructions("writer.md"),
    tools=[
        read_section_tool,
        save_section_tool,
        finalize_post_tool,
        infer_blog_id_tool,
        get_workflow_status_tool
    ],
    sub_agents=[create_scribr()]  # Scribr as sub-agent for style review
)
