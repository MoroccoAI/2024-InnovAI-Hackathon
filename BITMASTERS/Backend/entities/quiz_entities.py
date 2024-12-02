from pydantic import BaseModel, Field
from typing import List 

# Define the models for the quiz question and content
class QuizQuestion(BaseModel):
    question: str = Field(description='The quiz question')
    options: List[str] = Field(description='List of multiple-choice options')
    correct_answers: List[str] = Field(description='List of correct answers (can have multiple)')

class QuizContent(BaseModel):
    module_name: str = Field(description='Module Name')
    questions: List[QuizQuestion] = Field(description='List of quiz questions')

# Define the quiz input model without num_questions
class QuizInput(BaseModel):
    module_name: str
    course_name: str
    topics: List[str]

class QuizQAResponse(BaseModel):
    question: str
    user_answers: List[str]
    correct_answers: List[str]
    
class QuizUserAnswers(BaseModel):
    module_name: str
    questions: List[QuizQAResponse]

