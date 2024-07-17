from fastapi import HTTPException
import jwt
from jwt import InvalidTokenError
from app.settings import settings
import bcrypt
from datetime import datetime, timedelta

def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.acces_token_expiration_minutes,
        expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()

    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    to_encode.update({"iat": now})

    

    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )
    return encoded

def create_token(token_type: str, payload: dict):
    token_payload = payload.copy()
    token_payload['token_type'] = token_type
    return token_payload


def decode_jwt(
        token,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):
    try:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm]
        )
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return decoded

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode(), salt)
    return hash_password

def validate_password(password: str, hash_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hash_password)

