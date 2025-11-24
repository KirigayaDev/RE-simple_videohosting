from pydantic import BaseModel, constr, EmailStr

from .constants import USERNAME_REGEX


class UserLogin(BaseModel):
    username: constr(pattern=USERNAME_REGEX) | EmailStr
    password: str
