
from exam.schemas import ExamSchema
from exam.models import Exam

from sqlalchemy.orm import Session

def create_exam_svc(exam:ExamSchema,db:Session):
    add_exam = Exam(
        title = exam.title,
        subject = exam.subject,
        class_level = exam.class_level,
        term = exam.term,
        duration = exam.duration,
        is_published = exam.is_published
    )
    db.add(add_exam)
    db.commit()
    return {"message": "exam added successfully"}