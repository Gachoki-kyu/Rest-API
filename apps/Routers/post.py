from .. import models, utils, schemas, outh2
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, APIRouter, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Post, PostCreate, Post_Response


router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("/", response_model=List[Post_Response])
def read_post(db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str]=""):
    #cursor.execute('SELECT * FROM posts')
    #post = cursor.fetchall() 
    #print(post)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", response_model=schemas.PostCreate)
def create(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    #cursor.execute("INSERT INTO posts(title, content, published) VALUES(%s,%s,%s) RETURNING * ",
    #(posts.title, posts.content, posts.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    
    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model = Post_Response)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    #cursor.execute('SELECT * FROM posts WHERE id = %s', (str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="not authorized  to perform requested action")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):

    #cursor.execute('DELETE FROM posts WHERE id = %s returning * ', (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} is not available")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="not authorized  to perform requested action")

    post_query.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int,post: Post, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    #index = find_by_index(id)
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post1 = updated_post.first()

    if post1 == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} not found")

    if post1.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="not authorized  to perform requested action")

    updated_post.update(post.dict(), synchronize_session = False)
    db.commit()

    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    return{"message": updated_post.first()}