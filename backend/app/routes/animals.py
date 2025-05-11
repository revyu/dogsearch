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
            SELECT p.pet_id, p.name, p.gender, p.descriptions, p.images, a.addr_text, p.user_id
            FROM pets AS p
            JOIN addresses AS a ON a.address_id = p.address_id
        """)
        return [dict(pet) for pet in pets]
    finally:
        await close_db_connection(conn)

@router.get("/{pet_id}", response_model=Animal)
async def get_animal(pet_id: str):
    conn = await get_db_connection()
    try:
        pet = await conn.fetchrow("""
            SELECT p.pet_id, p.name, p.gender, p.descriptions, p.images, a.addr_text, a.user_id
            FROM pets AS p
            JOIN addresses AS a ON a.address_id = p.address_id
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
            INSERT INTO pets (pet_id, name, gender, descriptions, images, address, user_id)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING pet_id, name, gender, descriptions, images, address, user_id
        """, animal.pet_id, animal.name, animal.gender, animal.descriptions, 
             animal.images, animal.address, animal.user_id)
        return dict(pet)
    finally:
        await close_db_connection(conn)

@router.put("/{animal_id}", response_model=Animal)
async def update_animal(animal_id: str, animal_update: AnimalUpdate):
    conn = await get_db_connection()
    try:
        pet = await conn.fetchrow("""
            UPDATE pets
            SET name = $1, 
                gender = $2, 
                descriptions = $3, 
                images = $4, 
                address = $5,
                user_id = $6
            WHERE pet_id = $7
            RETURNING pet_id, name, gender, descriptions, images, address, user_id
        """, animal_update.name, animal_update.gender, animal_update.descriptions, 
             animal_update.images, animal_update.address, animal_update.user_id, 
             animal_id)
        if pet is None:
            raise HTTPException(status_code=404, detail="Животное не найдено")
        return dict(pet)
    finally:
        await close_db_connection(conn)

@router.delete("/{animal_id}")
async def delete_animal(animal_id: str):
    conn = await get_db_connection()
    try:
        pet = await conn.fetchrow("""
            DELETE FROM pets
            WHERE pet_id = $1
            RETURNING pet_id, name, gender, descriptions, images, address, user_id
        """, animal_id)
        if pet is None:
            raise HTTPException(status_code=404, detail="Животное не найдено")
        return {"message": "Объявление удалено"}
    finally:
        await close_db_connection(conn)
