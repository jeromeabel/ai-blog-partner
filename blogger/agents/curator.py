"""
The Curator Agent - Phase 2: Filter and Organize Content

This agent handles content filtering and organization using the ADK Agent pattern.
Unlike the old system, the agent does the LLM reasoning while tools handle I/O and validation.
"""

from google.adk.agents import Agent

from blogger.utils.tools import (
    read_draft_tool,
    read_file_tool,
    save_step_tool,
    validate_content_split_tool,
    validate_organization_tool,
)
from blogger.utils.utils import read_instructions


curator = Agent(
    model="gemini-2.0-flash-exp",  # Lighter model for organization tasks
    name="curator",
    description="Filter and organize draft content to match outline structure",
    instruction=read_instructions("curator.md"),
    tools=[
        read_draft_tool,
        read_file_tool,
        save_step_tool,
        validate_content_split_tool,
        validate_organization_tool,
    ],
)
