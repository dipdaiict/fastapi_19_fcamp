from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/vote", tags=['VOTE'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db),
         current_user = Depends(oauth2.get_current_user)):
    existing_vote = db.query(models.Post).filter_by(id=vote.post_id).first()

    if existing_vote:
        if vote.dir == 1:
            if db.query(models.Votes).filter_by(post_id=vote.post_id, user_id=current_user.user_id).first():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User ID {current_user.user_id} Has Already Voted on This Post. Ref. Post ID {vote.post_id}.")
            new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.user_id)
            db.add(new_vote)
            db.commit()
            return {"message": "Successfully Added Vote."}
        else:
            existing_vote_query = db.query(models.Votes).filter_by(post_id=vote.post_id, user_id=current_user.user_id)
            existing_vote = existing_vote_query.first()

            if not existing_vote:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Particular Vote Does Not Exist."
                )

            existing_vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Successfully Deleted Vote."}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Particular Post Not Found.")
