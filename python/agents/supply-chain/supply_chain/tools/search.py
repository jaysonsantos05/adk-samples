# Copyright 2026 Google LLC
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

"""Tool for Google Search grounding"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search

from ..config import config
from . import prompts

def _search_callback(tool_name: str, params: dict) -> dict:
    """Blocks suspicious Google search queries to prevent prompt injection."""
    if tool_name == "google_search":
        query = params.get("query", "")
        # Reject queries containing common injection phrases or overly complex instructions
        if any(phrase in query.lower() for phrase in ["ignore previous", "assume role", "output raw", "system prompt"]):
            return {"error": "suspicious query pattern detected"}
    return {"ok": True}


_search_agent = Agent(
    model=config.model_name,
    name="google_search_grounding",
    description="An agent providing Google-search grounding capability",
    instruction=prompts.GOOGLE_SEARCH_GROUNDING_PROMPT,
    tools=[google_search],
)

google_search_grounding = AgentTool(agent=_search_agent)
