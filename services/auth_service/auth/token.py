from fastapi.responses import ORJSONResponse

from jwt_tokens.coder import get_token_data

from .router import router


@router.get("/token")
async def authenticate_user(access_token: str) -> ORJSONResponse:
    payload = await get_token_data(access_token)
    if payload is None:
        return ORJSONResponse(status_code=401, content={"msg": "Unauthorized token"})

    return ORJSONResponse(status_code=200, content={"msg": "Token info", "payload": payload.model_dump(mode="json")})
