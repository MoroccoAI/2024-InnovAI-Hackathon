from agent_hub.agent import Agent, AgentTask, AgentInput
from pydantic import Field
import requests
import json
from agent_hub.state import State
from agent_hub.plan import TaskStatus
from typing import List, Dict
from agent_hub.llms import groq_llm
import os


SERPER_API_KEY = os.getenv("SERPER_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")
# Test Pipline
class WebSearcherInput(AgentInput):
    """
    Input schema for Web Searcher agent that handles web search queries.
    """
    query: str = Field(
        description="The search query to look up information for"
    )

class WebSearcher(Agent):
   
    
    def __init__(self, model="jina-reranker-v2-base-multilingual", top_n=10):
        description =  """
    An intelligent agent specialized in efficient information retrieval from the web.
    
    Best used for:
    - Quick information lookup and fact-checking
    - Research queries requiring data from multiple sources
    - Getting up-to-date information (news, prices, etc.)
    - Synthesizing information from multiple search results
    
    Advantages:
    - Much faster than browser-based search
    - Lower resource usage and cost
    - Efficient for pure information retrieval tasks
    
    Not suitable for:
    - Tasks requiring user authentication
    - Interactive web operations (form filling, clicking, etc.)
    - Tasks that need to maintain web session state
    - Complex web automation sequences
    
    """
        name = "WebSearcher"
        task = AgentTask.WEB_SEARCH
        super().__init__(name, description, task)
        self.reranker_model = model
        self.top_n = top_n

    def define_input_schema(self) -> type[WebSearcherInput]:
        return WebSearcherInput

    def search_web(self, query: str, type: str = "search", **params) -> List[Dict]:
        """Get raw search results from Serper API"""
        url = f"https://google.serper.dev/{type}"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        }
        payload_data = {"q": query}
        payload_data.update(params)
        payload = json.dumps(payload_data)
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()
        results = results["organic"]
        # rename "link" key to "url"
        for result in results:
            result["url"] = result.pop("link")
        return results

    def rerank_documents(self, query: str, docs: List[Dict]) -> List[Dict]:
        """Rerank search results using Jina API"""
        url = "https://api.jina.ai/v1/rerank"
        headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer " + JINA_API_KEY,
        }
        documents = [doc["snippet"] for doc in docs]
        payload = {
            "model": self.reranker_model,
            "query": query,
            "top_n": self.top_n,
            "documents": documents,
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            results = response.json()["results"]
            indices = [result["index"] for result in results]
            return [docs[index] for index in indices]
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

    def synthesize_response(self, query: str, ranked_results: List[Dict]) -> str:
        """Use LLM to synthesize final response from ranked results"""
        # Prepare prompt for LLM synthesis
        prompt = f"""Given the search query: "{query}"
        And the following search results:
        {json.dumps(ranked_results, indent=2)}
        
        Please synthesize a comprehensive response that:
        1. Directly answers the query
        2. Incorporates key information from the search results
        3. Cites sources where appropriate
        
        Response:"""

        # Call LLM to synthesize response
        return groq_llm.invoke(prompt)

    async def __acall__(self, state: State, **kwargs) -> Dict:
        """
        Execute the web search pipeline:
        1. Get search results
        2. Rerank results
        3. Synthesize response
        """
        web_input = WebSearcherInput(**state["next_agent_input"])
        query = web_input.query
        
        # Execute search pipeline
        raw_results = self.search_web(query)
        ranked_results = self.rerank_documents(query, raw_results)
        final_response = self.synthesize_response(query, ranked_results)

        return {
            "last_task_status": TaskStatus.SUCCESS,
            "last_task_output": final_response.content,
            "previous_outputs": ["\n\n**Web Searcher has finished the task with the following output**:\n" + final_response.content]
        }

    def __call__(self, state: State) -> Dict:
        """Synchronous version of the call method"""
        web_input = WebSearcherInput(**state["next_agent_input"])
        query = web_input.query
        
        raw_results = self.search_web(query)
        ranked_results = self.rerank_documents(query, raw_results)
        final_response = self.synthesize_response(query, ranked_results)

        return {
            "last_task_status": TaskStatus.SUCCESS,
            "last_task_output": final_response.content,
            "previous_outputs": ["\n\n**Web Searcher has finished the task with the following output**:\n" + final_response.content]
        }

    async def setup(self):
        """Setup the web searcher agent"""
        print("WebSearcher agent is setting up")
        # No API key verification needed since we're using hardcoded values for now

