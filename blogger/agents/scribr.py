"""
Scribr Agent - Senior Technical Writer Partner

General-purpose writing assistant for polishing titles, snippets, and text.
"""

from google.adk.agents.llm_agent import Agent

from blogger.utils.utils import read_instructions


scribr = Agent(
    model="gemini-3-pro-preview",
    name="scribr",
    description="A Senior Technical Writer Partner",
    instruction=read_instructions("scribr.md"),
)
