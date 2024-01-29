from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    user_id: int   


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime


class PostResponse(BaseModel):
    title: str
    content: str
    published: bool
    user_id: int   
    user: UserOut
    class Config:
        from_attributes = True

# Here we can do so many stuffs like we can extend our base class or copy attributes from another class and add extras attributes in class... so and Sooo
    
class PostResponse2(PostResponse):  # Return title, content, published, created_at
    created_at: datetime
    user_id: int
    res_user: UserOut

    class Config:
        from_attributes = True
# This is Implemented in Method of Specif Id output:
    
class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str

class NewUserResponse(BaseModel):
    email: EmailStr
    username: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schemas for Toke:
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel): 
    user_id: Optional[int] = None
    user_name: str
    user_email: str

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class PostResponse22(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime  # Adjust the type based on the actual type in your model
    user_id: int
    votes_count: Optional[int]  # Include the count of votes

    class Config:
        from_attributes = True    

class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

class FormattedPostSchema(BaseModel):
    post: PostSchema
    votes_count: int        