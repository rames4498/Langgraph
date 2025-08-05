from langchain_community.llms import Ollama
from langgraph.graph import StateGraph, MessagesState, START, END

from langchain_core.messages import HumanMessage, AIMessage

model = Ollama(model="llama3.2")

def call_llm(state:MessagesState):

    messages = state["messages"]

    reply =  model.invoke(messages[-1].content)
    return {"messages" : [reply]}

# defining the graph 

graph  = StateGraph(MessagesState)

graph.add_node("call_llm", call_llm)

graph.add_edge(START, "call_llm")
graph.add_edge("call_llm", END)

app  = graph.compile()

#input_message = {"messages":[HumanMessage(content="tell me some interesting facts about RCB in IPL")]}

def conversation_with_AI():
    while True:
        user_input = input("You :")
        
        if user_input.lower() in ["exit","quit"]:
            break
        
        input_message = {"messages":[HumanMessage(content=user_input)]}
        for chunk in app.stream(input_message, stream_mode="values"):
            chunk["messages"][-1].pretty_print()

conversation_with_AI()

