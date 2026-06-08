# AI Operations Commander

AI Operations Commander is a Google ADK incident-response agent that uses Dynatrace MCP tools to investigate production incidents.

A companion React/CopilotKit console is included for demonstration and operator interaction.

## Architecture

Google ADK Agent

↓

Dynatrace MCP Toolset

↓

Dynatrace Environment

### Optional Demo Console

React/Vite

↓

CopilotKit Runtime

↓

FastAPI Backend

↓

ADK Agent

---

## Features

* Google ADK agent
* Dynatrace MCP integration
* Incident investigation workflow
* Root cause analysis
* Evidence collection
* Recommended remediation actions
* AG-UI workflow streaming
* CopilotKit operator console
* React/Vite dashboard
* ngrok support for external access

---

## Local Run Commands

Open 5 Git Bash terminals.

### Terminal 1 — FastAPI Backend

```bash
cd ~/Downloads/ops

uvicorn backend.api:app --host 0.0.0.0 --port 8000
```

### Terminal 2 — ngrok Tunnel

```bash
cd ~/Downloads/ngrok

./ngrok.exe http 8000
```

### Terminal 3 — AG-UI / ADK Bridge

```bash
cd ~/Downloads/agent_operations_commander

python -m uvicorn agui_server:app --port 8010
```

### Terminal 4 — CopilotKit Runtime

```bash
cd ~/Downloads/ops/frontend

"/c/Program Files/nodejs/node.exe" copilot-runtime.js
```

Expected:

```text
CopilotKit Runtime running at http://127.0.0.1:8020/copilotkit
```

### Terminal 5 — React Frontend

```bash
cd ~/Downloads/ops/frontend

"/c/Program Files/nodejs/node.exe" node_modules/vite/bin/vite.js
```

Expected:

```text
VITE v5.4.21 ready

http://localhost:5173/
```

---

## URLs

Frontend

```text
http://localhost:5173
```

Backend

```text
http://localhost:8000
```

AG-UI

```text
http://localhost:8010
```

CopilotKit Runtime

```text
http://127.0.0.1:8020/copilotkit
```

---

## Dynatrace MCP Tools

* query-problems
* get-problems
* get-logs
* get-service-health
* get-metric-data
* execute-dql
* Smartscape discovery

---

## Disclaimer

The Previous Queries panel stores only investigations executed through the Real Dynatrace MCP workflow.

Demo incidents are synthetic examples used to demonstrate the operator experience and are not persisted.
