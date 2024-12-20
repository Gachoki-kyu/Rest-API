from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
   

class PostCreate(Post):
    pass

class userout(BaseModel):
    id: int
    email: EmailStr
    class config:
        orm_mode = True

class Post_Response(Post):
    id: int
    created_at: datetime
    user_id: int
    owner: userout


    class config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password: str
    


class Login(BaseModel):
    email : EmailStr
    password: str

class token1(BaseModel):
    access_token: str
    token_type: str

class tokendata(BaseModel):
    id: Optional[int] = None
