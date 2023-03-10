from datetime import datetime

from pydantic import BaseModel, EmailStr, conint, validator


class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
class Post(PostModel):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

class PostOut(Post):
    votes: int
    
class UserModel(BaseModel):
    email: EmailStr
    password1: str
    password2: str
    
    @validator('password2')
    def passwords_match(cls, password, values, **kwargs):
        # The validator takes in values[password2] as 'password' and checks it against values[password1]
        if "password1" in values and password != values["password1"]:
            raise ValueError("Passwords do not match, try again")
        return password


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class VoteModel(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)