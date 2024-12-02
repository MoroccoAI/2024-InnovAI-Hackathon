from pydantic import BaseModel, Field
from typing import List

class Topic(BaseModel):
  topic_name:str=Field(description='Topic Name')
  explanation:str=Field(description='Detailed Explanation of the Topic')

class TopicContent(BaseModel):
  module_name:str=Field(description='Module Name')
  introduction:str=Field(description='Brief Introduction to the Module')
  topics:List[Topic]

class TopicInput(BaseModel):
  module_name:str
  course_name:str
  topics:List[str]

class QuestionRequest(BaseModel):
    question: str
    topics:List[Topic]

# Response model
class SimpleResponse(BaseModel):
    response: str