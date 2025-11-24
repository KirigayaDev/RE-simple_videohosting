import asyncio

from fastapi import Cookie

from fastapi.responses import ORJSONResponse

from jwt_tokens.get_data import get_token_data
from jwt_tokens.blacklist import add_token_payload_to_blacklist

from .router import router


@router.post("/logout")
async def add_tokens_to_blacklist(access_token: str = Cookie(None), refresh_token: str = Cookie(None)) -> ORJSONResponse:
    access_payload = await get_token_data(access_token)
    refresh_payload = await get_token_data(refresh_token, verify_nbf=False)
    await asyncio.gather(add_token_payload_to_blacklist(access_payload),
                         add_token_payload_to_blacklist(refresh_payload))

    response = ORJSONResponse(status_code=200, content={"msg": "Successfully logout"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
