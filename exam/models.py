from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime,Integer,String,ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from database import Base

from utils.constant import AnswerOption,Level

class Exam(Base):
    __tablename__ = 'exams'
    id = Column(Integer,primary_key=True)
    title = Column(String(200))
    subject = Column(String(100))
    class_level = Column(SQLEnum(Level))
    term = Column(String(50))
    duration = Column(Integer,comment="Duration in minutes")
    is_published = Column(Boolean,default=False,nullable=False)
    
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
    __tablename__ = "student_answers"
    id = Column(Integer,primary_key=True)
    selected_option = Column(String,nullable=False)
    is_correct = Column(Boolean,default= False,nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    
    student = relationship("Student",back_populates="answers")
    question = relationship(Question,back_populates='answers')

class ExamAttempt(Base):
    __tablename__ = "exam_attempts"
    id = Column(Integer,primary_key=True)
    score = Column(Integer)
    time_taken = Column(Integer,comment="Time taken in minutes")  # in minutes or seconds?
    date = Column(DateTime, default=datetime.utcnow())
    exam_id = Column(Integer, ForeignKey("exams.id"))
    student_id = Column(Integer, ForeignKey("students.id"))

    
    exam = relationship(Exam,back_populates='exam_attempts')
    student = relationship("Student",back_populates='exam_attempts')