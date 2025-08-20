import random
import os
import subprocess
import sys
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START,END

# 1) Define state schema for the graph
class DataState(TypedDict):
    wishes:str


def Intro_node(state:DataState):
    state["wishes"] = state["wishes"].lower()
    return state   

# 2) Node: prefend "Hello World, " to the greeting
def normalize_node(state:DataState):
    state["wishes"]="here it is having HI..., " + state["wishes"]
    return state

#def upper_case_node(state:DataState):
    #state["wishes"] = state["wishes"].upper()
    #return state

def bye_node(state:DataState):
    state["wishes"] = "eshanth wt dng kk i'm living now Bye..," +state["wishes"]
    return state   

def regular_node(state:DataState):
    state["wishes"]="Hello, this is regular, no hi " + state["wishes"]
    return state

def choose_wish_node(state:DataState):
    if "hi" in state["wishes"].split():
        return "normal"
    elif "bye" in state["wishes"].split():
        return "bye"
    else:
        return "regular"

# 4) Build the stateGraph
builder = StateGraph(DataState)
builder.add_node("intro",Intro_node)
builder.add_node("normal",normalize_node)
#builder.add_node("upper",upper_case_node)
builder.add_node("bye",bye_node)
builder.add_node("regular",regular_node)

# 5).connect nodes with edges: START -> wish -> upper -> exclaim -> END
builder.add_edge(START, "intro")
builder.add_conditional_edges("intro",choose_wish_node,["normal","bye","regular"])
builder.add_edge("normal", END)
builder.add_edge("bye", END)
builder.add_edge("regular", END)

# 6) compile and run
graph = builder.compile()
result = graph.invoke({"wishes":input("Enter ur input..")})
print(result)
