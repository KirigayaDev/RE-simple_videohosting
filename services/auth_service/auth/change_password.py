import uuid

from fastapi import Cookie
from fastapi.responses import ORJSONResponse

from jwt_tokens.get_data import get_token_data

from database.crud.user.get import get_user_by_uuid
from database.crud.user.update import try_update_user

from schemas.user.change_password import UserChangePasswordSchema

from password_hasher.create import create_password_hash
from password_hasher.verify import verify_password

from .router import router


@router.post("/change_password")
async def login_user(change_password: UserChangePasswordSchema, access_token: str = Cookie(None)) -> ORJSONResponse:
    user_payload = await get_token_data(access_token)
    user = await get_user_by_uuid(user_payload.sub)
    if user is None:
        return ORJSONResponse(status_code=401, content={"msg": "Unauthorized"})
    if not verify_password(password=change_password.old_password, password_hash=user.password_hash):
        return ORJSONResponse(status_code=401, content={"msg": "Wrong password"})

    user.password_hash = create_password_hash(change_password.new_password)
    user.token_version_uuid = uuid.uuid4()

    await try_update_user(user)

    return ORJSONResponse(status_code=200, content={"msg": "successfully changed"})
