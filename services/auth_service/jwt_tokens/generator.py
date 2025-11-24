import datetime

from uuid import uuid4

from database.models.user import User

from .schemas import TokenPayloadSchema, JwtTokens

from .coder import encode_token


def generate_tokens(user: User, start_datetime: datetime.datetime) -> str:
    access_payload = TokenPayloadSchema(sub=user.uuid,
                                        nbf=start_datetime, iat=start_datetime,
                                        exp=start_datetime + datetime.timedelta(minutes=30),
                                        jti=uuid4(), token_version=user.token_version_uuid, token_type="access")

    refresh_payload = TokenPayloadSchema(sub=user.uuid,
                                         nbf=start_datetime + datetime.timedelta(minutes=30), iat=start_datetime,
                                         exp=start_datetime + datetime.timedelta(days=7),
                                         jti=uuid4(), token_version=user.token_version_uuid, token_type="refresh")

    access_token = encode_token(access_payload)
    refresh_token = encode_token(refresh_payload)

    return JwtTokens(access_token=access_token, refresh_token=refresh_token)
