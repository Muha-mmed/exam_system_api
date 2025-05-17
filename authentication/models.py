from sqlalchemy import Column,Integer,String,Boolean,DateTime,JSON,Enum as SQLEnum

from sqlalchemy.orm import relationship
from database import Base,engine
from utils.constant import Level, UserRole

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String,unique=True)
    level = Column(SQLEnum(Level),nullable=True)
    role = Column(SQLEnum(UserRole),default=UserRole.student,nullable=False)
    hash_password = Column(String)
    
    answers = relationship("StudentAnswer", back_populates="student")
    exam_attempts = relationship("ExamAttempt", back_populates="student")
    
    def __repr__(self):
        return f"<Student {self.first_name} {self.last_name}>"


Base.metadata.create_all(bind=engine)