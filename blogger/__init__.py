"""
AI Blog Partner - Interactive blog writing assistant.

Official ADK App export for CLI and Web UI.

Two modes of interaction:
1. `adk run blogger` or `adk web` - Guided conversational workflow
2. `python -m blogger.playground --agent <name>` - Direct agent testing
"""

from google.adk.apps import App
from blogger.coordinator import coordinator, root_agent

# Official ADK App - required for `adk run` and `adk web`
app = App(
    name="blogger",  # Must be valid Python identifier (no dashes)
    root_agent=root_agent,
)

__all__ = ["app", "coordinator", "root_agent"]
