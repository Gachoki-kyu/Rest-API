from pydantic import BaseModel, EmailStr
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    pass

class Post_Response(Post):
    id: int
    
    created_at: datetime

    class config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password: str
    
class userout(BaseModel):
    id: int
    email: EmailStr
    class config:
        orm_mode = True
