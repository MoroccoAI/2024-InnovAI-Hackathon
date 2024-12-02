from entities.learning_path_entities import *
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import Type

class LearningPathAgent:
  def __init__(self,model):
    self.__parser=PydanticOutputParser(pydantic_object=LearningPath)
    self.__model=model
    self.__system_prompt='''
    You are an AI-powered learning path generator designed to create personalized learning paths for users based on their level and diagnostic test results. The goal is to provide a structured and effective learning experience tailored to the user's needs.
    Your entire response/output is going to consist of a single JSON object, and you will NOT wrap it within JSON md markers

    ### Input Data
    1. **User Level**: [Beginner, Intermediate, Advanced]
    2. **Diagnostic Test Results**:
      - **Score**: [Score out of 100]
      - **Strengths**: [List of areas where the user performed well]
      - **Weaknesses**: [List of areas where the user needs improvement]
    3. **Course Information**:
      - **Course Name**: [Course Name]

    {format_instructions}
    '''
    self.__user_input="""
    Generate a personalized learning path for a user who is at an {level} level in the course "{course_name}". The user scored {score} on the diagnostic test, with strengths in {strengths}, and weaknesses in {weaknesses}.
    """
    self.__template=ChatPromptTemplate(
        [
            ('system',self.__system_prompt),
            ('human',self.__user_input)
        ],
        input=['level','course_name','score','strengths','weaknesses'],
        partial_variables={"format_instructions": self.__parser.get_format_instructions()}
    )
    self.chain=self.__template|self.__model|self.__parser

  def generate_learning_path(self,learning_path_input:Type[LearningPathInput])->Type[LearningPath]:
    content=self.chain.invoke(
        {
          'level':learning_path_input.level,
          'course_name':learning_path_input.course_name,
          'score':learning_path_input.score ,
          'strengths':learning_path_input.strengths,
          'weaknesses':learning_path_input.weaknesses
        }
    )
    return content