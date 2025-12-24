import orjson
import httpx

from schemas.user import UserSchema


async def get_user_data_by_token(access_token: str):
    async with httpx.AsyncClient(verify="/auth_service/certs/auth_service/rootCA.crt") as client:
        response = await client.get("https://auth_service:8000/auth/token", params={"access_token": access_token})
        if 200 <= response.status_code <= 299:
            data = orjson.loads(response.content.decode("utf-8"))
            return UserSchema(**data["user_info"])
