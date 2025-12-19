"""
AI Blog Partner - Interactive Coordinator

A conversational guide that helps users through the 3-step blog creation process.
This is NOT an automated orchestrator - it's a collaborative partner.
"""

import datetime

from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool

from blogger.agents.architect import architect
from blogger.agents.curator import curator
from blogger.agents.writer import writer
from blogger.utils.tools import (
    get_workflow_status_tool,
    infer_blog_id_tool,
    read_draft_tool,
    read_file_tool,
    save_step_tool,
)
from blogger.utils.utils import read_instructions

# === COORDINATOR AGENT ===

coordinator = Agent(
    name="coordinator",
    model="gemini-2.5-flash",
    description="AI Blog Partner - Interactive guide for the 3-step blog creation process",
    instruction=f"""{read_instructions("coordinator.md")}

Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
""",
    sub_agents=[architect, curator, writer],
    tools=[
        FunctionTool(get_workflow_status_tool),
        FunctionTool(infer_blog_id_tool),
        FunctionTool(read_draft_tool),
        FunctionTool(read_file_tool),
        FunctionTool(save_step_tool),
    ],
)

# Alias for ADK auto-discovery
root_agent = coordinator
