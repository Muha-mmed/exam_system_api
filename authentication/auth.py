from datetime import datetime,timedelta
from fastapi import Depends, HTTPException, Request
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
import os
from sqlalchemy.orm import Session
from authentication.models import Student
from database import get_db 

oauthSchema = OAuth2PasswordBearer(tokenUrl="/token")

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=30))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "sub": str(data.get("sub"))  # Must include 'sub' in data
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def current_user(db:Session = Depends(get_db),token: str = Depends(oauthSchema)) -> Student:
    credentials_exception = HTTPException(
        status_code=401,
        detail= "Could not validate credentials",
        headers= {"WWW-Authenticate": "Bearer"}
    )
    try:
      payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
      email = payload.get("sub")
      if not email:
          raise credentials_exception
      user = db.query(Student).filter(Student.email == email).first()
      if not user:
          raise credentials_exception
      return user
    except JWTError:
      raise credentials_exception

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error:bool = True):
        super(JWTBearer,self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer,self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=402,detail="Invalid authentication scheme.") 
            if not self.verify_token(credentials.credentials):
                raise HTTPException(status_code=403,detail="invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
    def verify_token(self,token:str):
        try:
          jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
          return True
        except JWTError:
          return False