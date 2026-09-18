from datetime import UTC, datetime, timedelta

from jose import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.config import settings

# pwdlib context using Argon2
password_context = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    """Hash the plain-text password using Argon2."""
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if the provided plain-text password matches the hashed password."""
    return password_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create a JSON Web Token payload and encode it."""
    to_encode = data.copy()
    now_utc = datetime.now(UTC)
    expire = now_utc + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
