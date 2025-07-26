from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage 
from agent import create_graph


def main():
    print("Qiskit Codebase Q&A Agent\n")

    app = create_graph()

    print("Agent is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You : ")
        if user_input.lower() == "exit":
            break
        
        inputs = [HumanMessage(content=user_input)]

        for output in app.stream({"messages" : inputs}):
            if "agent" in output:        
                response = output["agent"]["messages"][-1]
                print(f"Agent :\n{response.content}")

if __name__ == "__main__":
    main()
