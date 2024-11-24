from .. import models, utils, schemas
from typing import List
from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Post, PostCreate, Post_Response


router = APIRouter()


@router.get("/posts", response_model=List[Post_Response])
def read_post(db: Session = Depends(get_db)):
    #cursor.execute('SELECT * FROM posts')
    #post = cursor.fetchall() 
    #print(post)
    posts = db.query(models.Post).all()
    return posts


@router.post("/posts", response_model=schemas.PostCreate)
def create(posts: Post, db: Session = Depends(get_db)):
    #cursor.execute("INSERT INTO posts(title, content, published) VALUES(%s,%s,%s) RETURNING * ",
    #(posts.title, posts.content, posts.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/posts/{id}", response_model = Post_Response)
def get_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute('SELECT * FROM posts WHERE id = %s', (str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} not found")
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    #cursor.execute('DELETE FROM posts WHERE id = %s returning * ', (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} is not available")
    post.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}")
def update_post(id: int,post: Post, db: Session = Depends(get_db)):
    #index = find_by_index(id)
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} not found")
    updated_post.update(post.dict(), synchronize_session = False)
    db.commit()

    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    return{"message": updated_post.first()}