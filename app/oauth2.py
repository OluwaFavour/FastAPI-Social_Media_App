from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.database import conn, cur
from app.schemas import TokenData

oauth2_scheme  = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "2ae2fab5a0e0447e3f8da65c3ab923750a8fa568cd53b7212ccd731fec886674"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

async def get_access_token(data: dict):
    to_encode = data.copy() # Copy data/payload to a new variable
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)    # Set Expiry date
    to_encode.update({'exp' : expire})    # Add expiry date to new backup data
    
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)    # Encode the new data
    
    return encoded_jwt

async def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        
        id: str = str(payload.get("user_id"))
        
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get User
    token_data = await verify_access_token(token, credentials_exception=credentials_exception)
    
    user = cur.execute(
        """
        SELECT * FROM users WHERE id = %s;
        """, (token_data.id,)
    ).fetchone()
    
    return user