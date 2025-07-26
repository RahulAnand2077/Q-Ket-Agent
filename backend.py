# import os
# from dotenv import load_dotenv

# load_dotenv()
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agent import create_graph
from contextlib import asynccontextmanager

agent_graph = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup tasks: loads environment variables and initializes the agent graph.
    """
    global agent_graph
    print("Application startup: Loading .env and creating agent graph...")
    agent_graph = create_graph()
    print("Agent graph created successfully.")
    yield
    print("Application shutdown.")

app = FastAPI(
    title="Qiskit AI Agent API",
    description="API for interacting with the Qiskit agent.",
    lifespan=lifespan,
)

class AgentRequest(BaseModel):
    message : str

class AgentResponse(BaseModel):
    reply : str


@app.post("/invoke_agent",response_model=AgentResponse)
async def invoke_agent(request : AgentRequest):
    """
    Receives a user message, invokes the LangGraph agent, and returns the final response.
    """
    inputs = [HumanMessage(content=request.message)]
    full_response = ""
    for output in agent_graph.stream({"messages" : inputs}):
        if "agent" in output:
            final_answer = output["agent"]["messages"][-1]
            response_content = final_answer.content
            if isinstance(response_content, list):
                full_response = "".join(part for part in response_content)
            else:
                full_response = response_content
            
    return {"reply":full_response}

@app.get("/")
@app.head("/")
def read_root():
    return {"message" : "Qiskit AI Agent API is running."}