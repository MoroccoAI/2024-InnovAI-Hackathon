from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import Type
from entities.topic_content_entities import *

class TopicContentAgent:
  def __init__(self,model):
    self.__parser=PydanticOutputParser(pydantic_object=TopicContent)
    self.__model=model
    self.__system_prompt='''
    You're an interactive personal tutor who is an expert at explaining topics. Given a topic and the information to teach, please educate the user about it at a beginner level.
    Your entire response/output is going to consist of a single JSON object.

    ### Input Data
    1. **Module Name**: [Module Name]
    2. **Topics**: [List of Topics]

    {format_instructions}
    '''
    self.__user_prompt='''Generate detailed content for the module {module_name} in the course "{course_name}". The module includes the following topics: {topics}.'''
    self.__template=ChatPromptTemplate(
        [
            ('system',self.__system_prompt),
            ('human',self.__user_prompt)
        ],
        input=['module_name','course_name','topics'],
        partial_variables={"format_instructions": self.__parser.get_format_instructions()}
    )
    self.chain=self.__template|self.__model|self.__parser

  def generate_topic_content(self,topic_input:Type[TopicInput])->Type[TopicContent]:
    content=self.chain.invoke(
        {
          'module_name':topic_input.module_name,
          'course_name':topic_input.course_name,
          'topics':', '.join(topic_input.topics)
        }
    )
    return content