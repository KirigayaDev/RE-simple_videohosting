import uuid

from fastapi import Depends
from fastapi.responses import ORJSONResponse


from database.models.user import User
from database.crud.user.update import try_update_user

from schemas.user.change_password import UserChangePasswordSchema

from password_hasher.create import create_password_hash
from password_hasher.verify import verify_password

from .router import router
from ._get_current_user import get_current_user


@router.post("/change_password")
async def change_user_password(change_password: UserChangePasswordSchema,
                               user: User | None = Depends(get_current_user)) -> ORJSONResponse:
    if user is None:
        return ORJSONResponse(status_code=401, content={"msg": "Unauthorized"})
    if not verify_password(password=change_password.old_password, password_hash=user.password_hash):
        return ORJSONResponse(status_code=401, content={"msg": "Wrong password"})

    user.password_hash = create_password_hash(change_password.new_password)
    user.token_version_uuid = uuid.uuid4()

    if await try_update_user(user):
        return ORJSONResponse(status_code=200, content={"msg": "successfully changed"})

    else:
        return ORJSONResponse(status_code=500, content={"msg": "Error on update user"})
