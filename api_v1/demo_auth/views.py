import time
from typing import Annotated, Any
import secrets
import uuid
from time import time

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])

security = HTTPBasic()


@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password,
    }

usernames_to_passwords = {
    "admin": "admin",
    "vinc": "passwrod"
}


static_auth_token_to_username = {
    "nmUYoBNgYECceANCCO302GbGzPAGDPI1": "vinc",
    "MM8Uf0dt1lWfOzsZn7H1Ascq4nvITy0f": "liz",
}


def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )

    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc
    

    if not secrets.compare_digest(credentials.password.encode("utf-8"), correct_password.encode("utf-8")):
        raise unauthed_exc
    
    return credentials.username


def get_username_by_static_auth_token(
        secret_token: str = Header(alias=("x-auth-token"))
    ) -> str:

    if username:= static_auth_token_to_username.get(secret_token):
        return username
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token unauthorised"
    )


@router.get("/basic-auth-username")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username)
):
    return {
        "message": f"Hi {auth_username}",
        "username": auth_username,
    }


@router.get("/some_http_header_auth")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token)
):
    return {
        "message": f"Hi {username}",
        "username": username,
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_ID_SESSION_KEY = "web-app-session-id"


def generate_cookie_id() -> str:
    return uuid.uuid4().hex

def get_session_data(session_id: str = Cookie(alias=COOKIE_ID_SESSION_KEY)):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated"
        )
    
    return COOKIES[session_id]


@router.post("/login-cookies")
def demo_auth_login_set_cookies(
    response: Response,
    auth_username: str = Depends(get_auth_user_username)
):  
    session_id = generate_cookie_id()
    COOKIES[session_id] = {
        "login_at": int(time()),
        "username": auth_username,
    }

    response.set_cookie(COOKIE_ID_SESSION_KEY, session_id)
    return  {"result": "ok"}


@router.get("/check_cookie")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"Hello, {username}",
        **user_session_data,
    }


@router.get("/logout-cookie/")
def demo_auth_logout_cookie(
    response: Response,
    user_session_data: dict = Depends(get_session_data),
    session_id: str = Cookie(alias=COOKIE_ID_SESSION_KEY)
):  
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_ID_SESSION_KEY)
    username = user_session_data["username"]
    return {"message": f"Bye {username}"}