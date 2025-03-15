from fastapi import APIRouter, HTTPException
from typing import List
from ..models.animal import Animal, AnimalCreate, AnimalUpdate

router = APIRouter(prefix="/animals", tags=["animals"])

# Временная бд
fake_animals_db = [
    {
        "id": 1,
        "type": "кот",
        "name": "Жорик",
        "color": "бело-коричневый",
        "location": "Москва",
        "description": "Вечером выбежал из подъезда.",
        "status": "потерян",
        "photo_url": "https://example.com/photo.jpg",
        "latitude": 55.7558,
        "longitude": 37.6173,
        "created_at": "2025-03-08T12:00:00",
        "updated_at": None,
        "owner_id": 1
    }
]

@router.get("/", response_model=List[Animal])
async def get_animals():
    return fake_animals_db

@router.get("/{animal_id}", response_model=Animal)
async def get_animal(animal_id: int):
    for animal in fake_animals_db:
        if animal["id"] == animal_id:
            return animal
    raise HTTPException(status_code=404, detail="Животное не найдено")

@router.post("/", response_model=Animal)
async def create_animal(animal: AnimalCreate):
    new_id = len(fake_animals_db) + 1
    new_animal = {
        "id": new_id,
        "created_at": "2025-03-09T14:30:00",
        "updated_at": None,
        **animal.dict()
    }
    fake_animals_db.append(new_animal)
    return new_animal

@router.put("/{animal_id}", response_model=Animal)
async def update_animal(animal_id: int, animal_update: AnimalUpdate):
    for i, animal in enumerate(fake_animals_db):
        if animal["id"] == animal_id:
            update_data = animal_update.dict(exclude_unset=True)
            fake_animals_db[i].update(update_data)
            fake_animals_db[i]["updated_at"] = "2025-03-09T14:35:00"
            return fake_animals_db[i]
    raise HTTPException(status_code=404, detail="Животное не найдено")

@router.delete("/{animal_id}")
async def delete_animal(animal_id: int):
    for i, animal in enumerate(fake_animals_db):
        if animal["id"] == animal_id:
            del fake_animals_db[i]
            return {"message": "Объявление удалено"}
    raise HTTPException(status_code=404, detail="Животное не найдено")
