from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter()


@router.post("/users", response_model = schemas.userout)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #cursor.execute('INSERT INTO users(email, password) VALUES(%s,%s) RETURNING * ', (user.email, user.password))
    #new_user = cursor.fetchone()
    #conn.commit()
    hashed = utils.Hash(user.password)
    user.password = hashed

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.put("/users/{id}", response_model=schemas.userout)
def get_user(id: int, db: Session=Depends(get_db)):
    get_him = db.query(models.User).filter(models.User.id == id).first()
    if get_him == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{id} not found")
    return get_him
