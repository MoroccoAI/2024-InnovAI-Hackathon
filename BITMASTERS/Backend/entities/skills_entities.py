from pydantic import BaseModel, Field
from typing import List, Type , Dict,Union
 
class MCQQuestion(BaseModel):
    question_text: str = Field(description="MCQ question text")
    options: List[str] = Field(description="List of answer options", min_items=4, max_items=4)
    correct_answer: str = Field(description="Correct option label (e.g., 'A', 'B', 'C', 'D')")

class SubSkill(BaseModel):
    related_skill_name: str = Field(description="Name of the related skill")
    mcq_questions: List[MCQQuestion] = Field(description="List of MCQ questions for this related skill")

class Skill(BaseModel):
    main_skill: str = Field(description="Name of the main skill")
    related_skills: List[SubSkill] = Field(description="List of related skills and their MCQ questions")