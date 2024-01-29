from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from .. database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.params import Body
from typing import Optional, List
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.sql import func

router = APIRouter(
    tags=['POSTS'])


# router = APIRouter(
#     prefix="/posts"
# )   # If we can do this type so we can get clean routes... so we have to remove /posts from all the rotes it is directly captured by this router..

@router.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    # print(db.query(models.Post))  # To Know the Which Query Executed Behind The Statement...
    data = db.query(models.Post).all()   # Fetch all the data from Post Models
    return data

from fastapi.encoders import jsonable_encoder

# @router.get("/posts", response_model= List[schemas.PostResponse22])  
@router.get("/posts", response_model=List[schemas.FormattedPostSchema])  
def get_posts_(db: Session = Depends(get_db), limit:int=10, skip:int = 0, search: Optional[str]= ""):   # Here I will add the Limit Parameter which fetch the 10 Posts by default In Postman I query Like this {{URL}}posts?limit=<No of Post I want>
     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()   # Also We added Skip Parameter which by default skip the certain no of posts and return next decided posts  # {{URL}}posts?limit=4&skip=1
     results = db.query(models.Post, func.count(models.Votes.post_id).label("votes_count")).join(models.Votes, 
                     models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
     formatted_results = [{"post": {"id": post.id, "title": post.title, "content": post.content, "created_at": post.created_at},"votes_count": votes_count}
                            for post, votes_count in results]
     return formatted_results 


# Added Another Search Params: {{URL}}posts?limit=4&skip=0&search=Post  # Here Post is Keyword in title....
# Added Another Params: {{URL}}posts?limit=4&skip=0&search=Title%20No.  # Here %20 Means Space...

@router.post("/posts", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(posts: schemas.Post, db: Session = Depends(get_db),
                 current_user = Depends(oauth2.get_current_user)):  
    print(current_user)
    if posts.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform This Operation.")
    new_post = models.Post(user_id = posts.user_id, title = posts.title, content=posts.content, published=posts.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Retreive this newly created post and store with in new_post variable...
    return new_post

@router.post("/posts_method2", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(posts: schemas.Post, db: Session = Depends(get_db)):  
    new_post = models.Post(**posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Retreive this newly created post and store with in new_post variable...
    return new_post


# Here id is Path Parameters
@router.get("/posts/{id}", response_model=schemas.PostResponse2)
def get_posts(id: int, response: Response, db: Session = Depends(get_db),
               user_id: int = Depends(oauth2.get_current_user)):   # Here we manuplating the response code if data not found then instead of 200 Ok then 404 NOT Found..
    post_info = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} was Not Found....")   #This Method with built in exception.... I have al so not to use response when i use this method 
    return post_info

# Deleter Method:
# @router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db),
#                  user_id: int = Depends(oauth2.get_current_user)):
#     post_to_delete = db.query(models.Post).filter(models.Post.id == id).one_or_none()  # one_or_none() make it clear that at most one post is expected with the given ID.
#     if post_to_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} not found.")
#     if post_to_delete.user_id != user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform This Operations.")
#     db.delete(post_to_delete)
#     db.commit()
#     # return {"message": "Post successfully deleted."}    # By default status code is 204 Execute so No Content return but we want to return somr message then we have to use json repsone
#     return JSONResponse(content={"message": "Post successfully deleted."})


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user = Depends(oauth2.get_current_user)):
    print(current_user)
    post_to_delete = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} not found.")
    
    if post_to_delete.user_id != current_user.user_id:
        print(f"User {current_user.user_id} is not authorized to delete post ID:{id} owned by {post_to_delete.user_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform This Operation.")
    
    print(f"User {current_user.user_id} is authorized to delete post Post ID:{id}")
    
    # Delete the post
    db.delete(post_to_delete)
    db.commit()
    
    return JSONResponse(content={"message": "Post successfully deleted."})


# Update The Post by ID:
@router.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.Post,  db: Session = Depends(get_db),
                 current_user = Depends(oauth2.get_current_user)):
    post= db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post.first()
    updated_post_id = updated_post.dict()['user_id']
    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F"Post with ID: {id} Not Found.")
    if post_to_update.user_id != current_user.user_id:
        print(f"User {current_user.user_id} is not authorized to delete post ID:{id} owned by {post_to_update.user_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform This Operation.")
    if current_user.user_id != updated_post_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform This Operation. You can not change the user id.")
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post.first()


from fastapi.encoders import jsonable_encoder