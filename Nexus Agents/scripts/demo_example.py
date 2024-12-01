from langchain_core.messages import HumanMessage
from agent_hub.graph import graph



def invoke_graph(user_input: str):
    return graph.invoke({"messages": [HumanMessage(content=user_input)], "user_input": user_input})


user_input = "Can you check the weather in Paris (use the web search agent) and then write the results to a file called weather.txt?"
result = invoke_graph(user_input)
print(result)
print("*"*100)
print("Final Output:")
print(result["messages"][-1].content)