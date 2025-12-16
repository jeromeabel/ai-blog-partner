"""
The Architect Agent - Step 1: Draft → Outline

This agent helps users transform raw drafts into structured outlines
through interactive conversation.
"""

from google.adk.agents.llm_agent import Agent

from blogger.utils import read_instructions
from blogger.tools import read_draft_tool, read_file_tool, save_step_tool
from blogger.agents import scribr

architect = Agent(
    model="gemini-3-pro-preview",
    name="architect",
    description="The Architect - Expert Editor & Structural Thinker",
    instruction=read_instructions("architect.md"),
    tools=[read_draft_tool, read_file_tool, save_step_tool],
    agents=[scribr],  # Scribr helps polish titles and check for LLM-isms
)
