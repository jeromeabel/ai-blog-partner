import json
import re
from typing import AsyncGenerator

from google.adk.agents import Agent, BaseAgent, LoopAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.google_search_tool import google_search
from google.genai import Client, types

from blogger.agents import scribr
from blogger.tools import read_draft_tool, read_previous_content_tool, INPUTS_DIR
from blogger.utils import read_instructions
from blogger.validation_checkers import (
    ContentSplitValidationChecker,
    OutlineValidationChecker,
)

# Worker agents


class DraftLoaderAgent(BaseAgent):
    """
    Custom agent that loads draft and properly sets session state.

    This agent:
    1. Calls read_draft_tool to get the draft content
    2. Extracts the "content" field from the tool response
    3. Sets session.state["raw_draft"] with the content
    """

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # Get blog_id from session state (set by orchestrator)
        blog_id = ctx.session.state.get("blog_id")

        # Get list of valid blog_ids from inputs directory
        valid_blog_ids = []
        if INPUTS_DIR.exists():
            valid_blog_ids = [d.name for d in INPUTS_DIR.iterdir() if d.is_dir()]

        if not blog_id:
            # Fallback: try to extract from session events (conversation history)
            try:
                for event in reversed(ctx.session.events):
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, "text") and part.text:
                                text = part.text
                                
                                # Strategy 1: Check for exact matches of known valid IDs
                                for valid_id in valid_blog_ids:
                                    if valid_id in text:
                                        blog_id = valid_id
                                        ctx.session.state["blog_id"] = blog_id
                                        break
                                if blog_id:
                                    break

                                # Strategy 2: Regex extraction with validation
                                # Look for patterns like "blog_id: my-ai-journey-2" or "for blog_id: xyz"
                                match = re.search(
                                    r"(?:blog_id|blog)[:\s]+([a-zA-Z0-9_-]+)",
                                    text,
                                    re.IGNORECASE,
                                )
                                if match:
                                    candidate_id = match.group(1)
                                    # Only accept if it's a valid ID or looks very much like one (contains hyphens/underscores)
                                    # This prevents matching "Post" from "blog post" unless "Post" is a valid folder
                                    if candidate_id in valid_blog_ids:
                                        blog_id = candidate_id
                                        ctx.session.state["blog_id"] = blog_id
                                        break
                                    elif "-" in candidate_id or "_" in candidate_id:
                                        # If it has structure, it might be a new ID not yet created, or we accept it tentatively
                                        # But for reading drafts, it MUST exist.
                                        pass 
                    if blog_id:
                        break
            except AttributeError:
                # If events is not accessible, continue without fallback
                pass

        if not blog_id:
            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(
                            text=f"❌ Error: Could not find a valid blog_id in the conversation. Found inputs: {valid_blog_ids}. Please mention the blog ID (e.g., 'start my-ai-journey-2')."
                        )
                    ]
                ),
            )
            return

        # Call read_draft_tool
        result = read_draft_tool(blog_id)

        if result.get("status") == "error":
            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(
                            text=f"❌ Error loading draft: {result.get('message')}"
                        )
                    ]
                ),
            )
            return

        # Extract content and set session state
        content = result.get("content", "")
        ctx.session.state["raw_draft"] = content

        # Report success
        draft_path = result.get("path", "unknown")
        yield Event(
            author=self.name,
            content=types.Content(
                parts=[
                    types.Part(
                        text=f"✅ Draft loaded from {draft_path} ({len(content)} characters)\n\n<draft_content>\n{content}\n</draft_content>"
                    )
                ]
            ),
        )


# Instantiate the custom agent
draft_loader = DraftLoaderAgent(
    name="draft_loader",
    description="Loads raw draft into session state",
)

outline_creator = Agent(
    model="gemini-2.0-flash",
    name="outline_creator",
    description="Creates an outline for a blog post",
    instruction=read_instructions("outline_creator.md"),
    sub_agents=[scribr],
    tools=[FunctionTool(read_previous_content_tool)],
    output_key="blog_outline",
)


class ContentSplitterAgent(BaseAgent):
    """
    Custom agent that splits draft content and properly sets session state as a dict.

    This agent:
    1. Reads raw_draft and blog_outline from session state
    2. Uses LLM to analyze and split content
    3. Parses JSON response and sets session.state["content_split"] as a dict
    """

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # Get inputs from session state
        raw_draft = ctx.session.state.get("raw_draft", "")
        blog_outline = ctx.session.state.get("blog_outline", "")

        if not raw_draft:
            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(text="❌ Error: No raw_draft found in session state")
                    ]
                ),
            )
            return

        if not blog_outline:
            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(
                            text="❌ Error: No blog_outline found in session state"
                        )
                    ]
                ),
            )
            return

        # Create prompt for LLM
        prompt = f"""You are a content analyzer. Your task is to split the raw draft into two parts based on the outline structure.

**CRITICAL CONSTRAINTS:**
1. Do ONLY this task - split the content
2. Do NOT jump to other steps (writing, organizing, etc.)
3. Do NOT call any agents or transfer control
4. Output ONLY valid JSON - no markdown code blocks, no explanations

**Steps:**
1. Identify which content segments from raw_draft match the outline structure (draft_ok)
2. Identify content that doesn't fit the outline (draft_not_ok)
3. Ensure ALL original content is preserved (no content lost)
4. Do NOT add new content - only copy/paste from raw_draft

**Output Format (MUST be valid JSON):**
{{
    "draft_ok": "Content that matches the outline sections...",
    "draft_not_ok": "Remaining content that doesn't fit..."
}}

**Raw Draft:**
{raw_draft}

**Outline:**
{blog_outline}

        Output the JSON now:"""

        # Call LLM to analyze and split content
        client = Client()
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=types.Content(parts=[types.Part(text=prompt)]),
        )

        if not response.text:
            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(
                            text="❌ Error: LLM returned empty response"
                        )
                    ]
                ),
            )
            return

        llm_output = response.text.strip()
        # Try to parse JSON response
        try:
            # Remove markdown code blocks if present
            if llm_output.startswith("```"):
                lines = llm_output.split("\n")
                llm_output = "\n".join(lines[1:-1])

            result = json.loads(llm_output)

            # Validate structure
            if "draft_ok" not in result or "draft_not_ok" not in result:
                yield Event(
                    author=self.name,
                    content=types.Content(
                        parts=[
                            types.Part(
                                text=f"❌ Error: LLM output missing required keys. Got: {list(result.keys())}"
                            )
                        ]
                    ),
                )
                return

            # Set session state as a proper dict
            ctx.session.state["content_split"] = {
                "draft_ok": str(result["draft_ok"]),
                "draft_not_ok": str(result["draft_not_ok"]),
            }

            # Report success
            draft_ok_len = len(result["draft_ok"])
            draft_not_ok_len = len(result["draft_not_ok"])

            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(
                            text=f"Content split complete: draft_ok ({draft_ok_len} chars), draft_not_ok ({draft_not_ok_len} chars)\n\n<content_split>\n{json.dumps(result, indent=2)}\n</content_split>"
                        )
                    ]
                ),
            )

        except json.JSONDecodeError as e:
            yield Event(
                author=self.name,
                content=types.Content(
                    parts=[
                        types.Part(
                            text=f"❌ Error: Failed to parse JSON response: {e}\n\nLLM output: {llm_output[:500]}..."
                        )
                    ]
                ),
            )


# Instantiate the custom agent
content_splitter = ContentSplitterAgent(
    name="content_splitter",
    description="Splits draft content into matching/unused chunks",
)

# LoopAgent wrappers
robust_outline_step = LoopAgent(
    name="robust_outline_step",
    description="Creates blog outline with automatic quality retries",
    sub_agents=[
        draft_loader,  # Ensure draft is loaded/reloaded in the context
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
