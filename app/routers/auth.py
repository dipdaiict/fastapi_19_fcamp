from fastapi import APIRouter, status, HTTPException, Depends
from .. database import engine, get_db
from sqlalchemy.orm import Session
from ..schemas import UserLogin, Token
from .. import database, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=['AUTHENTICATION'])

@router.post('/login')
def login(login_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login_credentials.email).first()
    if not user:
         raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials...")
    if not utils.verify(login_credentials.password, user.password):
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials...")
    
    # Return Token:
    token = oauth2.create_token(data = {"user_id": user.username})  # We Just Ony Provide User Name
    return {"access_token": token, "token_type": "Bearer"}


@router.post('/login_form', response_model = Token)
def login(login_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Request Form Having Two Params: 
    # username which takes email id or user name what ever u provide 
    # password
    # ex: {"username": "bchbchcbdhc", "password": "jecjehce"}
    user = db.query(models.User).filter(models.User.email == login_credentials.username).first()
    if not user:
         raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials...")
    if not utils.verify(login_credentials.password, user.password):
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials...")
    
    # Return Token:
    token = oauth2.create_token(data = {"user_name": user.username, "user_id": user.id, "user_email": user.email})  # We Just Ony Provide User Name
    return {"access_token": token, "token_type": "Bearer"}
    
