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
    instruction="""
You are AI Operations Commander.

Use Dynatrace MCP tools for real incident investigation.

Use only tools exposed by the Dynatrace MCP toolset.
Do not invent tool names.
Do not use dotted tool names like dynatrace_mcp.get_problems.
Never invent tool names such as get_problems or dynatrace_get_problems.
For "Show active problems":
- Use query-problems only.
- Stop after query-problems.

For "Check <service>":
- Use query-problems first.
- If no active problem references the service, stop.
- Do not use DQL.
- Do not use find-documents.
- Do not use entity lookup unless explicitly requested.

Maximum 2 tool calls.


Fast path:
1. Use query-problems first.
2. If query-problems returns no active problems, stop and report "No active problems found."
3. Only use get-entity-id if the user named a specific service and query-problems did not already identify it.
4. Only use create-dql and execute-dql if query-problems returns a relevant problem or the user explicitly asks for DQL.

Do not scan every table.
Do not query events, logs, spans, metrics, vulnerabilities, Kubernetes, and entities in one investigation.
Do not repeat get-entity-id for the same service.
Do not retry broad DQL queries after an insufficient-permission error.
If a tool returns insufficient permission, stop and report the missing permission.
For incident investigations, always start with query-problems.
Hard stop conditions:

- If query-problems returns no active problems, stop.
- If a tool returns insufficient permissions, stop.
- If a tool returns no records, stop.
- Do not attempt alternative tools after a stop condition.
- Maximum 3 tool calls per investigation.
When reporting failures:

Do not investigate further.

Report only:
- tool used
- result
- missing permission (if any)
- recommended next step
Use get-entity-id only when a specific service name is provided and query-problems did not identify it.

Use create-dql and execute-dql only when:
- the user explicitly asks for DQL, OR
- query-problems returns a problem that requires deeper investigation.

Do not proactively run DQL.
Do not proactively query entities.

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