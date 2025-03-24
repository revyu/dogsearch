from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .animal import Animal  # Импортируем модель Animal

class UserBase(BaseModel):
    vk_id: Optional[int] = None
    phone: Optional[str] = None
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
