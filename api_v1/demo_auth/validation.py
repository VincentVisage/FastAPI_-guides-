
from fastapi.security import  OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError

from .helpers import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from users.schemas import UserSchema
from .crud import users_db
from auth import utils as auth_utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/demo-auth/jwt/login/")




def get_current_token_payload(
        # credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
    
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            jwt_token=token
        )
    except InvalidTokenError:
        raise InvalidTokenError
    return payload


def validate_token_type(
        token_type: str,
        payload: dict,
) -> bool:
    current_token_type = payload.get("type")
    if current_token_type == token_type:
        return True
    else: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type {current_token_type!r} expected {token_type!r}"
        )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid(user not found)",
    )


def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(
            payload: dict = Depends(get_current_token_payload)
    ) -> UserSchema:
        validate_token_type(token_type=token_type, payload=payload)
        return get_user_by_token_sub(payload)
    return get_auth_user_from_token


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(self, payload: dict = Depends(get_current_token_payload)):
        token_type = validate_token_type(token_type=self.token_type, payload=payload)
        return get_user_by_token_sub(payload)

# get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refersh = UserGetterFromToken(REFRESH_TOKEN_TYPE)
