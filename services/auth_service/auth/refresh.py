import datetime

from fastapi import Cookie

from fastapi.responses import ORJSONResponse

from jwt_tokens.get_data import get_token_data
from jwt_tokens.blacklist import add_token_payload_to_blacklist
from jwt_tokens.generator import generate_tokens

from database.crud.user.get import get_user_by_uuid

from .router import router


@router.post("/refresh")
async def authenticate_user(refresh_token: str = Cookie(None)) -> ORJSONResponse:
    old_refresh_payload = await get_token_data(refresh_token)

    if old_refresh_payload is None or old_refresh_payload.token_type != "refresh":
        return ORJSONResponse(status_code=401, content={"msg": "Unauthorized"})

    user = await get_user_by_uuid(old_refresh_payload.sub)
    new_tokens = generate_tokens(user, datetime.datetime.now())
    await add_token_payload_to_blacklist(old_refresh_payload)

    response = ORJSONResponse(status_code=200, content={"msg": "Successfully refreshed tokens"})
    response.set_cookie("access_token", new_tokens.access_token, httponly=True, secure=True, samesite="strict")
    response.set_cookie("refresh_token", new_tokens.refresh_token, httponly=True, secure=True, samesite="strict")
    return response
