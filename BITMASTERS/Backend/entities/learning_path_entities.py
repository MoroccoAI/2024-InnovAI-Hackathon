from pydantic import BaseModel, Field
from typing import List

class ModuleContent(BaseModel):
  module_name: str = Field(description="اسم الوحدة")
  topics: List[str] = Field(description="قائمة المواضيع")
  milestone: str = Field(description="وصف الإنجاز")

class LearningPath(BaseModel):
  student_level: str = Field(description="مستوى الطالب")
  course_name: str = Field(description="اسم الدورة")
  learning_path: List[ModuleContent]

class LearningPathInput(BaseModel):
  course_name: str
  level: str
  score: float
  weaknesses: List[str]
  strengths: List[str]
