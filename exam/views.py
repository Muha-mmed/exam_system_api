from fastapi import APIRouter,Depends, Form, HTTPException,status
from authentication.models import Student
from database import get_db

from sqlalchemy.orm import Session
from authentication.auth import JWTBearer, current_user
from exam.services import create_exam_svc, create_question_svc, delete_exam_svc, delete_question_svc, update_exam_svc, update_question_svc
from exam.schemas import ExamSchema,CreateExamSchema, QuestionSchema,UpdateExamSchema, UpdateQuestionSchema
from utils.constant import Level

from database import Base,engine

Base.metadata.create_all(bind=engine)

exam_routes = APIRouter(prefix="/exam",tags=["exam"])


@exam_routes.post("/create",status_code=201,dependencies=[Depends(JWTBearer())])
def create_exam(title: str = Form(...),
    subject: str = Form(...),
    class_level: Level = Form(...),
    term: str= Form(...),
    duration: int = Form(...),
    is_published :bool = Form(False),
    db:Session=Depends(get_db)):
    
    exam = CreateExamSchema(title = title, subject = subject,class_level = class_level,term = term,duration= duration,is_published= is_published)
    newExam = create_exam_svc(exam,db)
    return newExam

@exam_routes.patch('/update/exam',dependencies=[Depends(JWTBearer())])
def update_exam(
    title: str = Form(...),
    subject: str = Form(...),
    class_level: Level = Form(...),
    term: str= Form(...),
    duration: int = Form(...),
    is_published :bool = Form(False),
    user:Student= Depends(current_user),
    exam_id:int = Form(...),
    db:Session=Depends(get_db)
    ):
    new_data = UpdateExamSchema(title = title,subject=subject,class_level=class_level,term=term,duration=duration,is_published=is_published)
    exam = update_exam_svc(user,exam_id,new_data,db)
    
    return exam

@exam_routes.delete("/delete/exam",dependencies=[Depends(JWTBearer())])
def delete_exam(
    user:Student = Depends(current_user),
    exam_id:int = Form(...),
    db:Session = Depends(get_db)
):
    exam = delete_exam_svc(user,exam_id,db)
    return exam

# question route
@exam_routes.post('/create/question',dependencies=[Depends(JWTBearer())])
def create_question(question:QuestionSchema,user:Student=Depends(current_user),db:Session=Depends(get_db)):
    ques = create_question_svc(user,question,db)
    return ques

@exam_routes.post('/update/question',dependencies=[Depends(JWTBearer())])
def create_question(question:UpdateQuestionSchema,Q_id: int,user:Student=Depends(current_user),db:Session=Depends(get_db)):
    ques = update_question_svc(user,Q_id,question,db)
    return ques

@exam_routes.delete("/delete/question")
def delete_question(Q_id:int,user:Student=Depends(current_user),db:Session=Depends(get_db)):
    question = delete_question_svc(user,Q_id,db)
    return question