from typing import TypedDict,Annotated
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode
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
    ("system", """You are an expert Qiskit software developer assistant. Your primary goal is to provide accurate, helpful answers with code examples.

BEHAVIOR RULES:
- **Use Conversation History:** You MUST use the entire conversation history available in the 'messages' to understand the user's full request and context. If a user asks for "it" or an "example," refer to the previous messages to understand the topic.
- **Proactive Tool Use:** If a question requires knowledge about the codebase (classes, functions, implementation details), your first step should always be to use the `codebase_retriever` tool.
- **Handle Tool Errors:** If a tool returns an error message, inform the user about the specific error. Then, if you can, try to answer the question using your general knowledge, but state clearly that you are doing so because the tool failed.
- **Be Direct:** Do not get stuck in clarification loops. If a request is slightly ambiguous, make a reasonable assumption and provide an answer. For example, if asked for a "QAOA example," assume the user wants a basic implementation and use your tools to provide one."""),
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