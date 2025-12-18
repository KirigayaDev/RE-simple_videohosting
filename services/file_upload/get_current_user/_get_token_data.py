import httpx

from schemas.user import UserSchema


async def get_user_data_by_token(access_token: str):
    async with httpx.AsyncClient as client:
        response = await client.get("https://auth_service:8000/auth/token", params={"access_token": access_token})
        if 200 <= response.status_code <= 299:
            return UserSchema(**response.content["user_info"])
