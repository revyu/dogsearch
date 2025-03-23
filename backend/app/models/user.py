from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    vk_id: Optional[int] = None
    # name: Optional[str] = None
    # phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
