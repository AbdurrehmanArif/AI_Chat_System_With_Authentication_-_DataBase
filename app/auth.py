# app/auth.py
import hashlib
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Max bcrypt input bytes (not needed for SHA256 pre-hash, but kept for reference)
MAX_BCRYPT_BYTES = 72

def hash_password(password: str) -> str:
    """
    Hash a plain password using SHA-256 + bcrypt.
    """
    # SHA256 raw bytes (32 bytes)
    sha256_pw = hashlib.sha256(password.encode("utf-8")).digest()
    # Hash with bcrypt
    return pwd_context.hash(sha256_pw)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the hashed password.
    """
    sha256_pw = hashlib.sha256(plain_password.encode("utf-8")).digest()
    return pwd_context.verify(sha256_pw, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt