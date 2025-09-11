from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()
# ⚠ Replace with your actual Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq model with API key
model = ChatGroq(model="openai/gpt-oss-20b", api_key=GROQ_API_KEY)

def call_llm(state: MessagesState):
    messages = state["messages"]
    reply = model.invoke(messages)   # Send all messages
    return {"messages": [reply]}

# Define the graph
graph = StateGraph(MessagesState)
graph.add_node("call_llm", call_llm)
graph.add_edge(START, "call_llm")
graph.add_edge("call_llm", END)

app = graph.compile()

# Conversation loop
def conversation_with_AI():
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            break
        
        input_message = {"messages": [HumanMessage(content=user_input)]}
        for chunk in app.stream(input_message, stream_mode="values"):
            chunk["messages"][-1].pretty_print()

conversation_with_AI()
