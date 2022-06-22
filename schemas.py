from typing import Optional

from pydantic import BaseModel, Field


class TodoSchema(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(
        gt=0, lt=6, description="The priority must be between 1-5"
    )
    completed: bool


class UserSchema(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    is_active: Optional[bool]
    phone_number: Optional[str]


class UserVerificationSchema(BaseModel):
    username: str
    password: str
    new_password: str


class AddressSchema(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str
