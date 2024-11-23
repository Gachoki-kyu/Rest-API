from fastapi import FastAPI, Response, status, HTTPException ,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine,session_Local, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

try:
    conn = psycopg2.connect(host='localhost', database = "fastAPI", user = 'postgres',
    password ='bena313', cursor_factory = RealDictCursor)
    cursor = conn.cursor()
    print('Database was connected successiful')
except Exception as error:
    print('Failed to connect')
    print('error :', error)


my_posts = [{"title": "this is a title 1", "content": "this is content of post 1", "id": 1}, 
{"title":"favourite food", "content": "pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_by_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"Message": "welcome to my api"}

@app.get("/ben")
def test_post(db: session_Local = Depends(get_db)):
    return{"status": "success"}

@app.get("/posts")
def read_post():
    cursor.execute('SELECT * FROM posts')
    post = cursor.fetchall()
    print(post)
    return {"data": post}


@app.post("/posts")
def create(posts: Post):
    cursor.execute("INSERT INTO posts(title, content, published) VALUES(%s,%s,%s) RETURNING * ",
    (posts.title, posts.content, posts.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"message": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute('SELECT * FROM posts WHERE id = %s', (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} not found")
    return{"post detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('DELETE FROM posts WHERE id = %s returning * ', (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} is not available")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int,post: Post):
    index = find_by_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"message": post_dict}