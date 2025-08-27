import pydantic
from pydantic import ConfigDict, BaseModel, EmailStr

from typing import Annotated
from annotated_types import MaxLen, MinLen

class CreateUser(BaseModel):
    # username: Field(str, MinLen=3, MaxLen=25)
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    email: EmailStr | None = None
    password: bytes
    active: bool = True