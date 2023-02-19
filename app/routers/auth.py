from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.database import cur
from app.oauth2 import get_access_token
from app.schemas import Token
from app.utils import verify_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=Token,status_code=status.HTTP_202_ACCEPTED)
async def login(credentials: OAuth2PasswordRequestForm=Depends()):
    user = cur.execute(
    """
    SELECT * FROM users WHERE email = %s
    """, (credentials.username,)
    ).fetchone()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not await verify_password(credentials.password, user.get("password")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Create a Token
    # Return Token
    access_token = await get_access_token(data={"user_id": user.get('id')})
    
    return {"access_token": access_token, "token_type": "bearer"}