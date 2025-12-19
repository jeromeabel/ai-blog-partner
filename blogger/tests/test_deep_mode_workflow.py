
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# ADK Imports
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Agent Imports
from blogger.agents.analyzer import create_analyzer
from blogger.agents.architect import architect
from blogger.agents.curator import curator

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

async def run_agent(agent, message: str, verbose=True):
    print(f"\n--- Running {agent.name} with: '{message}' ---")
    
    session_service = InMemorySessionService()
    user_id = "test-user"
    session_id = f"test-session-{agent.name}"
    app_name = "blogger-test"
    
    await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
    
    runner = Runner(app_name=app_name, agent=agent, session_service=session_service)
    
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(parts=[types.Part(text=message)]),
    ):
        if not hasattr(event, "content") or not event.content:
            continue
        
        content = event.content
        if not hasattr(content, "role") or content.role != "model":
            continue
            
        if hasattr(content, "parts") and content.parts is not None:
            for part in content.parts:
                if hasattr(part, "text") and part.text:
                    response_text += part.text
                    print(part.text, end="", flush=True)
                elif hasattr(part, "function_call") and part.function_call:
                    if verbose:
                        print(f"\n[Tool Call: {part.function_call.name}]")

    print("\n--- Done ---")
    return response_text

async def test_deep_mode_workflow():
    # 1. Run Analyzer (Deep Mode)
    analyzer = create_analyzer()
    await run_agent(analyzer, "Run deep analysis on deep-mode-test")
    
    # Verify 0-analysis.md
    analysis_path = Path("posts/deep-mode-test/0-analysis.md")
    if analysis_path.exists():
        content = analysis_path.read_text()
        print("\n✅ Analysis file created.")
        if "mode: deep" in content:
            print("✅ Mode is 'deep'")
        else:
            print("❌ Mode is NOT 'deep'")
            
        if "Chunk #" in content:
            print("✅ Chunks found in markdown")
        else:
            print("❌ Chunks NOT found in markdown")
    else:
        print("❌ Analysis file NOT created.")
        return

    # 2. Run Architect
    # First, mock user approving outline v1 immediately for speed
    # Or just let Architect create v1, then we approve it.
    
    # Step 2a: Create outline
    await run_agent(architect, "Create an outline for deep-mode-test based on the analysis. Since this is a test, finalize it immediately as 1-outline.md without asking for confirmation.")
    
    # Check if 1-outline.md exists
    outline_final = Path("posts/deep-mode-test/1-outline.md")
    if not outline_final.exists():
        print("⚠️ Architect didn't save 1-outline.md. Creating dummy for Curator test.")
        outline_final.write_text("# Dummy Outline\n\n## Section 1\n\n## Section 2\n")

    # 3. Run Curator
    await run_agent(curator, "Organize content for deep-mode-test. Assume I approve the filtering plan (cut tangents). Proceed to organize and save the result immediately.")
    
    # Verify 2-draft_organized.md
    organized_path = Path("posts/deep-mode-test/2-draft_organized.md")
    if organized_path.exists():
        content = organized_path.read_text()
        print("\n✅ Organized draft created.")
        if "<!-- Chunk #" in content:
            print("✅ Chunk IDs found in organized draft")
        else:
            print("❌ Chunk IDs NOT found in organized draft")
    else:
        print("❌ Organized draft NOT created.")

if __name__ == "__main__":
    asyncio.run(test_deep_mode_workflow())
