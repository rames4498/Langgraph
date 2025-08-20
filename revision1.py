
import random
import os
import subprocess
import sys
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
#from langchain_core.runnables.graph import MermaidDrawMethod

# 1) Define state schema for the graph
class HelloWorldState(TypedDict):
    greeting: str

# 2) Node: prepend "Hello World, " to the greeting
def hello_world_node(state: HelloWorldState):
    state["greeting"] = "Hello World, " + state["greeting"]
    return state

# 3) Another node (optional) to add exclamation
def exclamation_node(state: HelloWorldState):
    state["greeting"] += "!"
    return state

# 4) Build the StateGraph
builder = StateGraph(HelloWorldState)
builder.add_node("greet", hello_world_node)
builder.add_node("exclaim", exclamation_node)

# 5) Connect nodes: START -> greet -> exclaim -> END
builder.add_edge(START, "greet")
builder.add_edge("greet", "exclaim")
builder.add_edge("exclaim", END)

# 6) Compile and run
graph = builder.compile()
result = graph.invoke({"greeting": ""})
print(result)   # Expected: {'greeting': 'Hello World, from LangGraph!!'}
