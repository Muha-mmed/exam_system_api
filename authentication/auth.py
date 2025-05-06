from datetime import datetime,timedelta
from fastapi import Depends, HTTPException
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
import os 

oauthSchema = OAuth2PasswordBearer(tokenUrl="/token")

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "sub": str(data.get("sub"))  # Must include 'sub' in data
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def current_user(token: str = Depends(oauthSchema)):
    credentials_exception = HTTPException(
        status_code=401,
        detail= "Could not validate credentials",
        headers= {"WWW-Authenticate": "Bearer"}
    )
    try:
      payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
      email = payload.get({"sub": str })
      if not email:
          raise credentials_exception
    except JWTError:
      raise credentials_exception
    return email