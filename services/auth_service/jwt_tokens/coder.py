import asyncio

import jwt

from configurations import jwt_settings

from database.crud.user.exists import user_and_token_version_exists

from .schemas import TokenPayloadSchema
from .blacklist import token_is_blacklisted

_ALGORITHM = "RS256"


def encode_token(payload: TokenPayloadSchema) -> str:
    return jwt.encode(payload.model_dump(mode="json"), jwt_settings.private_key, algorithm=_ALGORITHM)


def decode_token(token: str) -> TokenPayloadSchema | None:
    try:
        payload_dict = jwt.decode(token, jwt_settings.public_key, algorithms=[_ALGORITHM],
                                  audience="Re:simple_videohosting_auth")
        decoded = TokenPayloadSchema(**payload_dict)
        return decoded

    except jwt.PyJWTError:
        return None


async def get_token_data(token: str) -> TokenPayloadSchema | None:
    decoded: TokenPayloadSchema = decode_token(token)
    if decoded is None:
        return None
    is_blacklist, version_exists = await asyncio.gather(token_is_blacklisted(decoded),
                                                        user_and_token_version_exists(decoded.sub,
                                                                                      decoded.token_version))

    if is_blacklist or not version_exists:
        return None

    return decoded
