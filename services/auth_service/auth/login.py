from fastapi.responses import ORJSONResponse

from .router import router
from schemas.user.login import UserLogin


@router.get("/login")
async def login_user(login_data: UserLogin) -> ORJSONResponse:
    pass
