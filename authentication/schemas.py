from typing import Optional
from pydantic import BaseModel,EmailStr
from utils.constant import UserRole,Level


class UserSchema(BaseModel):
    first_name:str
    last_name: str
    email: EmailStr
    level: Optional[Level] = None
    role: UserRole

class CreateUser(BaseModel):
    first_name:str
    last_name: str
    email: EmailStr
    level: Optional[Level] = None
    password: str