from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from pydantic import BaseModel
from jwt import InvalidTokenError

from auth import utils as auth_utils
from users.schemas import UserSchema
from core.models.base import Base
from auth.utils import hash_password
from core.models.user import User
from .helpers import create_access_token, create_refresh_token, TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from .validation import get_current_auth_user, get_current_auth_user_for_refersh

from .crud import users_db
http_bearer = HTTPBearer(auto_error=False)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


router = APIRouter(prefix="/jwt", tags=["JwT"], dependencies=[Depends(http_bearer)])



def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password"
    )

    if not (user := users_db.get(username)):
        raise unauthed_exc
    
    if not auth_utils.validate_password(
        user_input_password=password,
        hashed_password=user.password
    ):
        raise unauthed_exc
    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user is not active"
        )
    
    return user


def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user)
):
    if user.active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive",
    )




@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user)
):
    
    token = create_access_token(user=user)

    refresh_token = create_refresh_token(user=user)

    return TokenInfo(
        access_token = token,
        refresh_token= refresh_token,
    )


@router.post("/refresh", response_model_exclude_none=True, response_model=TokenInfo)
def refresh_token_auth(user: UserSchema = Depends(get_current_auth_user_for_refersh)):
    access_token = create_access_token(user=user)

    return TokenInfo(
        access_token = access_token,
    )



@router.get("/users/me")
def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_active_auth_user)
    ):

    return {
        "username": user.username,
        "email": user.email
    }

