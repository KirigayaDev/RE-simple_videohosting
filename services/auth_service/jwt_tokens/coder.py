import jwt

from configurations import jwt_settings

from .schemas import TokenPayloadSchema

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


