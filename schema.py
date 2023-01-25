from pydantic import BaseModel, EmailStr, ValidationError, validator
import re
from typing import Type, Optional
from errors import HttpException


password_regex = re.compile("^(?=.*[a-z_])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!#%*?&_]{8,50}$")


def check_password(password: str):
    if len(password) > 50:
        raise ValueError('max length password is 50')
    if not re.search(password_regex, password):
        raise ValueError('password is too easy')
    return password


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def strong_password(cls, value):
        return check_password(value)


class PatchUserSchema(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]

    @validator('password')
    def strong_password(cls, value):
        return check_password(value)


def validate(data_to_validate: dict, validation_model: Type[CreateUserSchema] | Type[PatchUserSchema]):
    try:
        return validation_model(**data_to_validate).dict(exclude_none=True)
    except ValidationError as er:
        raise HttpException(400, er.errors())
