"""
User Pydantic schemas for request/response validation.
"""

import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime


def _validate_password_strength(value: str) -> str:
    """
    Enforce a minimum password policy: length is already handled by Field,
    and the value must mix character classes so simple passwords like
    "12345678" are rejected. (Pentest finding L1)
    """
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must include at least one uppercase letter")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must include at least one lowercase letter")
    if not re.search(r"\d", value):
        raise ValueError("Password must include at least one number")
    return value


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., pattern="^(visitor|customer|applicant|admin|developer|investor)$")


class UserCreate(UserBase):
    # Registration must never grant privileged roles directly. Admin accounts
    # are provisioned by seed scripts / the database only. The pattern below
    # is stricter than UserBase so a request with role="admin" is rejected
    # with 422 before it reaches the endpoint. (Pentest finding C1)
    # The registration screen no longer asks what the visitor came to do -
    # new accounts default to customer; applicants are created through the
    # open assessment flow (no login required) and promoted by the admin.
    role: str = Field(default="customer", pattern="^(visitor|customer|applicant)$")
    password: str = Field(..., min_length=8, max_length=100)
    # Applicant's chosen place of qualification - the category (+ optional
    # position) they will be assessed in.
    qualification_category_id: Optional[int] = None
    qualification_position_id: Optional[int] = None
    qualification_category_name: Optional[str] = Field(None, max_length=120)
    qualification_position_name: Optional[str] = Field(None, max_length=120)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        return _validate_password_strength(value)


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    username: Optional[str]
    last_login: Optional[datetime]
    terms_accepted_at: Optional[datetime]
    policies_accepted_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    qualification_category_id: Optional[int]
    qualification_position_id: Optional[int]
    qualification_category_name: Optional[str]
    qualification_position_name: Optional[str]

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None


class CustomerBase(BaseModel):
    company_name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def new_password_strength(cls, value: str) -> str:
        return _validate_password_strength(value)


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def new_password_strength(cls, value: str) -> str:
        return _validate_password_strength(value)
