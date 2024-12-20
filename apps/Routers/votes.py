from fastapi import FastAPI, HTTPException, Depends, APIRouter, status, Response
from .. import schemas, models, outh2, database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=['votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.vote, db: Session = Depends(database.get_db),
current_user: int = Depends(outh2.get_current_user)):
    find_vote=db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not find_vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="post not found")


    vote_query=db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    vote_found = vote_query.first()

    if (vote.direction == 1):
       if vote_found:
          raise HTTPException(status_code=status.HTTP_409_CONFLICT,
          detail="You have already voted in this direction")
       new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
       db.add(new_vote)
       db.commit()
       return{"message": "vote created"}
    else:
         if vote_found:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "vote removed"}
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail="vote not found")
         
      
    