from datetime import datetime, timedelta, timezone
from jose import jwt
from uuid import uuid4
from pwdlib import PasswordHash
from app.core.config import security_settings

pwd_hasher = PasswordHash.recommended()

# Hash password
def hash_password(password: str) -> str:
    return pwd_hasher.hash(password)

# Verify password
def verify_password(password: str, hashed: str) -> bool:
    return pwd_hasher.verify(password, hashed)

# Create Access Token (short-lived: 30 minutes)
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=security_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "jti": str(uuid4()), "type": "access"})
    return jwt.encode(to_encode, key=security_settings.JWT_SECRET, algorithm=security_settings.JWT_ALGORITHM)

# Create Refresh Token (long-lived: 7 days)
def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=security_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "jti": str(uuid4()), "type": "refresh"})
    return jwt.encode(to_encode, key=security_settings.JWT_REFRESH_SECRET, algorithm=security_settings.JWT_ALGORITHM)

# Decode JWT
def decode_token(token: str, token_type: str = "access") -> dict:
    key = security_settings.JWT_SECRET if token_type == "access" else security_settings.JWT_REFRESH_SECRET
    return jwt.decode(token, key=key, algorithms=[security_settings.JWT_ALGORITHM])