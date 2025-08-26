from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver  # in-memory checkpointer

# --- State definition ---
class GreetingState(TypedDict, total=False):
    name: str
    greetings: list[str]   # keep full history of greetings

# --- Node ---
def greeting_node(state: GreetingState):
    name = state.get("name", "Friend")   # fallback if missing
    greeting = f"Hello {name}"

    # append to greetings list
    past = state.get("greetings", [])
    past.append(greeting)

    return {"name": name, "greetings": past}

# --- Build graph ---
builder = StateGraph(GreetingState)
builder.add_node("greeting_node", greeting_node)

builder.add_edge(START, "greeting_node")
builder.add_edge("greeting_node", END)

# --- Use memory checkpointer ---
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# --- Run with persistent thread ---
print(graph.invoke({"name": "Sherlock"}, config={"configurable": {"thread_id": "1"}}))
# {'name': 'Sherlock', 'greetings': ['Hello Sherlock']}

print(graph.invoke({"name": "Watson"}, config={"configurable": {"thread_id": "1"}}))
# {'name': 'Watson', 'greetings': ['Hello Sherlock', 'Hello Watson']}

print(graph.invoke({}, config={"configurable": {"thread_id": "1"}}))
# falls back to "Friend", keeps history:
# {'name': 'Friend', 'greetings': ['Hello Sherlock', 'Hello Watson', 'Hello Friend']}
