from typing import TypedDict,Annotated,List
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage,AIMessage
import operator

from tools import codebase_retriever,code_writer,qiskit_docs_search,web_page_reader
from langchain_google_genai import ChatGoogleGenerativeAI

# Agent State
class AgentState(TypedDict):
    messages : Annotated[List[BaseMessage],operator.add]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.1)
tools = [codebase_retriever,code_writer,qiskit_docs_search,web_page_reader]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert Qiskit software developer assistant. Your primary goal is to provide accurate, helpful answers and code examples.

    BEHAVIOR RULES:
    - **Use Conversation History:** Always use the full conversation history to understand the user's context.
    - **Prioritize Tools:** When a user asks a question, first consider if a tool can help.

    HOW TO ANSWER QUESTIONS:
    - For general questions or implementation details, use `codebase_retriever` or the `qiskit_docs_search` and `web_page_reader` tool chain.

    HOW TO WRITE CODE:
    When the user asks you to write code (e.g., "give me code for X", "write an example of Y"), you MUST follow this three-step process:
    1.  **Search:** Use the `qiskit_docs_search` tool to find the most relevant documentation URL for the user's request.
    2.  **Read:** Use the `web_page_reader` tool with the URL you just found to get the latest context.
    3.  **Write:** Use the `code_writer` tool. Pass the user's original request as the `task_description` and the context you got from the `web_page_reader` as the `code_context`.
    """),
    MessagesPlaceholder(variable_name="messages"),
])

llm_with_tools = llm.bind_tools(tools)
agent = prompt| llm_with_tools

# Nodes
def agent_node(state: AgentState):
    print("---AGENT: Thinking---")
    response = agent.invoke({"messages": state['messages'][-10:]})
    return {"messages": [response]}

# Define the Graph 
def create_graph():
    workflow = StateGraph(AgentState)
    tool_node = ToolNode(tools)

    workflow.add_node("agent", agent_node)
    workflow.add_node("action", tool_node)

    workflow.set_entry_point("agent")

    def where_to_go(state: AgentState):
        last_message = state['messages'][-1]
        if last_message.tool_calls:
            return "action"
        return END

    workflow.add_conditional_edges("agent", where_to_go, {"action": "action", END:END})
    workflow.add_edge("action", "agent")

    return workflow.compile()