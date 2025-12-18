from fastapi import Request, Cookie, Header
from fastapi.exceptions import HTTPException

from database.models.user import User

from jwt_tokens.get_data import get_token_data
from jwt_tokens.coder import decode_token
from jwt_tokens.schemas import TokenPayloadSchema

from database.crud.user.get import get_user_by_token_payload

from .validate_csrf_token import _validate_csrf_token


async def get_current_user(request: Request, access_token: str = Cookie(None),
                           csrf_token: str = Header(None, alias="X-CSRF-Token", alias_priority=True)) -> User:
    if access_token is None:
        return None

    access_token_payload: TokenPayloadSchema = await get_token_data(access_token)
    if access_token_payload is None:
        raise HTTPException(status_code=401, detail={"msg": "expired access token"})

    if access_token_payload.token_type != "access":
        raise HTTPException(status_code=401, detail={"msg": "Wrong access token"})

    if not await _validate_csrf_token(request, access_token_payload, csrf_token):
        raise HTTPException(status_code=403, detail={"msg": "CSRF validation error"})

    user: User = await get_user_by_token_payload(access_token_payload)

    return user
