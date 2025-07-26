# 🤖 Qiskit AI Agent
An intelligent assistant for the Qiskit codebase, powered by LangGraph and Google's Gemini. This agent can answer questions about the codebase, explain concepts, and generate runnable code examples on demand.

## Overview
Navigating a large and complex codebase like Qiskit can be challenging for both new and experienced developers. This project introduces an AI-powered agent designed to act as an intelligent pair programmer. It accelerates code discovery and understanding by providing natural language answers to complex questions and generating code snippets, significantly reducing the time required to find information and learn the library.

The agent leverages a sophisticated Retrieval-Augmented Generation (RAG) pipeline and a stateful graph architecture built with LangGraph to hold coherent, multi-turn conversations.

## ✨ Key Features
- *Conversational Q&A:* 
    Ask complex questions about Qiskit classes, functions, and implementation details.

- *Intelligent Tool Use:*
    The agent dynamically decides whether to retrieve information from the codebase or generate new code using a separate code_writer tool.

- *On-Demand Code Generation:* 
    Ask the agent to write specific Qiskit code examples, such as implementing a quantum circuit or algorithm.

- *Stateful Memory:* 
    Built with LangGraph, the agent remembers the context of the conversation for follow-up questions.

- *Robust Error Handling:* 
    Gracefully manages tool failures and informs the user, attempting to answer from its own knowledge base if a tool fails.

## 🏗️ Architecture
The agent is built using LangGraph, which implements the logic as a stateful graph. This allows for more complex and controllable flows than a standard agent executor loop.

The core flow is as follows:

1. The user's input is added to the graph's state.

2. The Agent Node is called. It uses an LLM (Gemini) to decide the next step: either respond directly to the user or call a tool.

3. A Conditional Edge routes the flow.
    If a tool is needed, it goes to the *Action Node*.
    If no tool is needed, it goes to the *End*.

4. The Action Node executes the requested tool (e.g., codebase_retriever or code_writer) and adds the output to the state.

5. The flow loops back to the Agent Node, which now has the tool's output as context to formulate its final answer.

```Bash
graph TD
    A[Start] --> B(Agent Node);
    B --> C{Decision};
    C -->|Tool Call| D[Action Node];
    C -->|Final Answer| E[End];
    D --> B;
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

### 4. Set Up Google Cloud Authentication
This project requires a Google Cloud Service Account to use the Gemini API.

- Follow the official guide to [create a service account and download the JSON key](https://cloud.google.com/docs/authentication/client-libraries).

- Grant the "Vertex AI User" role to the service account.

- Place the downloaded service-account-key.json file in the root of the project directory.

### 5. Create .env File
Create a file named .env in the project root and add the following line:

    GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json

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
<!-- 
## 🔮 Future Work
[ ] Develop a user-friendly web interface using Streamlit.

[ ] Expose the agent's capabilities via a FastAPI backend.

[ ] Implement a re-ranking step after retrieval to improve search accuracy. 
-->

<!-- 📄 License
This project is licensed under the MIT License. See the LICENSE file for details. -->
