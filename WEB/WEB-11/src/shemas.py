from datetime import date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(min_length=3, strict=True, max_length=30)
    second_name: str = Field(min_length=3, strict=True, max_length=50)
    email: EmailStr
    phone: str = Field(min_length=10, strict=True, max_length=13)
    birthday: date
    description: str = Field(min_length=3, strict=True, max_length=250)


class ContactResponse(ContactModel):
    id: int = 1
    first_name: str = "User"
    second_name: str = "Example"
    email: EmailStr = "example@gmail.com"
    phone: str = "0000000000"
    birthday: date = date(year=1995, month=8, day=19)
    description: str = "Created first contact for test"

    class Config:
        orm_mode = True
