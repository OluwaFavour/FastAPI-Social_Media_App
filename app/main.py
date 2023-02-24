from fastapi import FastAPI

from app.config import settings
from app.routers import auth, post, user, vote

app = FastAPI()

print(settings.DB_HOST)

# Routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Home Page
@app.get("/")
async def root():
    return {"message": "Hello World!"}