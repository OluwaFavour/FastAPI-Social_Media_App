from passlib.context import CryptContext

# Password Hashing Settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database Settings
DB_HOST = 'localhost'
DB_NAME = 'fastapi'
DB_USER = 'postgres'
DB_PASSWORD = 'Fsticks810200'