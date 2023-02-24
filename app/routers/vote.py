from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.database import DictRow, conn, cur
from app.oauth2 import get_current_user
from app.schemas import VoteModel

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: VoteModel, current_user: DictRow = Depends(get_current_user)):
    # Check if the post exists
    post_query = cur.execute(
        """
        SELECT * FROM posts WHERE id = %s;
        """, (vote.post_id,)
    ).fetchone()
    if post_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} was not found")
    
    # Get the vote from the database
    vote_query = cur.execute(
        """
        SELECT * FROM votes WHERE post_id = %s AND user_id = %s;
        """, (vote.post_id, current_user['id'])
    ).fetchone()
    if (vote.dir == 1):
        # Check if the user has voted on this post
        if vote_query is None:
            # Add the vote to the database if the user has not voted on this post
            cur.execute(
                """
                INSERT INTO votes (post_id, user_id) VALUES (%s, %s);
                """, (vote.post_id, current_user['id'])
            )
            # Save changes to the database
            conn.commit()

            return {"message": "Vote added"}

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User has already voted on this post")
    else:
        # Check if the user has voted on this post
        if vote_query is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"User has not voted on this post")
        # Delete the vote if the user has voted on this post
        cur.execute(
            """
            DELETE FROM votes WHERE post_id = %s AND user_id = %s;
            """, (vote.post_id, current_user['id'])
        )
        # Save changes to the database
        conn.commit()
        
        return {"message": "Vote deleted"}