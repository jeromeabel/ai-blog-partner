from google.adk.agents import Agent, LoopAgent
from google.adk.tools.function_tool import FunctionTool

from blogger.agents import scribr
from blogger.tools import read_draft_tool
from blogger.validation_checkers import (
    ContentSplitValidationChecker,
    OutlineValidationChecker,
)

# Worker agents
outline_creator = Agent(
    model="gemini-3-pro-preview",
    name="outline_creator",
    description="Creates an outline for a blog post",
    instruction="""
    You are working with Scribr to create a blog post outline.

    Your task:
    1. Use the `read_draft_tool` to load the raw draft content
    2. Collaborate with Scribr to analyze the draft and create a structured outline
    3. The outline should have:
        - A clear title (# heading)
        - At least 3 main sections (## headings)
        - An Introduction section
        - A Conclusion section
        - Logical flow and structure

    Output the outline in Markdown format.
    """,
    sub_agents=[scribr],
    tools=[FunctionTool(read_draft_tool)],
    output_key="blog_outline",
)

content_splitter = Agent(
    model="gemini-3-pro-preview",
    name="content_splitter",
    description="Splits draft content into matching/unused chunks",
    instruction="""
    You are a content analyzer. Your task is to split the raw draft into two parts based on the outline structure.

    Steps:
    1. Use the `read_draft_tool` to load the raw draft content
    2. Read the `blog_outline` from session state
    3. Identify which content segments match the outline structure (draft_ok)
    4. Identify content that doesn't fit the outline (draft_not_ok)
    5. Ensure all original content is preserved (no content lost)

    Output a dictionary with two keys:
    - "draft_ok": String containing content that aligns with the outline
    - "draft_not_ok": String containing unused/unmatched content

    Example output format:
    {
        "draft_ok": "Content that matches the outline sections...",
        "draft_not_ok": "Remaining content that doesn't fit..."
    }
    """,
    tools=[FunctionTool(read_draft_tool)],
    output_key="content_split",
)

# LoopAgent wrappers
robust_outline_step = LoopAgent(
    name="robust_outline_step",
    description="Creates blog outline with automatic quality retries",
    sub_agents=[
        outline_creator,
        OutlineValidationChecker(name="outline_validator"),
    ],
    max_iterations=3,
)

robust_content_split_step = LoopAgent(
    name="robust_content_split_step",
    description="Split blog draft with automatic quality retries",
    sub_agents=[
        content_splitter,
        ContentSplitValidationChecker(name="content_split_validator"),
    ],
    max_iterations=2,
)
