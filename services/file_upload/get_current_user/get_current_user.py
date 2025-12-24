from fastapi import Request, Cookie, Header
from fastapi.exceptions import HTTPException

from schemas.user import UserSchema

from ._validate_csrf_token import _validate_csrf_token

from ._get_token_data import get_user_data_by_token


async def get_current_user(request: Request, access_token: str = Cookie(None),
                           csrf_token: str = Header(None, alias="X-CSRF-Token", alias_priority=True)) -> UserSchema:
    if access_token is None:
        return None

    user: UserSchema = await get_user_data_by_token(access_token)

    if user is None:
        raise HTTPException(status_code=401, detail={"msg": "Unauthorized"})

    if not await _validate_csrf_token(request, user, csrf_token):
        raise HTTPException(status_code=403, detail={"msg": "CSRF validation error"})

    return user
