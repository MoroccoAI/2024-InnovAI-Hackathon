from agent_hub.graph import State
from agent_hub.llms import get_llm
from agent_hub.plan import FrontLLMOutput
from langchain_core.messages import AIMessage, SystemMessage
class FrontLLM():
    def __init__(self):
        self.llm = get_llm().with_structured_output(FrontLLMOutput)
        self.name = "front_llm"
    def __call__(self, state: State):
        plan = state.get("plan", None)
        # if it's the first time the FrontLLM is called, there is no plan yet. step is to decide whether to answer directly or to use an agent
        if plan is None:
            system_message = SystemMessage(content="""You are a helpful assistant that can answer questions and perform tasks that require interacting with the computer.
                                           Your goal is to determine whether the user query requires computer interaction (the user query is complex and requires the LLM to use an agent to perform the task) or not (the user query is simple and the LLM should answer the user query without using an agent)""")
            front_llm_output = self.llm.invoke([system_message] + state["messages"])
            if front_llm_output.is_computer_interaction_required:
                return {"user_input": state["messages"][-1].content, "is_computer_interaction_required": True}
            else:
                return {"messages": [AIMessage(content=front_llm_output.llm_response)], "is_computer_interaction_required": False}
        else:
            plan_str = plan.model_dump_json()
            last_task_status = state["last_task_status"]
            last_task_output = state["last_task_output"]
            system_message = SystemMessage(content=f"""You are a helpful assistant that can answer questions and perform tasks that require interacting with the computer.
                                           The user has already asked a question and you have already decided whether to use an agent or not.
                                           Your goal is to answer the user query directly or to reuse the agent to perform the task given the plan and its last task status
                                           Here was the plan : {plan_str}
                                           Here was the last task status : {last_task_status}
                                           Here was the last task output : {last_task_output}.
                                           If everything is done, you can simply answer the user query directly and concisely.""")
            front_llm_output = self.llm.invoke([system_message] + state["messages"])
            return {"messages": [AIMessage(content=front_llm_output.llm_response)], "is_computer_interaction_required": front_llm_output.is_computer_interaction_required}
