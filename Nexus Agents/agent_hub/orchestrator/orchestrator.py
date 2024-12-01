from typing import List
from agent_hub.agent import Agent
from agent_hub.llms import get_llm
from agent_hub.state import State
from agent_hub.agent import AgentInput
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage ,AIMessage
from agent_hub.plan import OrchestratorPlan, AgentTask, TaskStatus
import asyncio

class OrchestratorInput(AgentInput):
    query: str


class Orchestrator(Agent):
    def __init__(self, available_agents: List[Agent]):
        description = """
        Orchestrator is a class that orchestrates the execution of a plan.
        """
        name = "Orchestrator"
        task = AgentTask.ORCHESTRATOR
        super().__init__(name, description, task)
        self.available_agents = available_agents
        self.agents_names_input_names = {agent.as_tool.__name__: agent.name for agent in available_agents}
        self.main_llm = get_llm("mistral", "pixtral-large-latest")
        self.plan_llm = get_llm("mistral", "pixtral-large-latest").with_structured_output(OrchestratorPlan)
        self.plan = None
        
    def define_input_schema(self)->type[OrchestratorInput]:
        return OrchestratorInput
    
    async def setup(self):
        """
        Setup the orchestrator by setting up the available agents.
        """
        print("Setting up the orchestrator")
        for agent in self.available_agents:
            print(f"Setting up agent: {agent.name}")
            await agent.setup()
        tools = [agent.as_tool for agent in self.available_agents]
        self.main_llm = self.main_llm.bind_tools(tools, tool_choice="any")
        print("Orchestrator setup complete")

    def create_plan(self, query: str) -> OrchestratorPlan:
        """
        Create a plan for computer interaction tasks by understanding available agents' capabilities
        and limitations.
        """
        system_prompt = f"""You are an expert planner designed to help AI systems interact with computers efficiently.
        Given a query from a user, you need to break it down into a series of specific tasks that can be handled by different agents (e.g., vision-based agents for screen interaction, CLI-based agents for terminal tasks).
        Ensure the plan is detailed, well-structured, and efficient.

        Instructions:
        1. Analyze the user's query and break it into distinct tasks.
        
        2. For each task, assign the most appropriate agent, keeping in mind the agent's strengths and limitations:
            - Vision-based agents are useful for GUI interactions but come with higher latency and token costs. So use them only when necessary.
            - CLI-based agents are efficient for text-based tasks and have lower resource usage.
            - Other agents like file system or web navigation agents should be used for specific actions like file handling or web browsing.
            - Some tasks are better handled by direct API calls or command-line operations
            - Complex UI interactions may require multiple steps
           
        3. Ensure the plan includes:
            - A task name.
            - A task description with specific details on what needs to be done.
            - The name of the agent that will execute the task.
            - Order and dependencies between tasks, as some tasks may need to be executed sequentially (e.g., opening a file before editing it).

        Important: Though the plan should be detailed, it should be concise and to the point (No unnecessary steps). Also you only have access to the following agents:

        Available specialized agents and their capabilities:
        {self._format_agent_capabilities()}
        
        Thus, you should only use the agents that are necessary to complete the task.
        Note: You can use the same agent multiple times if needed.
        IMPORTANT: Look at the agent's description and capabilities. Therefore don't give too granular queries. Give a high level query if the agents can handle them.
        """
        
        human_prompt = f"""Plan the computer interaction steps for this task: {query}
        Break it down into specific, atomic operations that match our agents' capabilities."""
        messages = [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]
        plan = self.plan_llm.invoke(messages)
        print("New Plan Created: \n", plan.model_dump_json(indent=4))
        return plan

    def _format_agent_capabilities(self) -> str:
        """
        Format available agents with detailed capability descriptions and limitations.
        """
        capability_template = """
        - {name}: {description}
        """
        #   Optimal for: {optimal_uses}
        #   Limitations: {limitations}
        #   Interaction method: {interaction_method}
        
        capabilities = []
        for agent in self.available_agents:
            # You would need to enhance Agent class to include these additional attributes
            capabilities.append(capability_template.format(
                name=agent.name,
                description=agent.description,
                # optimal_uses=agent.optimal_uses,
                # limitations=agent.limitations,
                # interaction_method=agent.interaction_method
            ))
        return "\n".join(capabilities)

    def execute_plan(self, plan: OrchestratorPlan, previous_outputs: List[str]):
        """
        Execute the plan by invoking the appropriate agents for each task.
        The orchestrator should manage dependencies, handle agent outputs, and ensure tasks are completed in the correct order.
        """
        current_task = plan.tasks[plan.current_task_index]
        main_llm_system_prompt = f"""You are an expert computer interaction coordinator that executes plans by calling specialized agents.
            Your role is to translate high-level tasks into specific agent instructions while being aware of computer interaction patterns.

            Key principles:
            1. Choose the most efficient interaction method:
            - Prefer CLI/API calls over vision-based interaction when possible
            - Use vision (VLM) agents only when GUI interaction is necessary
            - Chain multiple simple commands rather than complex GUI operations
            
            2. Provide detailed context to agents:
            - Include relevant file paths, window titles, or UI elements
            - Specify expected outcomes and verification criteria
            - Pass any state from previous operations
            
            3. Handle computer interaction carefully:
            - Verify critical operations before proceeding
            - Include fallback options for common failure cases
            - Consider system state (files open, applications running)
            
            4. Optimize for reliability:
            - Break complex UI interactions into smaller steps
            - Add verification steps after critical operations
            - Handle timeouts and retries appropriately

            Available specialized agents:
            {self._format_agent_capabilities()}
            
            Plan:
            {plan.model_dump_json(indent=4)}
            
            Current task:
            {current_task.model_dump_json(indent=4)}

            Look at the previous agents' outputs and use them to complete the current task and provide necessary context to the agent.
            Previous outputs: {previous_outputs}
            For each task, you should:
            1. Analyze what type of computer interaction is needed
            2. Choose the most efficient agent and interaction method

        IMPORTANT: You should pick one of the available agents to execute the task. Only if and only if the task is not handled by any agent, you don't need to pick an agent.
        """
        messages = [SystemMessage(content=main_llm_system_prompt), HumanMessage(content=current_task.description)]
        retry_count = 0
        while retry_count < 3:
            try:
                llm_output = self.main_llm.invoke(messages)
                break
            except Exception as e:
                print(f"Error executing task: {current_task.name}. Error: {e}")
                retry_count += 1
                print(f"Retrying {retry_count} times")
                continue
        
        next_agent_input = None
        next_agent_name = None
        
        if llm_output.tool_calls:
            for tool_call in llm_output.tool_calls:
                next_agent_input = tool_call["args"]
                next_agent_name = self.agents_names_input_names[tool_call["name"]]
                break  # Take the first tool call
        else :
            print(f"No tool call found in the LLM output. Output: {llm_output.content}")
        print("************************************************************")
        print(f"Executing task: {current_task.name}\nby calling agent: {next_agent_name}\nwith input: {next_agent_input}")
        print("************************************************************")
        return next_agent_input, next_agent_name

    def update_plan(self, plan: OrchestratorPlan)->OrchestratorPlan:
        """
        Update the plan based on the last task status.
        """
        return self.create_plan(plan.goal)
        
    def __call__(self, state: State):
        """
        The orchestrator will be called with a user query to execute the tasks defined in the plan.
        """
        orchestrator_input = OrchestratorInput(query=state["user_input"])
        # First, create a detailed plan for the query
        plan = state.get("plan", None)
        previous_outputs = state.get("previous_outputs", [])
        print(f"Inside Orchestrator, current plan: {plan.model_dump_json(indent=4) if plan else 'None'}")
        last_task_status = state.get("last_task_status", TaskStatus.PENDING)
        if plan is None:
            plan = self.create_plan(orchestrator_input.query)
        elif last_task_status == TaskStatus.FAILURE:
            plan = self.update_plan(plan)
        elif last_task_status == TaskStatus.SUCCESS and plan.current_task_index < len(plan.tasks) - 1:
            plan.tasks[plan.current_task_index].task_status = TaskStatus.SUCCESS
            plan.current_task_index += 1
        else:
            plan.is_completed = True
        # Execute the tasks based on the plan
        if not plan.is_completed:
            next_agent_input, next_agent_name = self.execute_plan(plan, previous_outputs)
        else :
            next_agent_input = None
            next_agent_name = None
        return {"plan": plan, "next_agent_input": next_agent_input, "next_agent_name": next_agent_name}
    async def __acall__(self, state: State):
        print(" Async Orchestrator received the query:")
