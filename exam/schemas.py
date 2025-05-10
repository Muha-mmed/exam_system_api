from pydantic import BaseModel

from utils.constant import AnswerOption,Level

class ExamSchema(BaseModel):
    title: str
    subject: str 
    class_level: Level
    term: str
    duration: int
    is_published : bool = False