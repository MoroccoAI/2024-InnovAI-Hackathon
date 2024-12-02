from pydantic import BaseModel, Field
from typing import List, Union
from pydantic import root_validator
# Define Exercise Models
class ExerciseBase(BaseModel):
    type: str = Field(description="Type of exercise")

    def display(self):
        raise NotImplementedError

    class Config:
        discriminator = 'type'

class MCQ(ExerciseBase):
    type: str = Field(default="mcq", description="Multiple Choice Question")
    question_text: str = Field(description="MCQ question text")
    options: List[str] = Field(description="List of answer options", min_items=4, max_items=4)
    correct_answer: str = Field(description="Correct option label (e.g., 'A', 'B', 'C', 'D')")

    def display(self):
        print(f"Type: {self.type}")
        print(f"Question: {self.question_text}")
        for idx, option in enumerate(self.options, start=65):  # starts from 'A'
            print(f"{chr(idx)}: {option}")
        print(f"Answer: {self.correct_answer}\n")

class CodeGeneration(ExerciseBase):
    type: str = Field(default="code", description="Code generation exercise")
    question: str = Field(description="Code to be generated or corrected")
    answer: str = Field(description="Correct code")

    def display(self):
        print(f"Type: {self.type}")
        print(f"Question: {self.question}")
        print(f"Answer: {self.answer}\n")

class TheoreticalQuestion(ExerciseBase):
    type: str = Field(default="theoretical", description="Theoretical question")
    question: str = Field(description="Theoretical question")
    answer: str = Field(description="Correct answer explanation")

    def display(self):
        print(f"Type: {self.type}")
        print(f"Question: {self.question}")
        print(f"Answer: {self.answer}\n")

# ExerciseList Model
class ExerciseList(BaseModel):
    exercises: List[Union[MCQ, CodeGeneration, TheoreticalQuestion]]

    @root_validator(pre=True)
    def log_parsed_exercises(cls, values):
        for exercise in values.get("exercises", []):
            print(f"Parsing exercise with type: {exercise.get('type')}")
        return values

