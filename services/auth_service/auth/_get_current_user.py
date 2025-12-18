from fastapi import Request
from fastapi.exceptions import HTTPException

from database.models.user import User

from jwt_tokens.get_data import get_token_data
from jwt_tokens.schemas import AccountTokenPayloadSchema

from database.crud.user.get import get_user_by_uuid


async def get_current_user(request: Request) -> User:
    # TODO добавить в эту проверку проверку csrf
    cookies = request.cookies
    token: str = cookies.get('access_token', None)
    if token is None:
        return None

    payload: AccountTokenPayloadSchema = await get_token_data(token)

    if payload is None:
        raise HTTPException(401, "expired token")

    user: User = await get_user_by_uuid(payload.sub)

    return user
