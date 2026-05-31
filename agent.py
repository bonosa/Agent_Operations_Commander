import os
import requests
from dotenv import load_dotenv

load_dotenv()
print("DT_API_TOKEN loaded:", bool(os.getenv("DT_API_TOKEN")))
print("DT_ENVIRONMENT loaded:", bool(os.getenv("DT_ENVIRONMENT")))
from google.adk.tools.mcp_tool.mcp_toolset import (
    McpToolset,
    StreamableHTTPConnectionParams,
)

from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context


FASTAPI_BASE_URL = "https://plod-nerd-crier.ngrok-free.dev"


def analyze_incident_tool(
    question: str,
    service: str = "checkout-api",
) -> dict:
    """
    Call the AI Operations Commander backend.
    """

    response = requests.post(
        f"{FASTAPI_BASE_URL}/api/analyze",
        json={
            "question": question,
            "service": service,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


ai_operations_commander_google_search_agent = LlmAgent(
    name="AI_Operations_Commander_google_search_agent",
    model="gemini-3.5-flash",
    description="Agent specialized in performing Google searches.",
    sub_agents=[],
    instruction="Use the GoogleSearchTool to find information on the web.",
    tools=[
        GoogleSearchTool()
    ],
)

ai_operations_commander_url_context_agent = LlmAgent(
    name="AI_Operations_Commander_url_context_agent",
    model="gemini-3.5-flash",
    description="Agent specialized in fetching content from URLs.",
    sub_agents=[],
    instruction="Use the UrlContextTool to retrieve content from provided URLs.",
    tools=[
        url_context
    ],
)
DYNATRACE_MCP_URL = (
    "https://voy88054.apps.dynatrace.com/"
    "platform-reserved/mcp-gateway/v0.1/servers/dynatrace-mcp/mcp"
)

dynatrace_mcp_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=DYNATRACE_MCP_URL,
        headers={
            "Authorization": f"Bearer {os.environ['DT_API_TOKEN']}"
        },
        timeout=30.0,
    )
)
 
root_agent = LlmAgent(
    name="AI_Operations_Commander",
    model="gemini-3.5-flash",
    description=(
        "Gemini-powered AI incident response commander using Dynatrace MCP."
    ),
    sub_agents=[],
    instruction="""
You are AI Operations Commander.

Use the Dynatrace MCP tools first for incident, outage, service health, logs, problems, root cause, Smartscape, DQL, or troubleshooting questions.

Do not call analyze_incident_tool.

Format responses as a compact incident dashboard.

Do not write long paragraphs.

Use this format:

🚨 INCIDENT DASHBOARD

| Severity | Service | Signal | Status |
|---|---|---|---|
| <severity> | <service> | <main metric/problem> | <status> |

🎯 Root Cause
- <one sentence>

📊 Evidence
- <fact>
- <fact>
- <fact>

⚡ Actions
- <action>
- <action>
- <action>

🕒 Timeline
- <event>
- <event>
- <event>
""",
    tools=[
        dynatrace_mcp_toolset,
    ],
 )