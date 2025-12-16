"""
AI Blog Partner - Interactive Coordinator

A conversational guide that helps users through the 3-step blog creation process.
This is NOT an automated orchestrator - it's a collaborative partner.
"""

import datetime
from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool

from blogger.utils import read_instructions
from blogger.tools import read_draft_tool, read_file_tool, save_step_tool
from blogger.step_agents.architect import architect


# === COORDINATOR AGENT ===

coordinator = Agent(
    name="coordinator",
    model="gemini-2.5-flash",
    description="AI Blog Partner - Interactive guide for the 3-step blog creation process",
    instruction=f"""{read_instructions('coordinator.md')}

Current date: {datetime.datetime.now().strftime('%Y-%m-%d')}
""",
    sub_agents=[
        architect,  # Step 1: Draft → Outline (brainstorming)
        # Step 2: Butcher (coming soon)
        # Step 3: Writer (coming soon)
    ],
    tools=[
        FunctionTool(read_draft_tool),
        FunctionTool(read_file_tool),
        FunctionTool(save_step_tool),
    ],
)

# Alias for ADK auto-discovery
root_agent = coordinator
