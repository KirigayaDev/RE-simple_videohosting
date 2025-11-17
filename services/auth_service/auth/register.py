from fastapi.responses import HTMLResponse, ORJSONResponse

from .router import router


@router.post("/register/")
async def try_register_user() -> ORJSONResponse:
    pass

