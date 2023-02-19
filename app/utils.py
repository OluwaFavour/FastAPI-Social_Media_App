from app.settings import pwd_context


async def get_hashed_password(password):
    """Hashes a plain password based on the bcrypt algorithm in the password context

    Args:
        password (str): The password that you want to hash

    Returns:
        str: A hashed password
    """
    return pwd_context.hash(password)

async def verify_password(password, hashed_password):
    """Compares a plain password with an hashed password

    Args:
        password (str): The plain password to verify
        hashed_password (str): The hashed password to verify

    Returns:
        bool: Returns True if the hashed password is the hashed version of the plain password
    """
    return pwd_context.verify(password, hashed_password)
