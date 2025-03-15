from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    vk_id: int = Field(..., description="ID пользователя ВКонтакте")
    first_name: str = Field(..., description="Имя пользователя")
    last_name: str = Field(..., description="Фамилия пользователя")
    
class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class User(UserInDB):
    pass
