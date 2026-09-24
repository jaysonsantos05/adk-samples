# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Academic_websearch_agent for finding research papers using search tools."""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro"


def _validate_websearch_tool_call(tool_name: str, tool_input: dict) -> dict | None:
    """Validate web search queries before execution to prevent prompt injection."""
    if tool_name == "google_search":
        query = tool_input.get("query", "")
        # Block queries with suspicious patterns that might indicate injection
        suspicious_patterns = ["ignore", "disregard", "new instruction", "system:", "<script"]
        if any(pattern in query.lower() for pattern in suspicious_patterns):
            return {"error": "Query blocked due to suspicious content"}
    return None

academic_websearch_agent = Agent(
    model=MODEL,
    name="academic_websearch_agent",
    instruction=prompt.ACADEMIC_WEBSEARCH_PROMPT,
    output_key="recent_citing_papers",
    tools=[google_search],
    before_tool_callback=_validate_websearch_tool_call,
    safety_settings=[
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ],
)
