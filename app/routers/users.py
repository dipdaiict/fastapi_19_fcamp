from .. import models, schemas, utils
from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from .. database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['USERS']
)  # Here Tags Used for Group the Below Functionalitioes so during docs we can get the groups....   


@router.post("/createuser", status_code=status.HTTP_201_CREATED, response_model=schemas.NewUserResponse)
def createuser(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # HASH THE PASSWORD:
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Retreive this newly created post and store with in new_post variable...
    return new_user

@router.get("/users/{username}", response_model=schemas.UserOut)
def user_data(username: str, db: Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.username == username).first()
    if user_data is None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username: {username} not found.")
    return user_data
