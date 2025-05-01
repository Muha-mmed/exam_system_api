from fastapi import APIRouter,Depends,HTTPException

from sqlalchemy.orm import Session

from authentication.schemas import UserSchema
from database import get_db
from authentication.services import signUp
auth = APIRouter()

@auth.post("/signup")
def create_user(user: UserSchema, db:Session= Depends(get_db)):
    new_user = signUp(user,db)
    if not new_user:
        raise HTTPException(status_code=401,detail="invalid input")
    return new_user