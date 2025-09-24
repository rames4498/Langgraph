from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize model
model = ChatGroq(model="openai/gpt-oss-20b", api_key=GROQ_API_KEY)

# Node: send conversation history to model
def call_llm(state: MessagesState):
    messages = state["messages"]
    reply = model.invoke(messages)
    return {"messages": [reply]}

# Build graph
graph = StateGraph(MessagesState)
graph.add_node("call_llm", call_llm)
graph.add_edge(START, "call_llm")
graph.add_edge("call_llm", END)

app = graph.compile()

# Conversation loop with memory
def conversation_with_memory():
    # System instruction (context)
    system_msg = SystemMessage(content="You are a friendly teacher. Always explain things step by step.")
    
    # Start with system message in history
    history = [system_msg]

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Add new user message to history
        history.append(HumanMessage(content=user_input))

        # Run the graph with full history
        state = {"messages": history}
        result = app.invoke(state)   #  use invoke instead of run

        # Get AI reply and add it to history
        reply = result["messages"][-1]
        print("AI:", reply.content)
        history.append(reply)  # <- This makes the AI remember!

if __name__ == "__main__":
    conversation_with_memory()
