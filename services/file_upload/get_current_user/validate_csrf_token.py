from fastapi import Request


async def _validate_csrf_token(request: Request, access_token_payload: TokenPayloadSchema, csrf_token: str) -> bool:
    if request.method in ["GET", "HEAD", "OPTIONS"]:
        return True

    csrf_token_payload = decode_token(csrf_token)
    if csrf_token_payload is None or csrf_token_payload.sub != access_token_payload.sub or \
            csrf_token_payload.token_version != access_token_payload.token_version or \
            csrf_token_payload.token_type != "csrf":
        return False

    return True
