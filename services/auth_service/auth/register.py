from fastapi import status
from fastapi.responses import ORJSONResponse

from schemas.user.register import UserRegisterSchema

from database.crud.user.create import try_create_user

from .router import router


@router.post("/register/")
async def try_register_user(user_data: UserRegisterSchema) -> ORJSONResponse:
    result = await try_create_user(user_data)
    result_dict = {"message": "Success"} if result else {"message": "Failure"}
    status_code = status.HTTP_201_CREATED if result else status.HTTP_400_BAD_REQUEST
    return ORJSONResponse(status_code=status_code, content=result_dict)
