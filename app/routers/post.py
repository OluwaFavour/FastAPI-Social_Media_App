from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.database import conn, cur, DictRow
from app.oauth2 import get_current_user
from app.schemas import Post, PostModel

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# GET
@router.get("/", response_model=List[Post])
async def get_posts():
    posts = cur.execute(""" SELECT * FROM posts """).fetchall()
    return posts

@router.get("/{id}")
async def get_post(id: int):
    post = cur.execute("""
                       SELECT * FROM posts WHERE id = %s;
                       """, (id,)).fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found"
                            )
    else:
        return post
    

# POST
@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_posts(request: PostModel, current_user: DictRow=Depends(get_current_user)):
    # Make Query
    current_user_id = current_user.get("id")
    new_post = cur.execute("""
                   INSERT INTO posts (title, content, published, owner_id)
                   VALUES (%s, %s, %s, %s) RETURNING *;
                   """,
                   (request.title, request.content, request.published, current_user_id)).fetchone()
    
    # Commit/Save Changes
    conn.commit()
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, current_user: DictRow=Depends(get_current_user)):
    current_user_id = current_user
    # Make Query
    post = cur.execute("""
                SELECT * FROM posts WHERE id = %s;
                """, (id,)).fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found"
                            )
    
    if post.get("owner_id") != current_user_id: # Delete Post if current logged in user is owner
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized")    
    
    cur.execute("""
                DELETE FROM posts WHERE id = %s;
                """, (id,))
    # Save changes
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=Post, status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: int, request: PostModel, current_user: DictRow=Depends(get_current_user)):
    current_user_id = current_user
    # Make Query
    post = cur.execute("""
                SELECT * FROM posts WHERE id = %s;
                """, (id,)).fetchone()
    
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with if: {id} was not found")
        
    if post.get("owner_id") != current_user_id: # Update Post if current logged in user is owner
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized")
    
    updated_post = cur.execute("""
                            UPDATE posts SET title = %s, content = %s, published = %s
                            WHERE id = %s RETURNING *;
                            """, (request.title, request.content, request.published, id)).fetchone()
    # Save CHanges
    conn.commit()
    return updated_post