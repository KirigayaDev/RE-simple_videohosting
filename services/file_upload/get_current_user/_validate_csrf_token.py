from fastapi import Request

from schemas.user import UserSchema

from jwt_tokens.coder import decode_token


async def _validate_csrf_token(request: Request, user: UserSchema, csrf_token: str) -> bool:
    if request.method in ["GET", "HEAD", "OPTIONS"]:
        return True

    csrf_token_payload = decode_token(csrf_token)
    if csrf_token is None:
        return False

    if csrf_token_payload is None or csrf_token_payload.sub != user.uuid or \
            csrf_token_payload.token_version != user.token_version_uuid or \
            csrf_token_payload.token_type != "csrf":
        return False

    return True
