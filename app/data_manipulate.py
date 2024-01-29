### Note: Here We Implemented Method in Which We Directly Talk to the databse using SQL Statements. We can Do Same things using Object Relational Mapper.
### In ORM layer between FastAPI & SQL Database which is Intermediteries...
### Why ORM is Good?
## - Object-Oriented Paradigm:
## - Productivity: Instead of SQLnic to Pythonic
## - Code Readability and Maintainability:
## - Database Easily Portability:
## - Automatic Query Generation:
## - Security:  Prevent from SQL injection attacks
## - Query Language Abstraction:

# Example of ORM: SQLAlchemy

# Importing Necesary Packages and Modules:
from fastapi import FastAPI, Response, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time

app = FastAPI()

# Model: for Data Validation:
class Post(BaseModel):
    title: str
    content: str
    published: bool = True    
    rating: Optional[int] = None   

# I have table named posts in fastapi database which having columns names ID, Title, Content, Published, Created_at.
# from this columns ID, Created_at Columns data have been handled by database server side......

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

# While Loop Try to establish conenction after every two seconds of Database Connection Failed.
            
@app.get("/")  
def read_root():
    return {"Sucesss"}          

# Retreive the Posts:
@app.get("/posts")
def get_posts():
     cursor.execute("""SELECT * FROM posts""")
     posts = cursor.fetchall()
     print(posts)
     return {"This are the Posts": posts}


# Add The New Posts iN Database:
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    #  cursor.execute(f"""INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})""")  
    ## Using this type of method data sql injection chances high occured....
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()  # To save the Changes in Database...
    return {"Created Posts Data": new_post}
 

# To retreive Individula Posts:
@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    return_data = cursor.fetchone()

    if return_data is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    return {"Data": return_data}

# Delete Method:
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    del_data = cursor.fetchone()
    conn.commit() 
    if del_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F"Post with ID: {id} Not Found.")
    print(del_data)
    return {"Message": "post Successfully Deleted..."}  

# PUT method for updating a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, id))
    
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=404, detail=f"Post with ID: {id} not found so we can not update it.")
    return {"Message": "Post successfully updated", "UpdatedData": updated_post}


# Patch Method for Updating Post Content:
# Patch Method To Modify Content:
@app.patch("/posts/{id}")
def partial_update_post(id: int, updateddict: dict= Body(...)):
    set_clause = ", ".join(f"{field} = %s" for field, value in updateddict.items() if value is not None)

    if not set_clause:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    cursor.execute(f"UPDATE posts SET {set_clause} WHERE id = %s RETURNING *",
        list(updateddict.values()) + [id])
    updated_post = cursor.fetchone()

    if updated_post is None:
        raise HTTPException(status_code=404, detail=f"Post with ID: {id} not found")
    conn.commit()
    return {"Message": "Post successfully updated", "UpdatedData": updated_post}
