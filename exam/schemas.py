from typing import Optional
from pydantic import BaseModel

from utils.constant import AnswerOption,Level

class CreateExamSchema(BaseModel):
    title: str
    subject: str 
    class_level: Level
    term: str
    duration: int
    is_published : bool = False
class ExamSchema(BaseModel):
    title: str
    subject: str 
    class_level: Level
    term: str
    duration: int
    is_published : bool
    
    class Config:
        from_attribute = True
    
class UpdateExamSchema(BaseModel):
    title: Optional[str]=None
    subject: Optional[str]=None
    class_level: Optional[Level]=None
    term:  Optional[str]=None
    duration: Optional[int]=None
    is_published : bool = False

class QuestionSchema(BaseModel):
    description : Optional[str] = None
    question : str
    option_a : str
    option_b : str
    option_c : str
    option_d : str
    correct_answer : AnswerOption
    
class UpdateQuestionSchema(BaseModel):
    description : Optional[str] = None
    question : Optional[str] = None
    option_a : Optional[str] = None
    option_b : Optional[str] = None
    option_c : Optional[str] = None
    option_d : Optional[str] = None
    correct_answer : Optional[AnswerOption] = None