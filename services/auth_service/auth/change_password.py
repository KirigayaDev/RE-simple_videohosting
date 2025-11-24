from fastapi import Cookie
from fastapi.responses import ORJSONResponse

from .router import router


@router.post("/change_password")
async def login_user(access_token: str = Cookie(None)) -> ORJSONResponse:
    return ORJSONResponse(status_code=401, content={"msg": "Wrong user data"})
