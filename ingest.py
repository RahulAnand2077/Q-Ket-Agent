import os
import git
from langchain_community.document_loaders import DirectoryLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter,Language
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

REPO_PATH = "qiskit_repo_data"
DB_PATH = "chroma_db"

def ingest_codebase():
    print("Loading Python and Markdown documents...")
    loader_kwargs = {'encoding': 'utf-8'}
    py_loader = DirectoryLoader(
        REPO_PATH, glob="**/*.py", 
        loader_cls=TextLoader,
        loader_kwargs=loader_kwargs, 
        use_multithreading=True, 
        show_progress=True
    )
    md_loader = DirectoryLoader(
        REPO_PATH, 
        glob="**/*.md", 
        loader_cls=TextLoader,
        loader_kwargs=loader_kwargs, 
        use_multithreading=True, 
        show_progress=True
    )
    
    py_docs = py_loader.load()
    md_docs = md_loader.load()
    docs = py_docs + md_docs
    
    if not docs:
        print("No documents found. Check the repository and loader configuration.")
        return
        
    print(f"Loaded {len(docs)} total documents.")

    print("Splitting Docs...")
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,chunk_size=2000,chunk_overlap=200
    )
    texts = python_splitter.split_documents(docs)
    print(f"Split into {len(texts)} chunks.")

    print("Creating and saving vector store...")
    load_dotenv()
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    vector_store = Chroma.from_documents(
        documents=texts,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )
    print(f"Vector store created and saved to {DB_PATH}.")

if __name__=="__main__":
    ingest_codebase()