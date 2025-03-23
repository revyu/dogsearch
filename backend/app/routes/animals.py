from fastapi import APIRouter, HTTPException
from typing import List
from ..models.animal import Animal, AnimalCreate, AnimalUpdate
from ..database.db import get_db_connection, close_db_connection

router = APIRouter(prefix="/animals", tags=["animals"])

@router.get("/", response_model=List[Animal])
async def get_animals():
    conn = await get_db_connection()
    try:
        pets = await conn.fetch("""
            SELECT pet_id, name, gender, descriptions, images, address
            FROM pets
        """)
        return [dict(pet) for pet in pets]
    finally:
        await close_db_connection(conn)

@router.get("/{pet_id}", response_model=Animal)
async def get_animal(pet_id: str):
    conn = await get_db_connection()
    try:
        pet = await conn.fetchrow("""
            SELECT pet_id, name, gender, descriptions, images, address
            FROM pets
            WHERE pet_id = $1
        """, pet_id)
        if pet is None:
            raise HTTPException(status_code=404, detail="Животное не найдено")
        return dict(pet)
    finally:
        await close_db_connection(conn)

@router.post("/", response_model=Animal)
async def create_animal(animal: AnimalCreate):
    conn = await get_db_connection()
    try:
        pet = await conn.fetchrow("""
            INSERT INTO pets (pet_id, name, gender, descriptions, images, address)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING pet_id, name, gender, descriptions, images, address
        """, animal.pet_id, animal.name, animal.gender, animal.descriptions, 
             animal.images, animal.address)
        return dict(pet)
    finally:
        await close_db_connection(conn)

@router.put("/{animal_id}", response_model=Animal)
async def update_animal(animal_id: str, animal_update: AnimalUpdate):
    conn = await get_db_connection()
    try:
        pet = await conn.fetchrow("""
            UPDATE pets
            SET name = $1, gender = $2, descriptions = $3, images = $4, address = $5
            WHERE pet_id = $6
            RETURNING pet_id, name, gender, descriptions, images, address
        """, animal_update.name, animal_update.gender, animal_update.descriptions, 
             animal_update.images, animal_update.address, animal_id)
        if pet is None:
            raise HTTPException(status_code=404, detail="Животное не найдено")
        return dict(pet)
    finally:
        await close_db_connection(conn)

@router.delete("/{animal_id}")
async def delete_animal(animal_id: int):
    conn = await get_db_connection()
    try:
        pet = await conn.fetchrow("""
            DELETE FROM pets
            WHERE pet_id = $1
            RETURNING pet_id, name, gender, descriptions, images, address
        """, str(animal_id))
        if pet is None:
            raise HTTPException(status_code=404, detail="Животное не найдено")
        return {"message": "Объявление удалено"}
    finally:
        await close_db_connection(conn)
