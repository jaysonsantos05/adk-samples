"""Google Search Agent definition for ADK Gemini Live API Toolkit demo."""

import os

from google.adk.agents import Agent
def validate_search_tool(tool_name, tool_input):
    if tool_name == "google_search":
        query = tool_input.get("query", "")
        if not isinstance(query, str) or len(query) > 500:
            return {"error": "Invalid or oversized search query"}
    return {}

agent = Agent(
        name="google_search_agent",
        model=os.getenv(
            "DEMO_AGENT_MODEL", "gemini-2.5-flash-native-audio-preview-12-2025"
        ),
        tools=[google_search],
        before_tool_callback=validate_search_tool,
    instruction="You are a helpful assistant that can search the web.",
)
