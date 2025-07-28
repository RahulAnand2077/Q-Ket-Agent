# 🤖 Qiskit AI Agent
An intelligent assistant for the Qiskit codebase, powered by LangGraph and Google's Gemini. This agent can answer questions about the codebase, explain concepts, and generate runnable code examples on demand.

## Overview
Navigating a large and complex codebase like Qiskit can be challenging. This project introduces an AI-powered agent designed to act as an intelligent pair programmer. It accelerates code discovery and understanding by providing natural language answers to complex questions and generating code snippets, significantly reducing the time required to learn the library.

The agent leverages a sophisticated multi-tool workflow and a stateful graph architecture built with LangGraph to hold coherent, multi-turn conversations.

## ✨ Key Features
- *Conversational Q&A:* 
    Ask complex questions about Qiskit classes, functions, and implementation details.

- *Multi-Step Tool Use:*
    The agent can intelligently chain tools together, such as searching for documentation online, reading the content, and then writing code based on what it found.

- *On-Demand Code Generation:* 
    Ask the agent to write specific Qiskit code examples, such as implementing a quantum circuit or algorithm, with context from the latest documentation.

- *Conversational Memory:* 
    The conversation state is managed by the Streamlit frontend. On each turn, the entire chat history is sent to the stateless LangGraph backend, ensuring the agent has full context for coherent follow-up questions.

- *Robust Error Handling:* 
    Gracefully manages tool failures and informs the user, attempting to answer from its own knowledge base if a tool fails.

## 🏗️ Architecture
This project uses a decoupled frontend/backend architecture, which is robust and scalable.

- Stateful Frontend (Streamlit): 
    The user interface is built with Streamlit. It is responsible for managing the entire conversation state. It stores the full message history and sends it to the backend with every new request.

- Stateless Backend (FastAPI & LangGraph): 
    The backend is a stateless API built with FastAPI. It receives the full conversation history, processes it using a LangGraph-defined agent, and returns a single response. It holds no memory of the conversation between requests.

This design keeps the complex agent logic on the backend while allowing the frontend to be simple and focused on the user experience.

```Bash
    subgraph Frontend (Streamlit)
        A[User Enters Prompt] --> B{Update Session State};
        B --> C[Send Full History via API Request];
    end
    subgraph Backend (FastAPI)
        D[Receive History] --> E(Invoke LangGraph Agent);
        E --> F[Return Final Response];
    end
    C --> D;
    F --> G[Display Response in UI];
    B --> G;
```

## 🛠️ Tech Stack
- 🧠 *LangChain & LangGraph*

- 👾 *Google Gemini*

- 📚 *ChromaDB : Vector Database*

- 🔢 *Google embedding-001*

- 📄 *Tree-sitter : Code & Document Handling*

- 🐍 *Python*

- 🔥 *Streamlit*

- 🍃 *FastAPI* 

- 🦉 *Tavily Search API*

## ⚙️ Setup and Installation
Follow these steps to set up and run the project locally.

### 1. Clone this Repository

```Bash
git clone https://github.com/RahulAnand2077/Q-Ket-Agent
cd Q-Ket-Agent
```

### 2. Create and Activate Virtual Environment

```Bash
# Windows
python -m venv venv
.\venv\Scripts\Activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```Bash
pip install -r requirements.txt
```

### 4. Configure API Keys & Credentials
- Set Up Google Cloud Authentication

    This project requires a Google Cloud Service Account to use the Gemini API.

    - Follow the official guide to [create a service account and download the JSON key](https://cloud.google.com/docs/authentication/client-libraries).

    - Grant the "Vertex AI User" role to the service account.

    - Place the downloaded service-account-key.json file in the root of the project directory.

- Tavily Search:

    Get a free API key from [tavily.com](https://www.tavily.com/).

### 5. Create .env File
Create a file named .env in the project root and add the following line:

    GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json
    TAVILY_API_KEY="tvly-..."

### 6. Prepare the Codebase for Indexing
Download or clone the Qiskit source code into the project directory.

```Bash
git clone https://github.com/Qiskit/qiskit.git
```

### 7. Create the Vector Database
Change the REPO_PATH to the path of cloned Qiskit repo. 

Run the ingestion script to embed the Qiskit codebase and create the local ChromaDB database.

``` Bash
python ingest.py
```

### 8. Run FastAPI server
To start the server:

``` Bash
uvicorn backend:app --reload 
```

### 9. Run Streamlit frontend
To start the frontend:

``` Bash
streamlit run app.py
```

## 📜 Project Structure

├── app.py              # The Streamlit frontend application

├── backend.py          # The FastAPI backend server

├── agent.py            # LangGraph agent and graph definition

├── tools.py            # Custom tools for the agent (RAG, web search, etc.)

├── ingest.py           # Script to process and embed the Qiskit codebase

├── requirements.txt    # Project dependencies

├── .env                # File for API keys (not committed to git)

└── qiskit_code/        # Local clone of the Qiskit repository (ignored by git)
