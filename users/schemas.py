from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from annotated_types import MaxLen, MinLen

class CreateUser(BaseModel):
    # username: Field(str, MinLen=3, MaxLen=25)
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
