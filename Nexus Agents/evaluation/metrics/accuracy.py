from agent_hub.llms import groq_llm
from pydantic import BaseModel, Field


class RewardMetric(BaseModel):
    score: float = Field(description="The score of the quality of the search results given the input, output and expected output. it should range between 0 and 1")
    reason: str = Field(description="The reason for the score")
    
    
llm = groq_llm.with_structured_output(RewardMetric)


def search_result_quality_metric(input, output, expected_output):
    prompt = f"""You are evaluating the quality of web search results.
            
        Given a search query and the actual vs expected search results, evaluate how well the output matches what was expected.

        Search Query: {input}
        Actual Search Results: {output} 
        Expected Search Results: {expected_output}

        Score the results from 0 to 1 where:
        0 = Completely irrelevant or incorrect results
        0.5 = Partially relevant results but missing key information
        1 = Perfect match (not necessarily exact, but relevant) with expected results

        Provide your score and detailed reasoning for the evaluation."""

    response = llm.invoke(prompt)
    return response