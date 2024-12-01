from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
import json



llm = OllamaLLM(model="llama3.2:1b",
                temperature=0,
                base_url="http://ollama:11434")

def extract_details(document_text):


    system_message = SystemMessagePromptTemplate.from_template(
        """
        You are an AI bot designed to extract structured information. Parse the given text and extract:
        - Key skills
        - Experiences
        - Tools
        Output strictly in valid JSON format. Do not include any extra text or explanations.
        """
    )
    human_message = HumanMessagePromptTemplate.from_template("{resume_text}")

    prompt_template = ChatPromptTemplate.from_messages([system_message, human_message])

    chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        output_parser=StrOutputParser()
    )

    result = chain.run({"resume_text": document_text})


    try:
        start_idx = result.find("{")
        end_idx = result.rfind("}") + 1
        if start_idx == -1 or end_idx == -1:
            raise ValueError("No JSON object found in LLM response.")
        
        json_str = result[start_idx:end_idx]
        result = json.loads(json_str)  # Parse the JSON
        
    except (json.JSONDecodeError, ValueError) as e:
        return {"error": f"Error parsing JSON: {str(e)}"}

    return result



def compare_details(resume_details, job_offer_details):
    prompt = f"""
    You are an AI assistant designed to help job seekers improve their resumes. Compare the following:

    Resume:
    {resume_details}

    Job Description:
    {job_offer_details}

    Identify:
    1. Skills mentioned in the job description but missing in the resume.
    2. Tools required by the job that are not listed in the resume.
    3. Experiences the job requires that are absent from the resume.

    Provide your answer in a clear, human-readable format. Example:
    - Missing skills: [list them]
    - Missing tools: [list them]
    - Missing experiences: [list them]
    """
    
    return llm.invoke(prompt)
    