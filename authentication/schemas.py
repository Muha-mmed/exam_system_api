from typing import Optional
from pydantic import BaseModel,EmailStr
from database import Base,engine
from utils.constant import UserRole


class UserSchema(BaseModel):
    first_name:str
    last_name: str
    email: EmailStr
    level: Optional[str] = None
    role: UserRole