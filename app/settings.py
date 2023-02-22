from passlib.context import CryptContext

from app.config import settings

# Password Hashing Settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database Settings
DB_HOST = settings.DB_HOST
DB_NAME = settings.DB_NAME
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD