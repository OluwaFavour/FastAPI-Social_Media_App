from fastapi import APIRouter, HTTPException, status

from app.database import conn, cur
from app.schemas import UserModel, UserOut
from app.utils import get_hashed_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# GET
@router.get("/{id}", response_model=UserOut)
async def get_user(id: int):
    user = cur.execute(
    """SELECT * FROM users where id = %s;
    """, (id,)
    ).fetchone()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exit")
    
    return user


# POST
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(request: UserModel):
    # Check if user exists before using email
    user = cur.execute(
        """
        SELECT email FROM users WHERE email = %s
        """, (request.email,)
    ).fetchone()
    
    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email has been taken already")
    else:
        hashed_password = await get_hashed_password(request.password2)
        user = cur.execute(
        """
        INSERT INTO users (email, password)
        VALUES (%s, %s) RETURNING *;
        """, (request.email, hashed_password)
        ).fetchone()
        
        # Save/commit changes
        conn.commit()
        return user