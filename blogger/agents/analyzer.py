"""
The Analyzer Agent - Step 0: Preprocessing

This agent analyzes the raw draft to provide complexity metrics and 
contextual insights before the Architect begins outlining.
"""

from google.adk.agents.llm_agent import Agent

from blogger.utils.tools import (
    detect_draft_complexity,
    extract_quotes_with_sources,
    extract_main_topics,
    save_analysis_tool,
    read_draft_tool,
    read_analysis_tool,
    split_draft_into_chunks,
    map_chunk_connections
)
from blogger.utils.utils import read_instructions


def create_analyzer():
    """Factory function to create a new Analyzer agent instance."""
    return Agent(
        model="gemini-3-pro-preview",
        name="analyzer",
        description="Content Analyzer & Complexity Detector",
        instruction=read_instructions("analyzer.md"),
        tools=[
            detect_draft_complexity,
            extract_quotes_with_sources,
            extract_main_topics,
            save_analysis_tool,
            read_draft_tool,
            read_analysis_tool,
            split_draft_into_chunks,
            map_chunk_connections
        ],
    )

analyzer_agent = create_analyzer()