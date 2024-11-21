from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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

@app.get("/posts")
def read_post():
    return {"data": my_posts}


@app.post("/posts")
def create(posts: Post):
    post_dict = posts.dict()
    post_dict['id'] = 3
    my_posts.append(post_dict)
    return {"message": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, ):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} not found")
    return{"post detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_by_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} is not available")
    my_posts.pop(index)
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