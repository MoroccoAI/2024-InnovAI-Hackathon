from agent_hub.agent import Agent, AgentTask, AgentInput
from pydantic import Field
import time
from agent_hub.plan import TaskStatus
from agent_hub.state import State
from agent_hub.cli.cli_generator import generate_cli_command
import subprocess
import logging
import os
from pathlib import Path

class CLIAgentInput(AgentInput):
    """
    Input schema for CLI agent that handles command line operations and file management.
    """
    operation: str = Field(
        description="High-level description of the operation to perform (e.g. 'create a new directory called projects', 'list files in current directory')"
    )

class CLIAgent(Agent):
    def __init__(self):
        description = """
        An agent specialized in executing CLI operations and file management tasks. 
        Can understand natural language descriptions and generate appropriate shell commands.
        Handles tasks like file operations, directory management, system commands, and more.
        """
        name = "CLIAgent"
        task = AgentTask.CLI_COMMAND
        super().__init__(name, description, task)
        
        # Set project root
        self.project_root = Path(__file__).parent.parent.parent
        os.chdir(self.project_root)

    def define_input_schema(self)->type[CLIAgentInput]:
        return CLIAgentInput

    async def __acall__(self, state: State, **kwargs) -> str:
        """
        Translates the high-level operation description into appropriate CLI commands
        and executes them safely
        """
        print(f"CLIAgent processing operation: {state['next_agent_input'].operation}")
        time.sleep(2)
        
        # TODO: Implement command generation logic using LLM
        # This would analyze the operation description and generate appropriate shell commands
        # Example:
        # if "create directory" in input.operation.lower():
        #     command = f"mkdir {parsed_directory_name}"
        # elif "list files" in input.operation.lower():
        #     command = "ls -la"
        
        # TODO: Implement safe command execution
        # This would include:
        # - Validation of generated commands
        # - Security checks
        # - Actual execution using subprocess or similar
        # - Error handling
        cli_input = CLIAgentInput(**state["next_agent_input"])
        print(f"CLIAgent has finished the task: {cli_input.operation}")
        return {"last_task_status": TaskStatus.SUCCESS,
                "last_task_output": f"CLIAgent has finished the task: {cli_input.operation}",
                "previous_outputs": [f"\n\n**CLIAgent has finished the task:**\n{cli_input.operation}"]}

    def __call__(self, state: State):
        cli_input = CLIAgentInput(**state["next_agent_input"])
        print(f"Processing CLI operation: {cli_input.operation}")
        command = generate_cli_command(cli_input.operation)
        try:
            output = run_command(command)
            if not output:
                return {"last_task_status": TaskStatus.FAILURE,
                        "last_task_output": f"CLIAgent failed to execute the command: {command}",
                        "previous_outputs": [f"\n\n**CLIAgent failed to execute the command:**\n{command}"]}
        except Exception as e:
            return {"last_task_status": TaskStatus.FAILURE,
                    "last_task_output": f"CLIAgent failed to execute the command: {command}",
                    "previous_outputs": [f"\n\n**CLIAgent failed to execute the command:**\n{command}"]}
        
        print(f"Executed command: {command}")
        
        return {"last_task_status": TaskStatus.SUCCESS,
                "last_task_output": f"CLIAgent has finished the task: {cli_input.operation}",
                "previous_outputs": [f"\n\n**CLIAgent has finished the task:**\n{cli_input.operation}"]}

    async def setup(self):
        """
        Setup the CLI agent's environment and permissions
        """
        print("CLIAgent is setting up")
        # TODO: 
        # - Set up command execution environment
        # - Verify necessary permissions
        # - Initialize command templates/patterns



def run_command(command):
    """Run a command and log output"""
    try:
        process = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
            shell=True
        )
        logging.info(process.stdout)
        if process.stderr:
            logging.error(process.stderr)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command: {e}")
        if e.output:
            logging.error(e.output)
        if e.stderr:
            logging.error(e.stderr)
        return False