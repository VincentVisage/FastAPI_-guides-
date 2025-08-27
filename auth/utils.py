from typing import Any
from datetime import timedelta, datetime, timezone


import jwt
import bcrypt

from core.config import settings


def encode_jwt(
        payload: dict[str, Any],
        private_key: str = settings.auth_jwt.private_token_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
    ):
    
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    
    if expire_timedelta:
        to_encode.update(
            exp= now + expire_timedelta
        )
    else:
        to_encode.update(
            exp= now + timedelta(minutes=expire_minutes)
        )
    to_encode.update(
        iat=now
    )

    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
        )  
    
    return encoded


def decode_jwt(
        jwt_token: str | bytes,
        public_key: str = settings.auth_jwt.public_token_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):  
    
    decoded = jwt.decode(
        jwt=jwt_token,
        key=public_key,
        algorithms=algorithm
    )

    return decoded


def hash_password(
        password: str
) -> bytes:   
    
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    hashed_password = bcrypt.hashpw(
        password=pwd_bytes,
        salt=salt
    )

    return hashed_password


def validate_password(
        user_input_password: str,
        hashed_password: bytes,
) -> bool:
    
    return bcrypt.checkpw(
        password=user_input_password.encode(), 
        hashed_password=hashed_password,
    )