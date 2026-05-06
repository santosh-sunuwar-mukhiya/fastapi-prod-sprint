from datetime import datetime, timedelta, timezone
from jose import jwt
from pwdlib import PasswordHash
from app.core.config import security_settings

pwd_hasher = PasswordHash.recommended()

# Hash password
def hash_password(password: str) -> str:
    return pwd_hasher.hash(password)

# Verify password
def verify_password(password: str, hashed: str) -> bool:
    return pwd_hasher.verify(password, hashed)

# Create JWT
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, key=security_settings.JWT_SECRET, algorithm=security_settings.JWT_ALGORITHM)

# Decode JWT
def decode_token(token: str):
    return jwt.decode(token, key=security_settings.JWT_SECRET, algorithms=[security_settings.JWT_ALGORITHM])