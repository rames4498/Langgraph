from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

h = HumanMessage(content="Hi, what's the weather?")
a = AIMessage(content="It's sunny today.")
s = SystemMessage(content="You are a helpful assistant that replies briefly.")

print(h.content)   # "Hi, what's the weather?"
print(a.content)   # "It's sunny today."
# pretty_print may exist on the message objects:
h.pretty_print()   # shows: "Human: Hi, what's the weather?"
a.pretty_print()   # shows: "AI: It's sunny today."

print("**************************")
#from langchain_core.messages import HumanMessage, AIMessage

# initial state
state = {"messages": [HumanMessage(content="Hello")]}
print(state.values())
# node function returns a partial update
node_output = {"messages": [AIMessage(content="Hi — how can I help?")]}

# reducer logic (what MessagesState does under the hood)
state["messages"].extend(node_output["messages"])
print(state["messages"], "this is...")
# state now:
# [HumanMessage("Hello"), AIMessage("Hi — how can I help?")]
print(type(state))
print(state)


print("**************************")

from langchain_core.messages import AIMessage

raw_reply = "Sure, here are three facts."
# normalize to AIMessage
if isinstance(raw_reply, str):
    reply = AIMessage(content=raw_reply)
else:
    reply = raw_reply

# return from node
print({"messages": [reply]})

