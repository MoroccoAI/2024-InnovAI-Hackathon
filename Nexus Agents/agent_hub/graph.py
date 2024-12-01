from typing_extensions import TypedDict
from agent_hub.state import State
from langgraph.graph import StateGraph, START, END
from agent_hub.orchestrator.orchestrator import Orchestrator
from agent_hub.browser.browser_agent import BrowserUse
from agent_hub.web_searcher.web_searcher import WebSearcher
from agent_hub.cli.cli_agent import CLIAgent
from agent_hub.front_llm import FrontLLM
import asyncio


browse_use = BrowserUse()
cli_agent = CLIAgent()
web_searcher = WebSearcher()
agents = [browse_use, cli_agent, web_searcher]
orchestrator = Orchestrator(available_agents=agents)
front_llm = FrontLLM()

asyncio.run(orchestrator.setup())

def next_step(state: State):
    next_agent_name = state["next_agent_name"]
    if next_agent_name is not None:
        return next_agent_name
    else:
        return front_llm.name

def is_computer_interaction_required(state: State):
    is_computer_interaction_required = state["is_computer_interaction_required"]
    if is_computer_interaction_required:
        return orchestrator.name
    else:
        return END

graph_builder = StateGraph(State)

graph_builder.add_node(orchestrator.name, orchestrator)
graph_builder.add_node(front_llm.name, front_llm)
graph_builder.add_edge(START, front_llm.name)
graph_builder.add_conditional_edges(front_llm.name, is_computer_interaction_required)
for agent in agents:
    graph_builder.add_node(agent.name, agent)
    graph_builder.add_edge(agent.name, orchestrator.name)

graph_builder.add_conditional_edges(orchestrator.name, next_step)


graph = graph_builder.compile()

from pathlib import Path
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod

# Create docs directory if it doesn't exist
Path("docs").mkdir(exist_ok=True)

# Generate and save the Mermaid diagram
png_data = graph.get_graph().draw_mermaid_png(
    draw_method=MermaidDrawMethod.API,
    background_color="white",
    padding=10
)

# Save the PNG data to a file
output_path = "docs/mermaid_graph.png"
with open(output_path, "wb") as f:
    f.write(png_data)