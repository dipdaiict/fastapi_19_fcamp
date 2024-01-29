# Importing Necesary Packages and Modules:
from fastapi import FastAPI, Response, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time

# Creating FastAPI Instance:
app = FastAPI()

# Model:
class Post(BaseModel):
    title: str
    content: str
    published: bool = True    # It is based on user depend if user provide then it written otherwise by default it takes true
    rating: Optional[int] = None   # Here this is if user provide data then it will take the data and store it otherwise it will not store


# Database Connection:
while True:
        try: 
            conn = psycopg2.connect(host='localhost', database='fastapi',
                                    user='postgres', password='postgres',
                                    cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("Database Conenction Sucesfull..")
            break
        except Exception as e:
            print("Database Connection Failed...")
            print("Error: ", e)     
            time.sleep(2)   # Retry after every two seconds

# Root endpoint:   [Also Knwon as Path Operation / Route]
@app.get("/")    # [ Known as Decorator for Magical Operation like works as APIS.... [GET is Mehotd & '/' is Path]]
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts_():
     cursor.execute("""SELECT * FROM posts""")
     posts = cursor.fetchall()
     print(posts)
     return {"Data": posts}


@app.post("/createposts")
def create_posts(payload: dict = Body(...)):   # Here it extract all the inputs in body and create dict and store it on the payload variable (Validation).
    print(payload)
    return {"new post": f"title: {payload['title']} and content is {payload['content']}"}

## So Here New Concern is User Provide Valid Type of Data or Not. So Therefor we need Schema So for that we have ti use external library schema validation...
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True    # It is based on user depend if user provide then it written otherwise by default it takes true
    rating: Optional[int] = None   # Here this is if user provide data then it will take the data and store it otherwise it will not store

@app.post("/createposts2", status_code= status.HTTP_201_CREATED)  # Here We Manipulate Status Code because Instead of 200 ok We Use 201 Created...
def create_posts(payload: Post):  # from accessing valeus from pydantic model we have to use payload.title and payload.content instead we can do that payload.dict()
    print(f"{payload.title}: {payload.content}")
    print(f"{payload.published}")
    print(f"{payload.rating}")
    print(payload.dict())
    return {"new post": f"title: {payload.title} and content is {payload.content}"} 

# To Handle Predineed Values for that we have to create Enum Class:
from enum import Enum

class Place(str, Enum):  # Sublcalss That Inherant from Str and Enum Class
     amd = "Ahmedabad"
     brd = "Baroda"
     srt = "Surat"

@app.get("/place/{place_name}")
def get_place(place_name: Place):
    if place_name == Place.amd:
        return {"Place": Place.amd}
    if place_name == Place.brd:
        return {"Place": Place.brd}   
    return {"Place": Place.srt}


val = [{'id': 1,
    "title": "First Post",
    "content": "This is the content of the first post.",
    "published": True,
    "rating": 4},
    {'id': 2,
    "title": "Second Post",
    "content": "This is the content of the second post.",
    "published": False,
    "rating": None},
    {'id': 3,
     'title': 'Third Post',
     'content': 'This is the content of the third post.',
     'published': True,
     'rating': 5},

    {'id': 4,
     'title': 'Fourth Post',
     'content': 'This is the content of the fourth post.',
     'published': False,
     'rating': 2},

    {'id': 5,
     'title': 'Fifth Post',
     'content': 'This is the content of the fifth post.',
     'published': True,
     'rating': 8}
]

@app.get("/posts")
def get_posts():
    return {"Data": val}

# Handling Path as Parameters:
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return {"file_content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File Not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Reading file: {str(e)}") 
    

@app.post("/posts")
def get_posts(post: Post):
    print(post)
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000)
    print(val.append(post_dict))
    return {"Data": post_dict}

def find_post_by_id(id):
    for post in val:
        if post["id"] == id:
            return post

# Here id is Path Parameters
@app.get("/posts/{id}")
def get_posts(id: int, response: Response):   # Here we manuplating the response code if data not found then instead of 200 Ok then 404 NOT Found..
    post_info = find_post_by_id(id)
    if not post_info:
        # response.status_code = 404  # tHis is also hardcoded value  method # if Not found id with data then set reposne code (status code) as 404 Not Found instead of 200 OK with null data
        # response.status_code = status.HTTP_404_NOT_FOUND  # This iswithout hardcoded Method
        # return {'Message': f"Post with id: {id} was Not Found...."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} was Not Found....")   #This Method with built in exception.... I have al so not to use response when i use this method 
    return {"Data": post_info}

# Clean Code:
@app.get("/posts/{id}")
def get_posts(id: int):
    post_info = find_post_by_id(id)
    if not post_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} was Not Found....")   #This Method with built in exception.... I have al so not to use response when i use this method 
    return {"Data": post_info}


# Handling Path as Parameters:
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return {"file_content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File Not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Reading file: {str(e)}") 

def find_index_post(id):
    for  i, post in enumerate(val):
        if post['id'] == id:
            return i

# Delete Method:
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F"Post with ID: {id} Not Found.")
    val.pop(index)
    return {"Message": "post Successfully Deleted..."}  # We Set the Status Code 204 So This Status is Nt Return after Post Delete...

# Update Method:
# Update a post by ID
@app.put("/posts/{id}", response_model=Post)
def update_post(id: int, updated_post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F"Post with ID: {id} Not Found.")
    
    current_post = val[index]
    updated_data = updated_post.dict(exclude_unset=True)

    for key, value in updated_data.items():
        current_post[key] = value

    # Alternate:
    # current_post.update(updated_data)
    # return {"Message": "Resource Sucessfully Updated....", "Updated Data": updated_post}
    # Return the updated post using the Post model
    return Post(**current_post)    
