import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from agent import root_agent

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

adk_agent = ADKAgent(
    adk_agent=root_agent,
    app_name="default",
    user_id="user",
)
add_adk_fastapi_endpoint(
    app=app,
    agent=adk_agent,
    path="/copilotkit",

)