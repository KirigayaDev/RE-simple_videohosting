import datetime

from fastapi.responses import ORJSONResponse

from schemas.user.login import UserLogin
from database.crud.user.get import get_user_by_username, get_user_by_email
from password_hasher.verify import verify_password
from jwt_tokens.generator import generate_tokens
from ._validators import _is_email_str

from .router import router


@router.post("/login")
async def login_user(login_data: UserLogin) -> ORJSONResponse:
    if _is_email_str(login_data.login):
        user = await get_user_by_email(login_data.login)

    elif isinstance(login_data.login, str):
        user = await get_user_by_username(login_data.login)

    if user is not None and verify_password(password=login_data.password, password_hash=user.password_hash):
        tokens = generate_tokens(user, datetime.datetime.now())
        response = ORJSONResponse(status_code=200, content={"msg": "Successfully authorized"})
        response.set_cookie("access_token", tokens.access_token, httponly=True, secure=True, samesite="strict")
        response.set_cookie("refresh_token", tokens.refresh_token, httponly=True, secure=True, samesite="strict")
        return response

    return ORJSONResponse(status_code=401, content={"msg": "Wrong user data"})
