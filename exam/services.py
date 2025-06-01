from fastapi import HTTPException,status
from authentication.models import Student
from exam.schemas import ExamSchema, QuestionSchema,UpdateExamSchema,CreateExamSchema
from exam.models import Exam,Question

from sqlalchemy.orm import Session

# SERVICE DEPENDENCY 👨‍🏭🧑
def get_exam(exam_id:int,db:Session):
    exam = db.query(Exam).filter_by(id = exam_id).first()
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="exam don't exist")
    return exam

def get_question(Q_id:int,db:Session):
    question = db.query(Question).filter_by(id = Q_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Question not found")
    return question
    
def get_question():
    pass

# EXAM SERVICES 🌟🤞
# LIST ALL EXAM 
def all_exam_svc(db:Session)->ExamSchema:
    return db.query(Exam).all()

# CREATE EXAM 
def create_exam_svc(user:Student,exam:CreateExamSchema,db:Session):
    if user.role == "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    try:
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
    except:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error creating exam")

# UPDATE ALREADY MADE EXAM
def update_exam_svc(user:Student,exam_id:int,new_data:UpdateExamSchema,db:Session):
    exam = get_exam(exam_id,db)
    try:
        if user.role == "student":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        update_exam = new_data.model_dump(exclude_unset=True)
        try:
            for key,value in update_exam.items():
                setattr(exam,key,value)
            db.commit()
            return exam
        except:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Exam update failed")
    except Exception as e:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

# DELETE EXAM 
def delete_exam_svc(user:Student,exam_id:int,db:Session):
    exam = get_exam(exam_id,db)
    try:
        if user.role =="student":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You don't have access to this")
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid exam id")
        db.delete(exam)
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Exam Deleted ✅")
    except:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Error in deleting exam ")
  
  
# Question SERVICE 🈂️❓🌟

def create_question_svc(user:Student,add_question:QuestionSchema,db:Session):
    try:
        if user.role == 'student':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You don't have access to this")
        new_question = Question(
            description = add_question.description,
            question = add_question.question,
            option_a = add_question.option_a,
            option_b = add_question.option_b,
            option_c = add_question.option_c,
            option_d = add_question.option_d,
            correct_answer = add_question.correct_answer
        )
        db.add(new_question)
        db.commit()
        return {"message": "question added successfully ✅"}
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Exam update failed")

def update_question_svc(user:Student,Q_id:int,new_data:str,db:Session):
    ques = get_question(Q_id,db)
    try:
      if user.role == 'student':
          raise HTTPException()
      update_Q = new_data.model_dump(exclude_unset = True)
      try:
        for key,value in update_Q.items():
            setattr(ques,key,value)
        db.commit()
        raise 
      except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Question update failed")
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Question update failed")
    
def delete_question_svc(user:Student,Q_id:int,db:Session):
    ques = get_question(Q_id,db)
    try:
        if user.role =="student":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You don't have access to this")
        if not ques:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid question id")
        db.delete(ques)
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Exam Deleted ✅")
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Error in deleting question")