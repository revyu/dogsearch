from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AnimalBase(BaseModel):
    type: str = Field(..., description="Тип животного (кот, собака и т.д.)")
    name: Optional[str] = Field(None, description="Кличка животного")
    color: str = Field(..., description="Окрас животного")
    location: str = Field(..., description="Место, где животное было потеряно/найдено")
    description: str = Field(..., description="Описание животного")
    status: str = Field(..., description="Статус (потерян, найден)")
    photo_url: Optional[str] = Field(None, description="URL фотографии животного")
    latitude: float = Field(..., description="Широта местоположения")
    longitude: float = Field(..., description="Долгота местоположения")
    owner_id: Optional[int] = Field(None, description="ID владельца животного")

class AnimalCreate(AnimalBase):
    pass

class AnimalUpdate(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    photo_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Animal(AnimalBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
