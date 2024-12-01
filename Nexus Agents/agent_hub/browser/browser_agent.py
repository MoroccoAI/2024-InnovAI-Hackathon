from browser_use import Agent as BrowserAgent
from agent_hub.agent import Agent as BaseAgent, AgentTask, AgentInput
from pydantic import Field
from agent_hub.llms import mistral_llm
import nest_asyncio
import asyncio
from agent_hub.state import State
from agent_hub.plan import TaskStatus
import asyncio

class BrowserUseInput(AgentInput):
    """Input schema for browser operations."""
    query: str = Field(
        description="browser operation to perform"
    )

class BrowserUse(BaseAgent):
    def __init__(self):
        description = """
    An agent that emulates human-like web browsing behavior for complex web interactions.
    
    Best used for:
    - Tasks requiring authentication (logging into platforms)
    - Multi-step web processes (booking flights, shopping)
    - Interactive web operations (form filling, button clicking)
    - Tasks needing session state maintenance
    
    Advantages:
    - Can handle complex web interactions
    - Maintains session state and cookies
    - Supports authenticated operations
    - Can execute JavaScript and handle dynamic content
    
    Trade-offs:
    - Slower than direct API or search operations
    - Higher resource usage
    - More complex error handling needed
    - Not suitable for bulk operations
    
    Note: For simple information retrieval, prefer WebSearcher agent as it's
    more efficient. Use BrowserUse only when actual browser interaction
    is necessary for the task.
    """
        name = "BrowserUse"
        nest_asyncio.apply()
        task = AgentTask.WEB_BROWSER
        super().__init__(name, description, task)

    async def setup(self):
        """Initialize the browser agent with Mistral LLM."""
        try:
            # Install playwright browsers if not already installed
            import subprocess
            subprocess.run(["playwright", "install"], check=True)
            print("BrowserUse is ready")
        except Exception as e:
            print(f"Error during BrowserUse setup: {e}")
            raise e

    def __call__(self, state: State):
        browse_input = BrowserUseInput(**state["next_agent_input"])
        print(f"Sync BrowserUse is calling the available agents for the task: {browse_input}")
        try:
            # Get the current event loop or create a new one
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            browser_agent = BrowserAgent(
                task=browse_input.query,
                llm=mistral_llm
            )
            
            # Run the async code in the event loop
            result = loop.run_until_complete(browser_agent.run())
            return {
                "last_task_status": TaskStatus.SUCCESS,
                "last_task_output": result,
                "previous_outputs": ["\n\n**BrowserUse has finished the task with the following output**:\n" + str(result)[:200]]
            }
        except Exception as e:
            print(f"Error executing task: {browse_input.query}. Error: {e}")
            return {
                "last_task_status": TaskStatus.FAILURE,
                "last_task_output": f"Error executing task: {browse_input.query}. Error: {e}",
                "previous_outputs": [f"\n\n**Error executing task:**\n{browse_input.query}. Error: {e}"]
            }
        
        

    async def __acall__(self, state: State, **kwargs) -> str:
        browse_input = BrowserUseInput(**state["next_agent_input"])
        print(f"Async BrowserUse is calling the available agents for the task: {browse_input}")
        try:
            browser_agent = BrowserAgent(
                task=browse_input.query,
                llm=mistral_llm
            )
            
            result = await browser_agent.run()
            return {
                "last_task_status": TaskStatus.SUCCESS,
                "last_task_output": result,
                "previous_outputs": ["\n\n**BrowserUse has finished the task with the following output**:\n" + str(result)[:200]]
            }
        except Exception as e:
            print(f"Error executing task: {browse_input.query}. Error: {e}")
            return {
                "last_task_status": TaskStatus.FAILURE,
                "last_task_output": f"Error executing task: {browse_input.query}. Error: {e}",
                "previous_outputs": [f"\n\n**Error executing task:**\n{browse_input.query}. Error: {e}"]
            }
        
    def define_input_schema(self) -> type[BrowserUseInput]:
        return BrowserUseInput