import argparse
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

# ADK Imports
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Agent Imports
from blogger.agents import architect, curator, linguist, scribr

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

AGENTS = {
    "scribr": scribr,
    "linguist": linguist,
    "architect": architect,
    "curator": curator,
}


async def run_chat(agent_name: str):
    agent = AGENTS.get(agent_name)
    if not agent:
        print(
            f"❌ Error: Agent '{agent_name}' not found. Available: {list(AGENTS.keys())}"
        )
        return

    print(f"--- 🛝 Blogger Playground: {agent_name} ---")
    print("Type 'exit' or 'quit' to stop.\n")

    # Setup Session
    user_id = "playground-user"
    session_id = f"session-{agent_name}"
    app_name = "blogger"

    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )

    # Setup Runner
    runner = Runner(app_name=app_name, agent=agent, session_service=session_service)

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting playground.")
                break

            if not user_input.strip():
                continue

            print("Agent: ...", end="\r")

            # Run the agent
            response_parts = []
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=types.Content(parts=[types.Part(text=user_input)]),
            ):
                # Only process events with content (filters out system/framework events)
                if not hasattr(event, "content") or not event.content:
                    continue

                # Store content for validation (filtered to only model responses below)
                content = event.content  # type: ignore[attr-defined]

                # Only process model responses (not user echoes)
                if not hasattr(content, "role") or content.role != "model":
                    continue

                # Process each part of the model's response
                if hasattr(content, "parts") and content.parts is not None:
                    for part in content.parts:
                        # Handle text responses
                        if hasattr(part, "text") and part.text:
                            response_parts.append(part.text)
                        # Handle function calls (tools)
                        elif hasattr(part, "function_call") and part.function_call:
                            func_name = part.function_call.name
                            print(f"\r🔧 Agent is using tool: {func_name}")

            # Print collected response
            if response_parts:
                full_response = "".join(response_parts)
                print(f"\rAgent: {full_response}")
                print("-" * 40)

        except KeyboardInterrupt:
            print("\nExiting playground.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Blogger Playground")
    parser.add_argument(
        "--agent", default="scribr", help="Agent to chat with (scribr, linguist, architect, curator)"
    )

    args = parser.parse_args()

    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY not found in environment. Check blogger/.env")

    try:
        asyncio.run(run_chat(args.agent))
    except KeyboardInterrupt:
        pass
