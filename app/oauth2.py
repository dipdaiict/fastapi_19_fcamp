from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Three Piece of InformationRequire for Token Generation:
SECRET_KEY = settings.secret_key  # To Verify with backedn
ALGORITHM = settings.algorithm
EXPIRATION_TIME_OF_TOKEN = settings.expiration_time_of_token
# EXPIRATION_TIME_OF_TOKEN = 1    # For Testing Purpose One Minute


def create_token(data: dict()):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME_OF_TOKEN)
    to_encode.update({"exp": expire })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        user_email:str = payload.get("user_email")
        user_name:str = payload.get("user_name")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id = id, user_email=user_email, user_name=user_name)
    except JWTError:
        raise credentials_exception    
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could Not Validate Credentials", headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token, credentials_exception)
