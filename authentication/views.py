from fastapi import APIRouter,Depends,HTTPException

from sqlalchemy.orm import Session

from authentication.auth import create_access_token
from authentication.schemas import UserSchema,CreateUser
from database import get_db
from authentication.services import signUp,login
auth = APIRouter()

db_dependency: Session= Depends(get_db)

@auth.post("/signup")
def create_user(user: CreateUser, db:Session= db_dependency):
    new_user = signUp(user,db)
    if not new_user:
        raise HTTPException(status_code=401,detail="invalid input")
    token = create_access_token({"sub": user.email})
    return {"access_token": token}

@auth.post("/login")
def login_user(email: str,password:str, db:Session= db_dependency):
    user = login(email,password,db)
    if user["message"] == "email or password don't correct":
        raise HTTPException(status_code=401,detail="invalid input")
    token = create_access_token({"sub": email})
    return {"access_token": token}