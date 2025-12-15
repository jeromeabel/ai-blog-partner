from google.adk.agents import Agent, LoopAgent

from blogger.agents import scribr
from blogger.utils import read_instructions
from blogger.validation_checkers import ReorganizationValidationChecker

organizer = Agent(
    name="organizer",
    model="gemini-3-pro-preview",
    instruction=read_instructions("organizer.md"),
    description="Reorganizes draft content to match outline structure",
    output_key="draft_organized",
    sub_agents=[scribr],
)

robust_organizer_step = LoopAgent(
    name="robust_organizer_step",
    description="Reorganizes draft with automatic quality validation",
    sub_agents=[
        organizer,
        ReorganizationValidationChecker(name="reorganization_validator"),
    ],
    max_iterations=3,
)
