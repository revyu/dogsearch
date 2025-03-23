from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AnimalBase(BaseModel):
    # type: Optional[str] = None
    pet_id: str
    name: Optional[str] = None
    gender: Optional[str] = None
    # color: Optional[str] = None
    # location: Optional[str] = None
    # description: Optional[str] = None
    # status: Optional[str] = None
    # photo_url: Optional[str] = None
    # latitude: Optional[float] = None
    # longitude: Optional[float] = None
    # owner_id: Optional[int] = None
    descriptions: Optional[List[str]] = None
    images: Optional[List[str]] = None
    address: Optional[str] = None

class AnimalCreate(AnimalBase):
    pass

class AnimalUpdate(AnimalBase):
    pass

class Animal(AnimalBase):
    class Config:
        from_attributes = True
