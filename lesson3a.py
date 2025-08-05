from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Define a state
class userState(TypedDict):
    is_premium: bool
    message: str  # this will store the message

# Step 1: Greet the user
def greet_user(state: userState):
    state["message"] = "Welcome. "
    return state

# Step 2: Just return the state without branching here
def check_subscription(state: userState):
    return state

# Step 3: Final messages
def premium_greeting(state: userState):
    state["message"] += "Thanks for being a premium user."
    return state

def normal_greeting(state: userState):
    state["message"] += "Enjoy being our customer."
    return state

# Step 4: Conditional edge selector function
def decide_next_node(state: userState) -> str:
    return "premium_greeting" if state["is_premium"] else "normal_greeting"

# Build the graph
builder = StateGraph(userState)

# Add nodes
builder.add_node("greet_user", greet_user)
builder.add_node("check_subscription", check_subscription)
builder.add_node("premium_greeting", premium_greeting)
builder.add_node("normal_greeting", normal_greeting)

# Add edges
builder.add_edge(START, "greet_user")
builder.add_edge("greet_user", "check_subscription")

# Conditional branching based on a separate decision function
builder.add_conditional_edges("check_subscription", decide_next_node)

builder.add_edge("premium_greeting", END)
builder.add_edge("normal_greeting", END)

# Compile and run
graph = builder.compile()

print("\nPremium User:")
result = graph.invoke({"is_premium": True, "message": ""})
print(result)

print("\nNormal User:")
result = graph.invoke({"is_premium": False, "message": ""})
print(result)
