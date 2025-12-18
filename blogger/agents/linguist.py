"""
Linguist Agent - English Language Coach

General-purpose language assistant for grammar, style, and clarity.
"""

from google.adk.agents.llm_agent import Agent

from blogger.utils.utils import read_instructions


linguist = Agent(
    model="gemini-3-pro-preview",
    name="linguist",
    description="The English Language Coach",
    instruction=read_instructions("linguist.md"),
)
