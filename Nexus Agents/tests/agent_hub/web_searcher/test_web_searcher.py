import pytest
from agent_hub.web_searcher.web_searcher import WebSearcher, WebSearcherInput
from agent_hub.agent import Agent, AgentInput
from agent_hub.plan import TaskStatus, AgentTask

@pytest.fixture
def web_searcher():
    return WebSearcher()

def test_agent_inheritance(web_searcher):
    """Test that WebSearcher properly implements Agent interface"""
    assert isinstance(web_searcher, Agent)
    assert hasattr(web_searcher, '__call__')
    assert hasattr(web_searcher, '__acall__')
    assert hasattr(web_searcher, 'setup')

def test_input_schema():
    """Test that input schema is properly defined"""
    assert issubclass(WebSearcherInput, AgentInput)
    input_instance = WebSearcherInput(query="test query")
    assert input_instance.query == "test query"

def test_agent_attributes(web_searcher):
    """Test basic agent attributes"""
    assert web_searcher.name == "WebSearcher"
    assert web_searcher.task == AgentTask.WEB_SEARCH
    assert isinstance(web_searcher.description, str)

def test_basic_call(web_searcher):
    """Test that the agent can be called with proper input"""
    state = {
        "next_agent_input": {
            "query": "test query"
        }
    }
    result = web_searcher(state)
    
    assert isinstance(result, dict)
    assert "last_task_status" in result
    assert "last_task_output" in result

@pytest.mark.asyncio
async def test_async_interface(web_searcher):
    """Test that async methods are implemented"""
    await web_searcher.setup()
    # Just verifying the interface exists and can be called