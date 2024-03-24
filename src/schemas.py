from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, EmailStr, PastDate


class ContactModel(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[PastDate] = Field(None)


class ContactUpdate(BaseModel):
    date_of_birth: PastDate


class ContactResponse(ContactModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
