from fastapi import FastAPI, Response, status, HTTPException ,Depends, APIRouter
from .. import database, models, schemas, utils, outh2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter( tags = ['Authentication'])

@router.post("/login")
def login(sign_in: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == sign_in.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
         detail = 'Incorrect email or password')
    if not utils.verify(sign_in.password, user.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
         detail = 'Incorrect email or password')

    create_token = outh2.create_access_token({'user_id': user.id})
    return {'access token':create_token , "token type": 'bearer'}

