from entities.exercice_agent_entities import *
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from typing import List
from entities.qa_entities import *

# ExerciseGenerator Class
class ExerciseGenerator:
    def __init__(self, model, topics: List[Topic], num_exercises: int = 2):
        self.model = model
        self.topics = topics
        self.num_exercises = num_exercises
        self.parser = PydanticOutputParser(pydantic_object=ExerciseList)

        self.system_prompt = '''
        You are an exercise generator for a course module.
        Given a topic name and explanation, generate {num_exercises} exercises.
        The exercises should be diverse in type, including code generation, MCQ, and theoretical questions.
        For MCQs, provide a question text, four answer options labeled A, B, C, D, and indicate the correct answer.
        Your response should be a JSON object with a key "exercises" containing a list of exercises.
        Each exercise should have a "type" field and corresponding fields based on the type:
        - For "mcq": "question_text", "options" (list of 4 strings), "correct_answer" (one of "A", "B", "C", "D")
        - For "code": "question", "answer"
        - For "theoretical": "question", "answer"

        {format_instructions}
        '''

        self.user_prompt = '''
        Generate {num_exercises} exercises for the topic "{topic_name}".
        Use the explanation: {explanation} to create relevant questions.
        '''

        self.template = ChatPromptTemplate(
            messages=[
                ('system', self.system_prompt),
                ('human', self.user_prompt)
            ],
            input_variables=['topic_name', 'explanation', 'num_exercises'],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            }
        )

        self.chain = self.template | self.model | self.parser

    def generate_exercises(self) -> List[ExerciseBase]:
        all_exercises = []
        for topic in self.topics:
            try:
                response = self.chain.invoke({
                    'topic_name': topic.topic_name,
                    'explanation': topic.explanation,
                    'num_exercises': self.num_exercises
                })
                exercises = response.exercises
                all_exercises.extend(exercises)
            except Exception as e:
                print(f"Error generating exercises for topic {topic.topic_name}: {e}")
        return all_exercises