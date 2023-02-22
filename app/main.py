from fastapi import FastAPI
from app.routers import post, user, auth
from app.config import settings

app = FastAPI()

print(settings.DB_HOST)

# Routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# Home Page
@app.get("/")
async def root():
    return {"message": "Hello World!"}