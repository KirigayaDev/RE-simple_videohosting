import datetime

from pydantic import BaseModel, UUID4


class UserSchema(BaseModel):
    uuid: UUID4
    username: str
    email: str
    created_at: datetime.datetime
    token_version_uuid: UUID4
    display_name: str
