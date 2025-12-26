from pydantic import BaseModel
from typing import Optional, List


class UserUpdate(BaseModel):
    f_name: Optional[str] = None
    l_name: Optional[str] = None
    mobile: Optional[int] = None
    organisation_type: Optional[str] = None
    individual_type: Optional[str] = None
    purpose_or_objective: Optional[str] = None
    user_type: Optional[str] = None
    role: Optional[str] = None

class UserListResponse(BaseModel):
    uid: int
    f_name: Optional[str]
    l_name: Optional[str]
    email_id: str
    user_name: str
    mobile: Optional[int] = None
    role: str

    class Config:
        from_attributes = True
