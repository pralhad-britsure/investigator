from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict
from src.models.user import Role


class UserBase(BaseModel):
    f_name: Optional[str] = None
    l_name: Optional[str] = None
    mobile: Optional[int] = None
    email_id: EmailStr
    organisation_type: Optional[str] = None
    individual_type: Optional[str] = None
    purpose_or_objective: Optional[str] = None
    user_type: Optional[str] = None
    #user_password: Optional[str] = None
    role: Optional[str] = "Patron"

class UserCreate(UserBase):
    pass


class UserLogin(BaseModel):
    user_name: str
    user_password: str


class UserResponse(UserBase):
    uid: int
    user_name: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    access: Optional[Dict[str, int]] = None



class ForgotPasswordRequest(BaseModel):
    user_name: str = Field(...)
    new_password: str = Field(...)
    confirm_new_password: str = Field(...)


class UserDetailsResponse(BaseModel):
    f_name: str
    l_name: str
    mobile: Optional[str] = None
    email_id: str
    role: str

    class Config:
        from_attributes = True
