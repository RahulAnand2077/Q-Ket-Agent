import streamlit as st
import requests 
import re

# Uncomment this line for running locally
# API_URL = "http://127.0.0.1:8000/invoke_agent"

# Comment this line for running locally
API_URL = "https://q-ket-agent.onrender.com"

st.set_page_config(
    page_title="Qiskit AI Assistant",
    page_icon="🤖",
    layout="wide"
)
st.title("🤖 Qiskit AI Agent")
st.caption("Your AI-powered pair programmer for the Qiskit codebase.")

def format_agent_response(text: str) -> str:
    """Cleans up the agent's response for proper markdown rendering."""
    # Ensure code blocks start on a new line
    text = re.sub(r'(?<!\n)```', '\n```', text)
    # Ensure code blocks end on a new line
    text = re.sub(r'```(?!\n)', '```\n', text)
    return text

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(placeholder="Ask a question about the Qiskit codebase..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("The agent is thinking..."):
            try:
                # Uncomment this line for running locally
                # response = requests.post(API_URL, json={"message": prompt})
                
                # Comment this line for running locally
                response = requests.post(API_URL+"/invoke_agent", json={"message": prompt})
                response.raise_for_status()  
                
                agent_reply = response.json()["reply"]
                processed_reply = format_agent_response(agent_reply)
                
                st.markdown(processed_reply, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": processed_reply})

            except requests.exceptions.RequestException as e:
                error_message = f"Could not connect to the backend: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})