from typing import TypedDict,Annotated
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode
# from langchain.agents import create_tool_calling_agent
# from langchain_core.messages import ToolMessage
import operator

from tools import codebase_retriever,code_writer
from langchain_google_genai import ChatGoogleGenerativeAI

# Agent State
class AgentState(TypedDict):
    messages : Annotated[list,operator.add]


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.1)
tools = [codebase_retriever,code_writer]
tool_exe = ToolNode(tools)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a powerful Qiskit assistant that can both answer questions and write code.
    You will be given a conversation history and a new user question.
    Based on this, you must decide whether to call a tool or respond to the user.
    If you need more information to answer, use a tool.
    If you have enough information, provide a final, comprehensive answer."""),
    MessagesPlaceholder(variable_name="messages"),
])

llm_with_tools = llm.bind_tools(tools)

agent = prompt| llm_with_tools

# Nodes
def should_continue(state: AgentState):
    print("---AGENT: Thinking---")
    response = agent.invoke({"messages": state['messages']})
    return {"messages": [response]}

# Define the Graph 
def create_graph():
    workflow = StateGraph(AgentState)

    tool_node = ToolNode(tools)

    workflow.add_node("agent", should_continue)
    workflow.add_node("action", tool_node)

    workflow.set_entry_point("agent")

    def where_to_go(state: AgentState):
        last_message = state['messages'][-1]
        if last_message.tool_calls:
            return "action"
        return END

    workflow.add_conditional_edges("agent", where_to_go, {"action": "action", END: END})
    workflow.add_edge("action", "agent")

    return workflow.compile()