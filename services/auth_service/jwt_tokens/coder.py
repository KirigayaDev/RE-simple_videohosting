import jwt

from configurations import jwt_settings

from .schemas import TokenPayloadSchema
from .blacklist import token_is_blacklisted

_ALGORITHM = "RS256"


def encode_token(payload: TokenPayloadSchema) -> str:
    return jwt.encode(payload, jwt_settings.private_key, algorithm=_ALGORITHM)


def decode_token(token: str) -> TokenPayloadSchema | None:
    try:
        payload_dict = jwt.decode(token, jwt_settings.public_key, algorithm=_ALGORITHM)
        decoded = TokenPayloadSchema(**payload_dict)
        return decoded

    except jwt.PyJWTError:
        return None


async def get_token_data(token: str) -> TokenPayloadSchema | None:
    decoded = decode_token(token)
    if decoded is None or token_is_blacklisted(decoded):
        return None

    return decoded
