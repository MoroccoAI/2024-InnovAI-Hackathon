# import asyncio
# from agent_hub.browser.browser_agent import BrowserUse
# browse_use = BrowserUse()
# asyncio.run(browse_use.setup())

# # Now you can use it in your graph or directly
# result =  browse_use.__call__({ 
#     "next_agent_input": {
#         "query": "Find a one-way flight from Bali to Oman on 12 January 2025 on Google Flights"
#     }
# })
# with open("result.txt", "w") as f:
#     f.write(result)


from langchain_core.messages import HumanMessage
from agent_hub.graph import graph



def invoke_graph(user_input: str):
    return graph.invoke({"messages": [HumanMessage(content=user_input)], "user_input": user_input})


result = invoke_graph("Can you check the weather in Paris?")
print(result)