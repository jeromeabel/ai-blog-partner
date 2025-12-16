"""
Test script for AI Blog Partner workflow.

Tests Steps 1 and 2 with a real blog draft.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from blogger.workflow import orchestrator

# Load environment variables from blogger/.env
env_path = Path(__file__).parent.parent / "blogger" / ".env"
load_dotenv(env_path)


async def test_workflow():
    """Run Steps 1 and 2 of the workflow."""

    blog_id = "my-ai-journey-2"

    print("=" * 80)
    print("AI BLOG PARTNER - WORKFLOW TEST")
    print("=" * 80)
    print(f"\nBlog ID: {blog_id}")
    print(f"Testing: Step 1 (Draft to Outlines) + Step 2 (Organization)\n")

    # Session identifiers
    user_id = "test-user"
    session_id = "test-session-1"
    app_name = "ai-blog-partner-test"

    # Create session service and session
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )

    # Create runner
    runner = Runner(
        app_name=app_name,
        agent=orchestrator,
        session_service=session_service
    )

    # Test Step 1 and Step 2
    prompt = f"""
    Execute Steps 1 and 2 of the blog writing pipeline for blog_id: {blog_id}

    Step 1: Draft to Outlines
    - Load the draft
    - Create outline
    - Split content into draft_ok and draft_not_ok
    - Save outputs

    Step 2: Organization
    - Reorganize draft_ok to match outline structure
    - Save draft_organized.md

    Please execute these steps and report the results.
    """

    print("Starting workflow...\n")
    print("-" * 80)

    # Run the orchestrator
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(parts=[types.Part(text=prompt)])
    ):
        # Print agent outputs
        if hasattr(event, 'content') and event.content:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    print(f"\n[{event.author}]")
                    print(part.text)
                    print("-" * 80)

    print("\n" + "=" * 80)
    print("WORKFLOW COMPLETED")
    print("=" * 80)

    # Get session to show state
    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )

    # Show session state
    print("\n📊 Session State Keys:")
    for key in session.state.keys():
        value = session.state[key]
        if isinstance(value, str):
            preview = value[:100] + "..." if len(value) > 100 else value
            print(f"  - {key}: {len(value)} chars")
            print(f"    Preview: {preview}")
        elif isinstance(value, dict):
            print(f"  - {key}: dict with keys: {list(value.keys())}")
        else:
            print(f"  - {key}: {type(value)}")

    # Check output files
    from pathlib import Path
    outputs_dir = Path("outputs") / blog_id

    print(f"\n📁 Output Files in {outputs_dir}:")
    if outputs_dir.exists():
        for file in sorted(outputs_dir.glob("*.md")):
            size = file.stat().st_size
            print(f"  - {file.name} ({size} bytes)")
    else:
        print(f"  Directory not found: {outputs_dir}")


if __name__ == "__main__":
    asyncio.run(test_workflow())
