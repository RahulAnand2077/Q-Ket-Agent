import asyncio
from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_tavily import TavilySearch

DB_PATH = "chroma_db"
EMBEDDING_MODEL = "models/embedding-001"

@tool
def codebase_retriever(query : str) -> str:
    """
    Searches and retrieves relevant context from the Qiskit codebase vector store.
    Use this tool to answer any questions about Qiskit's implementation,
    code structure, or functionality.
    """
    print(f"-- Using codebase_retriever with query: {query} --")

    async def _retriever():    
        embedding_model = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
        vector_store = Chroma(
            persist_directory=DB_PATH,
            embedding_function=embedding_model
        )

        retriever = vector_store.as_retriever(search_kwargs={"k":5})
        retrieved_docs = await retriever.ainvoke(query)

        if not retrieved_docs:
            return "No relevant documents found in the codebase for this query."

        context_parts = []
        for i,doc in enumerate(retrieved_docs):
            source = doc.metadata.get("source","Unknown")
            content = doc.page_content
            context_parts.append(f"-- Context Snippet {i+1} from {source} --\n{content}")

        context = "\n\n".join(context_parts)
        return f"Retrieved context:\n{context}"
    
    try:
        return asyncio.run(_retriever())
    
    except Exception as e:
        print(f"ERROR in codebasee_retriever: {e}")
        return f"An error occurred while trying to retrieve from the codebase: {e}"

@tool
def code_writer(task_description : str, code_context : str)-> str:
    """
    Generates new, runnable Qiskit code based on a task description and relevant code context.
    Use this tool ONLY after you have already retrieved context with the codebase_retriever.
    Do not use this tool for asking questions, only for writing new code.
    """
    print(f"Using code_writer for task: {task_description}")

    writer_llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro",temperature=0.1)

    template="""
    You are an expert Qiskit programmer. Your task is to write a single, complete, and runnable
    Python code snippet to accomplish the user's goal.
    You will be given a task description and some relevant code context from the existing library.
    Base your code on the patterns and functions seen in the context.
    The code should be complete with all necessary imports from qiskit.

    CONTEXT:
    {context}

    TASK:
    {task}

    Complete, runnable Python code:
    """

    prompt = PromptTemplate.from_template(template)

    chain = prompt | writer_llm

    generated_code = chain.invoke({
        "task":task_description,
        "context":code_context
    })

    return generated_code.content

@tool
def web_page_reader(url: str) -> str:
    """
    Reads the full text content of a given web page URL.
    Use this tool ONLY after you have a specific URL from a search tool.
    """
    print(f"-- Using web_page_reader for URL: {url} --")
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        # Join the document contents into a single string
        content = "\n\n".join([doc.page_content for doc in docs])
        return content
    except Exception as e:
        print(f"ERROR in web_page_reader: {e}")
        return f"An error occurred while trying to read the page: {e}"

@tool
def qiskit_docs_search(query: str) -> str:
    """
    Searches for the official Qiskit documentation page for a specific topic, class, or function.
    Use this tool first to find the correct URL before you can read its content.
    Returns a list of search results with URLs.
    """
    print(f"-- Using qiskit_docs_search with query: {query} --")
    # We use the Tavily search tool, which you've set up before.
    # We add "site:quantum.cloud.ibm.com/docs" to restrict the search to the docs.
    search = TavilySearch(max_results=3)
    results = search.invoke(f"site:quantum.cloud.ibm.com/docs {query}")
    return results