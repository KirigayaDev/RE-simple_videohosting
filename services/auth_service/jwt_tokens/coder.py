import jwt

from .schema import TokenPayloadSchema
from configurations import jwt_settings

_ALGORITHM = "RS256"


def encode_token(payload: TokenPayloadSchema):
    return jwt.encode(payload, jwt_settings.private_key, algorithm=_ALGORITHM)


async def decode_token(token: str):
    try:
        decoded = jwt.decode(token, jwt_settings.public_key, algorithm=_ALGORITHM)
        # TODO дописать бросания исключений если не совпадает token_version или если jti в блэклисте
        return decoded

    except jwt.PyJWTError:
        return None
