from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime,Integer,String,ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from database import Base,engine

from utils.constant import AnswerOption

class Exam(Base):
    __tablename__ = 'exams'
    id = Column(Integer,primary_key=True)
    title = Column(String,max_length=200)
    subject = Column(String,max_length=100)
    class_level = Column(String, max_length=50)
    term = Column(String,max_length=50)
    duration = Column(Integer,help_text="Duration in minutes")
    is_published = Column(Boolean,default=False)
    
    questions = relationship("Question",back_populates='exam')
    exam_attempts = relationship("ExamAttempt",back_populates='exam')

    
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer,primary_key=True)
    description = Column(String,nullable=True)
    question = Column(String,nullable=False)
    option_a = Column(String,nullable=False)
    option_b = Column(String,nullable=False)
    option_c = Column(String,nullable=False)
    option_d = Column(String,nullable=False)
    correct_answer = Column(SQLEnum(AnswerOption),nullable=False)
    exam_id = Column(Integer,ForeignKey("exams.id"))
    
    exam = relationship(Exam,back_populates='questions')
    answers = relationship("StudentAnswer",back_populates='question')

class StudentAnswer(Base):
    id = Column(Integer,primary_key=True)
    selected_option = Column(String,nullable=False)
    is_correct = Column(Boolean)
    question_id = Column(Integer, ForeignKey("questions.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    
    student = relationship("Student",back_populates="answers")
    question = relationship(Question,back_populates='answers')

class ExamAttempt(Base):
    id = Column(Integer,primary_key=True)
    score = Column(Integer)
    time_taken = Column(Integer)  # in minutes or seconds?
    date = Column(DateTime, default=datetime.utcnow)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    student_id = Column(Integer, ForeignKey("students.id"))

    
    exam = relationship(Exam,back_populates='exam_attempts')
    student = relationship("Student",back_populates='exam_attempts')
    
Base.metadata.create_all(bind=engine)