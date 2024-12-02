from entities.skills_entities import *
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

class SkillAssessmentAgent:
    def __init__(self, model):
        self.model = model
        self.parser = PydanticOutputParser(pydantic_object=Skill)

        # Fix: Escape curly braces in the JSON example and handle format_instructions
        self.system_prompt = '''
        You are a skill assessment generator. Given a text input, identify the main skill and 5 related skills.
        For each related skill, generate 3 MCQ questions with 4 options each and indicate the correct answer.
        Your response should be a JSON object.

        {format_instructions}
        '''

        # Generate the correct format instructions using the parser
        format_instructions = self.parser.get_format_instructions()
        self.template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "Generate skills and MCQ questions based on the following text: {input_text}")
        ])

        self.chain = self.template | self.model | self.parser

    def generate_skill_assessment(self, input_text: str) -> Skill:
        try:
            # Pass format_instructions along with input_text
            skill_assessment = self.chain.invoke({
                "input_text": input_text,
                "format_instructions": self.parser.get_format_instructions()
            })
            return skill_assessment
        except Exception as e:
            print(f"Error generating skill assessment: {e}")
            return None
