from typing import List
from pydantic import BaseModel, Field
from enum import Enum


class TaskStatus(Enum):
    """
    The status of a task with an optional comment/reason field.
    """
    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"


class Task(BaseModel):
    """
    A task is a single task to be performed by the orchestrator.
    """
    name: str
    description: str
    execution_agent_name: str
    task_status: TaskStatus = TaskStatus.PENDING
    
class OrchestratorPlan(BaseModel):
    """
    A plan is a list of tasks to be performed by the orchestrator in order to successfully complete the main task asked by the user.
    This includes the necessary calls to the available agents.
    """
    tasks: List[Task]
    goal: str
    current_task_index: int = 0
    is_completed: bool = False

class AgentTask(Enum):
    """
    A task is a specific action that an agent can perform.
    """
    WEB_SEARCH = "web_search"
    CLI_COMMAND = "cli_command"
    FILE_MANIPULATION = "file_manipulation"
    CODER = "coder"
    ORCHESTRATOR = "orchestrator"
    WEB_BROWSER = "web_browser"

class FrontLLMOutput(BaseModel):
    """
    The output of the FrontLLM.
    """
    is_computer_interaction_required: bool = Field(description="Whether the user query requires computer interaction (the user query is complex and requires the LLM to use an agent to perform the task) or not (the user query is simple and the LLM should answer the user query without using an agent)")
    llm_response: str = Field(description="The normal response of the LLM in case the task doesn't need computer interaction (like replying to greetings, etc...)")
