from abc import ABC
from typing import List
from enum import Enum
from abc import abstractmethod
from pydantic import BaseModel
from langchain_core.tools import StructuredTool
from agent_hub.plan import AgentTask


class AgentInput(BaseModel, ABC):
    """
    Agent that performs a task.
    """

class Agent(ABC):
    """
    An agent is a class that can perform a task.
    """
    as_tool : type[AgentInput] = None
    
    def __init__(self, name: str, description: str, task: AgentTask):
        """
        Initialize the agent with a name, description, and task.
        """
        self.name = name
        self.description = description
        self.task = task
        self.as_tool = self.define_input_schema()
        

    @abstractmethod
    def define_input_schema(self)->type[AgentInput]:
        pass
    
    def get_input_from_dict(self, input_dict: dict)->AgentInput:
        return self.as_tool(**input_dict)
    
    def as_tool(self):
        return self.as_tool

    @abstractmethod
    async def setup(self):
        """
        Setup the agent.
        """
        pass

    @abstractmethod
    async def __acall__(self, input: AgentInput, **kwargs) -> str:
        """
        Execute the agent's task.
        
        Args:
            input: The instruction/command to execute
            **kwargs: Additional arguments needed for execution
            
        Returns:
            str: The result of executing the task
        """
        pass

    @abstractmethod
    def __call__(self, input: AgentInput, **kwargs) -> str:
        """
        Call another agent to execute a task.
        
        Args:
            other_agent: The agent to call
            
        Returns:
            str: The result from the other agent's execution
        """
        pass
