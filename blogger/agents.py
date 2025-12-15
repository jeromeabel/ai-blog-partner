from google.adk.agents.llm_agent import Agent

from blogger.utils import read_instructions

## Agents
scribr = Agent(
    model="gemini-3-pro-preview",
    name="scribr",
    description="A Senior Technical Writer Partner",
    instruction=read_instructions("scribr.md"),
)

linguist = Agent(
    model="gemini-3-pro-preview",
    name="linguist",
    description="The English Language Coach",
    instruction=read_instructions("linguist.md"),
)
