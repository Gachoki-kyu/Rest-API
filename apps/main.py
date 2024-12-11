from fastapi import FastAPI, Response, status, HTTPException ,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from .Routers import post,user, auth
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .schemas import Post, Post_Response, PostCreate
from .database import engine,session_Local, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Message": "welcome to my api"}