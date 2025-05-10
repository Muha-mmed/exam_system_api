from fastapi import APIRouter,Depends
from database import get_db

from sqlalchemy.orm import Session
from authentication.auth import JWTBearer
from exam.services import create_exam_svc
from exam.schemas import ExamSchema
exam_routes = APIRouter(prefix="/exam",tags=["exam"])

@exam_routes.post("/create",status_code=201,dependencies=[Depends(JWTBearer())])
def create_exam(exam:ExamSchema,db:Session=Depends(get_db)):
    newExam = create_exam_svc(exam,db)
    return newExam