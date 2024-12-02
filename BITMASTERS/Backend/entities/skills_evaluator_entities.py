from pydantic import BaseModel
from enum import Enum
from typing import List

class PerformanceLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"

class SkillScore(BaseModel):
    name: str
    score: float

class DetailedEvaluation(BaseModel):
    course_name: str
    level: PerformanceLevel
    score: float
    weaknesses: List[SkillScore]
    strengths: List[SkillScore]