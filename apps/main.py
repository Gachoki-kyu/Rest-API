from fastapi import FastAPI
from .Routers import post,user, auth, votes
from . import models
from .database import engine
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def read_root():
    return {"Message": "welcome to my api.....mbwa wewe najua unajiuliza ni nini inaendelea hapa"}