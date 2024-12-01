
from typing import Any
from typing import Annotated

from typing_extensions import TypedDict
    
from langgraph.graph.message import add_messages
from agent_hub.agent import AgentInput, Agent
from agent_hub.plan import AgentTask, TaskStatus, OrchestratorPlan
from operator import add
from typing import List
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    # messages: Annotated[list, add_messages]
    plan : OrchestratorPlan = None
    last_task_status : TaskStatus = None
    last_task_output : Any = None
    next_agent_input : AgentInput = None
    next_agent_name : str = None
    messages: Annotated[list, add_messages]
    user_input: str = None
    is_computer_interaction_required: bool = False
    previous_outputs : Annotated[List[str], add] = []