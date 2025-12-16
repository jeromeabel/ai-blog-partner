"""
AI Blog Partner - Multi-agent blog writing assistant.

Official ADK App export for CLI and Web UI.
"""

from google.adk.apps import App
from blogger.workflow import orchestrator

# Alias for ADK auto-discovery
root_agent = orchestrator

# Official ADK App - required for `adk run` and `adk web`
app = App(
    name="blogger",  # Must be valid Python identifier (no dashes)
    root_agent=orchestrator,
)

__all__ = ["app", "orchestrator", "root_agent"]
