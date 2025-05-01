from sqlalchemy import Column,Integer,String,Boolean,DateTime,JSON,Enum as SQLEnum


from database import Base,engine
from utils.constant import UserRole

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    level = Column(String,nullable=True)
    role = Column(SQLEnum(UserRole),default=UserRole.student,nullable=False)
    hash_password = Column(String)

Base.metadata.create_all(bind=engine)