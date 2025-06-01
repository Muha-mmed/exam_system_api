from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from authentication.models import Student
from authentication.schemas import UserSchema,CreateUser

hash_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def existing_user(email:str,db:Session):
    user = db.query(Student).filter(Student.email == email).first()
    return user

def hash_pwd(password):
    return hash_context.hash(password)

def verify_pwd(password:str,hash_pwd:str) -> bool:
    return hash_context.verify(password,hash_pwd)

def signUp(user: CreateUser,db:Session):
    if existing_user(user.email,db):
        return {"message": "user with email already exist"}
    try:
        newuser = Student(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        level = user.level,
        hash_password = hash_pwd(user.hash_password)
        )
        db.add(newuser)
        db.commit()
        return newuser
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error creating user")

def login(email: str, password: str, db: Session):
    user = existing_user(email, db)
    try:
        if not user or not verify_pwd(password, user.hash_password):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="email or password don't correct")
        return user
    except Exception as e:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))